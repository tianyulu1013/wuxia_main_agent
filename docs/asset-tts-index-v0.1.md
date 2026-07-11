# 资产与 TTS 牌堆索引设计 v0.2

## 1. 目标

本文定义如何从 PSD 资产目录生成资产索引和 TTS 牌堆索引。

第一阶段目标不是自动操作 TTS，而是：

- 识别每个 PSD 当前所在牌堆。
- 生成每个牌堆的卡名顺序。
- 生成 TTS `cardNames` 数据块。
- 标记需要重新生成 release 图片的牌堆。
- 检测重复 PSD、废弃旧版、临时借位和命名不一致。
- 为未来整理牌堆提供 `canonical_deck` 建议。

## 2. 资产根目录

当前项目优先使用：

```text
actual_psd/
```

`actual_psd/` 是 Windows Junction，指向作者本机真实 PSD 目录：

```text
E:\Tabletop Simulator Resources\Xia\卡牌PSD文件
```

如果其他环境没有 `actual_psd/`，工具可以退回读取 `psd卡牌/` 样本目录，但样本目录不能作为最终权威。

## 3. 当前真实目录结构

```text
actual_psd/
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
  *.psd  # 根目录模板文件
```

当前真实统计：

| 目录 | PSD 数量 | 说明 |
|---|---:|---|
| `actual_psd/人物/金庸/1` | 70 | TTS 人物牌堆 |
| `actual_psd/人物/金庸/2` | 70 | TTS 人物牌堆 |
| `actual_psd/人物/金庸/3` | 35 | TTS 人物牌堆 |
| `actual_psd/人物/古龙/1` | 70 | TTS 人物牌堆 |
| `actual_psd/人物/古龙/2` | 45 | TTS 人物牌堆 |
| `actual_psd/人物/温瑞安/1` | 70 | TTS 人物牌堆 |
| `actual_psd/人物/温瑞安/2` | 5 | 当前合并补充牌堆 |
| `actual_psd/人物/黄易/1` | 70 | TTS 人物牌堆 |
| `actual_psd/人物/黄易/2` | 2 | 当前不作为独立 release 牌堆 |
| `actual_psd/人物/其他武侠玄幻` | 58 | TTS 人物牌堆 |
| `actual_psd/人物/现代鬼畜` | 27 | TTS 人物牌堆 |
| `actual_psd/场景` | 11 | TTS 场景牌堆，牌背不同 |
| `actual_psd/基础卡` | 12 | 基础五行卡与牌背 |
| `actual_psd/废弃` | 6 | 废弃/旧版资产，不生成 TTS release deck |
| `actual_psd/*.psd` | 6 | 模板文件，不生成 TTS release deck |

## 4. Deck 概念

`current_deck` 表示 PSD 当前所在文件夹，也就是当前 TTS 发布所用牌堆。

```yaml
title: 段誉
asset_path: actual_psd/人物/金庸/1/段誉.PSD
current_deck: character_jin_yong_1
canonical_deck: character_jin_yong_1
placement_status: normal
```

`canonical_deck` 表示按卡牌类型、作者、理论分类推导出的归属。它不一定等于当前文件夹。

```yaml
title: 尤鸟倦
asset_path: actual_psd/人物/温瑞安/2/尤鸟倦.psd
current_deck: character_huang_yi_wen_rui_an_extra
canonical_deck: character_huang_yi_2
placement_status: temporary_placement
```

## 5. Deck Key 映射

| 当前路径 | deck key |
|---|---|
| `actual_psd/人物/金庸/1` | `character_jin_yong_1` |
| `actual_psd/人物/金庸/2` | `character_jin_yong_2` |
| `actual_psd/人物/金庸/3` | `character_jin_yong_3` |
| `actual_psd/人物/古龙/1` | `character_gu_long_1` |
| `actual_psd/人物/古龙/2` | `character_gu_long_2` |
| `actual_psd/人物/温瑞安/1` | `character_wen_rui_an_1` |
| `actual_psd/人物/温瑞安/2` | `character_huang_yi_wen_rui_an_extra` |
| `actual_psd/人物/黄易/1` | `character_huang_yi_1` |
| `actual_psd/人物/黄易/2` | `character_huang_yi_2` |
| `actual_psd/人物/其他武侠玄幻` | `character_other_wuxia_xuanhuan` |
| `actual_psd/人物/现代鬼畜` | `character_modern_meme` |
| `actual_psd/场景` | `scene` |
| `actual_psd/基础卡` | `basic_cards` |

`actual_psd/废弃` 不生成 deck key，只生成废弃资产索引。

## 6. Slot 顺序

TTS 命名脚本依赖 `cardNames` 顺序。第一版不能把文件名排序视为权威顺序。

