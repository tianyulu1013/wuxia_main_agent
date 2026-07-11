# 五行卡牌规则知识库与设计助手：项目架构说明 v0.1

## 1. 项目定位

本项目的第一目标不是立刻制作电脑游戏，而是建立一套可长期维护的规则知识库、卡牌资料库、候选更新流程和发布辅助工具。

当前游戏是一套多年演化的复杂原创桌游，规则中存在大量例外、裁定、文本改写、剧情触发和人工判断。第一阶段的架构必须尊重这一事实：不强行把所有规则程序化，不假设未明确的规则，不丢失原文。

长期方向包括：

- 辅助维护卡牌资料与历史版本。
- 审稿新卡和改卡，识别规则风险。
- 根据更新日志生成候选更新，作者确认后生效。
- 生成面向玩家的发布资料。
- 辅助 TTS 牌堆 release。
- 最后再逐步探索电脑游戏或半自动规则引擎。

## 2. 设计原则

### 2.1 原文优先

所有卡牌、规则、裁定、更新日志都必须保留原文。结构化解析只是附加层，不替代原文。

### 2.2 作者裁定最高优先级

资料冲突时，权威优先级为：

1. 作者口头裁定。
2. 已完成牌面 PSD/JPG。
3. 更新日志。
4. `已制作.xlsx`。
5. 规则文档。

由于游戏尚未公开发布，作者裁定是最终解释。

### 2.3 厚原文，薄结构

第一版核心库采用“厚原文 + 薄结构 + 可扩展标注”的方式：

- 先保存完整卡文。
- 粗拆卡牌类型、基础字段、生命结构、标签、特技块。
- 不急于完整拆解所有规则项。
- 为未来扩展预留 `extensions`、`rulings`、`review` 等区域。

### 2.4 不强求全部电子化

部分规则会修改文本、删字、重解释卡牌、改变剧情胜负，短期内不适合完全程序化。这些规则应被标记出来，而不是强行实现。

### 2.5 发布辅助优先

当前最大痛点是维护文档、更新日志、TTS 牌堆和玩家说明。因此第一阶段应优先做发布辅助，而不是电脑游戏。

## 3. 当前资料来源

项目当前已有资料：

- `已制作.xlsx`：当前全量基础资料。
- `五行卡牌规则.docx`：规则文档，定义较混乱，但包含大量基础规则。
- `2025更新日志.docx`：近年更新日志，包含新增、修改、删除、格式标记。
- PSD/JPG 牌面：已制作牌面，牌面优先级高于表格和日志。
- TTS release 图片：例如 `3.06古龙1.png`、`3.06金庸1.png` 等。
- TTS 命名脚本：按钮脚本框架固定，`cardNames` 和 `deckGUID` 需要维护。

## 4. 核心对象模型

### 4.1 Card

`Card` 是物理卡牌和资料单位，对应抽牌、弃牌、TTS slot、PSD 文件。

一张 Card 可以包含一个或多个人物单元，也可以是物品、称号、场景或附加人物。

建议字段：

```yaml
card:
  id: string
  title: string
  card_type: battle_character | attached_character | item | title | scene
  source:
    author: string
    work: string
    universe_tags: string[]
  raw_fields:
    life: string
    identity: string
    description: string
    relationship: string
    weapons: string
  units: Unit[]
  life_pools: LifePool[]
  skill_blocks: SkillBlock[]
  relationship_rules: RuleItem[]
  asset_refs: AssetRefs
  version_info: VersionInfo
  review: ReviewInfo
  extensions: {}
```

### 4.2 Unit

`Unit` 是规则中的人物单元。它可以被杀死、被计数、拥有性别、身份、标签和个人规则。

普通人物通常是 1 个 Card、1 个 Unit、1 个 LifePool。

多人一卡则是 1 个 Card 包含多个 Unit。共享生命、多人计数、五个人头等都必须支持。

建议字段：

```yaml
unit:
  id: string
  title: string
  gender: male | female | unknown | mixed | other
  head_count: number
  identity:
    description: string
    tags: string[]
    identity_rules: RuleItem[]
  weapons: WeaponTag[]
  life_pool_refs: string[]
  status_defaults: []
  personal_rules: RuleItem[]
  extensions: {}
```

