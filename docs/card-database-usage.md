# 卡牌数据库使用说明

当前数据库来源：

- `outputs/2025-excel-sync-candidate/已制作_2025日志同步候选_PSD校准.xlsx`

生成结果：

- SQLite：`data/cards.sqlite`
- JSONL：`data/cards_current/all_cards.jsonl`
- 导入报告：`docs/current-card-database-report.md`

## 重新生成

```powershell
C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\build_card_database.py
```

## 查询

统计：

```powershell
C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\query_cards.py stats
```

按名称精确查：

```powershell
C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\query_cards.py title 周芷若
```

全文包含搜索：

```powershell
C:\Users\biaaa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\query_cards.py search 不利 --limit 20
```

## 主要表

- `cards`：主表，包含标题、类别、描述、关系、兵器、出处、作者、性别、来源 sheet/行号等。
- `cards_fts`：全文索引表。中文查询默认建议用 `query_cards.py search`，它使用包含搜索，避免 SQLite FTS 中文分词问题。

常用 SQL：

```sql
SELECT title, category, source_sheet, source_row
FROM cards
WHERE normalized_title = '周芷若';
```

```sql
SELECT title, category, source_sheet, source_row
FROM cards
WHERE all_text LIKE '%不利%'
LIMIT 20;
```
