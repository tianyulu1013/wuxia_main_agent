# AI理解与评审历史文件审计

审计日期：2026-07-23。  
本轮动作：建立清单、退出默认加载、增加历史警示；不删除历史数据。

## 一、最高风险：不应再作为AI默认依据

### 旧轮次AI评审

- `data/review/ai_card_reviews_round1.jsonl`
- `data/review/ai_card_reviews_round2.jsonl`
- `data/review/ai_card_reviews_round2.csv`
- `data/review/ai_card_reviews_round3.jsonl`
- `data/review/ai_card_reviews_round4.jsonl`
- `data/review/ai_card_reviews_round4.csv`
- `data/review/ai_card_reviews_summary.json`
- `docs/ai-card-review-batch-report.md`
- `docs/ai-card-review-author-watchlist.md`
- `docs/ai-card-review-understanding-map.md`

问题：

- 来自旧版批量评审方法。
- 未以当前默认游戏流程、类别路由和功能模块逐卡复核。
- 聚合平均分、作者组画像和旧功能标签容易被误当成当前标尺。
- CSV与JSONL存在内容重复。

当前处理：

- 全部退出新技能默认加载。
- `docs/ai-card-review-understanding-map.md`已增加历史警示。

建议后续：

- JSONL保留一份作为历史证据并移入归档目录。
- 确认CSV无独有信息后，可删除重复CSV。
- 聚合摘要、批次报告和理解地图确认无独有作者裁定后，可删除或只保留一份归档。

## 二、旧版技能和评价模板

- `.agents/skills/wuxia-card-review-calibration/SKILL.legacy.md`
- `.agents/skills/wuxia-workflow-guide/SKILL.legacy.md`
- `docs/skills/wuxia-card-calibration-sop.legacy.md`
- `docs/skills/wuxia-card-review-workcard.legacy.md`
- `docs/skills/wuxia-card-review.md`
- `docs/card-understanding-calibration.md`

问题：

- 混合当前规则、旧评分标尺、旧类别理解和旧批量流程。
- 曾把附加人物、物品、称号按取得成本或人物名额逻辑评价。
- 曾把场景当作可做普通强度比较的卡牌。
- 部分旧文件仍引用整份规则总表和全部术语。

当前处理：

- 新技能和新模板已成为默认入口。
- 原文件保留并明确标记为历史。

建议后续：

- 等新体系经过若干张卡验证后，统一移入`docs/archive/ai-review-v0/`。
- 若确认没有独有作者原话，再决定删除纯流程重复文件。

## 三、混装文件：必须迁移后再清理

### `docs/rulebook-confirmed-rulings.md`

现状：

- 同时包含核心游戏规则、专项规则、评价方法、段正淳案例、王重阳案例、玩家意愿和发布流程。

风险：

- AI整份加载后无法判断哪些是普遍规则、哪些只是评价方法或单卡案例。

当前处理：

- 已退出默认必读。
- 已增加“迁移中的历史总表”警示。

建议后续：

- 将核心流程迁入`docs/ai-understanding/core/`。
- 将死亡、存在状态、结盟等拆入专项规则模块。
- 将具体人物推导迁入案例库。
- 将玩家意愿迁入玩家动态。
- 全部迁移核对后再归档或删除总表。

### `data/review/rule_terms.json`

当前共有23个条目。

明确不属于特殊术语的条目：

- `基础战斗与主动特技放出模型`
- `战斗人物功能分类与评卡基准`

处理建议：

- 前者迁入核心战斗模块。
- 后者迁入战斗人物类别和功能模块。
- 迁移核对后从术语JSON删除。

`大辈结盟`属于特殊词义，可以保留；其中混入的段正淳具体触发案例应拆到单卡理解或案例库。

### `docs/rule-terms-understanding.md`

问题：

- 同时包含特殊词义、基础战斗、评价方法和具体人物案例。

当前处理：

- 已退出默认整份加载并增加迁移警示。

建议后续：

- 术语说明只保留术语层用途和查询方法。
- 具体内容以`data/review/rule_terms.json`对应词条为准。
- 非术语部分迁完后删除重复正文。

## 四、当前评审数据中的混合质量

### `data/review/card_evaluations.json`

当前约193条：

