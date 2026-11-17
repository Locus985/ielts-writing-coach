#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rag_search.py — 在技能自带的语料库上做检索（BM25），把"凭记忆写"换成"先查再写"

为什么需要它：
    大模型凭记忆背官方评分标准，会把不同年份的版本混在一起，编出不存在的条文。
    唯一稳的办法是：把权威文本切成带编号的块（chunk），检索时只能引用检索到的块，
    引用后还能用 verify_citations.py 逐字核对。

用法：
    python rag_search.py "overview 怎么写 关键特征"            # 默认前 5 条
    python rag_search.py "cohesion mechanical" --k 8
    python rag_search.py "学费 大学" --file fact-registry
    python rag_search.py "Task Response band 7" --task 2 --full
    python rag_search.py --list                               # 看索引里有哪些块

输出：
    每条结果 = 相关度 + 引用号 + 标题 + 出处 + 正文（默认截断 400 字，--full 不截断）

索引规则：
    1. 文件里写了 <!-- chunk: ID | 标题 | src: 来源 --> 的，按锚点切块，ID 就是这个引用号。
    2. 没写锚点的段落，自动按"标题 + 段落"切块，ID 形如 PLAYBOOK-T2#07。
    3. 索引缓存在 kb_index.json，源文件改动后自动重建。

纯标准库，无依赖。
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF_DIR = os.path.join(ROOT, "references")
EX_DIR = os.path.join(ROOT, "examples")
CACHE = os.path.join(ROOT, "kb_index.json")

ANCHOR = re.compile(r"<!--\s*chunk:\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*src:\s*([^>]*?)\s*-->")

# BM25 参数（经验值，文本块短，b 取大一点抑制长度偏置）
K1 = 1.5
B = 0.75

EN_STOP = set("""
a an the and or but if because so that this these those there their they them it its is are was were be been being
do does did have has had of in on at to from with without for by as than then thus also just only more most much
many some any each other another such what which who whom whose when where why how all both few own same into over
under again further once about above below between through during before after up down out off here what's i you he
she we my your his her our us me him not no nor too very can could will would shall should may might must
""".split())

# 中英混合查询的桥接词：用户说中文，语料是英文
BRIDGE = {
    "小作文": ["task 1", "chart", "graph", "overview", "figures"],
    "大作文": ["task 2", "essay", "prompt"],
    "给分点": ["descriptor", "criteria", "band"],
    "评分": ["band", "criteria", "score"],
    "打分": ["band", "score", "criteria"],
    "扣分": ["penalty", "penalised", "limit", "inaccuracy"],
    "范文": ["model", "example", "sample"],
    "跑题": ["off-topic", "tangential", "prompt"],
    "衔接": ["cohesion", "cohesive", "mechanical"],
    "连贯": ["coherence", "progression"],
    "词汇": ["lexical", "vocabulary", "collocation"],
    "语法": ["grammatical", "structures", "accuracy"],
    "字数": ["underlength", "words"],
    "模板": ["memorised", "formulaic", "template"],
    "背诵": ["memorised", "memorised phrases"],
    "例子": ["example", "support", "illustrate"],
    "趋势": ["trend", "increase", "decrease"],
    "地图": ["map", "changes"],
    "流程": ["process", "diagram", "stages"],
    "学费": ["tuition", "fees"],
    "拥堵": ["congestion", "charge"],
    "糖税": ["sugar", "levy", "soft drinks"],
    "素材": ["fact", "evidence", "example"],
    "引用": ["citation", "source", "src"],
}

CJK = re.compile(r"[\u4e00-\u9fff]+")
WORD = re.compile(r"[a-z][a-z'\-]*|\d+(?:\.\d+)?")