### 4.3 LifePool

`LifePool` 表示生命结构。它可以属于单个 Unit，也可以被多个 Unit 共享；一个 Unit 也可能有多个生命阶段。

需要支持：

- 无生命属性。
- 多生命阶段。
- 死亡后重生。
- 共享生命。
- 生命到 0 不死。
- 生命流失。

建议字段：

```yaml
life_pool:
  id: string
  owner_unit_refs: string[]
  max_life: number | null
  has_life: boolean
  stage_index: number
  shared: boolean
  default_zero_life_behavior: death | no_death | special | unknown
  can_take_damage: boolean
  can_lose_life: boolean
  transition_rule: RuleItem | null
  revive_rules: RuleItem[]
  extensions: {}
```

### 4.4 SkillBlock

`SkillBlock` 是牌面上的特技块。

特技类型包括：

- 内功
- 招式
- 武功
- 技能
- `*`
- 字，也就是无前缀特技
- 符卡
- future/unknown

“内功、招式、武功”统称大招，内部建议字段名为 `is_major_art`。

建议字段：

```yaml
skill_block:
  id: string
  card_id: string
  owner_scope: card | unit | formation | life_stage
  owner_ref: string
  display_name: string
  printed_type: 内功 | 招式 | 武功 | 技能 | "*" | 字 | 符卡 | unknown
  inherited_printed_type: boolean
  is_exclusive: boolean
  is_identity: boolean
  is_major_art: boolean
  raw_text: string
  printed_order: number
  printed_line_refs: []
  rule_items: RuleItem[]
  extensions: {}
```

### 4.5 RuleItem

`RuleItem` 是从特技块、关系区、身份描述、物品文本等拆出的规则项。

一个 SkillBlock 可以拆成多个 RuleItem。每个 RuleItem 触发时仍应保留对原 SkillBlock 的引用，因为有些规则会统计特技使用次数。

建议字段：

```yaml
rule_item:
  id: string
  parent_ref: string
  raw_text: string
  rule_kind: active | controllable | passive | triggered | replacement | continuous | manual | unknown
  timing: []
  condition_text: string
  cost_text: string
  target_text: string
  effect_text: string
  duration_text: string
  targets: []
  event_hooks: []
  tags: []
  digitalization_level: executable | semi_executable | manual_adjudication | semantic_rewrite | non_electronic
  ambiguity_level: low | medium | high
  needs_ruling: boolean
  counts_as_using_skill_block: boolean
  extensions: {}
```

## 5. 重要规则概念

### 5.1 Card / Unit / LifePool 分离

必须区分：

- Card：物理卡牌。
- Unit：人物单元。
- LifePool：生命池。

例如：

- 普通人物：1 Card + 1 Unit + 1 LifePool。
- 全真七子：1 Card + 7 Unit + 7 LifePool。
- 袁冠南萧中慧：1 Card + 2 Unit + 1 shared LifePool。
- 多条命人物：1 Unit + 多个 LifePool 或动态重生规则。
- 无生命人物：1 Unit + 0 LifePool 或 `has_life = false`。

### 5.2 攻击、伤害、流失、杀死、清除

这些概念不能混用：

- 攻击：通常作用于 Unit，并可能造成 LifePool 伤害。
- 伤害：扣在 LifePool 上，是攻击或效果造成的伤害。
- 生命流失：扣在 LifePool 上，但不是攻击，也不是伤害，而是效果。
- 杀死：作用于 Unit，不要求先扣血。
- 离场：语义不稳定，需要每张卡裁定。
- 清除：作用于 Card，使整张卡离开本局游戏。多人一卡被清除时全部没了。

### 5.3 事件与目标

目标系统必须支持多层级对象：

- 玩家
- 一方
- 阵营/联盟
- Card
- Unit
- LifePool
- SkillBlock
- RuleItem
- Event
- Event source
- Event target
- 基础五行卡
- 物品
- 称号
- 附加人物
- 场景
- 地点
- 挑战顺序
- 结算顺序

李布衣等卡说明，事件来源、对象、结算顺序本身也可能成为目标。

### 5.4 场景与地点

