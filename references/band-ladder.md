# 分档语言指纹：怎么写出"看起来就是 6.5 / 7.5 / 8.5"的文章

用户指定档位时，不要拿一篇 8 分文章删几句词冒充 6 分。**每一档要重写**：句子长度、例子具体度、错误密度、连接方式全都不同。下面给判定标准和对照样本。

## 一、各档的硬指标（写作时照着控制）

下表第 3 列与 `scripts/essay_stats.py` 输出的"每句从属从句"是**同一个口径**（脚本里的 `dc_per_t`），可以直接对照。

| 档位 | 词数 | 平均句长 | 每句从属从句 | 错误密度 | 例子具体度 | 段落 |
|---|---|---|---|---|---|---|
| 5.5 | 225–245 | 12–14 词 | 0.15–0.25 | 每 3–4 句 1 处明显错误 | 泛泛（"很多人""有些国家"） | 3 段，可能不分段清楚 |
| 6.0 | 235–255 | 14–16 词 | 0.25–0.35 | 每 5–6 句 1 处 | 笼统，靠 "for example" 硬举 | 4 段，主体段偏短 |
| 6.5 | 250–270 | 16–18 词 | 0.35–0.45 | 每 8–10 句 1 处 | 有一个具体点，其余笼统 | 4 段，结构清楚 |
| 7.0 | 260–280 | 18–20 词 | 0.45–0.55 | 每 12–15 句 1 处 | 两个理由各有一个具体落点 | 4 段，段内顺序合理 |
| 7.5 | 270–295 | 18–22 词 | 0.55–0.65 | 每 15–20 句 1 处（多为搭配不准，不是语法错） | 具体且与论点咬合 | 4 段，有让步/反驳 |
| 8.0 | 275–300 | 19–23 词 | 0.60–0.75 | 零星，非系统性 | 具体到机制层面 | 4 段，段落有推进而非并列 |
| 8.5 | 280–310 | 20–24 词 | 0.70–0.85 | 极少，且是不影响理解的 slip | 精准、有反常识的洞察 | 4 段，段与段之间有递进 |
| 9.0 | 285–315 | 20–26 词 | 0.75–0.95 | 几乎为零 | 每个论断都能落到一个可验证的现象 | 分段完全服从论证 |

注意三件事：

1. **词数不涨分，但不足会掉分。** 260 词写好是 7.5，350 词注水还是 6。上表是"该档常见长度"，不是目标。
2. **5.5 档的词数区间低于官方 250 词下限**，这一档在真实考试里正好对应"字数不足 + 论证没展开"的答卷。写范文时要提醒用户：那是被打低分的样子，不是努力方向。
3. **8.5 以上不靠生僻词，靠"每个词都对"。** 强行塞 `plethora`、`myriad`、`paradigm shift` 只会掉到 7。

### 这些数字是哪来的（别把经验当标准）

| 列 | 依据 | 性质 |
|---|---|---|
| 词数 | 官方最低字数（Task 1 ≥150 / Task 2 ≥250）+ 常见答卷长度分布 | 下限是官方，区间是经验 |
| 平均句长、每句从属从句 | 指标定义参考 Lu (2010) 的 MLS / DC-T；**具体阈值是经验值** | 经验 |
| 错误密度 | 按官方 "error-free sentences are frequent"（7 分）等措辞折算 | 经验（换算关系无官方对应） |
| 例子具体度 | 直接对应官方 TR 描述语的 over-generalise / well extended | 官方措辞 + 我的转述 |

**用的时候就一句话**：这张表帮你把"语言长相"调到目标档附近，但**定档只认 `rubric-task2.md` 的描述语**。表与描述语冲突时，以描述语为准，并把冲突报给用户。

## 二、同一段内容的五个档位（大作文主体段）

题目：*Some people think university students should study whatever they like. Others believe they should only be allowed to study subjects useful in the future. Discuss both views and give your own opinion.*
这一段要说的意思：兴趣能带来持续投入。

### 5.5 档

> Firstly, students should study the subject they like. Because if they study the subject they like, they will be more happy and they can learn better. For example, my friend he likes music very much, so he study music in university and he is very good at it now. If students study a subject they do not like, they cannot learn well, they will waste their time. So interest is very important for study.

**为什么是 5.5**：`Because` 开头独立成句（句子片段）；`my friend he` 重复主语；`he study` 主谓不一致；`more happy` 应为 `happier`；两个句子用逗号连接（run-on）。观点只有一层"兴趣重要"，没有机制。连接靠 `Firstly / For example / So`，机械。

### 6.5 档

> One reason for allowing students to choose their own subjects is that interest makes learning more effective. Students who study a field they enjoy tend to spend more time on it and are less likely to give up when the work becomes difficult. For example, a student who is genuinely interested in history will read beyond the reading list and write better essays than someone who was pushed into engineering by their parents. In contrast, students who are forced into "useful" subjects often lose motivation after the first year.

**为什么是 6.5**：语法基本干净，有定语从句、比较结构；但"为什么兴趣带来投入"仍停在常识层（`tend to spend more time`），例子是假设的人（a student who...），没有落到真实机制。`In contrast` 用得对，但整段仍是"观点 + 举例"两件套，缺后果和落点。

### 7.5 档

