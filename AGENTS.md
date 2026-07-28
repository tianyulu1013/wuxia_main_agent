# Codex 项目指令：五行卡牌

本项目是一套复杂原创桌游的资料整理、查询、发布和评审辅助工程。当前阶段不是电脑游戏，也不是完整规则引擎。

新对话开始后，先阅读：

- `PROJECT_STATE.md`
- `docs/source-of-truth-policy.md`
- `docs/daily-workflow.md`

## 最高原则

- 用户是唯一作者，作者口头裁定优先级最高。
- 不要假设规则。不明确时主动提问。
- **严禁在没有用户明确口头允许的情况下擅自进行任何 git commit 或 git push 推送操作。任何代码或数据库的远程提交与发布均必须等待用户的指令。**
- 不要把 AI 理解写入源数据库。
- 源数据库只记录牌面事实和作者裁定。
- AI 强度评价、攻略、电子化推测、设计风险写入评语层，不得污染源数据。
- 旧更新日志的一次性同步已经基本结束，后续不再用旧日志反向覆盖当前数据库。

## 数据层

- 源数据：`data/cards.sqlite`、`data/cards_current/*.jsonl`
- 作者裁定/覆盖：`data/card_unit_overrides.json`、`data/card_field_overrides.json`、`data/author_ability_overrides.json`
- 单卡完整评审：`data/review/cards/<卡名>/`（`README.md`总分析，其余文件按维度拆分）
- 评审路由：`data/review/cards/index.json`
- 极简横向统计：`data/review/comparison/`（正面输出、侧面输出、正面生存、侧面生存、全局影响、名次保障／败局规避各一个文件）
- 网页评语摘要：`data/review/card_evaluations.json`
- 历史兼容评语入口：`data/review/card_notes/`
- 理解校准样本：`data/review/understanding_samples.json`
- 卡牌理解笔记：`data/review/card_understanding_notes.json`
- 术语理解层：`data/review/rule_terms.json`
- AI模块化理解入口：`docs/ai-understanding/README.md`
- 改卡候选：`data/change_candidates.json`
- 改卡候选框架：`docs/change-candidate-framework.md`

不要把评语层、候选层、规则理解层写进源数据层。

## 常用流程

查卡：

- 优先使用 `data/cards.sqlite` 或 `scripts/query_cards.py`
- 网页入口通常是 `http://127.0.0.1:8765`

改卡：

1. 查当前卡牌文本、卡面、已有裁定。
2. 分析艺术形象、规则稳定性、文本清晰度、玩法强度。
3. 生成候选新版文本。
4. 写入候选层或先给用户确认。
5. 用户确认后才更新数据库、Excel、PSD、更新日志。

多人一卡：

- `unit` 必须是真实人物/单位。
- 不使用虚拟 `全体` unit。
- 共同特技通过 owner units 包含所有真实 unit 表示。
- 单人卡默认一个 unit。
- `五个人头` 基本按一个 unit 处理，但计人数为 5。

发布：

- 主工程仓库：`https://github.com/tianyulu1013/wuxia_main_agent`
- 静态发布仓库：`https://github.com/tianyulu1013/wuxia_static_publish`
- `site_export/` 和 `static_publish_repo/` 不进入主工程 Git。

## 重要概念

不要混淆：

- 攻击 / 伤害 / 扣血 / 生命流失 / 杀死 / 死亡 / 离场 / 清除
- 回合 / 轮
- 不在场 / 离场 / 破空
- 专属特技 / 身份特技 / 字 / 大招

专属特技是特技名带 `【】`，不是特技类型。身份特技通常是描述末尾带 `（身份）`。`内功`、`招式`、`武功` 统称“大招”。

## 评审反馈与自适应分析机制

每一张卡牌的评审都不应是孤立存在的，AI 必须严格执行闭环反馈与自适应分析：

1. **作者反馈分层记录**：当作者作出口头裁定或校准后，先判断内容性质。普遍流程进入核心规则，局部机制进入专项规则，特殊词义进入术语层，评价方法进入类别/功能模块，具体单卡计算进入案例和单卡理解，玩家意愿进入玩家动态；不得把所有反馈一律写入 `data/review/rule_terms.json`。本卡相关作者原话仍须在`data/review/cards/<卡名>/author-calibration.md`的“作者校准完整记录”中保存。
2. **横向自适应检索**：在分析后面的卡牌前，AI 必须检索机制相近 of已锁定卡牌锚点及“可迁移结论”，对比其爆发、生存和泛用性分值，以此修正新卡评价，严禁分值倒挂或无依据脑补。
3. **评审模块完整性限制**：完整单卡证据必须在`data/review/cards/<卡名>/`中分文件包含**正面输出**、**侧面输出**、**正面生存**、**侧面生存**、**全局影响力**、**名次保障／败局规避**、**优点**、**缺点**、**规则风险**、**电子化风险**和**作者校准**。`README.md`与网页`card_evaluations.json`只承担摘要，但必须提供完整证据路由，严禁因摘要化而丢失任何模块。
4. **分文件不减证据密度**：人物目录只用于按需读取，不得把详细维度文件也压缩成结论。计算文件必须保留变量定义、概率来源、期望与方差推导、离散分布、截断算法和适用边界；生存文件必须保留承伤模型与环境敏感性；玩法比较文件必须保留从机制证据到强弱结论的完整推理链和现实反制。结构化JSON不能替代Markdown推导。
5. **横向统计必须极简**：横向比较默认只读`data/review/comparison/`中当前维度对应的一个文件。正面、侧面输出各人物只保留一个主期望、确定穿透输出、穿透率和一句说明；横表摘要登记全体均值、总体标准差及穿透来源集中度。正面、侧面生存、全局影响及名次保障／败局规避只保留强弱判断和一句依据。复杂公式与分支留在单卡目录，不复制进横向表。
6. **详细统计继续逐人写入**：每名已完成精评的战斗人物仍须同步`data/review/calibrated_stats.json`和`data/review/combat_baselines.json`，用于未来复算和环境回归；它们不是日常横向比较的默认读取入口。


## 详细技能文档

需要更细流程时阅读：

- `docs/skills/wuxia-project-handoff.md`
- `docs/skills/wuxia-source-policy.md`
- `docs/skills/wuxia-database-architecture.md`
- `docs/skills/wuxia-data-query.md`
- `docs/skills/wuxia-card-review.md`
- `docs/change-candidate-framework.md`
- `docs/rule-terms-understanding.md`
- `docs/ai-understanding/README.md`
- `.agents/skills/wuxia-card-change-flow/SKILL.md`
- `docs/skills/wuxia-multi-unit.md`
- `docs/skills/wuxia-release-publish.md`
- `.agents/skills/wuxia-release-flow/SKILL.md`
- `docs/skills/wuxia-rulebook-work.md`
