# 核心资料字段映射与验证样例 v0.1

## 1. 目的

本文定义 `已制作.xlsx` 到第一版核心资料库的字段映射，并用 6 张代表性卡牌验证数据模型不会过早锁死。

第一版目标不是完整结构化所有规则，而是：

- 不丢失原文。
- 建立稳定基础字段。
- 粗拆可安全识别的结构。
- 标记复杂结构和待裁定问题。
- 支持后续发布辅助、候选更新和 AI 审稿。

## 2. Excel 工作表映射

### 2.1 战斗人物

来源工作表：`战斗人物`

| Excel 字段 | 核心字段 | 说明 |
|---|---|---|
| 名称 | `title` | 中文显示名；不是内部唯一 ID。 |
| 血量 | `raw_fields.life` | 原文保留；同时粗识别生命池。 |
| 身份 | `raw_fields.identity` | 身份描述、身份标签、生命阶段说明等均先保留。 |
| 描述 | `raw_fields.description` | 主要规则文本，保留原文。 |
| 关系 | `raw_fields.relationship` | 独立规则区，不是备注。 |
| 兵器 | `raw_fields.weapons` | 原文保留；粗识别武器标签。 |
| 出处 | `source.work` | 规则可引用字段。 |
| 作者 | `source.author` | 规则可引用字段。 |
| 性别 | `raw_fields.gender` / `units[].gender` | 普通人物可直接映射；多人一卡需人工或半自动拆分。 |

默认：

- `card_type = battle_character`
- `status = active`

### 2.2 附加人物

来源工作表：`附加人物`

字段基本同战斗人物：

- `card_type = attached_character`
- 保留 `血量`、`身份`、`描述`、`关系`、`兵器` 等字段。
- 当前表没有性别字段，核心库仍应支持后续补充性别。
- 附加人物是否实际拥有兵器、是否可出战、是否可被杀死，均不在导入阶段强行判断。

### 2.3 物品

来源工作表：`物品`

| Excel 字段 | 核心字段 |
|---|---|
| 名称 | `title` |
| 描述 | `raw_fields.description` |
| 特性 | `raw_fields.traits` |
| 出处 | `source.work` |
| 作者 | `source.author` |
| 类别 | `category` |

默认：

- `card_type = item`

### 2.4 称号

来源工作表：`称号`

| Excel 字段 | 核心字段 |
|---|---|
| 名称 | `title` |
| 描述 | `raw_fields.description` |
| 出处 | `source.work` |
| 作者 | `source.author` |

默认：

- `card_type = title`

### 2.5 场景

来源工作表：`场景`

| Excel 字段 | 核心字段 |
|---|---|
| 名称 | `title` |
| 描述 | `raw_fields.description` |
| 出处 | `source.work` |
| 作者 | `source.author` |

默认：

- `card_type = scene`
- `scene_back_type = scene`

### 2.6 废弃

来源工作表：`废弃`

`废弃` 不应被视为一种卡牌类型。它是状态。

废弃卡可能属于任意类别，包括战斗人物、附加人物、物品、称号、场景等。

第一版导入时，如果废弃表结构与战斗人物相同，可先按战斗人物字段保留原文，同时标记：

- `status = deprecated`
- `card_type = unknown`

后续由作者确认真实类别。

## 3. ID 规则

中文名是 `title`，不作为唯一主键。

第一版内部 ID 不建议依赖纯拼音。原因是中文同音、近音、异体名很多，例如“段玉”和“段誉”容易冲突。

建议使用稳定 opaque ID：

```text
{card_type}_{short_source_code}_{short_hash}
```

例如：

- `battle_character_jy_a13f92`
- `battle_character_gl_09bc21`

同时保留可读字段：

```yaml
title: 周芷若
display_key: 金庸 / 倚天屠龙记 / 周芷若
```

ID 稳定性优先于可读性；对外显示始终使用中文名。未来如果需要更可读的别名，可增加 `aliases`，但不作为主键。

## 4. 第一版自动粗识别

### 4.1 生命

| 情况 | 处理 |
|---|---|
| `血量` 为普通数字，如 `2000` | 创建 1 个默认 LifePool。 |
| `血量` 为空 | `has_life = false`，但仍可被杀死。 |
| `血量` 含多个数字，如 `2500 3800` | 创建多个生命阶段候选，并标记需确认转换规则。 |
| `血量` 是共享生命 | 不能仅靠血量字段判断，需要从文本或人工确认。 |
| 复活/重生 | 静态资料中不预生成多条生命。先作为规则项记录；运行时才产生重生状态或额外生命。 |

