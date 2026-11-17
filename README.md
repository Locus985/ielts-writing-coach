# 雅思大小作文教练 / IELTS Writing Coach

一个跑在 WorkBuddy 里的雅思写作技能：拆题、列给分点、按你指定的档位写范文、批改你自己的作文。它不联网，不装依赖，评分标准里的每一条都能顺着编号查到官方原文。

## 为什么需要它

雅思范文到处都是，能用的不多。网上标着 band 8 的范文，你照着写一篇交给考官，分数可能只有 6，因为没人告诉你那个 8 分是靠什么撑起来的。

AI 写雅思作文还有另一个毛病：满篇 `In today's modern society` 和 `delve into`，看着高级，读着像说明书。官方词汇描述语的 Band 4 里写着 `inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material)`，背来的句子本身就在扣分之列。网上不少文章把这句挂在 6 分名下，那是标错了档位。

这个技能的做法是先讲清这道题的给分点在哪儿，再按你选的档位往下写。

## 能做什么

**拆题。** 给一道 Task 2 议论文，它判题型（观点类、讨论类、利弊类、问题解决类、双问类），指出题目里有几个必须回答的问题，漏一个就直接掉到 5 分。给一道 Task 1，它先读图，分清是线图、柱图、饼图、表格、流程还是地图，再决定怎么分组。

**给分点。** 针对这一道题列出四项标准各自要满足什么，每条后面挂一个官方描述语的编号。

**分档范文。** 5.5 到 9.0 每档都能写。同一道题在 6.5 和 8.0 两个档位下差在哪儿，可以并排看。范文里的数字必须能在事实登记表里指到一行，指不到就改成定性描述。

**批改。** 按四项标准逐项打分，每处扣分引你原句，最后给三条最值得改的地方和一段改写示范。

## 安装

克隆到技能目录：

```bash
git clone https://github.com/<your-name>/ielts-writing-coach.git \
  ~/.workbuddy/skills/ielts-writing-coach
```

Windows 上目录是 `C:\Users\<你的用户名>\.workbuddy\skills\ielts-writing-coach`。

装完重开一个会话，说「这道大作文帮我拆题，范文要 6.5 分」就能触发。

## 三个脚本

不需要联网，不需要 `pip install`，纯 Python 标准库（3.8 以上）。

语料库检索：

```bash
python scripts/rag_search.py "小作文 overview 关键特征" --task 1
python scripts/rag_search.py "cohesion mechanical 衔接"
python scripts/rag_search.py "糖税 改革" --file fact-registry
python scripts/rag_search.py --list
```

中文提问能查到英文原文，因为索引里同时存了中英文关键词。`kb_index.json` 是缓存，首次运行自动生成，仓库里没放这个文件。

作文体检：

```bash
python scripts/essay_stats.py my-essay.txt --task 2
```

数词数、句长与起伏、连接词密度、模板句命中、AI 风格词、从属从句密度、名词化密度、段落均衡。它只统计表面特征，不打分。

引用核对：

```bash
python scripts/verify_citations.py draft.md --strict
```

抓三类问题：编号编造、引文改词、英文引文没标出处。有任何一项，退出码为 1。

## 它凭什么可信

评分标准锚点化。四项标准从 4 档到 9 档，每档一条编号，共 30 条。例如 `[R:T2.TR.7]` 指大作文任务回应第 7 档，`[R:T2.GRA.7]` 指语法第 7 档。打分的每一处判断都要带编号，你可以打开 `references/rubric-task2.md` 逐字核对这句话是官方原文还是概括出来的。

Task 1 的情况要说清楚：任务完成（TA）有独立的 6 条锚点，另外三项直接复用 Task 2 的编号，差异写在 `T1.DIFF.1` 里。官方对 Task 1 的词汇和语法描述多了一句 `within the scope of the task`，小作文只需要描述图表那一小片词汇，不必强求议论词汇，这个差异不写清就会把范文标准抬错。

版本对齐。官方在 2023 年 5 月改写过写作评分标准，旧版写 `addresses all parts of the task`，现行版写 `the main parts of the prompt`。市面上的教材至今大量在传旧版，两句话长得极像，混在一起看不出来。仓库里有一张新旧对照表，看到旧措辞被当成现行标准，可以直接判定出处有问题。

