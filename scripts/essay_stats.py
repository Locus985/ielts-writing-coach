#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""essay_stats.py — IELTS 作文体检工具（只做可数的检查，不做评分）

用法：
    python essay_stats.py 作文.txt                  # 自动判断 Task 1 / Task 2
    python essay_stats.py 作文.txt --task 2
    python essay_stats.py 作文.txt --json           # 输出 JSON，便于二次处理

输出内容：
    词数 / 句数 / 平均句长 / 句长标准差 / 段落分布
    连接词频次（超量标 [注意]）
    高频重复实词 Top 8
    模板句命中清单
    破折号数量、被动语态粗估、句首重复
    语言指纹：平均小句长、每句从属从句（近似）、MSTTR、名词化密度、
              段落均衡度、AI 风格词、三连并列

说明：
    1. 只统计"表面特征"，不判断论点好坏。分数仍要按 references/rubric-task2.md 的锚点逐条比对。
    2. 词数按空格切分，连字符词算一个词，与考场统计口径基本一致（略有出入，够用）。
    3. 句法指标是"正则近似版"：真正的 L2SCA（Lu, 2010）需要句法分析器。这里的数值只能做
       同一篇改前改后的对比，不能当成 L2SCA 的绝对值。
    4. 纯标准库，无需安装任何依赖。
