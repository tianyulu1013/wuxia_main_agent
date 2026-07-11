# Phase 1：发布辅助 MVP 需求说明

## 1. 目标

Phase 1 的目标是先解决当前最痛的工作：资料更新、候选确认、玩家发布说明、TTS 牌堆辅助。

本阶段不做完整电脑游戏，不做完整规则引擎，也不要求所有卡牌规则完全结构化。

第一版应做到：

- 从 `已制作.xlsx` 建立当前资料基础库。
- 从 `2025更新日志.docx` 或作者口述修改中生成候选更新。
- 让作者确认候选更新。
- 确认后生成新的发布资料。
- 标记需要更新 PSD 的卡。
- 推导受影响 TTS 牌堆。
- 生成 TTS 命名所需的 `cardNames` 数据块。
- 生成玩家可读的更新说明。

## 2. 不做什么

Phase 1 暂不做：

- 自动修改 PSD。
- 自动生成 TTS 拼版图。
- 自动更新 TTS 内 object 或 deck GUID。
- 完整解析所有特技规则。
- 自动裁定复杂规则。
- 电脑游戏原型。

这些内容保留为后续阶段。

## 3. 输入资料

### 3.1 当前全量资料

来源：`已制作.xlsx`

当前工作表：

- `战斗人物`
- `附加人物`
- `物品`
- `称号`
- `场景`
- `废弃`

用途：

- 初始化核心资料库。
- 作为旧版本文本的基础。
- 生成对外 report。

### 3.2 更新日志

来源：`2025更新日志.docx`

用途：

- 解析新增卡。
- 解析修改卡。
- 解析废弃或删除。
- 生成候选更新。

注意：

- 日志可能是完整新版，也可能是增量补丁。
- 划去线、加粗等格式未来可用于识别删除和新增，但第一版可以先以纯文本和人工确认为主。
- 新增卡通常可以视为完整文本。
- 大改动可能写完整版本。

### 3.3 牌面与 PSD

来源：`psd卡牌/` 目录。

当前已存在完整 PSD 目录，约 552 个 PSD 文件，主要结构为：

```text
psd卡牌/
  人物/
    金庸/1
    金庸/2
    金庸/3
    古龙/1
    古龙/2
    温瑞安/1
    温瑞安/2
    黄易/1
    黄易/2
    其他武侠玄幻/
    现代鬼畜/
  场景/
  基础卡/
  废弃/
```

用途：

- 牌面优先级高于日志和 Excel。
- 推导 TTS 牌堆归属。
- 标记是否需要更新牌面。
- 扫描 PSD 文件名和目录，生成 TTS `cardNames` 顺序候选。

第一版只记录路径和状态，不解析 PSD 图层。

注意：`psd卡牌/废弃` 不是 TTS 牌堆。它是废弃/旧版资产目录，不应生成 release deck。

### 3.4 作者口述裁定

来源：作者在对话中确认的规则和裁定。

用途：

- 最高优先级权威来源。
- 进入 `rulings` 或确认后的版本记录。

## 4. 权威资料优先级

当资料冲突时：

1. 作者裁定。
2. 已完成牌面。
3. 更新日志。
4. `已制作.xlsx`。
5. 规则文档。

系统不得自动覆盖高优先级资料。冲突应进入候选更新报告，由作者确认。

## 5. 核心库第一版范围

第一版核心库采用“厚原文 + 薄结构”。

### 5.1 必须保存的基础字段

所有卡牌：

- `id`
- `title`
- `card_type`
- `source.author`
- `source.work`
- `raw_fields`
- `status`
- `version`
- `review`
- `asset_refs`
- `extensions`

战斗人物、附加人物：

- `raw_fields.life`
- `raw_fields.identity`
- `raw_fields.description`
- `raw_fields.relationship`
- `raw_fields.weapons`
- `gender`

物品：

- `raw_fields.description`
- `raw_fields.traits`
- `category`

称号：

- `raw_fields.description`

场景：

- `raw_fields.description`
- `scene_back_type`，用于区分 TTS 场景牌背。

### 5.2 第一版可粗拆字段

第一版可以尝试自动识别：

- 生命是否为空。
- 多生命阶段，例如 `2500 3800`。
- 武器标签，例如 `【剑】`、`【刀S】`。
- 身份标签，例如 `【恶】`。
- 专属特技，即 `【特技名】`。
- 身份特技，即文本末尾含 `(身份)`。
- 特技块前缀：内功、招式、武功、技能、`*`、字、符卡。

所有自动识别结果都应视为候选结构，可人工修正。

### 5.3 暂不完整解析