场景和地点不同：

- 场景偏全局环境。
- 地点偏人物当前所在位置和可达性。
- 场景卡通常没有 owner。
- 场景牌背面不同，TTS 中应独立牌堆。

### 5.5 轮与回合

- 回合：某人物自己出战并战斗一次。
- 轮：己方任一人物出战一回合，己方相关人物均经过一轮。

例如“马钰下轮后归还”指己方经过一轮，而不是马钰本人再次出战。

## 6. 标签系统

标签必须可扩展，不能写死。

### 6.1 武器标签

例如：

- `【剑】`
- `【刀】`
- `【奇门】`
- `【刀S】`

`S` 表示该武器专家。`【刀S】` 可理解为同时拥有 `刀` 与 `刀专家`。

### 6.2 身份标签

例如：

- `【恶】`
- `【残】`
- 未来可能有 `【侠】`

身份标签可能被规则引用，应作为规则可查询字段。

### 6.3 专属特技

特技名两侧带 `【】` 通常表示专属特技，一般无法学习或复制，但可能有例外。

### 6.4 身份特技

当前牌面中身份特技通常以末尾 `(身份)` 标记，不够醒目，容易遗漏。

结构化资料中应单独标记 `is_identity = true`，即使牌面暂时不修改。

## 7. 电子化等级

用于 AI 审稿和未来规则引擎规划。

### executable

边界清楚，可未来自动执行。

例如：造成 300 伤害、获得毒、攻击 +100。

### semi_executable

大部分可执行，但依赖少量上下文或裁定。

例如：选择一个可见剑法学习；改变一张可移动卡的位置。

### manual_adjudication

可以记录状态，但结果需要玩家或作者裁定。

例如复杂剧情、特殊胜负、身份变化。

### semantic_rewrite

通过删字、改字、重解释牌面文本来改变规则。应从普通人工裁定中单独拎出，因为风险极高。

### non_electronic

暂不尝试电子化，只保留文本和裁定。

## 8. 审稿维度

AI 审稿不是只评强度，而应多维度评估。

### 8.1 规则稳定性

最高优先级。检查是否破坏核心规则、目标层级、结算顺序、状态定义。

### 8.2 无限循环风险

检查复活、反击、替死、复制、响应、事件重定向等是否可能循环。

### 8.3 文本可解释性

检查目标、来源、持续时间、触发时机、使用次数是否清楚。

### 8.4 电子化等级

标记规则可执行程度。

### 8.5 游戏定位

可打多标签，例如：

- 输出
- 肉盾
- 辅助
- 控制
- 防御
- 复活
- 场景型
- 剧情型
- 混乱型

### 8.6 艺术形象贴合度

评估机制是否贴合原作或艺术形象。这是本游戏设计的重要目标。

### 8.7 强度评分

强度可使用数字评分，但不是第一优先级。游戏平衡主要来自随机抓牌和快速对局，而非单卡均衡。

## 9. 更新与版本流程

### 9.1 候选更新

更新日志、口述修改、新卡文本都先进入候选更新队列。

候选更新建议字段：

```yaml
change_candidate:
  id: string
  source: string
  change_type: modify | add | delete | ruling
  target_card_title: string
  target_card_id: string
  fields_changed: []
  current_text: string
  patch_text: string
  proposed_text: string
  confidence: high | medium | low
  needs_author_confirmation: boolean
  psd_status: needs_psd_update | psd_updated | not_needed
  affects_tts_deck: boolean
  review_notes: []
  unresolved_questions: []
```

### 9.2 确认流程

默认按卡确认，复杂卡可展开到字段或规则项。

候选更新应显示：

- 当前原文。
- 日志补丁。
- 合成后的候选新版。
- AI 风险提示。
- 待确认问题。

确认后进入当前权威版本。

### 9.3 历史版本

文本版本应保留，便于回滚和追踪。

旧 PSD 不保留，因为体积大。PSD 只记录当前路径和状态。

## 10. TTS Release 辅助

### 10.1 当前工作流