顺序来源优先级：

1. 已在 TTS 中验证可用的命名脚本 `cardNames`。
2. 作者明确提供的顺序。
3. Photoshop 联系表实际输出顺序。
4. 文件名排序候选。

当前作者提供的 TTS slot 顺序记录在：

```text
docs/tts-slot-orders-v0.1.md
```

这些顺序应作为已有牌堆的 `user_confirmed_tts_order` 草案，用于核对 PSD 文件夹并生成 `cardNames`。

## 7. 合并牌堆

`黄易温瑞安` 是当前合并补充牌堆，不是 canonical 作者分类。

当前实际路径：

```text
actual_psd/人物/温瑞安/2
```

当前包含：

- `严苍茫`
- `尤鸟倦`
- `左丘超然`
- `左游仙`
- `车占风`

其中 `尤鸟倦`、`左游仙` 理论上归黄易，但当前为了减少 TTS 牌堆数量，暂时放在合并补充牌堆。

## 8. 资产索引字段

每个 PSD 生成一个 asset record。

```yaml
asset:
  id: asset_short_hash
  title_from_filename: string
  normalized_title: string
  asset_type: psd
  path: string
  extension: psd
  current_deck: string | null
  canonical_deck: string | null
  slot_order: number | null
  slot_order_source: user_confirmed_tts_order | filename_sort_candidate | script_card_names | contact_sheet
  placement_status: normal | temporary_placement | deprecated_old_version | duplicate_needs_review | template
  matched_card_id: string | null
  matched_card_title: string | null
  match_confidence: high | medium | low | none
  notes: []
```

## 9. 命名与别名

PSD 文件名、TTS `cardNames`、资料库标准卡名可能不同。不能简单自动改名，需要维护作者确认过的别名/裁定表。

当前已确认的别名包括：

| TTS/资料库名称 | PSD 文件名候选 |
|---|---|
| `郭襄（峨眉祖师）` | `郭襄` |
| `杨过（小）` | `杨过（少年）` |
| `杨过（大侠）` | `杨过` |
| `玄铁重剑` | `玄铁剑` |
| `辟邪剑法` | `辟邪剑谱` |
| `萧秋水（少年）` | `萧秋水(少年)` |
| `嬴政` | `秦始皇` |
| `雾雨魔理沙` | `魔理沙` |

`迪卢木多` 已确认属于 `现代` 牌堆，位置在 `许存舟` 后、`金坷垃三人组` 前。

作者确认后的正式裁定记录在：

```text
docs/card-name-rulings-v0.1.md
```

后续工具应优先读取裁定表；检查报告中的“缺失/多出”如果能被裁定表解释，应视为已确认别名，而不是错误。

## 10. 重复 PSD 分类

同名 PSD 出现在多个目录时，不自动合并。

已知分类：

- `割头小鬼`：旧版在 `废弃`，新版在正式牌堆。
- `朱泪儿`：旧版在 `废弃`，新版在正式牌堆。
- `尤鸟倦`、`左游仙`：真实目录中同时存在于 `温瑞安/2` 和 `黄易/2`，当前 release 以 `温瑞安/2` 合并牌堆为准。

## 11. cardNames 生成

每个 `tts_deck` 可以生成 Lua 数据块：

```lua
deckGUID = "PASTE_NEW_DECK_GUID_HERE"
numberOfCards = 70

cardNames = {
  "东方不败",
  "丁典",
  "丁春秋",
}
```

生成规则：

- 优先使用 `docs/tts-slot-orders-v0.1.md` 中确认过的顺序。
- 中文保持 UTF-8。
- `deckGUID` 第一版使用占位符，等待 TTS 生成后手工填入。
- `numberOfCards` 等于当前 deck 的 slot 数量。
- 对别名使用作者确认过的展示名，而不是强行改 PSD 文件名。

## 12. Release 影响判断

当一张卡更新后，系统按以下顺序判断影响：

1. 根据卡名和别名表匹配 asset。
2. 找到 asset 的 `current_deck`。
3. 将该 deck 标记为受影响。
4. 如果 `psd_status = needs_psd_update`，提示作者先更新 PSD。
5. 如果 PSD 已更新，则该 deck 需要重新生成 TTS 图片。
6. 生成该 deck 的最新 `cardNames` 候选。

如果 card title 匹配多个 asset：

- 一个在 `废弃`，一个在正式目录：优先正式目录，并提示存在旧版。
- 多个都在正式目录：进入人工确认。

## 13. 当前工具输出

当前对照报告：

```text
docs/tts-slot-order-check.md
```

当前检查脚本：

```text
scripts/check_tts_slot_orders.py
```

脚本优先读取 `actual_psd/`，不存在时才退回 `psd卡牌/`。