第一版不要求完整解析：

- 目标对象。
- 触发时机。
- 复杂剧情。
- 多人一卡内部全部 Unit。
- 共享生命。
- 多生命阶段转换。
- 事件顺序操控。
- 删字、改字、语义重写。

这些先通过 tag 和备注标记。

## 6. 候选更新模型

候选更新是 Phase 1 的核心。

作者给出更新日志或口述修改后，系统生成候选记录。候选记录不直接进入权威库，必须由作者确认。

### 6.1 候选更新字段

```yaml
change_candidate:
  id: string
  source:
    type: update_log | oral_ruling | manual_input | asset_scan
    ref: string
  change_type: add | modify | delete | deprecate | ruling | asset_update
  target:
    card_id: string | null
    card_title: string
    card_type: string | null
  fields_changed:
    - field: string
      current_text: string
      patch_text: string
      proposed_text: string
  confidence: high | medium | low
  questions:
    - string
  review:
    risk_tags: []
    digitalization_level: executable | semi_executable | manual_adjudication | semantic_rewrite | non_electronic | unknown
    notes: []
  release_impact:
    needs_psd_update: boolean
    psd_status: needs_psd_update | psd_updated | not_needed | unknown
    affects_tts: boolean
    affected_tts_decks: []
    affects_report: boolean
  status: pending | accepted | rejected | needs_revision
```

### 6.2 候选更新显示方式

默认按卡显示。

每张卡显示：

- 卡名。
- 类型。
- 当前原文。
- 更新日志补丁。
- 合成后的候选新版。
- AI 识别风险。
- 待作者确认问题。
- 是否需要更新 PSD。
- 是否影响 TTS 牌堆。

复杂卡可展开到字段或规则项确认。

### 6.3 确认动作

作者可以：

- 接受候选更新。
- 拒绝候选更新。
- 修改候选文本后接受。
- 标记需要更多裁定。
- 标记 PSD 已更新。
- 标记暂不发布。

## 7. PSD 状态

每张卡可以有一个 PSD 状态：

- `not_needed`：不需要更新牌面。
- `needs_psd_update`：文本已变，需要更新 PSD。
- `psd_updated`：作者已确认 PSD 更新。
- `unknown`：不确定。

第一版不验证 PSD 内文字是否真的更新。作者确认即可。

## 8. TTS Release 辅助

### 8.1 当前 TTS 工作流

当前方式：

- PSD 按牌堆文件夹组织。
- 每个文件夹最多 70 张。
- 牌堆通常按作者拆分，例如古龙1、古龙2、金庸1。
- 场景单独放，因为背面颜色不同。
- Photoshop 联系人表生成拼版图。
- TTS 导入拼版图后产生新的 deck GUID。
- TTS 中按钮 object 的脚本框架固定。
- 每个按钮 object 维护对应牌堆的 `deckGUID` 和 `cardNames`。

当前 PSD 文件夹本身已经表达了大部分 TTS 牌堆归属。例如：

- `psd卡牌/人物/金庸/1`
- `psd卡牌/人物/金庸/2`
- `psd卡牌/人物/金庸/3`
- `psd卡牌/人物/古龙/1`
- `psd卡牌/人物/古龙/2`

第一版应优先以这些目录作为 deck key 的来源。

注意：deck 目录不一定等于纯作者牌堆。为了减少 TTS 牌堆数量，可能存在临时借位目录。例如温瑞安、黄易多出的少量卡可能被临时放在同一类补充目录中。因此：

- TTS deck 归属以 PSD 所在文件夹为准。
- 作者、出处仍来自核心卡牌资料。
- 不要假设 `psd卡牌/人物/温瑞安/2` 中全部都是温瑞安卡。
- 同名 PSD 出现在多个目录时，应作为资产冲突或重复候选列出，不能自动合并。
- 资产索引应区分 `current_deck` 与 `canonical_deck`：
  - `current_deck`：当前 PSD 所在文件夹，用于现在的 TTS 发布。
  - `canonical_deck`：按卡牌作者/类型推导出的理论归属，用于未来整理。

### 8.2 第一版输出

第一版生成：

- 本次受影响牌堆列表。
- 每个受影响牌堆中的卡名顺序。
- 每个受影响牌堆的 `cardNames = {...}` 数据块。
- `numberOfCards` 建议值。
- `deckGUID` 待填提示。
- 哪些牌堆需要重新用 Photoshop 联系人表生成图片。

第一版不自动生成 TTS 图片，不自动填 deck GUID。

### 8.2.1 deck key 建议

从目录生成稳定 deck key：