def read(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return ""


def stem(w):
    """极简词干化，只为让 scoring / scores / scored 落到同一个词。"""
    if len(w) <= 3:
        return w
    for suf in ("ational", "ation", "ments", "ment", "ingly", "ing", "edly", "ed", "ies", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            base = w[: -len(suf)]
            if suf == "ies":
                return base + "y"
            return base
    return w


def tokenize(text):
    text = text.lower()
    toks = [stem(w) for w in WORD.findall(text)]
    for run in CJK.findall(text):
        if len(run) == 1:
            toks.append(run)
        else:
            toks.extend(run[i:i + 2] for i in range(len(run) - 1))
    return toks


def parse_chunks():
    chunks = []
    files = []
    if os.path.isdir(REF_DIR):
        files += [os.path.join(REF_DIR, f) for f in sorted(os.listdir(REF_DIR)) if f.endswith(".md")]
    if os.path.isdir(EX_DIR):
        files += [os.path.join(EX_DIR, f) for f in sorted(os.listdir(EX_DIR)) if f.endswith((".txt", ".md"))]

    for path in files:
        raw = read(path)
        if not raw.strip():
            continue
        base = os.path.splitext(os.path.basename(path))[0]
        anchors = list(ANCHOR.finditer(raw))

        if anchors:
            # 锚点文件：锚点之间为一块；锚点之前的内容（文件头）也保留
            head = raw[: anchors[0].start()].strip()
            if len(head) > 200:
                chunks.append({
                    "id": base.upper() + "#HEAD",
                    "title": "文件前言：" + base,
                    "src": "self",
                    "file": os.path.basename(path),
                    "text": head,
                })
            for i, m in enumerate(anchors):
                end = anchors[i + 1].start() if i + 1 < len(anchors) else len(raw)
                body = raw[m.end(): end].strip()
                body = re.sub(r"^---+\s*$", "", body, flags=re.M).strip()
                if len(body) < 20:
                    continue
                chunks.append({
                    "id": m.group(1).strip(),
                    "title": m.group(2).strip() or m.group(1).strip(),
                    "src": m.group(3).strip(),
                    "file": os.path.basename(path),
                    "text": body,
                })
        else:
            # 无锚点：按二级标题切。整节优先作为一个块（保住表格和上下文的完整性），
            # 只有超长节才按段落拆，避免把一张表切成互不相连的碎片。
            sections = re.split(r"\n(?=##\s)", raw)
            n = 0
            for sec in sections:
                m = re.match(r"##\s+(.+)", sec)
                heading = m.group(1).strip() if m else base
                sec_body = (sec[m.end():] if m else sec).strip()
                if len(sec_body) < 40:
                    continue
                pieces = []
                if len(sec_body) <= 1400:
                    pieces = [sec_body]
                else:
                    buf = ""
                    for para in re.split(r"\n\s*\n", sec_body):
                        para = para.strip()
                        if not para:
                            continue
                        if len(para) < 40 and buf:
                            buf += "\n\n" + para
                            continue
                        if buf:
                            pieces.append(buf)
                        buf = para
                    if buf:
                        pieces.append(buf)
                for piece in pieces:
                    n += 1
                    chunks.append({
                        "id": "%s#%02d" % (base.upper(), n),
                        "title": heading,
                        "src": base,
                        "file": os.path.basename(path),
                        "text": piece,
                    })
    return chunks


def signature():
    h = hashlib.md5()
    for d in (REF_DIR, EX_DIR):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                st = os.stat(p)
                h.update(("%s%d%d" % (f, st.st_size, int(st.st_mtime))).encode())
    return h.hexdigest()


def build_index(force=False):
    sig = signature()
    if not force and os.path.exists(CACHE):
        try:
            with open(CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("signature") == sig:
                return cached
        except Exception:
            pass

    chunks = parse_chunks()
    df = {}
    for c in chunks:
        c["tf"] = {}
        for t in tokenize(c["title"] + " " + c["text"]):
            c["tf"][t] = c["tf"].get(t, 0) + 1
        c["len"] = sum(c["tf"].values())
        for t in c["tf"]:
            df[t] = df.get(t, 0) + 1

    avg = (sum(c["len"] for c in chunks) / len(chunks)) if chunks else 0
    data = {
        "signature": sig,
        "n": len(chunks),
        "avg_len": avg,
        "df": df,
        "chunks": chunks,
    }
    try:
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass
    return data


def expand(query):
    q = query.lower()
    extra = []
    for zh, ens in BRIDGE.items():
        if zh in query:
            extra += ens
    return q + " " + " ".join(extra)


def search(query, k=5, task=None, file_filter=None, full=False):
    data = build_index()
    chunks = data["chunks"]
    df = data["df"]
    N = data["n"] or 1
    avg = data["avg_len"] or 1

    q_tf = {}
    for t in tokenize(expand(query)):
        q_tf[t] = q_tf.get(t, 0) + 1

    scored = []
    for c in chunks:
        if file_filter and file_filter.lower() not in c["file"].lower():
            continue
        if task:
            blob = (c["id"] + " " + c["title"]).lower()
            if task == 1 and re.search(r"\bt2\.|task 2", blob):
                continue
            if task == 2 and re.search(r"\bt1\.|task 1", blob):
                continue
        s = 0.0
        for t, qn in q_tf.items():
            if t not in c["tf"]:
                continue
            f = c["tf"][t]
            idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            s += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * c["len"] / avg))
        # 标题命中加权，避免长段淹没精确标题
        for t in q_tf:
            if t in c["title"].lower():
                s *= 1.3
                break
        # 问到具体档位时，把同档的块顶上来（"7 分要什么" 优先给 T2.TR.7，而不是别的档）
        m = re.search(r"band\s*([4-9])|([4-9])\s*分|([4-9])\.0", query.lower())
        if m:
            band = m.group(1) or m.group(2) or m.group(3)
            if re.search(r"\.%s$" % band, c["id"]):
                s *= 1.8
        if s > 0:
            scored.append((s, c))

    scored.sort(key=lambda kv: -kv[0])
    out = scored[:k]
    return out


def main():
    ap = argparse.ArgumentParser(description="技能语料库检索（BM25）")
    ap.add_argument("query", nargs="*", help="检索词，中英皆可")
    ap.add_argument("--k", type=int, default=5, help="返回条数，默认 5")
    ap.add_argument("--task", type=int, choices=[1, 2], help="只要 Task 1 或 Task 2 的块")
    ap.add_argument("--file", help="只在某个文件名里找，如 rubric band-ladder fact-registry")
    ap.add_argument("--full", action="store_true", help="不截断正文")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--list", action="store_true", help="列出全部块的编号与标题")
    ap.add_argument("--rebuild", action="store_true", help="强制重建索引")
    args = ap.parse_args()

    if args.rebuild:
        build_index(force=True)

    if args.list:
        data = build_index()
        print("索引：%d 块｜平均长度 %.0f 词" % (data["n"], data["avg_len"]))
        for c in data["chunks"]:
            print("  %-22s %-14s %s" % (c["id"], c["file"], c["title"][:60]))
        return

    q = " ".join(args.query).strip()
    if not q:
        raise SystemExit("给一个检索词。例：python rag_search.py \"overview 关键特征\"")

    hits = search(q, args.k, args.task, args.file, args.full)
    if args.json:
        print(json.dumps([{"id": c["id"], "score": round(s, 2), "title": c["title"],
                           "src": c["src"], "file": c["file"], "text": c["text"]}
                          for s, c in hits], ensure_ascii=False, indent=2))
        return

    if not hits:
        print("没命中。换个词，或去掉 --file / --task 限制。")
        print("提示：语料是英文写的，用中文查时加一个英文关键词更稳，如 \"overview 小作文\"。")
        return

    for s, c in hits:
        body = c["text"] if args.full else (c["text"][:400] + ("…" if len(c["text"]) > 400 else ""))
        print("─" * 60)
        print("[R:%s]  相关度 %.2f" % (c["id"], s))
        print("%s ｜ %s ｜ 源：%s" % (c["title"], c["file"], c["src"]))
        print(body)
    print("─" * 60)
    print("引用时写 [R:编号]。写进交付物后，跑 python verify_citations.py 对一遍逐字是否一致。")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