- TTS 是实际在线游玩环境。
- 牌堆按作者组织。
- 每个牌堆最多约 70 张。
- 场景独立牌堆，因背面颜色不同。
- PSD 按牌堆文件夹组织。
- Photoshop 联系人表生成拼版图。
- TTS 导入拼版图后会生成新的 deck GUID。
- 按钮 object 中脚本框架固定，主要需要维护 `deckGUID` 和 `cardNames`。

### 10.2 第一版辅助目标

第一版不自动操作 TTS，不自动生成拼版图也可以。优先生成：

- 本次受影响牌堆清单。
- 需要重做 PSD 的卡。
- 需要重新生成的牌堆图片。
- 每个受影响牌堆的最新 `cardNames` 块。
- `deckGUID` 待填提醒。
- 玩家更新说明。

### 10.3 后续可能优化

- 自动生成完整 Lua 脚本。
- 自动处理中文编码，避免乱码。
- 自动生成 Photoshop 联系人表所需文件列表。
- 未来探索 TTS 自动化，但不作为第一阶段目标。

## 11. 存储架构

建议采用：

**文件为权威源 + SQLite 作为查询索引。**

理由：

- 文件适合 Git 管理、diff、回滚。
- SQLite 适合搜索、筛选、生成 report。
- 用户无需直接编辑底层文件。
- 数据库可由文件重建，避免锁死。

建议目录：

```text
data/
  source/
  cards/
  changes/
  rulings/
  reviews/
  tts/
assets/
exports/
index.sqlite
```

### 11.1 data/source

保存原始资料快照或引用，例如 Excel、规则文档、更新日志。

### 11.2 data/cards

保存当前权威卡牌资料。可按类型、作者、作品拆分。

### 11.3 data/changes

保存候选更新和已确认更新。

### 11.4 data/rulings

保存作者裁定。

### 11.5 data/reviews

保存 AI 审稿结果。

### 11.6 data/tts

保存 TTS 牌堆、slot、cardNames、deck GUID 状态。

### 11.7 assets

保存 PSD 路径索引，不一定复制 PSD。

### 11.8 exports

保存生成的 report、玩家更新说明、TTS 脚本、release 清单等。

## 12. 阶段计划

### Phase 1：发布辅助 MVP

目标：先减少手工维护文档和 TTS 发布的痛点。

内容：

- 导入 `已制作.xlsx`。
- 生成核心资料初版。
- 解析 `2025更新日志.docx`，生成候选更新。
- 生成候选更新报告。
- 生成确认后的玩家更新说明。
- 生成 Excel/腾讯文档 report。
- 生成 TTS 受影响牌堆清单和 `cardNames` 块。

### Phase 2：AI 审稿助手

目标：帮助评审新卡和改卡。

内容：

- 规则风险检测。
- 循环风险检测。
- 文本歧义检测。
- 目标/来源/持续时间检查。
- 艺术形象贴合度问题清单。
- 强度评分与标签。

### Phase 3：规则问答与裁定库

目标：支持“这张卡和那张卡怎么交互”的查询。

内容：

- 规则文档结构化。
- 裁定记录。
- 卡牌交互检索。
- 不确定性提示。

### Phase 4：TTS 自动化增强

目标：进一步减少 TTS 手工步骤。

内容：

- 更完整的 Lua 生成。
- PSD 文件夹/牌堆同步检查。
- 发布包生成。
- 可能的拼版辅助。

### Phase 5：电子化与电脑游戏探索

目标：在资料库成熟后，逐步探索可执行规则。

内容：

- 简化战斗模拟器。
- 半自动裁定弹窗。
- 可执行规则引擎。
- 复杂语义规则保留人工裁定。

## 13. 下一步

下一步建议进入 Phase 1 的需求细化：

1. 明确核心资料文件格式。
2. 明确导入 `已制作.xlsx` 的字段映射。
3. 明确候选更新报告格式。
4. 明确玩家更新说明格式。
5. 明确 TTS `cardNames` 生成格式和编码策略。

在正式实现前，应先用少量卡牌样例验证模型：

- 普通单人：如周芷若。
- 多人一卡多生命：如全真七子。
- 共享生命：袁冠南萧中慧。
- 多生命阶段：金轮法王。
- 复杂剧情/人工裁定：眉间尺。
- 事件/顺序操控：李布衣。

