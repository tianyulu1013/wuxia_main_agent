---
name: wuxia-workflow-guide
description: Global workflow and data-layer guide for 五行卡牌. Use at the start of a project conversation, then route to the minimum specialized skill and AI-understanding modules needed.
---

# 五行卡牌全局工作流

## 最高原则

- 用户是唯一作者，当前口头裁定优先。
- 不清楚规则时询问，不从其他游戏补规则。
- AI理解、评价、案例和玩家动态不得污染源数据。
- 未经明确允许，不提交、不推送、不发布。

## 数据层

- 结构化源数据（唯一可信源）：`data/cards_current/*.jsonl`
- 编译输出数据库：`data/cards.sqlite`
- 自动同步回填 Excel 镜像：`outputs/.../已制作_2025日志同步候选_PSD校准.xlsx`
- 改卡候选：`data/change_candidates.json`
- 单卡完整评审：`data/review/card_evaluations.json`、`data/review/card_notes/`
- 单卡理解：`data/review/card_understanding_notes.json`
- 特殊术语：`data/review/rule_terms.json`
- 玩家动态：`data/review/player_dynamics.json`
- 比较案例与锚点：`docs/ai-understanding/cases/`、`data/review/card_calibration_anchors.json`
- 战斗人物量化基线：`data/review/combat_baselines.json`（用`scripts/query_combat_baselines.py`按卡名或功能查询）
- 精评进度：`data/review/calibration_progress.md`（人类可读）与`data/review/calibration_queue.json`（机器可读）
- AI理解入口：`docs/ai-understanding/README.md`
- 数据源与编译架构技能书：`docs/skills/wuxia-database-architecture.md`

`data/card_reviews.json`和旧轮次AI评审属于历史兼容材料，不是新评审默认写入目标。

## 工作流路由

### 查卡

优先查询`data/cards.sqlite`或使用`scripts/query_cards.py`。多人一卡再读取`docs/skills/wuxia-multi-unit.md`。

### 改卡与新卡

加载`wuxia-card-change-flow`。讨论阶段只写候选层；作者完成卡面并要求同步后，才更新源数据和批次产物。

### 强度评价与理解校准

加载`wuxia-card-review-calibration`和`wuxia-rule-understanding`。先读最小核心，再按卡牌类别、战斗人物功能、局部规则和同功能案例路由。

### 规则整理

加载`wuxia-rule-understanding`。新规则按内容进入核心规则、专项规则、特殊术语、评价模块、案例或玩家动态，不再全部追加到一个总文件。

### 发布

加载`wuxia-release-flow`。本地修改不等于发布；提交、推送、部署和公开版本变更必须有作者明确指令。

## AI理解的最小加载顺序

1. `docs/ai-understanding/core/game-flow.md`
2. `docs/ai-understanding/core/combat-baseline.md`
3. 当前卡牌类别模块
4. 战斗人物的相关功能模块
5. 牌面触发的专项规则
6. 实际出现的特殊术语
7. 战斗人物先查询白人参考及二至四个同功能量化基线
8. 少量同功能案例
9. 本卡理解与必要玩家动态

禁止整份加载全部规则、术语、案例和历史评审。

战斗人物完成作者校准和定量计算后，必须把正面输出、侧面目标输出、场下输出、方差、正面生存和侧面生存同步到`data/review/combat_baselines.json`；无法计算的字段保留`null`并写明原因。这样后续评审以已校准人物为横向基线，不反复从白人或全部旧工作卡起算。

每张卡完成本轮精评后，还要同步`data/review/calibration_queue.json`和`data/review/calibration_progress.md`，明确区分“本轮精评完成但环境回归开放”与“只有旧评语、尚未重新精评”。

## 中文与文件安全

修改中文Markdown、JSON、技能或规则文件时加载`wuxia-windows-utf8-safety`，优先使用补丁，并在写入后检查UTF-8、替换字符和结构有效性。