### 4.2 标签

可粗识别：

- `【恶】`、`【残】` 等身份标签。
- `【剑】`、`【刀】`、`【奇门】`、`【棍杖】` 等武器标签。
- `【刀S】` 等专家标签。
- `【特技名】` 作为专属特技候选。
- 文本末尾 `(身份)` 作为身份特技候选。

### 4.3 特技块

可粗识别前缀：

- 内功
- 招式
- 武功
- 技能
- `*`
- 字，也就是无前缀特技
- 符卡

注意：

- Excel 中前缀可能延续到后续缩进行。
- 空行后的无前缀块应识别为 `字`。
- 粗拆结果只是候选，不直接等同权威结构。

## 5. 六张验证样例

### 5.1 周芷若：普通单人

用途：

- 验证普通单人结构。
- 验证标准主动招式。
- 验证多武器标签。
- 验证关系区。

建议模型：

```yaml
card:
  title: 周芷若
  card_type: battle_character
  source:
    author: 金庸
    work: 倚天屠龙记
  units:
    - title: 周芷若
      gender: female
      head_count: 1
      life_pool_refs: [life_001]
      identity:
        description: 可双持兵器
  life_pools:
    - id: life_001
      max_life: 2000
      has_life: true
      default_zero_life_behavior: death
  tags:
    structure: [single_unit, single_life]
  review:
    notes:
      - 玄铁指环涉及循环与清除，需要标记规则风险。
```

### 5.2 全真七子：多人一卡，多 Unit，多 LifePool

用途：

- 验证多人一卡。
- 验证多个子人物各有生命。
- 验证阵法/组合形态。
- 验证人头、性别、个人规则。

建议模型：

```yaml
card:
  title: 全真七子
  card_type: battle_character
  units:
    - title: 马钰
      life_pool_refs: [life_ma_yu]
      identity:
        description: 丹阳子
    - title: 丘处机
      life_pool_refs: [life_qiu_chuji]
      identity:
        description: 长春子
    - title: 王处一
      life_pool_refs: [life_wang_chuyi]
      identity:
        description: 铁脚仙 / 玉阳子
    - title: 刘处玄
      life_pool_refs: [life_liu_chuxuan]
      identity:
        description: 长生子
    - title: 谭处端
      life_pool_refs: [life_tan_chuduan]
      identity:
        description: 长真子
    - title: 郝大通
      life_pool_refs: [life_hao_datong]
      identity:
        description: 广宁子
    - title: 孙不二
      gender: female
      life_pool_refs: [life_sun_buer]
      identity:
        description: 清净散人
  life_pools:
    - id: life_ma_yu
      max_life: 2000
    - id: life_qiu_chuji
      max_life: 2200
    - id: life_wang_chuyi
      max_life: 1900
    - id: life_liu_chuxuan
      max_life: 1500
    - id: life_tan_chuduan
      max_life: 1400
    - id: life_hao_datong
      max_life: 1000
    - id: life_sun_buer
      max_life: 800
  tags:
    structure: [multi_unit, multi_life_pool, formation]
  unresolved_questions:
    - 王处一的两个身份/规则如何拆分为一个 Unit 的多个称号或两个规则块，需要确认。
```

### 5.3 袁冠南 萧中慧：多人一卡，共享生命

用途：

- 验证多个 Unit 共享一个 LifePool。
- 验证同一张卡中针对单一人物的技能。
- 验证性别为“多人”的处理。

建议模型：

```yaml
card:
  title: 袁冠南 萧中慧
  card_type: battle_character
  units:
    - title: 袁冠南
      gender: male
      life_pool_refs: [life_shared]
    - title: 萧中慧
      gender: female
      life_pool_refs: [life_shared]
  life_pools:
    - id: life_shared
      max_life: 4500
      shared: true
      owner_unit_refs: [袁冠南, 萧中慧]
  tags:
    structure: [multi_unit, shared_life_pool]
  review:
    notes:
      - 针对男女、杀死一人、共享生命池的交互需要保留人工裁定能力。
```

### 5.4 金轮法王：多生命阶段

用途：

- 验证 `血量 = 2500 3800`。
- 验证生命阶段转换。
- 验证身份区包含阶段转换规则。

建议模型：

