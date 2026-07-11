from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from generate_ability_layout_report import (
    apply_action_codes,
    is_actionable,
    load_adjudications,
    should_show_action,
)


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT
              c.id AS card_id,
              c.title,
              c.source_sheet,
              c.source_row,
              a.ordinal,
              a.kind,
              a.name,
              a.text,
              a.review_flags_json
            FROM card_abilities a
            JOIN cards c ON c.id = a.card_id
            ORDER BY c.source_sheet, c.source_row, a.ordinal
            """
        ).fetchall()
    finally:
        conn.close()

    items = []
    for row in rows:
        item = dict(row)
        item["review_flags"] = json.loads(item.pop("review_flags_json"))
        if not is_actionable(item):
            continue
        items.append(item)

    apply_action_codes(items, load_adjudications())

    for item in items:
        if not should_show_action(item):
            continue
        print(
            f"{item['action_code']}\t{item['card_id']}::{item['ordinal']:03d}\t"
            f"{item['title']}\t{item['source_sheet']}!{item['source_row']}\t"
            f"{item['kind']}\t{item.get('name') or ''}\t{item['text']}"
        )


if __name__ == "__main__":
    main()
