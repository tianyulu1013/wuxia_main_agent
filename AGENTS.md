# Codex 项目指令：五行卡牌

本项目是一套复杂原创桌游的资料整理、查询、发布和评审辅助工程。当前阶段不是电脑游戏，也不是完整规则引擎。

新对话开始后，先阅读：

- `PROJECT_STATE.md`
- `docs/source-of-truth-policy.md`
- `docs/daily-workflow.md`

## 最高原则

- 用户是唯一作者，作者口头裁定优先级最高。
- 不要假设规则。不明确时主动提问。
- 不要把 AI 理解写入源数据库。
- 源数据库只记录牌面事实和作者裁定。
- AI 强度评价、攻略、电子化推测、设计风险写入评语层，不得污染源数据。
- 旧更新日志的一次性同步已经基本结束，后续不再用旧日志反向覆盖当前数据库。

## 数据层

- 源数据：`data/cards.sqlite`、`data/cards_current/*.jsonl`
- 作者裁定/覆盖：`data/card_unit_overrides.json`、`data/card_field_overrides.json`、`data/author_ability_overrides.json`
- AI/作者评语：`data/card_reviews.json`
- 理解校准样本：`data/review/understanding_samples.json`
- 卡牌理解笔记：`data/review/card_understanding_notes.json`
- 术语理解层：`data/review/rule_terms.json`
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

## 详细技能文档

需要更细流程时阅读：

- `docs/skills/wuxia-project-handoff.md`
- `docs/skills/wuxia-source-policy.md`
- `docs/skills/wuxia-data-query.md`
- `docs/skills/wuxia-card-review.md`
- `docs/change-candidate-framework.md`
- `docs/card-understanding-calibration.md`
- `docs/rule-terms-understanding.md`
- `.agents/skills/wuxia-card-change-flow/SKILL.md`
- `docs/skills/wuxia-multi-unit.md`
- `docs/skills/wuxia-release-publish.md`
- `.agents/skills/wuxia-release-flow/SKILL.md`
- `docs/skills/wuxia-rulebook-work.md`