数字有出处。范文里每个数字都要在 `references/fact-registry.md` 里指到一行，标了来源等级。查不到一手来源的事实单独列在待核区，只许定性描述，不许加数字。例如英格兰本科学费上限 2025/26 是 £9,535（GOV.UK），英国含糖饮料税实施后 2015 到 2018 年应税饮料糖含量降 28.8%（PHE 2019 报告），这两个都能指到文件。

成文后过一道闸门。定稿前跑语言体检和引用核对两个脚本，模板句和编造的编号会被拦下来。

## 目录结构

```
ielts-writing-coach/
├── SKILL.md                      主流程：路由、拆题、检索、写作、批改、禁令
├── README.md
├── LICENSE
├── references/
│   ├── rubric-task1.md           Task 1 任务完成锚点库（9 到 4 档）与三项措辞差异
│   ├── rubric-task2.md           Task 2 四项标准锚点库（9 到 4 档）
│   ├── scoring-rubric.md         评分标准使用说明与新旧版本对照
│   ├── task1-playbook.md         六种图表怎么读、overview 写法、数据语言
│   ├── task2-playbook.md         五种题型、四段骨架、论证公式、话题素材
│   ├── band-ladder.md            5.5 到 9.0 每档的词数、句长、错误密度
│   ├── anti-ai-voice.md          模板句黑名单、句式毛病、真人写作特征
│   ├── assessment-protocol.md    批改顺序、半分怎么给、十二种常见病
│   ├── fact-registry.md          可引用事实与来源等级
│   ├── sources.md                25 条参考文献，标注核验等级
│   └── rag-protocol.md           检索协议与引用规则
├── scripts/
│   ├── rag_search.py             BM25 检索，140 个知识块
│   ├── essay_stats.py            语言体检
│   └── verify_citations.py       引用逐字核对
└── examples/
    └── demo-task2-band6.5.txt    一篇 6.5 档大作文范文
```

## 已知局限

官方 2023 版评分标准 PDF 没能直接下载，`ielts.org` 返回 403，British Council 站点超时。描述语文本由三个来源交叉核对一致（搜索引擎抓到的官方 PDF 正文、GitHub 上的提取件、IDP 官网文章页），手里没有一手原件。这一条写在 `sources.md` 第六节，没有藏起来。

`band-ladder.md` 里「平均句长 18 到 20 词对应 7 分」这类阈值是经验值，文件里已标注非官方。定档只认描述语原文。

`essay_stats.py` 输出的「语言形态参考」是按句长和从句密度做的归类，不是评分。词汇多样性（MSTTR）我只保留为改前改后的对比指标，因为 250 词的短文 TTR 天然偏高，用它会把手写的 6.5 分范文误判成 8 分。

## 版权与许可

代码与写作内容采用 MIT 许可，见 `LICENSE`。

`references/` 里的评分描述语引自 IELTS 官方公开的 band descriptors，用于逐字对照和引用核验，版权归 IELTS（British Council、IDP、Cambridge University Press & Assessment）所有。本仓库不包含剑桥真题的图表原图或教师批改样本。

## English summary

IELTS Writing Coach is a WorkBuddy skill for IELTS Writing Task 1 and Task 2. Give it a prompt and it identifies the task type, lists what the four criteria require for that specific prompt, and writes a model answer at any band from 5.5 to 9.0. Send your own essay and it marks the four criteria in turn, quoting the sentence behind each deduction.

Every band level of the four criteria carries an anchor ID, 30 in total, such as `[R:T2.TR.8]` for task response at band 8 or `[R:T2.GRA.7]` for grammatical range at band 7. Each mark must cite one, so a claim can be traced back to the official wording. Numbers in a model answer have to point to a row in the fact registry; anything unresolved stays qualitative. A bundled script compares citations character by character and fails on invented IDs, altered quotes, or unattributed English quotations.

Three Python scripts handle retrieval, text statistics, and citation checking. None needs a network connection or a package install. Descriptor wording was cross-checked across three sources rather than taken from a downloaded original, since the official 2023 PDF was not directly accessible; this is documented in `references/sources.md`.
