#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_citations.py — 逐条核对交付物里的引用是不是真的

解决什么问题：
    模型最像样的幻觉，不是编造整段，而是"引一句英文，说是官方原话，其实差了两个词"。
    这种错最难被用户发现，因为看起来完全可信。

它检查三件事：
    1. 引用号 [R:XXX] 在语料库里存在吗？（不存在 = 编的）
    2. 引用号后面紧跟的英文引文，是不是该块的原文？（逐字比对，忽略大小写、空白、标点）
    3. 文中的英文引文有没有漏标引用号？（漏标 = 无法溯源）

用法：
    python verify_citations.py 输出.md
    python verify_citations.py 输出.md --strict     # 有警告也算失败
    python verify_citations.py 输出.md --json

退出码：0 通过；1 失败。可以放在交付前的最后一步。
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    from rag_search import build_index
except Exception as e:  # pragma: no cover
    raise SystemExit("找不到 rag_search.py，两个脚本要放在同一目录。原始错误：%s" % e)

CITE = re.compile(r"\[R:\s*([^\]]+?)\s*\]")
# 英文引号：直引号 + 弯引号；要求长度 >= 15 个字符，避免把单词当引文
QUOTED = re.compile(r"[\"“]([^\"“”]{15,600})[\"”]")


def norm(s):
    s = s.lower()
    s = s.replace("’", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9']+", " ", s)
    return " ".join(s.split())


def load(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise SystemExit("读不了这个文件：%s" % path)


def main():
    ap = argparse.ArgumentParser(description="核对引用号与引文是否属实")
    ap.add_argument("path", help="要检查的交付物（.md / .txt）")
    ap.add_argument("--strict", action="store_true", help="有未标引用号的英文引文也算失败")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        raise SystemExit("找不到文件：%s" % args.path)

    text = load(args.path)
    idx = build_index()
    by_id = {c["id"]: c for c in idx["chunks"]}

    ok, bad_id, mismatched, uncited = [], [], [], []

    for m in CITE.finditer(text):
        raw_ids = re.split(r"[,，;；|\s]+", m.group(1).strip())
        ids = [i for i in raw_ids if i]
        # 引用号后面同一行的第一段英文引文（最多看 200 字符之后）
        tail = text[m.end(): m.end() + 400]
        qm = re.search(r"[\"“]([^\"“”]{15,600})[\"”]", tail)

        for cid in ids:
            if cid not in by_id:
                bad_id.append(cid)
                continue
            if qm:
                quote = qm.group(1)
                if norm(quote) in norm(by_id[cid]["text"] + " " + by_id[cid]["title"]):
                    ok.append((cid, quote))
                else:
                    mismatched.append((cid, quote))
            else:
                ok.append((cid, None))

    # 全文里没绑定引用号的英文引文
    cited_quotes = set()
    for cid, q in ok + mismatched:  # noqa: F841
        if q:
            cited_quotes.add(norm(q))
    for qm in QUOTED.finditer(text):
        q = qm.group(1)
        if norm(q) in cited_quotes:
            continue
        # 只看同一行内是否有 [R: —— 用 200 字符窗口会跨到上一行，导致漏报
        line_start = text.rfind("\n", 0, qm.start()) + 1
        line_ctx = text[line_start: qm.start()]
        if "[R:" in line_ctx or "[R：" in line_ctx:
            continue
        uncited.append(q)

    failed = bool(bad_id or mismatched or (args.strict and uncited))

    if args.json:
        print(json.dumps({
            "cited_ok": len(ok),
            "bad_ids": bad_id,
            "mismatched": [{"id": i, "quote": q} for i, q in mismatched],
            "uncited": uncited,
            "pass": not failed,
        }, ensure_ascii=False, indent=2))
    else:
        print("=" * 56)
        print("引用核对：%s" % os.path.basename(args.path))
        print("=" * 56)
        print("语料库：%d 块" % idx["n"])
        print("有效引用：%d 处" % len(ok))
        if bad_id:
            print("")
            print("[失败] 引用号不存在（这是编的）：")
            for i in sorted(set(bad_id)):
                print("   [R:%s]" % i)
            near = sorted(by_id.keys())
            for i in sorted(set(bad_id))[:3]:
                prefix = ".".join(i.split(".")[:2])
                cand = [k for k in near if k.startswith(prefix)][:8]
                if cand:
                    print("    %s 的合法编号：%s" % (prefix, "、".join(cand)))
        if mismatched:
            print("")
            print("[失败] 引文与原文对不上（逐字比对未通过）：")
            for i, q in mismatched:
                print("   [R:%s] \"%s\"" % (i, q[:90]))
                print("        原文开头：%s" % by_id[i]["text"][:90].replace("\n", " "))
        if uncited:
            print("")
            print("[警告] %d 处英文引文没标引用号，读者无法溯源：" % len(uncited))
            for q in uncited[:6]:
                print("   \"%s\"" % q[:90])
            if len(uncited) > 6:
                print("   …还有 %d 处" % (len(uncited) - 6))
        print("")
        print("结论：%s" % ("不通过，先改引用再交付。" if failed else "通过。"))
        if not failed and uncited and not args.strict:
            print("（未标引用号的引文只算警告；要一并拦下就加 --strict）")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