> The case for free choice rests on how motivation actually works. A student who has chosen a subject has already made a judgement about what they are good at, and that judgement tends to hold: undergraduates who change courses usually do so because the subject they were placed in demanded a kind of work they had never enjoyed. In China, where many students are assigned a major on the basis of exam scores rather than preference, this shows up in the transfer applications that follow the first year's results. A system that ignores preference does not produce committed graduates; it produces capable people who would rather be somewhere else.

**为什么是 7.5**：机制清楚（"自己做的判断会成立"）；例子落到真实制度（中国按分数分配专业 → 转专业申请）；结尾一句把论点收紧（`capable people who would rather be somewhere else`）。错误为零，但没有 8 分那种"层层递进"的密度。

### 8.5 档

> Motivation is not a mood that can be supplied later; it is the residue of a decision the student has made themselves. Where admission is settled by examination scores rather than preference, the mismatch surfaces early, in second-year drop-out figures and in the queues for internal transfer that form the week results are posted. Letting applicants choose does not guarantee commitment, but it removes the most common reason for its absence: a course of study that was never theirs to begin with.

**为什么是 8.5**：开头一句重新定义了"兴趣"（不是情绪，是决策的产物），这是观点层面的推进，不是措辞层面的漂亮；三个具体现象（退学率、转专业排队、放榜那一周）都指向同一机制；最后一句承认局限（`does not guarantee`）后立刻收紧。没有一个词是为了显得高级而存在的。

### 从 6.5 到 8.5，实际改了什么

1. **把"常识"换成"机制"**：`interest makes learning more effective` → `a judgement they made themselves tends to hold`
2. **把假设的例子换成真实的现象**：`a student who is interested in history` → `transfer applications after the first year's results`
3. **加一句承认局限**：`does not guarantee commitment, but...`
4. **句子长短交错**：8.5 版有一句 8 词，有一句 40 词，节奏不是平的
5. **删掉所有"强调副词"**：very / really / extremely / highly 在 7.5 以上基本不出现

## 三、Task 1 的两个档位对照

题目：折线图，2000–2020 年三个国家家庭互联网接入率（A 国 20%→90%，B 国 45%→60%，C 国 5%→85%）。

### 6.0 档

> The line graph shows the percentage of households with internet access in three countries between 2000 and 2020. Overall, all three countries increased. In 2000, country A was 20% and country B was 45% and country C was 5%. In 2010, country A was 55%, country B was 52% and country C was 40%. In 2020, country A was 90%, country B was 60% and country C was 85%. Country A increased the most. Country C also increased a lot.

**为什么是 6.0**：有 overview（`all three countries increased`）但等同于没说；数据是逐年念，没有分组；没有交叉点（C 在 2015 前后超过 B，这是全图最值得写的一件事，被漏掉了）；句式重复 `was ... was ... was`。

### 8.0 档

> The graph tracks household internet access in three countries over two decades. Overall, access rose everywhere, but the gap between the leaders and the late starters closed almost completely: country C, which began at 5%, finished within five points of country A, the early leader.
> Country A climbed steadily from 20% in 2000 to 55% by 2010, then accelerated to 90% in 2020. Country C followed a steeper curve from a far lower base, passing 40% in 2010 and overtaking country B in the middle of the decade. Country B, by contrast, grew slowly and levelled off after 2010, ending at 60%, the lowest of the three.

**为什么是 8.0**：overview 说的是"差距缩小"这个真正的故事，一个数字都没放；细节按"上升组 / 停滞组"分组；点出了超越（`overtaking country B`）；`from a far lower base`、`levelled off` 是精准而非华丽。

## 四、给用户的选档建议（拆题时用得上）

| 用户现状 | 该看/该练的范文档位 | 为什么 |
|---|---|---|
| 5.0–5.5 | 6.0 | 差距在一档以内，能照着改；9 分范文会让他觉得"这不是英语，是魔法" |
| 6.0 | 6.5–7.0 | 补齐 overview / 论证展开这两件事就够 |
| 6.5 | 7.0–7.5 | 重点在"具体化"和"去机械化衔接" |
| 7.0 | 7.5–8.0 | 重点在让步、反驳、词汇精准度 |
| 7.5+ | 8.0–8.5 | 重点在段落推进和句法节奏，不再是句子层面 |

**不要给 6 分考生写 9 分范文。** 那不是激励，是劝退；而且他背下来用，反而因为不自然被压分。

## 五、8.5 / 9.0 的诚实说明

- 8.5–9.0 的范文，母语者写出来才自然。非母语者模仿时最容易出现两种痕迹：一是生僻词堆砌，二是句式过度对称（三个从句排比）。
- 如果你写出来的 9 分范文读起来"每句都很厉害"，那它其实是 7.5。真正的高分段落是**不均匀**的：有一句很长，有一句只有六个词。
- 用户坚持要 9.0 时，照写，但在说明里加一句：这一档在真实考试里通常对应母语者水平，参考结构即可，不要逐句背。

## 六、写完对照检查

- [ ] 平均句长是否符合目标档位？（太均匀说明你在用同一个句型模板）
- [ ] 复杂句是不是"为了复杂而复杂"？（拆开读一遍，读不懂就降档）
- [ ] 每一档的错误密度是否匹配？（6.0 允许有错，但不要故意写错别字；8.0 不许有系统性错误）
- [ ] 例子有没有落到具体的人/地/机构/机制？
- [ ] 有没有三个并列的形容词或三个并列的从句？（有就删一个）
