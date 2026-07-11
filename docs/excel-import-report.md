# Excel 导入报告

- 来源：`已制作.xlsx`
- 输出目录：`data/cards_raw/`
- 总记录数：533

## Sheet 统计

| Sheet | 分类 | 记录数 | 最大行 | 最大列 | 未命名表头数 | 有未命名列内容的行数 | 空名称行数 |
|---|---|---:|---:|---:|---:|---:|---:|
| 战斗人物 | `combat_characters` | 417 | 575 | 9 | 0 | 0 | 0 |
| 附加人物 | `attached_characters` | 30 | 200 | 27 | 19 | 0 | 0 |
| 物品 | `items` | 58 | 61 | 7 | 1 | 0 | 0 |
| 称号 | `titles` | 11 | 200 | 4 | 0 | 0 | 0 |
| 场景 | `scenes` | 12 | 200 | 4 | 0 | 0 | 1 |
| 废弃 | `deprecated` | 5 | 6 | 9 | 0 | 0 | 0 |

## 分类统计

- `attached_characters`: 30
- `combat_characters`: 417
- `deprecated`: 5
- `items`: 58
- `scenes`: 12
- `titles`: 11

## 作者统计

- 金庸: 177
- 古龙: 115
- 温瑞安: 75
- 其他: 74
- 黄易: 73
- 李凉: 11
- 梁羽生: 3
- 老舍: 1
- 鲁迅: 1
- 射雕英雄传: 1

## 重名标题

- 朱泪儿: 附加人物!7, 废弃!6
- 杨过: 战斗人物!243, 战斗人物!244
- 萧秋水: 战斗人物!392, 战斗人物!393
- 郭襄: 战斗人物!170, 战斗人物!237

## 需要人工查看的结构问题

- `场景` 存在空名称行，行：13

## 输出文件

- `data/cards_raw/all_cards.jsonl`
- `data/cards_raw/combat_characters.jsonl`
- `data/cards_raw/attached_characters.jsonl`
- `data/cards_raw/items.jsonl`
- `data/cards_raw/titles.jsonl`
- `data/cards_raw/scenes.jsonl`
- `data/cards_raw/deprecated.jsonl`
- `data/cards_raw/manifest.json`
