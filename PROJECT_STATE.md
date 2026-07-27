# 五行卡牌项目交接状态

新对话请先读本文。本项目是一套规则复杂、已有多年积累的原创桌游资料整理与查询工程。当前阶段不是做电脑游戏，也不是做完整规则引擎，而是先把卡牌资料、查询、发布、评审辅助的基础打稳。

## 当前核心目标

- 建立可信的当前卡牌数据库。
- 提供本地查询网页和可发布的静态查询站。
- 支持多人一卡、特技所属、身份/属性/兵器/出处/关系/特技等字段查询。
- 分离源数据、作者裁定、AI 评语、改卡候选，避免 AI 理解污染牌面事实。
- 后续再整理规则书、剧本书、卡牌评审助手；电脑游戏最后再考虑。

## 用户工作原则

- 用户是唯一作者，口头裁定优先级最高。
- 不要自行假设规则；不清楚就问。
- 不要脑补源数据库内容。AI 的理解、攻略、强度评价必须放在评语层或另一个派生层。
- 旧更新日志的一次性同步基本结束。以后数据库和新版 Excel 是当前基准，旧日志只作历史线索。
- 改卡流程应是：用户提出意见 -> 生成候选文本 -> 用户确认 -> 更新数据库/Excel/PSD/日志。
- 平衡不是最高目标；艺术形象符合度、规则稳定性、文本清晰度很重要。

## 权威数据顺序

1. 作者口头裁定。
2. 当前数据库与当前基准 Excel。
3. 当前 release/PSD 牌面，用于核对录入错误。
4. 旧更新日志，仅作为历史线索。
5. 未来更新日志，由确认后的数据库/Excel 变更生成。

详见：

- `docs/source-of-truth-policy.md`
- `docs/data-layer-policy.md`

## 主要文件与目录

- `data/cards.sqlite`：当前 SQLite 数据库。
- `data/cards_current/*.jsonl`：当前结构化卡牌数据。
- `data/card_unit_overrides.json`：多人一卡、unit、特技所属等作者裁定。
- `data/card_field_overrides.json`：字段修正。
- `data/author_ability_overrides.json`：特技结构修正。
- `data/review/cards/<卡名>/`：已精评人物的完整证据目录；`README.md`为总分析，其余文件按输出、生存、全局影响、风险、作者校准等维度拆分。
- `data/review/cards/index.json`：单卡评价目录的机器可读路由索引。
- `data/review/card_evaluations.json`：网页使用的结构化摘要；不再承载整篇完整证据。
- `data/review/card_notes/`：历史兼容入口；已迁移人物只保留指向新目录的导航。
- `data/review/calibration_progress.md`、`data/review/calibration_queue.json`：本轮逐卡精评的人类可读进度与机器可读状态。
- `data/card_reviews.json`：历史兼容评语文件，不再作为新评审默认写入目标。
- `docs/ai-understanding/`：AI内部使用的核心流程、类别、功能、专项规则路由和案例体系。
- `data/change_candidates.json`：改卡候选。
- `web/card_browser/`：本地查询网页前端。
- `scripts/serve_card_browser.py`：启动本地查询服务。
- `scripts/export_static_site.py`：导出纯静态站。
- `site_export/`：生成的静态站目录，不进主仓库。
- `static_publish_repo/`：独立静态发布 Git 仓库，不进主仓库。
- `docs/`：架构、审计、统计、规则整理、工作流文档。

## 查询网页

本地入口：

```text
http://127.0.0.1:8765
```

启动脚本：

```powershell
python scripts/serve_card_browser.py
```

已支持：

- 卡名/全文查询。
- 字段级查询：名称、身份/属性、兵器、出处、关系、特技文本。
- 默认隐藏废弃卡。
- 多人一卡 unit 展示。
- 卡面 PNG 展示。
- 评语/裁定展示。
- 改卡候选展示。
- 统计页和筛选统计。

## 多人一卡原则

- 不再使用“全体”作为虚拟 unit。
- 每张卡有真实 unit；特技通过 owner unit 列表表示属于谁。
- 如果一个特技属于所有 unit，就记录所有 unit 名称，而不是记录 `全体`。
- 单人卡默认一个 unit。
- `五个人头` 是极特殊卡：基本按一个 unit 处理，但计人数为 5。
- 共享生命和多人各自生命要区别记录，例如袁冠南萧中慧、阿三阿四是共享生命，四大恶人、全真七子等是各自生命。

## 已知重要裁定与概念

- 专属特技：特技名带 `【】`，不是特技类型。
- 身份特技：通常描述末尾带 `（身份）`。
- `字`：无内功/招式/武功/技能等前缀的特技类型。
- `内功`、`招式`、`武功` 统称应使用中文概念“大招”，英文可理解为 major technique，不建议写成 big move。
- 招式区、内功区、武功、连绵、五行打卡等规则很复杂，不要简单类比普通卡牌游戏。
- 有些牌会破坏规则，例如删字、只剩某行文字等，未来可能需要人工裁定或外挂式处理。
- `攻击`、`伤害`、`扣血`、`生命流失`、`杀死`、`死亡`、`离场`、`清除` 是不同概念。
- `不在场无此人` 不是离场；破空是一种离场但可胜利。
- 回合与轮不同：回合通常是某人自己出战一次；轮是己方有人出战一次。

## 发布状态

主工程 GitHub：

```text
https://github.com/tianyulu1013/wuxia_main_agent
```

静态发布 GitHub：

```text
https://github.com/tianyulu1013/wuxia_static_publish
```

静态站生成流程：

```powershell
python scripts/export_static_site.py
```

生成 `site_export/` 后，同步到 `static_publish_repo/`，在发布仓库提交并推送。Netlify 配置：

```text
Build command: 留空
Publish directory: .
```

## 后续最可能继续的任务

1. 规则书整理：读取 `五行卡牌规则.docx`，结合已讨论裁定，重写结构更清楚的规则书。
2. 查询网页完善：属性字段、更多筛选统计、规则书/剧本书入口、卡面更新流程。
3. 数据修正：发现卡牌录入或多人一卡所属错误时，直接修正数据库/覆盖层，必要时写入卡面待办。
4. 评语层建设：人物强度、定位、设计特点、设计风险、电子化风险、攻略写入`data/review/cards/<卡名>/`，不得写入源数据。
5. 新卡评审助手：根据用户自然语言修改意见，生成候选新版文本和更新说明。

## 新对话建议开场

可以直接对 Codex 说：

```text
请先阅读 PROJECT_STATE.md、docs/source-of-truth-policy.md、docs/daily-workflow.md，然后继续当前五行卡牌项目。
```

如果任务涉及规则书，再读：

```text
docs/ai-understanding/README.md
docs/ai-understanding/core/game-flow.md
docs/ai-understanding/core/combat-baseline.md
```

再根据当前卡牌类别和牌面机制定向读取局部模块；不要默认整份加载旧规则总表。

如果任务涉及网页或发布，再读：

```text
docs/static-hosting-plan.md
web/card_browser/
scripts/export_static_site.py
```

如果任务涉及多人一卡，再读：

```text
docs/multi-unit-completeness-report.md
docs/multi-unit-ownership-report.md
data/card_unit_overrides.json
```
