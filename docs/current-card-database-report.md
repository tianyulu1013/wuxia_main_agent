# 当前卡牌数据库导入报告

- 来源 Excel：`outputs\2025-excel-sync-candidate\已制作_2025日志同步候选_PSD校准.xlsx`
- SQLite：`data\cards.sqlite`
- JSONL：`data\cards_current/all_cards.jsonl`
- 导入时间 UTC：`2026-07-11T17:13:16.072270+00:00`
- 总记录数：536

## Sheet 统计

| Sheet | 分类 | 记录数 | 最大行 | 最大列 | 未命名表头数 | 有未命名列内容行数 | 空名称行数 |
|---|---|---:|---:|---:|---:|---:|---:|
| 战斗人物 | `combat_characters` | 420 | 578 | 9 | 0 | 0 | 0 |
| 附加人物 | `attached_characters` | 30 | 200 | 27 | 19 | 0 | 0 |
| 物品 | `items` | 59 | 62 | 7 | 1 | 0 | 0 |
| 称号 | `titles` | 11 | 200 | 4 | 0 | 0 | 0 |
| 场景 | `scenes` | 11 | 200 | 4 | 0 | 0 | 1 |
| 废弃 | `deprecated` | 5 | 6 | 9 | 0 | 0 | 0 |

## 分类统计

- `attached_characters`: 30
- `combat_characters`: 420
- `deprecated`: 5
- `items`: 59
- `scenes`: 11
- `titles`: 11

## 作者统计

- 金庸: 180
- 古龙: 116
- 温瑞安: 75
- 其他: 74
- 黄易: 73
- 李凉: 11
- 梁羽生: 3
- 老舍: 1
- 鲁迅: 1

## 重名标题

- 朱泪儿: 附加人物!7, 废弃!6
- 杨过: 战斗人物!243, 战斗人物!244
- 萧秋水: 战斗人物!392, 战斗人物!393
- 郭襄: 战斗人物!170, 战斗人物!237

## 查询示例

```sql
SELECT title, category, source_sheet, source_row FROM cards WHERE normalized_title = '周芷若';
```

```sql
SELECT title, category, source_sheet, source_row FROM cards WHERE all_text LIKE '%不利%' LIMIT 20;
```
