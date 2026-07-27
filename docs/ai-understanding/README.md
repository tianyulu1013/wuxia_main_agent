# AI 理解模块入口

本目录只服务于 AI 对五行卡牌规则和评价方法的内部理解，不是玩家规则书，也不是牌面事实层。

当前逐卡精评完成范围与下一张衔接入口见：

- `data/review/calibration_progress.md`：人类可读进度总表；
- `data/review/calibration_queue.json`：机器可读队列与校准状态。
- `data/review/cards/index.json`：已精评人物按卡名、按维度读取的机器路由；
- `data/review/cards/<卡名>/README.md`：该人物的默认总分析入口。

## 默认加载顺序

处理卡牌设计、改卡或评价时：

1. 始终读取：
   - `core/game-flow.md`
   - `core/combat-baseline.md`
   - `parser-guide.md` (用于指导卡面缺省翻译与模糊度审计)
2. 根据卡牌类别，只读取一个类别模块：
   - 战斗人物：`evaluation/card-types/combat-character.md`
   - 附加人物：`evaluation/card-types/attached-character.md`
   - 物品：`evaluation/card-types/item.md`
   - 称号：`evaluation/card-types/title.md`
   - 场景：`evaluation/card-types/scene.md`
3. 只有战斗人物继续判断主要功能，再按 `evaluation/functions/README.md` 加载相关功能模块。
4. 根据牌面关键词，通过 `rules/README.md` 加载涉及的专项规则。
5. 仅在牌面出现特殊术语时查询 `data/review/rule_terms.json`。
6. 战斗人物先从`data/review/combat_baselines.json`查询白人参考和二至四个同功能量化基线；详见`evaluation/combat-baseline-registry.md`。
7. 网页和报告先展示评分、再展示统计、最后展示评语与推理；详见`evaluation/review-score-and-statistics.md`。
7. 仅加载与当前卡同类别、同主要功能的校准案例。
8. 若本卡已有精评目录，先读`data/review/cards/<卡名>/README.md`，再按问题定向读取维度文件；最后补读本卡作者裁定、理解笔记和玩家动态。

禁止为了“保险”一次读取整个规则书、全部术语、全部案例或全部历史评审。
同样禁止为了评价一张新卡而批量读取`data/review/cards/`内所有人物或某人物全部维度。

历史AI评语、旧工作卡和旧案例可以作为“可能有哪些问题、曾经如何理解”的检索线索，但其中每一条语义、公式、分数和`locked`状态都必须按当前规则重新验证。没有当前作者校准和现行工作卡验收的旧结论，不得直接成为比较锚点。

`evaluation/`根目录下的`frontal-combat.md`、`global-effects.md`、`support-and-items.md`属于历史兼容方法文件，不再默认加载。当前评价只从`evaluation/card-types/`选择一个类别模块，并在战斗人物需要时从`evaluation/functions/`选择功能模块。

## 三种评价对象

### 战斗人物

唯一需要竞争两张战斗人物名额的卡牌类型。先判断主要功能，再评价能力、实战兑现和人物名额价值。

### 直接进入本局的卡

附加人物、物品和称号被摸到后直接进入本局，不需要在弃牌阶段与战斗人物竞争。评价其在已经进入本局的前提下，能为本局增加多少实际帮助。

### 场景

场景定义整局游戏所处的环境。场景不做普通强度评分，只评价它如何改写整局流程、策略、规则稳定性和游戏体验。

## 信息归属

- 核心规则：普遍适用的游戏流程和基础结算。
- 专项规则：死亡、离场、结盟、地点、多单位等按关键词触发的规则。
- 特殊术语：只解释游戏中特殊词语的准确含义。
- 评价模块：告诉 AI 某类卡或某项功能应怎样分析。
- 校准案例：保存具体卡牌的完整计算、适用范围和不可迁移边界。
- 战斗人物量化基线：保存已校准人物的正面输出、侧面目标输出、场下输出、波动和正/侧面生存摘要，供后续按功能横向检索；不替代案例中的完整推导。
- 单卡评价目录：每个人物用独立目录保存完整评审；`README.md`只给总分析和路由，具体语义、计算、生存、全局影响、风险及作者原问原答分文件保存。
- 精评进度总表：记录本轮已经逐张完成的卡、完成范围、文件入口和仍开放的环境回归；不把旧批量评语误记为已精评。
- 单卡理解：只保存该卡自己的作者裁定和理解。
- 玩家动态：保存玩家意愿、桌面心理和政治选择，不能当作牌面规则。

## 当前替代关系

本目录是后续 AI 理解和评审的默认入口。下列旧文件暂不删除，但不再默认整份加载：

- `docs/rulebook-confirmed-rulings.md`
- `docs/rule-terms-understanding.md`
- `docs/ai-card-review-understanding-map.md`
- `docs/card-understanding-calibration.md`
- `docs/skills/wuxia-card-review.md`
- 旧轮次 AI 评审与聚合报告
- `evaluation/`根目录的三份旧式总评模块

详细清单见 `legacy-file-audit.md`。

下次继续迁移与清理时，按`migration-todo.md`执行。
