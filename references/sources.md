# 依据台账（每条优化背后的出处）

这份表的作用：任何一个设计决定，都能追到"为什么这么做"。同时标明**我拿到了什么、没拿到什么**——没拿到全文的，不许在交付里说成"我读了原文"。

核实日期：2026-11-17。

**来源等级**（自己心里要有数）：
- **A 一手**：官方文件全文／论文原文，我实际读到内容
- **B 二手**：权威机构页面或检索索引给出的全文片段，未取得原始文件
- **C 书目**：有明确出版信息，但我没核到原文页码
- **待核**：流传广但没找到可靠出处

---

## 一、雅思评分标准（技能的核心依据）

| # | 来源 | 等级 | 用来支撑什么 |
|---|---|---|---|
| 1 | **IELTS Writing Band Descriptors**（Task 1 与 Task 2 合并本，2023 年 5 月更新），British Council `takeielts.britishcouncil.org/sites/default/files/[downloads]/ielts_writing_band_descriptors.pdf` | **B**：直连返回超时（curl 状态 000），但检索索引返回了该 PDF 的连续正文（Band 9/8/7 四项 + Band 3/2/1/0 片段），与第 2 条逐字一致 | `rubric-task1.md` / `rubric-task2.md` 全部英文描述语；`META.1` 的"完整满足"规则 |
| 2 | GitHub 仓库 `AaronL725/ielts-writing-review-skills` 内的 band descriptors 提取件（本地 `_ref/`） | **A**（结构完整，9–0 全档） | 与第 1 条交叉核对，确认不是某一家的改写 |
| 3 | IDP 官方文章《IELTS Writing Task 2: Why can't I get a band 8》`ielts.idp.com/korea/prepare/article-writing-task-2-why-cant-i-get-a-band-8/en-gb` | **A**（页面可访问，已读） | 7 分与 8 分的差异点（over-generalise、cohesion 过度使用连接词、每段中心议题） |
| 4 | **IDP IELTS Focus: Academic Writing Task 2, Student Book**（IDP Education, 2020）`info.ielts.idp.com/rs/561-EIU-022/images/...pdf` | **A**（已下载 60 页，pypdf 可读；但评分表为图形，文字提不出来） | **反面对照**：证明旧版写的是 `fully addresses all parts of the task`。用于 `scoring-rubric.md` 的"版本陷阱"一节 |
| 5 | 官方改版说明与第三方整理（ielts.org 2023-05 公告经 e2language、PrepEx 转述） | **B** | 确认 2023 年 5 月改版、取消了考官机密版、现行 PDF 为 Task 1+2 合并本 |
| 6 | **IELTS 官方 "Trust IELTS"** `ielts.org/take-a-test/preparation-resources/trust-ielts`；《IELTS is the most trusted…》 | **A** | "Selected results are marked twice" → 支撑批改要给区间、标注不确定性 |
| 7 | 中国雅思官网《公平公正 测评精准成绩可靠》`chinaielts.org/why-choose-ielts/fairness` | **A** | 写作由全球阅卷中心匿名双评、考官每两年再认证 → 同上 |

**版本结论**：技能统一采用 2023 年 5 月现行版。凡出现 `addresses all parts of the task` 的，一律视为旧版，不得称"现行官方标准"。

---

## 二、事实类（写进范文的数字必须有出处）

| # | 来源 | 等级 | 数据用途 |
|---|---|---|---|
| 8 | **GOV.UK**《Changes to tuition fees: 2025 to 2026 academic year》`gov.uk/government/publications/tuition-fees-and-student-support-2025-to-2026-academic-year/...` | **A**（已读全文） | 英格兰 2025/26 学费上限 £9,535 |
| 9 | **legislation.gov.uk** SI 2026/329《Higher education: tuition fee limits … 2026 to 2027 and 2027 to 2028》 | **A**（已读摘要正文） | 2026/27 £9,790；2027/28 £10,050；历史沿革 £9,000→£9,250→£9,535 |
| 10 | **Public Health England**《Sugar reduction: report on progress between 2015 and 2018》(2019) | **A**（已读摘要） | 应税饮料糖含量 2015–2018 降 28.8%；同期其他食品类别仅 2.9% |
| 11 | **NIHR**《Sugar levels in UK soft drinks lowered following government levy》＋ PLoS Medicine 研究（牛津/剑桥等） | **A** | 2019 年 2 月仅 15% 饮料仍应税（原 52%）；改配方是主要机制 |
| 12 | 英国议会 **Health and Social Care Committee** 书面证词（2025，Recipe for Change） | **B**（二手转述 OHID 数据） | 2015–2024 降 47.4%；累计税收超 £22 亿。标注为二手 |
| 13 | **TfL**《Annual report 2002/03》 | **A** | 拥堵收费 2003-02-17 启动、£5、8 平方英里、07:00–18:30；头三个月车流 −16%、拥堵 −32% |
| 14 | **TfL**《Central London Congestion Charging Scheme: ex-post evaluation》 | **A** | 收费区车流约 −17%（2002→2003），模型与实测对照 |
| 15 | **TfL** 2025 年收费调整咨询页 `haveyoursay.tfl.gov.uk/congestion-charge-proposals` | **A** | 官方回顾口径：拥堵 −30%、车流 −15%；费率沿革 £5→£8→£15→（提议）£18 |

