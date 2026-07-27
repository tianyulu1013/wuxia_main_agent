# 评语层与改卡候选层

这两层不是牌面事实数据。

## 文件

- `data/review/cards/<卡名>/`：当前完整单卡评审，按维度分文件。
- `data/review/cards/index.json`：人物与维度的结构化路由。
- `data/review/card_evaluations.json`：网页使用的结构化摘要。
- `data/review/card_notes/`：历史兼容入口；已迁移人物只保留导航。
- `data/review/card_understanding_notes.json`：单卡作者校准和理解。
- `data/card_reviews.json`：历史兼容评语文件，不再作为新评审默认写入目标。
- `data/change_candidates.json`：改卡候选、候选新版文本、更新日志草稿、确认状态。

## 原则

- 牌面/Excel/数据库仍是源数据层。
- 作者口头裁定可以写入评语层，但不能自动改写源数据。
- AI理解、强度评价、电子化判断只能写入评语层。
- 改卡候选必须经作者确认后，才进入源数据更新流程。

## 推荐流程

1. 作者提出修改意图。
2. AI生成候选新版文本和理由，写入 `change_candidates.json`。
3. 作者确认、拒绝或继续讨论。
4. 确认后再改 PSD、Excel 和数据库。
5. 最后生成对玩家可读的更新日志。