"""

import argparse
import json
import os
import re
import statistics
import sys

# ---------------------------------------------------------------- 词表

STOPWORDS = set("""
a an the and or but if because so that this these those there their they them
it its is are was were be been being am do does did doing have has had having
i you he she we my your his her our us me him not no nor too very can could
will would shall should may might must of in on at to from with without for
by as than then thus also just only more most much many some any each other
another such what which who whom whose when where why how all both few own
same into over under again further once about above below between through
during before after up down out off here there one two three
""".split())

CONNECTORS = [
    "firstly", "secondly", "thirdly", "first of all", "last but not least",
    "moreover", "furthermore", "in addition", "besides", "additionally",
    "however", "nevertheless", "nonetheless", "on the other hand", "in contrast",
    "by contrast", "conversely", "whereas", "while", "although", "though",
    "therefore", "thus", "consequently", "as a result", "hence",
    "for example", "for instance", "such as", "in other words",
    "in conclusion", "to conclude", "to sum up", "in summary", "all in all",
    "overall", "in general", "according to", "due to", "because of",
]

TEMPLATES = [
    "in today's modern society", "in today’s modern society",
    "in modern society", "with the development of", "with the rapid development",
    "every coin has two sides", "a double-edged sword", "double-edged sword",
    "last but not least", "it is undeniable", "it goes without saying",
    "plays a crucial role", "plays a vital role", "play a key role",
    "hotly debated", "heated debate", "in a nutshell", "all in all",
    "this essay will", "as we all know", "it is widely believed",
    "more and more people", "delineates the trajectory", "staggering",
    "plummeted", "plethora", "myriad", "delve into", "shed light on",
    "in the contemporary world", "nowadays", "at the present time",
]

MARKERS = re.compile(r"[.!?]+[\s\"'”’)]|$")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*|\d+(?:[.,]\d+)?")

# AI 高频风格词。依据：Kobak et al. (2025) Science Advances 发现 2024 年 PubMed 摘要中
# delves / underscores / showcasing 等风格词异常激增；Liang et al. (2024, ICML) 在 ICLR 审稿中
# 发现 meticulous / intricate / commendable 异常高频；Juzek & Ward (2025, COLING) 整理了 21 个过度使用词。
# 注意：这些词本身不算错，只是"密度异常"时会显得像机器写的。别当成禁用词表。
AI_STYLE_WORDS = [
    "delve", "delves", "delving", "showcase", "showcases", "showcasing",
    "underscore", "underscores", "underscoring", "intricate", "meticulous",
    "commendable", "pivotal", "tapestry", "testament", "realm", "multifaceted",
    "nuanced", "holistic", "paradigm", "synergy", "leverage", "robust",
    "myriad", "plethora", "crucial", "foster", "navigate", "streamline",
    "bolster", "landscape", "furthermore", "moreover",
]

# 从属连词 + 关系词，用来近似"从句数"（Lu 2010 的 DC/T 需要句法分析器，这里只做粗估）
# 刻意剔除了 that / as / before / after / once —— 它们兼作指示代词、介词、副词，
# 一律计入会把句子简单的中式英语也算成"从句很多"，实测会让 6 分作文显示成 8 分形态。
SUBORDINATORS = [
    "which", "who", "whom", "whose", "where", "when", "while",
    "although", "though", "because", "since", "unless", "whether",
    "whereas", "even though", "so that", "if",
]

# 名词化后缀（Halliday 意义上的名词化，是书面语密度的主要来源之一）
NOMINAL_SUFFIX = ("tion", "sion", "ment", "ity", "ness", "ance", "ence", "ism", "ization", "isation")

# 语言形态经验区间。非官方标准，只判断"语言长相像不像这一档"，最终定档仍须按 rubric。
# 只用两个相对稳的指标：平均句长、每句从属从句数。
# 词汇多样性（MSTTR）不参与分档 —— 短文本的 TTR 天然偏高，实测 250 词的 6.5 分作文也能到 0.87，
# 用它分档会系统性地把中等作文判成高分。
BAND_HINTS = [
    (15.0, 0.30, "6.0 档形态：短句为主，从句很少"),
    (18.0, 0.50, "6.5 档形态：简单句与复杂句混用，从句开始出现"),
    (22.0, 0.75, "7.0–7.5 档形态：复杂结构稳定，从句密度适中"),
    (99.0, 99.0, "8.0 档形态：句长有明显起伏，复杂句用得准"),
]


def read_text(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise SystemExit("读不了这个文件，试着另存为 UTF-8 再跑一次。")


def split_paragraphs(text):
    blocks = re.split(r"\n\s*\n", text.strip())
    if len(blocks) == 1:
        lines = [ln.strip() for ln in text.strip().split("\n") if ln.strip()]
        if len(lines) > 2 and sum(len(ln.split()) for ln in lines) / len(lines) > 12:
            return lines
    return [b.strip() for b in blocks if b.strip()]


def split_sentences(text):
    raw = MARKERS.split(text)
    out = []
    for chunk in raw:
        chunk = " ".join(chunk.split())
        if chunk and len(WORD_RE.findall(chunk)) >= 2:
            out.append(chunk)
    return out


def count_words(text):
    return len(WORD_RE.findall(text))


def analyse(text):
    paras = split_paragraphs(text)
    body = "\n".join(paras)
    sents = split_sentences(body)
    words = WORD_RE.findall(text)
    lower = text.lower()

    sent_lens = [count_words(s) for s in sents] or [0]
    avg = statistics.mean(sent_lens)
    sd = statistics.pstdev(sent_lens) if len(sent_lens) > 1 else 0.0

    # 连接词
    conn_hits = {}
    for c in CONNECTORS:
        n = len(re.findall(r"(?<![A-Za-z])" + re.escape(c) + r"(?![A-Za-z])", lower))
        if n:
            conn_hits[c] = n
    conn_total = sum(conn_hits.values())
    per_100 = round(conn_total / max(count_words(text), 1) * 100, 1)

    # 高频实词
    freq = {}
    for w in words:
        lw = w.lower()
        if lw in STOPWORDS or len(lw) < 4 or lw.isdigit():
            continue
        freq[lw] = freq.get(lw, 0) + 1
    top_repeat = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:8]

    # 模板句
    tpl_hits = []
    for t in TEMPLATES:
        n = lower.count(t)
        if n:
            tpl_hits.append((t, n))

    # 句首重复
    firsts = {}
    for s in sents:
        w = WORD_RE.findall(s)
        if w:
            k = w[0].lower()
            if k not in ("the", "a", "an", "this", "it", "i", "in", "there"):
                firsts[k] = firsts.get(k, 0) + 1
    head_repeat = [(k, v) for k, v in firsts.items() if v >= 3]

    # 被动语态粗估
    passive = len(re.findall(
        r"\b(?:is|are|was|were|been|be|being)\s+(?:\w+ed|shown|made|given|taken|"
        r"done|built|used|seen|known|found|held|kept|left|sent|brought)\b", lower))

    # 破折号
    dashes = text.count("—") + text.count("–")

    # 可数名词裸奔的粗查（只提示，不判错）
    bare_plural = len(re.findall(
        r"\b(?:many|several|various|numerous|few|different)\s+[a-z]+(?<![s])\b", lower))

    # ---- 以下是 Lu (2010) 句法复杂度指标的"正则近似版" ----
    # 说明：真正的 L2SCA 需要句法分析器（Stanford Parser）。这里用从属连词/关系词计数近似从句数，
    # 用句子近似 T-unit。数值只能横向比较同一篇的前后版本，不能当成 L2SCA 的绝对值。
    n_words = count_words(text)
    n_sent = max(len(sents), 1)
    sub_hits = 0
    for sub in SUBORDINATORS:
        sub_hits += len(re.findall(r"(?<![A-Za-z])" + re.escape(sub) + r"(?![A-Za-z])", lower))
    # 小句数近似 = 句子数 + 从属标记数（每个从属标记通常引入一个从句）
    n_clauses = n_sent + sub_hits
    mlc = round(n_words / max(n_clauses, 1), 1)          # 平均小句长
    dc_per_t = round(sub_hits / n_sent, 2)               # 每句的从属从句数（近似 DC/T）

    # 词汇多样性：MSTTR-50（每 50 词算一次类符/形符比，再取平均，抵消文本长度影响）
    toks = [w.lower() for w in words if len(w) > 1]
    window = 50
    if len(toks) >= window:
        vals = []
        for i in range(0, len(toks) - window + 1, window):
            seg = toks[i:i + window]
            vals.append(len(set(seg)) / window)
        msttr = round(sum(vals) / len(vals), 3)
    else:
        msttr = round(len(set(toks)) / max(len(toks), 1), 3)

    # 名词化密度（-tion / -ment / -ity 这类后缀词占比）
    nominal = sum(1 for w in toks if len(w) > 5 and w.endswith(NOMINAL_SUFFIX))
    nominal_ratio = round(nominal / max(len(toks), 1) * 100, 1)

    # 段落均衡度：各段词数的标准差（AI 文本常见"每段差不多长"）
    para_words = [count_words(p) for p in paras]
    para_sd = round(statistics.pstdev(para_words), 1) if len(para_words) > 1 else 0.0

    # AI 风格词命中
    ai_hits = {}
    for w in AI_STYLE_WORDS:
        n = len(re.findall(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", lower))
        if n:
            ai_hits[w] = n
    ai_total = sum(ai_hits.values())

    # 三连并列（"A, B, and C"）粗查：AI 写作的高频节奏
    triads = len(re.findall(r",\s*[a-z][a-z'\-]{1,20},\s*(?:and|or)\s+[a-z]", lower))

    return {
        "words": count_words(text),
        "sentences": len(sents),
        "paragraphs": len(paras),
        "para_words": [count_words(p) for p in paras],
        "avg_sentence_len": round(avg, 1),
        "sentence_len_sd": round(sd, 1),
        "longest": max(sent_lens) if sent_lens else 0,
        "shortest": min(sent_lens) if sent_lens else 0,
        "connectors": conn_hits,
        "connector_total": conn_total,
        "connectors_per_100_words": per_100,
        "top_repeated": top_repeat,
        "template_hits": tpl_hits,
        "repeated_openings": head_repeat,
        "passive": passive,
        "dashes": dashes,
        "many_plus_singular": bare_plural,
        "mlc": mlc,
        "dc_per_t": dc_per_t,
        "msttr": msttr,
        "nominal_ratio": nominal_ratio,
        "para_sd": para_sd,
        "ai_style": ai_hits,
        "ai_total": ai_total,
        "triads": triads,
    }


def guess_task(text, paras):
    low = text.lower()
    t1 = ["the chart", "the graph", "the table", "the diagram", "the map",
          "the pie chart", "the bar chart", "the line graph", "the figures",
          "illustrates", "shows the", "summarise the information"]
    score = sum(1 for k in t1 if k in low)
    if re.search(r"\b(discuss both|to what extent|do you agree|advantages? outweigh|"
                 r"positive or negative|what are the (?:reasons|problems)|"
                 r"give your own opinion|do you think)\b", low):
        return 2
    return 1 if score >= 2 else 2


def report(text, task=None):
    paras = split_paragraphs(text)
    if task is None:
        task = guess_task(text, paras)
    d = analyse(text)
    d["task"] = task

    min_words = 150 if task == 1 else 250
    lines = []
    add = lines.append

    add("=" * 52)
    add("雅思写作体检报告（Task %d）" % task)
    add("=" * 52)
    add("")

    # 字数
    status = "达标" if d["words"] >= min_words else "不足，差 %d 词" % (min_words - d["words"])
    add("[字数] %d 词（最低 %d）→ %s" % (d["words"], min_words, status))
    add("[段落] %d 段，各段词数：%s" % (d["paragraphs"], d["para_words"]))

    # 句长
    add("[句数] %d 句｜平均 %.1f 词/句｜最长 %d｜最短 %d"
        % (d["sentences"], d["avg_sentence_len"], d["longest"], d["shortest"]))
    add("[句长标准差] %.1f" % d["sentence_len_sd"])
    if d["sentence_len_sd"] < 4 and d["sentences"] >= 8:
        add("    [注意] 句长太均匀，读起来像同一个句型的复制。挑 2 句拆短，挑 1 句合长。")
    if d["avg_sentence_len"] > 30:
        add("    [注意] 平均句长超过 30 词，多为长句拼接，GRA 容易被判 control 不足。")

    # 连接词
    add("")
    add("[连接词] 共 %d 次，每 100 词 %.1f 次" % (d["connector_total"], d["connectors_per_100_words"]))
    if d["connectors"]:
        items = sorted(d["connectors"].items(), key=lambda kv: -kv[1])
        add("    " + "｜".join("%s %d" % (k, v) for k, v in items))
        heavy = [k for k, v in items if v >= 4]
        if heavy:
            add("    [注意] 单个连接词用到 4 次以上：%s。CC 容易被判 mechanical。" % "、".join(heavy))
    if d["connectors_per_100_words"] > 6:
        add("    [注意] 连接词密度偏高（真实的 8 分作文通常在 3–5 次/100 词）。")

    # 重复词
    add("")
    add("[高频实词] " + "｜".join("%s×%d" % (w, n) for w, n in d["top_repeated"]))
    if d["top_repeated"] and d["top_repeated"][0][1] >= 6:
        add("    [注意] 最高频实词出现 6 次以上，LR 的 range 会被判受限。")

    # 模板句
    add("")
    if d["template_hits"]:
        add("[模板句命中] " + "｜".join("%s×%d" % (t, n) for t, n in d["template_hits"]))
        add("    [注意] 这些是考官高频识别的套话，逐条删（见 anti-ai-voice.md）。")
    else:
        add("[模板句命中] 无")

    # 其他
    add("")
    if d["dashes"]:
        add("[破折号] %d 处 —— 考场作文几乎不用，改为逗号/冒号/句号。" % d["dashes"])
    else:
        add("[破折号] 0 处")
    add("[被动语态粗估] %d 处%s" % (d["passive"],
                                "（Task 1 流程图/地图属正常，Task 2 偏多）" if d["passive"] > 6 else ""))
    if d["repeated_openings"]:
        add("[句首重复] " + "｜".join("%s×%d" % (k, v) for k, v in d["repeated_openings"]))
    if d["many_plus_singular"]:
        add("[疑似可数名词裸奔] %d 处（many/several + 单数形式，建议人工核）" % d["many_plus_singular"])

    # ---- 语言指纹：客观指标 ----
    add("")
    add("【语言指纹】以下为可计算的客观指标，用来对照 band-ladder.md 的档位描述")
    add("[句法] 平均句长 %.1f 词｜平均小句长 %.1f 词｜每句从属从句 %.2f"
        % (d["avg_sentence_len"], d["mlc"], d["dc_per_t"]))
    add("    小句长长期低于 9 词，说明复杂结构用不出来；高于 16 词要警惕句子失控。")
    add("[词汇多样性] MSTTR(50) %.3f%s"
        % (d["msttr"], "（词数少于此值时偏高，仅参考）" if d["words"] < 200 else ""))
    add("[名词化密度] %.1f%%（-tion/-ment/-ity 这类抽象名词占比；书面语通常 4–8%%）"
        % d["nominal_ratio"])
    if d["paragraphs"] > 1:
        add("[段落均衡] 各段词数标准差 %.1f%s"
            % (d["para_sd"],
               "  [注意] 段落长度过于接近，是机械排版的常见痕迹" if d["para_sd"] < 8 and d["paragraphs"] >= 4 else ""))
    if d["ai_total"]:
        add("[AI 风格词] 共 %d 次：%s"
            % (d["ai_total"], "｜".join("%s×%d" % (k, v) for k, v in
                                        sorted(d["ai_style"].items(), key=lambda kv: -kv[1]))))
        add("    这些词不算错，但密度异常时会读起来像机器写的（依据见 sources.md 第 16–18 条）。")
    else:
        add("[AI 风格词] 无")
    add("[三连并列] %d 处（\"A, B, and C\" 的排比节奏；超过 2 处要拆）" % d["triads"])

    # 语言形态落到哪一档（经验值，非官方）
    hint = BAND_HINTS[-1][2]
    for th_mls, th_dc, label in BAND_HINTS:
        if d["avg_sentence_len"] <= th_mls and d["dc_per_t"] <= th_dc:
            hint = label
            break
    add("[语言形态参考] %s" % hint)
    add("    这是按句长与从句密度做的经验归类，不是评分。定档仍须按 rubric 逐条比对。")
    add("    词汇多样性（MSTTR）不参与归类：短文本天然偏高，只用于同一篇改前改后对比。")

    add("")
    add("-" * 52)
    add("以上只是表面特征。分数请按 references/rubric-task2.md 的锚点逐条比对后人工定档，")
    add("脚本查不出的三件事：有没有答完题目、例子真不真、论证有没有机制。")
    return "\n".join(lines), d


def main():
    ap = argparse.ArgumentParser(description="IELTS 作文体检（只统计，不评分）")
    ap.add_argument("path", help="作文文本文件路径（.txt / .md）")
    ap.add_argument("--task", type=int, choices=[1, 2], help="1=小作文，2=大作文；不填自动判断")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        raise SystemExit("找不到文件：%s" % args.path)

    text = read_text(args.path)
    if count_words(text) < 20:
        raise SystemExit("词数少于 20，按官方口径这类答卷四项都是 Band 1，不用体检了。")

    text_out, data = report(text, args.task)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(text_out)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