- `ai_unreviewed`：156
- `ai_draft`：22
- `author_reviewed`：15

风险：

- 旧状态并不等于通过当前模块化工作卡。
- `author_reviewed`也不能自动视为作者确认的完整物理模型。

建议：

- 文件继续保留为当前评审容器。
- 新评审增加所用类别模块、功能模块、核心规则版本和案例来源。
- 旧条目只有重新审计后才能成为当前锚点。

### `data/review/card_calibration_anchors.json`

当前11个锚点均标记为`locked`，但来源混合：

- 王重阳为本轮作者校准的正面作战案例。
- 其余旧锚点多为旧AI评审沉淀，不能只因`locked`就视为作者确认。

建议：

- 增加`calibration_source`和`function_type`准入门槛。
- 未注明作者确认或当前工作卡来源的锚点降为历史待审。
- 完整推导迁入`docs/ai-understanding/cases/`，JSON只保留索引和结构化比较字段。

### `data/review/strength_calibration.json`

价值：

- 含作者体感标尺，不应直接删除。

风险：

- 使用旧1—5分体系，并混有早期评价方法。
- 与当前百分制、类别路由和功能评价尚未建立明确换算。

建议：

- 保留为作者历史强度参考。
- 不直接换算成当前百分制。
- 逐条核对后拆分为作者确认锚点和过时方法说明。

### `data/card_reviews.json`

现状：

- 早期评语容器，体量较小。
- 与`data/review/card_evaluations.json`、单卡笔记和理解笔记职责重叠。

建议：

- 已退出新评审默认写入。
- 核对是否存在未迁移作者裁定。
- 迁移独有内容后再考虑删除。

### `data/review/understanding_samples.json`

现状：

- `card_understanding_v0_1`种子样本。

风险：

- 样本理由来自旧评价模型。
- 样本入选不等于当前有效案例。

建议：

- 保留为历史选题清单。
- 逐张通过当前流程后，才迁入模块化案例库。

## 五、历史单卡工作卡与笔记

- `data/review/workcards/`当前91份，其中90份为旧`batch_*`工作卡。
- `data/review/card_notes/`当前82份单卡笔记。

价值：

- 可能包含独有作者原话、旧结算尝试和问题记录。

风险：

- 格式、规则基础和锁定门槛不一致。
- 旧工作卡不应被新AI自动当成已验证案例。

建议：

- 不删除。
- 新工作卡继续留在当前目录。
- 旧`batch_*`工作卡以后移入`data/review/archive/workcards-v0/`。
- 搬迁前先扫描并提取独有作者裁定。

## 六、项目历史审计和迁移报告

典型文件：

- `docs/2025-*.md`
- `docs/*audit*.md`
- `docs/*report*.md`
- `docs/*v0.1.md`
- `docs/rulebook-docx-extract.md`
- `docs/rulebook-structure-audit.md`
- `docs/project-architecture-v0.1.md`
- `docs/core-data-mapping-v0.1.md`

这些文件多数是数据同步、Excel、PSD、日志或旧架构审计证据，不是当前卡牌理解规则。

建议：

- 保留历史证据。
- 从AI评卡和改卡默认入口排除。
- 以后按“数据迁移报告、旧规则材料、旧架构说明”分目录归档。
- 不在未核对脚本或报告引用前批量删除。

## 七、本轮不建议删除的文件

- 源数据、覆盖层和改卡候选。
- `data/review/player_dynamics.json`
- `data/review/card_understanding_notes.json`
- `data/review/card_evaluations.json`
- `data/review/card_notes/`
- `docs/rulebook-refactored.md`
- 当前模块化AI理解目录。

这些文件仍有当前用途，清理应以内容迁移和入口修正为主。

## 八、建议清理顺序

1. 先验证新模块体系处理数张不同类别卡是否够用。
2. 清理术语层中的非术语条目。
3. 审计11个旧比较锚点的来源。
4. 核对`data/card_reviews.json`是否有独有作者裁定。
5. 归档旧轮次JSONL和旧工作卡。
6. 删除确认重复且无独有信息的CSV、聚合摘要和旧流程文档。
7. 最后迁移并退役`docs/rulebook-confirmed-rulings.md`总表。

后续执行清单已转入`migration-todo.md`；本审计文件保留发现依据，不作为每日任务列表。
