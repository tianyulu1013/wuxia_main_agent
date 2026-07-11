from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"
REPORT = ROOT / "docs" / "multi-unit-ownership-report.md"


CONFIRMED_MULTI_UNIT_TITLES = [
    "全真七子",
    "阿三阿四",
    "欢乐英雄",
    "渡厄 渡劫 渡难",
    "玄冥二老",
    "龙木二岛主",
    "江南七怪",
    "太岳四侠",
    "金坷垃三人组",
    "三才剑客",
    "袁冠南 萧中慧",
    "五个人头",
    "血变",
    "千手书生",
    "凌退思",
    "胡青牛王难姑",
    "四大恶人",
    "石中玉",
    "十大恶人",
]


def compact(value: object, limit: int = 140) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[:limit] + "..."


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        placeholders = ",".join("?" for _ in CONFIRMED_MULTI_UNIT_TITLES)
        cards = conn.execute(
            f"""
            SELECT *
            FROM cards
            WHERE title IN ({placeholders})
            ORDER BY source_sheet, source_row
            """,
            CONFIRMED_MULTI_UNIT_TITLES,
        ).fetchall()
        abilities = conn.execute(
            f"""
            SELECT c.title, c.source_sheet, c.source_row,
                   a.ordinal, a.kind, a.name, a.text,
                   a.owner_units_json, a.owner_identity, a.owner_weapons_json
            FROM card_abilities a
            JOIN cards c ON c.id = a.card_id
            WHERE c.title IN ({placeholders})
            ORDER BY c.source_sheet, c.source_row, a.ordinal
            """,
            CONFIRMED_MULTI_UNIT_TITLES,
        ).fetchall()
    finally:
        conn.close()

    by_title: dict[str, list[sqlite3.Row]] = {}
    for row in abilities:
        by_title.setdefault(row["title"], []).append(row)

    found_titles = {row["title"] for row in cards}
    missing_titles = [title for title in CONFIRMED_MULTI_UNIT_TITLES if title not in found_titles]

    lines = [
        "# 多人一卡所属人物待裁定",
        "",
        "本报告只包含作者确认的多人一卡。单人卡不需要 `所属人物` 字段。",
        "",
        f"- 确认多人一卡：{len(cards)} 张",
        f"- 名称未匹配：{len(missing_titles)} 个",
        "",
    ]
    if missing_titles:
        lines.extend(["## 名称未匹配", ""])
        for title in missing_titles:
            lines.append(f"- {title}")
        lines.append("")

    lines.extend(["## 已确认多人一卡", ""])
    for card in cards:
        rows = by_title.get(card["title"], [])
        owned_count = sum(1 for row in rows if row["owner_units_json"])
        lines.extend(
            [
                f"### {card['title']} / {card['source_sheet']}!{card['source_row']}",
                "",
                f"- 生命：{card['life'] or '—'}",
                f"- 身份：{compact(card['identity'], 180) or '—'}",
                f"- 已有所属人物字段：{owned_count}/{len(rows)}",
                "- 当前特技：",
            ]
        )
        for row in rows:
            owners = json.loads(row["owner_units_json"]) if row["owner_units_json"] else None
            owner_parts = [f"所属：{', '.join(owners)}" if owners else "所属：待定/默认"]
            if row["owner_identity"]:
                owner_parts.append(f"身份：{row['owner_identity']}")
            if row["owner_weapons_json"]:
                owner_parts.append(f"兵器：{', '.join(json.loads(row['owner_weapons_json']))}")
            lines.append(
                f"  - `#{row['ordinal']}` `{row['kind']}` / `{row['name'] or '未命名'}` "
                f"({'；'.join(owner_parts)})：{compact(row['text'])}"
            )
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
