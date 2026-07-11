# 资产与 TTS 牌堆索引样例报告 v0.1

## 1. 扫描范围

扫描目录：

```text
psd卡牌/
```

当前 PSD 总量约 551 个。另有根目录样例 PSD、JPG、release PNG、PDF、规则文档等，不计入 TTS PSD 索引。

## 2. Deck 计数

| current_deck | 来源目录 | PSD 数量 | 用途 |
|---|---|---:|---|
| `character_jin_yong_1` | `psd卡牌/人物/金庸/1` | 70 | TTS 人物牌堆 |
| `character_jin_yong_2` | `psd卡牌/人物/金庸/2` | 70 | TTS 人物牌堆 |
| `character_jin_yong_3` | `psd卡牌/人物/金庸/3` | 35 | TTS 人物牌堆 |
| `character_gu_long_1` | `psd卡牌/人物/古龙/1` | 70 | TTS 人物牌堆 |
| `character_gu_long_2` | `psd卡牌/人物/古龙/2` | 45 | TTS 人物牌堆 |
| `character_wen_rui_an_1` | `psd卡牌/人物/温瑞安/1` | 70 | TTS 人物牌堆 |
| `character_wen_rui_an_2` | `psd卡牌/人物/温瑞安/2` | 5 | TTS 补充牌堆，含临时借位 |
| `character_huang_yi_1` | `psd卡牌/人物/黄易/1` | 70 | TTS 人物牌堆 |
| `character_huang_yi_2` | `psd卡牌/人物/黄易/2` | 2 | TTS 补充牌堆 |
| `character_other_wuxia_xuanhuan` | `psd卡牌/人物/其他武侠玄幻` | 58 | TTS 人物牌堆 |
| `character_modern_meme` | `psd卡牌/人物/现代鬼畜` | 27 | TTS 人物牌堆 |
| `scene` | `psd卡牌/场景` | 11 | TTS 场景牌堆，牌背不同 |
| `basic_cards` | `psd卡牌/基础卡` | 12 | 基础卡/牌背素材 |
| none | `psd卡牌/废弃` | 6 | 废弃旧版资产，不生成 TTS deck |

## 3. 重复 PSD 报告

### deprecated_old_version

这些重复表示旧卡废弃后重做，新版在正式牌堆，旧版在废弃目录。

| 卡名 | 废弃资产 | 正式资产 |
|---|---|---|
| 割头小鬼 | `psd卡牌/废弃/割头小鬼.PSD` | `psd卡牌/人物/古龙/1/割头小鬼.psd` |
| 朱泪儿 | `psd卡牌/废弃/朱泪儿.PSD` | `psd卡牌/人物/古龙/2/朱泪儿.psd` |

### temporary_placement

这些重复表示临时借位。理论归属不等于当前 TTS 文件夹。

| 卡名 | 当前资产 | 重复资产 | canonical_deck 备注 |
|---|---|---|---|
| 尤鸟倦 | `psd卡牌/人物/温瑞安/2/尤鸟倦.psd` | `psd卡牌/人物/黄易/2/尤鸟倦.psd` | 理论上归黄易；当前借位是权宜之计 |
| 左游仙 | `psd卡牌/人物/温瑞安/2/左游仙.PSD` | `psd卡牌/人物/黄易/2/左游仙.PSD` | 理论上归黄易；当前借位是权宜之计 |

系统不能自动删除或合并这些重复，只能列出供确认。

## 4. Deck 样例：`character_jin_yong_3`

来源目录：

```text
psd卡牌/人物/金庸/3
```

数量：35。

TTS 实际顺序候选，由作者提供：

```text
三尸脑神丹
何铁手
四大恶人
全真七子
冷月宝刀
周伯通
周威信
周芷若
宋远桥
小昭
岳不群
岳飞
左冷禅
张三丰
张召重
张无忌
张翠山
归辛树
木桑道长
梅念笙
石中玉
田伯光
田归农
神雕
莫大先生
胡青牛王难姑
袁士霄
贝海石
赏善罚恶令
赵半山
赵敏
软猬甲
金蛇剑
阿紫
黄真
```

对应 `cardNames` 候选：

```lua
deckGUID = "PASTE_NEW_DECK_GUID_HERE"
numberOfCards = 35

cardNames = {
  "三尸脑神丹",
  "何铁手",
  "四大恶人",
  "全真七子",
  "冷月宝刀",
  "周伯通",
  "周威信",
  "周芷若",
  "宋远桥",
  "小昭",
  "岳不群",
  "岳飞",
  "左冷禅",
  "张三丰",
  "张召重",
  "张无忌",
  "张翠山",
  "归辛树",
  "木桑道长",
  "梅念笙",
  "石中玉",
  "田伯光",
  "田归农",
  "神雕",
  "莫大先生",
  "胡青牛王难姑",
  "袁士霄",
  "贝海石",
  "赏善罚恶令",
  "赵半山",
  "赵敏",
  "软猬甲",
  "金蛇剑",
  "阿紫",
  "黄真"
}
```

注意：此前按文件名排序得到的顺序与 TTS 实际顺序不同。以后已有牌堆必须优先使用 TTS 脚本中已验证的 `cardNames`，或作者提供的顺序；文件名排序只能作为新牌堆的候选。

## 5. Deck 样例：`scene`

来源目录：

```text
psd卡牌/场景
```

数量：11。

文件名排序候选：

```text
光明顶
华山之巅
少室山
恶人谷
排难解纷当六强
昆仑神宫
桃花岛
活死人墓
老魔小丑
锁妖塔
长坂坡擂台
```

场景牌背不同，应独立生成 TTS release deck。

## 6. Asset Record 样例

### 普通资产

```yaml
asset:
  title_from_filename: 周芷若
  normalized_title: 周芷若
  asset_type: psd
  path: psd卡牌/人物/金庸/3/周芷若.PSD
  current_deck: character_jin_yong_3
  canonical_deck: character_jin_yong_3
  placement_status: normal
  matched_card_title: 周芷若
  match_confidence: high
```

### 废弃旧版资产

```yaml
asset:
  title_from_filename: 朱泪儿
  normalized_title: 朱泪儿
  asset_type: psd
  path: psd卡牌/废弃/朱泪儿.PSD
  current_deck: null
  canonical_deck: null
  placement_status: deprecated_old_version
  matched_card_title: 朱泪儿
  match_confidence: medium
```

### 临时借位资产

```yaml
asset:
  title_from_filename: 尤鸟倦
  normalized_title: 尤鸟倦
  asset_type: psd
  path: psd卡牌/人物/温瑞安/2/尤鸟倦.psd
  current_deck: character_wen_rui_an_2
  canonical_deck: character_huang_yi_2
  placement_status: temporary_placement
  matched_card_title: 尤鸟倦
  match_confidence: high
```

## 7. 待确认

1. `character_jin_yong_3` 已确认文件名排序不等于 TTS 命名顺序，应保存作者提供的 TTS 顺序。
2. 场景 deck 是否需要生成 `cardNames` 脚本。
3. 基础卡是否需要生成 `cardNames` 脚本。
4. `尤鸟倦`、`左游仙` 当前 TTS 实际使用哪一份 PSD。
5. 第一版是否接受 `cardNames` 只按当前 TTS 物理牌堆生成，不尝试按 canonical deck 拆分。
