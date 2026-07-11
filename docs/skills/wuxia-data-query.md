# Skill: 数据读取与查询

## 适用场景

查卡、核对字段、分析特技、生成统计、前端显示问题排查。

## 首选数据

- `data/cards.sqlite`
- `data/cards_current/all_cards.jsonl`
- `data/cards_current/abilities.jsonl`
- `data/card_unit_overrides.json`
- `data/card_field_overrides.json`
- `data/author_ability_overrides.json`

## 查询工具

本地网页：

```powershell
python scripts/serve_card_browser.py
```

浏览器：

```text
http://127.0.0.1:8765
```

命令行：

```powershell
python scripts/query_cards.py <关键词>
```

## 查询原则

- 查身份本身，例如 `【恶】`，优先查身份/属性字段。
- 查针对身份的效果，例如杀 `【恶】`，查特技文本。
- 查出处，使用出处字段。
- 查兵器，使用兵器字段。
- 默认不把废弃卡混入普通统计；除非用户明确查废弃。

## 不要做的事

- 不要用旧更新日志覆盖当前数据库。
- 不要把 Excel、PSD、日志之间的小差异当作自动改库依据。
- 不要因为解析器误读就发明复杂规则；应修正数据或记录卡面待办。