---

## 三、AI 文本特征（支撑"去 AI 味"从经验判断升级为有据可查）

| # | 来源 | 等级 | 用来支撑什么 |
|---|---|---|---|
| 16 | Kobak, D., González-Márquez, R., Horvát, E.-Á., & Lause, J. (2025). *Delving into LLM-assisted writing in biomedical publications through excess vocabulary.* **Science Advances, 11(27)**, eadt3813. DOI: 10.1126/sciadv.adt3813（预印本 arXiv:2406.07016） | **B**（摘要与多家转述一致；DOI 直连 403） | 1500 万篇 PubMed 摘要中，2024 年 "delves / underscores / showcasing" 等**风格词**异常激增；估计 ≥13.5% 的 2024 摘要经 LLM 处理。→ 支撑"AI 词表"不是拍脑袋 |
| 17 | Liang, W. et al. (2024). *Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews.* ICML 2024 | **B**（经转述，未读原文） | ICLR 2024 审稿中 meticulous / intricate / commendable 出现率异常升高（转述数字：34.7× / 11.2× / 9.8×）。用于说明"形容词偏好"是跨语域现象 |
| 18 | Juzek, T. & Ward, Z. (2025). *Why Does ChatGPT "Delve" So Much?* COLING 2025 | **B** | 21 个过度使用词清单；并指出"单纯换词不够，结构习惯才是根" |

**这三条共同指向一个结论**（也是本技能 `anti-ai-voice.md` 的设计逻辑）：删词只是表面，真正要改的是**句长趋同、段落同构、无具体例证、结尾必总结**这四件事。所以 `essay_stats.py` 统计的是句长标准差、段落词数方差、并列结构次数，而不只是查黑名单。

---

## 四、语言测量方法（支撑脚本的指标选择）

| # | 来源 | 等级 | 用来支撑什么 |
|---|---|---|---|
| 19 | Lu, X. (2010). *Automatic analysis of syntactic complexity in second language writing.* **International Journal of Corpus Linguistics, 15(4), 474–496.**（L2SCA 工具，14 项指标） | **A**（14 项指标的名称与公式经多篇论文交叉核实） | `essay_stats.py` 的 MLS / MLT / MLC / DC-T / CN-T 近似指标；并承认"正则近似 ≠ L2SCA" |
| 20 | Wolfe-Quintero, K., Inagaki, K., & Kim, H.-Y. (1998). *Second Language Development in Writing: Measures of Fluency, Accuracy, and Complexity.* | **C** | 长度类指标（MLT、MLC）与写作发展的关系，是第 19 条的理论前置 |
| 21 | Swales, J. (1990). *Genre Analysis: English in Academic and Research Settings.* | **C** | Task 1 的 overview 属于该体裁的**必现语步**（obligatory move），这是"没 overview 就掉档"的体裁学依据；官方 7 分描述语的 `presents a clear overview` 与之吻合 |
| 22 | Weigle, S. C. (2002). *Assessing Writing.* Cambridge University Press. | **C** | 评分者变异（rater variance）是写作评分的固有来源 → 支撑"给区间、标最不确定项" |

---

## 五、RAG 与防幻觉（支撑检索层设计）

| # | 来源 | 等级 | 用来支撑什么 |
|---|---|---|---|
| 23 | Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. arXiv:2005.11401 | **C**（方法论文献，未逐字核原文） | 生成前先检索外部证据，能显著降低事实性错误 → `rag_search.py` 的存在理由 |
| 24 | Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* arXiv:2312.10997 | **C** | 幻觉分"内在幻觉"（与给定材料矛盾）与"外在幻觉"（材料里没有）→ `verify_citations.py` 分别对应：引文对不上 = 内在；引用号不存在 = 外在 |
| 25 | Asai, A. et al. (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection.* arXiv:2310.11511 | **C** | "生成后自评引用是否被支持"这一环节 → 交付前必跑引用核对 |

> 这三条属方法学引用，用来解释设计思路，不是雅思评分依据。别在给用户的批改里拿它们当论据。

---

## 六、待核清单（明确知道自己不知道）

| 事项 | 现状 |
|---|---|
| "用模板作文直接判 4 分" | 只见于培训机构博客。官方描述语无此条。技能里标**待核**，不当事实 |
| 芬兰基本收入试验的具体效应量 | 方向（心理状态改善、就业无显著负面）有共识；具体百分比未核到一手报告，标待核 |
| 安大略省 40 小时社区服务 | 流传广，未核到省教育厅一手文件，标待核 |
| 德国双元制覆盖比例、青年失业率 | 未核，只保留定性表述 |
| 日本/意大利护理人力缺口数字 | 未核，只保留定性 |
| IELTS 写作各分数段全球/中国考生均分 | 未核，技能中不出现任何"中国考生平均 5.8"这类数字 |
| 2023 版官方 PDF 的本地副本 | 直连 403/超时，只有检索索引返回的正文片段。**严格说我没有原件二进制** |

---

## 七、这份台账怎么维护

1. 新增任何带数字的素材，先在这里登记来源，再写进 `fact-registry.md`。
2. 官方文件一年内至少重核一次（学费每年调、拥堵收费 2026 年可能变）。
3. 等级为 B/C 的条目，对外表述时降一格说话："据官方公开说明"而不是"官方文件第 3 页写明"。
