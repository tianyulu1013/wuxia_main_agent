from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def print_rows(rows: list[sqlite3.Row], *, json_output: bool) -> None:
    data = [dict(row) for row in rows]
    if json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if not data:
        print("未找到")
        return
    for row in data:
        print(f"{row.get('title')} [{row.get('category')}] {row.get('source_sheet')}!{row.get('source_row')}")
        description = row.get("description")
        if description:
            compact = str(description).replace("\n", " ")
            if len(compact) > 180:
                compact = compact[:180] + "..."
            print(f"  {compact}")


def exact_title(title: str, json_output: bool) -> None:
    normalized = title.replace("（", "(").replace("）", ")").replace(" ", "")
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT title, category, source_sheet, source_row, life, identity, description, relationships, weapons
            FROM cards
            WHERE normalized_title = ?
            ORDER BY category, source_sheet, source_row
            """,
            (normalized,),
        ).fetchall()
    print_rows(rows, json_output=json_output)


def full_text(term: str, limit: int, json_output: bool) -> None:
    like_term = f"%{term}%"
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT title, category, source_sheet, source_row, description, relationships
            FROM cards
            WHERE title LIKE ?
               OR description LIKE ?
               OR relationships LIKE ?
               OR identity LIKE ?
               OR weapons LIKE ?
               OR source_work LIKE ?
               OR author_group LIKE ?
               OR all_text LIKE ?
            ORDER BY category, source_sheet, source_row
            LIMIT ?
            """,
            (like_term, like_term, like_term, like_term, like_term, like_term, like_term, like_term, limit),
        ).fetchall()
    print_rows(rows, json_output=json_output)


def stats(json_output: bool) -> None:
    with connect() as conn:
        counts = conn.execute(
            "SELECT category, COUNT(*) AS count FROM cards GROUP BY category ORDER BY category"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) AS count FROM cards").fetchone()["count"]
    data = {"total": total, "by_category": [dict(row) for row in counts]}
    if json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"总数: {total}")
        for row in data["by_category"]:
            print(f"- {row['category']}: {row['count']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the local wuxia card database.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a compact text view.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    title_parser = subparsers.add_parser("title", help="Exact title lookup.")
    title_parser.add_argument("title")
    title_parser.add_argument("--json", action="store_true", help="Print JSON instead of a compact text view.")

    search_parser = subparsers.add_parser("search", help="Full-text search using SQLite FTS.")
    search_parser.add_argument("term")
    search_parser.add_argument("--limit", type=int, default=20)
    search_parser.add_argument("--json", action="store_true", help="Print JSON instead of a compact text view.")

    stats_parser = subparsers.add_parser("stats", help="Show database counts.")
    stats_parser.add_argument("--json", action="store_true", help="Print JSON instead of a compact text view.")

    args = parser.parse_args()
    if args.command == "title":
        exact_title(args.title, args.json)
    elif args.command == "search":
        full_text(args.term, args.limit, args.json)
    elif args.command == "stats":
        stats(args.json)


if __name__ == "__main__":
    main()