```yaml
card:
  title: 金轮法王
  card_type: battle_character
  units:
    - title: 金轮法王
      gender: male
      life_pool_refs: [life_stage_1, life_stage_2]
      identity:
        tags: [恶]
  life_pools:
    - id: life_stage_1
      max_life: 2500
      stage_index: 1
      transition_rule:
        raw_text: 第一次生命用尽后返回西藏，去除不利，再出场...
    - id: life_stage_2
      max_life: 3800
      stage_index: 2
  tags:
    structure: [single_unit, multi_life_stage]
  review:
    notes:
      - 第一生命用尽后的规则变化影响招式和武功，需要作为 life_stage transition 记录。
```

### 5.5 无花：动态重生

用途：

- 验证基础单生命 + 动态重生。
- 验证“各条命各有一次”的规则。
- 验证静态资料与运行状态分离。

建议模型：

```yaml
card:
  title: 无花
  card_type: battle_character
  units:
    - title: 无花
      gender: male
      life_pool_refs: [life_base]
      identity:
        tags: [恶]
  life_pools:
    - id: life_base
      max_life: 2000
  skill_blocks:
    - display_name: 伊贺忍术
      printed_type: 技能
      raw_text: 木- 附2000重生（单局累积，基础一次）
      rule_items:
        - raw_text: 附2000重生（单局累积，基础一次）
          tags: [dynamic_revive]
    - display_name: 妙僧
      printed_type: 字
      is_exclusive: true
      raw_text: 各条命各有一次真无敌至下次与人交手前的机会...
  tags:
    structure: [single_unit, dynamic_revive]
  review:
    notes:
      - 无花静态上只有一个基础生命池；重生次数和额外生命属于运行时状态，不应在静态资料中预生成。
      - 妙僧按“各条命”计算真无敌机会，需要未来运行状态能引用动态生命次数。
```

### 5.6 李布衣：事件与顺序操控

用途：

- 验证事件目标。
- 验证几率控制。
- 验证结算顺序变化。
- 验证高规则权限卡。

建议模型：

```yaml
card:
  title: 李布衣
  card_type: battle_character
  units:
    - title: 李布衣
      gender: male
      life_pool_refs: [life_001]
  life_pools:
    - id: life_001
      max_life: 1111
  tags:
    structure: [single_unit, event_manipulation]
    risk: [randomness_control, resolution_order_manipulation, manual_adjudication_likely]
  review:
    digitalization_level: manual_adjudication
    notes:
      - 布衣神相可控制非抽卡几率，并改变相关事件来源、对象、结算顺序，需保留事件级目标模型。
```

## 6. 第一版核心库文件建议

第一版可以按卡牌类型和作者拆分：

```text
data/cards/
  battle_characters/
    jin_yong.yaml
    gu_long.yaml
    wen_rui_an.yaml
    huang_yi.yaml
    other.yaml
  attached_characters.yaml
  items.yaml
  titles.yaml
  scenes.yaml
```

如果单文件过大，再按作品或牌堆继续拆。

## 7. 第一版导入策略

建议分三步：

1. **Raw Import**
   - 完整导入 Excel 原字段。
   - 生成稳定 ID。
   - 不进行复杂解析。

2. **Light Enrichment**
   - 识别生命数字。
   - 识别标签。
   - 粗拆特技块。
   - 标记高复杂度卡。

3. **Sample Review**
   - 先输出本文 6 张样例的核心库草稿。
   - 作者确认数据形状。
   - 再批量处理。

## 8. SkillBlock 存储位置

第一版建议 SkillBlock 与 Card 存在同一个卡牌资料文件中，而不是拆到另一个文件。

原因：

- 人工审阅时能在一处看到完整卡牌。
- 不容易出现链接断裂。
- 后续如果需要索引或查询，可以由 SQLite 索引生成。

示意：

```yaml
card:
  title: 无花
  raw_fields:
    description: "..."
  skill_blocks:
    - display_name: 迎风一刀斩
      printed_type: 招式
      raw_text: "-木 可后撤2张释放..."
    - display_name: 伊贺忍术
      printed_type: 技能
      raw_text: "木- 附2000重生..."
```

## 9. 静态资料与运行状态

核心库第一版主要记录静态资料。

例如：

- 无花静态资料只有基础生命 2000。
- “附2000重生”是规则文本。
- 实际游戏中累积几个重生、当前第几条命、各条命是否用过真无敌，属于运行状态。

因此核心资料不应为了电子化过早生成运行时对象。需要时可在未来规则引擎中从规则项创建运行时状态。

## 10. 待确认问题

1. 多人一卡中的 Unit 拆分第一版是否全部人工标记，还是只给高复杂度 tag。
2. 第一版是否需要生成可直接人工审阅的 YAML 样例文件。
3. PSD 文件夹结构已进入 workspace，下一步可用 psd卡牌/ 扫描生成 asset/deck 索引。