```text
psd卡牌/人物/金庸/1 -> character_jin_yong_1
psd卡牌/人物/古龙/2 -> character_gu_long_2
psd卡牌/人物/温瑞安/2 -> character_wen_rui_an_2
psd卡牌/人物/黄易/2 -> character_huang_yi_2
psd卡牌/场景 -> scene
psd卡牌/基础卡 -> basic
```

deck key 只用于内部，不影响对外显示。即使目录中存在混合来源卡，也不改变 deck key。

`psd卡牌/废弃` 不生成 deck key，只生成废弃资产索引。

### 8.2.2 重复 PSD

PSD 扫描需要检测同名文件出现在多个目录的情况，但重复不一定是错误。

当前已发现的重复候选包括：

- `割头小鬼`：同时在废弃与古龙/1。
- `朱泪儿`：同时在废弃与古龙/2。
- `尤鸟倦`：同时在温瑞安/2 与黄易/2。
- `左游仙`：同时在温瑞安/2 与黄易/2。

解释：

- 出现在 `废弃` 与正式牌堆中的重复，通常表示旧版已废弃、新版已重做。
- `尤鸟倦`、`左游仙` 属于临时借位放置情况。理论上应归属黄易牌堆，当前放在温瑞安补充目录只是权宜之计。随着黄易/温瑞安人物继续制作，未来应迁回各自 canonical deck。

系统只能列出并分类，不能自动删除或合并。

### 8.3 cardNames 生成要求

生成时应注意：

- 保持中文正确编码。
- 顺序应与 PSD 文件夹/拼版图顺序一致。
- 若无法确定 Photoshop 联系人表排序，则系统应显式提示“排序需确认”。
- 不生成乱码文本。

建议输出格式：

```lua
deckGUID = "PASTE_NEW_DECK_GUID_HERE"
numberOfCards = 70

cardNames = {
  "卡名一",
  "卡名二",
  "卡名三"
}
```

## 9. 玩家更新说明

玩家更新说明应清楚，不需要暴露内部数据结构。

建议组织方式：

1. 按日期。
2. 按新增、修改、废弃、规则裁定分组。
3. 组内可按作者/作品/卡牌类型排序。

每条更新包含：

- 卡名。
- 类型。
- 变更摘要。
- 如有必要，说明需要玩家注意的规则变化。

示例：

```text
2025-12-03

新增
- 燕南飞：新增战斗人物，包含拔剑、蔷薇花魂、蔷薇剑等特技。

修改
- 无名：【无天剑境】调整为任何敌想要影响对无名造成不利效果时，先受到场上所有剑攻击。

裁定
- 可见剑法：本方扣着且在场的人物、非己方翻开的人物均可视为可见范围。
```

## 10. 对外 Report

对外 report 用于替代或同步腾讯文档。

第一版不要求完全复刻 `已制作.xlsx`，但需要清楚、可读、方便国内朋友查看。

建议至少输出：

- 战斗人物表。
- 附加人物表。
- 物品表。
- 称号表。
- 场景表。
- 废弃表。

字段可以沿用现有表格，但未来可以增加：

- 状态。
- 最近更新时间。
- 是否需裁定。
- 标签。

## 11. 人工确认点

Phase 1 中必须人工确认：

- 候选更新是否生效。
- 增量补丁是否合成正确。
- PSD 是否已更新。
- 牌堆顺序是否和 TTS 一致。
- 复杂规则是否需要裁定。
- 玩家更新说明是否可发布。

系统可以建议，但不能擅自确认。

## 12. 第一批验证样例

实现前应先用以下样例验证：

- 周芷若：普通单人、标准主动招式。
- 全真七子：多人一卡，多 Unit，多 LifePool。
- 袁冠南萧中慧：多人一卡，共享 LifePool。
- 金轮法王：多生命阶段。
- 无花：重生与多条命。
- 眉间尺：复杂剧情、人工裁定。
- 李布衣：事件与结算顺序操控。
- 风清扬：作者/作品作为规则条件。
- PSD 目录扫描：金庸/1、金庸/2、金庸/3、古龙/1、古龙/2、场景、基础卡、废弃。

## 13. MVP 成功标准

Phase 1 MVP 成功标准：

1. 能从 `已制作.xlsx` 生成核心资料初版。
2. 能从更新日志生成候选更新报告。
3. 能让作者按卡确认候选更新。
4. 能生成玩家更新说明。
5. 能生成对外 report。
6. 能列出受影响 TTS 牌堆。
7. 能生成对应牌堆的 `cardNames` 数据块。
8. 不丢失原文。
9. 不擅自假设复杂规则。
