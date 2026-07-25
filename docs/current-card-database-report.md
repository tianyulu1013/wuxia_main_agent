# 当前卡牌数据库导入报告

- 来源 Excel：`outputs\2025-excel-sync-candidate\已制作_2025日志同步候选_PSD校准.xlsx`
- SQLite：`data\cards.sqlite`
- JSONL：`data\cards_current/all_cards.jsonl`
- 导入时间 UTC：`2026-07-25T07:36:07.885583+00:00`
- 总记录数：541

## Sheet 统计

| Sheet | 分类 | 记录数 | 最大行 | 最大列 | 未命名表头数 | 有未命名列内容行数 | 空名称行数 |
|---|---|---:|---:|---:|---:|---:|---:|
| 战斗人物 | `combat_characters` | 423 | 424 | 11 | 0 | 0 | 0 |
| 附加人物 | `attached_characters` | 30 | 31 | 11 | 0 | 0 | 0 |
| 物品 | `items` | 59 | 60 | 11 | 0 | 0 | 0 |
| 称号 | `titles` | 11 | 12 | 11 | 0 | 0 | 0 |
| 场景 | `scenes` | 13 | 14 | 11 | 0 | 0 | 0 |
| 废弃 | `deprecated` | 5 | 6 | 11 | 0 | 0 | 0 |

## 分类统计

- `attached_characters`: 30
- `combat_characters`: 423
- `deprecated`: 5
- `items`: 59
- `scenes`: 13
- `titles`: 11

## 作者统计

- 金庸: 183
- 古龙: 119
- 其他: 75
- 温瑞安: 75
- 黄易: 73
- 李凉: 11
- 梁羽生: 3
- 老舍: 1
- 鲁迅: 1

## 重名标题

- 朱泪儿: 附加人物!6, 废弃!5
- 杨过: 战斗人物!242, 战斗人物!243
- 萧秋水: 战斗人物!391, 战斗人物!392
- 郭襄: 战斗人物!169, 战斗人物!236

## 查询示例

```sql
SELECT title, category, source_sheet, source_row FROM cards WHERE normalized_title = '周芷若';
```

```sql
SELECT title, category, source_sheet, source_row FROM cards WHERE all_text LIKE '%不利%' LIMIT 20;
```
