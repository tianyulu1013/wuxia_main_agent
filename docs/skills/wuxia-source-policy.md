# Skill: 源数据不污染

## 核心原则

源数据库只记录牌面事实和作者裁定。AI 的理解、推测、攻略、强度评价、电子化建议不能写入源数据库。

## 权威顺序

1. 作者口头裁定。
2. JSONL 结构化源数据（`data/cards_current/*.jsonl`）。
3. 编译回填后的基准 Excel（`已制作_2025日志同步候选_PSD校准.xlsx`）。
4. 当前 release/PSD 牌面，用于核对录入错误。
5. 旧更新日志，仅作为历史线索。
6. 未来更新日志，由确认后的变更生成。

## 编译与同步

详细的数据源关系和同步流程见：[五行卡牌数据源与编译架构](file:///d:/workspace/wuxia-card-agent/docs/skills/wuxia-database-architecture.md)。

## 可以写入源数据的内容

- 卡牌当前文本与结构化特技属性（直接修改 JSONL 中的 `abilities` 数组）。
- 作者明确裁定的字段。
- 作者确认过的多人一卡 unit、特技所属、共享生命。
- 作者确认过的字段修正。

## 不得写入源数据的内容

- AI 对人物关系的脑补。
- AI 对卡牌强弱的判断。
- AI 对规则如何电子化的推测。
- 攻略、用法、风险标签。
- 未经作者确认的候选改动。

## 正确存放位置

- 结构化源数据（唯一可信源）：`data/cards_current/*.jsonl`
- 编译输出数据库：`data/cards.sqlite`
- 自动同步回填的 Excel 镜像：`outputs/.../已制作_2025日志同步候选_PSD校准.xlsx`
- 历史兼容评语：`data/card_reviews.json`
- 当前评语层：`data/review/card_evaluations.json`、`data/review/card_notes/`、`data/review/card_understanding_notes.json`
- 改卡候选：`data/change_candidates.json`

## 遇到不确定内容

不要猜。记录为待问问题，或直接向用户确认。
