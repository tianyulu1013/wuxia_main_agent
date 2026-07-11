# Skill: 源数据不污染

## 核心原则

源数据库只记录牌面事实和作者裁定。AI 的理解、推测、攻略、强度评价、电子化建议不能写入源数据库。

## 权威顺序

1. 作者口头裁定。
2. 当前数据库与当前基准 Excel。
3. 当前 release/PSD 牌面，用于核对录入错误。
4. 旧更新日志，仅作为历史线索。
5. 未来更新日志，由确认后的变更生成。

## 可以写入源数据的内容

- 卡牌当前文本。
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

- 源数据：`data/cards.sqlite`、`data/cards_current/*.jsonl`
- 作者裁定/覆盖：`data/card_unit_overrides.json`、`data/card_field_overrides.json`、`data/author_ability_overrides.json`
- 评语层：`data/card_reviews.json`
- 改卡候选：`data/change_candidates.json`

## 遇到不确定内容

不要猜。记录为待问问题，或直接向用户确认。
