from __future__ import annotations

import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / "web" / "card_browser"
OUT_DIR = ROOT / "site_export"

sys.path.insert(0, str(ROOT / "scripts"))
import serve_card_browser as browser  # noqa: E402


def load_abilities(conn: sqlite3.Connection, card_id: str) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT id, ordinal, kind, name, raw_name, type_prefix, source_field,
               start_line, end_line, text, is_exclusive, is_identity,
               owner_units_json, owner_identity, owner_weapons_json, review_flags_json
        FROM card_abilities
        WHERE card_id = ?
        ORDER BY ordinal
        """,
        (card_id,),
    ).fetchall()
    return [
        {
            **dict(row),
            "is_exclusive": bool(row["is_exclusive"]),
            "is_identity": bool(row["is_identity"]),
            "owner_units": json.loads(row["owner_units_json"]) if row["owner_units_json"] else None,
            "owner_identity": row["owner_identity"],
            "owner_weapons": json.loads(row["owner_weapons_json"]) if row["owner_weapons_json"] else None,
            "review_flags": json.loads(row["review_flags_json"]),
        }
        for row in rows
    ]


def build_meta(conn: sqlite3.Connection) -> dict[str, object]:
    metadata = {row["key"]: row["value"] for row in conn.execute("SELECT key, value FROM metadata")}
    by_category = [
        {
            "category": row["category"],
            "category_label": browser.label_category(row["category"]),
            "count": row["count"],
        }
        for row in conn.execute("SELECT category, COUNT(*) AS count FROM cards GROUP BY category ORDER BY category")
    ]
    categories = [
        {"value": row["category"], "label": browser.label_category(row["category"])}
        for row in conn.execute("SELECT DISTINCT category FROM cards ORDER BY category")
    ]
    authors = [
        row["author_group"]
        for row in conn.execute(
            "SELECT DISTINCT author_group FROM cards WHERE author_group IS NOT NULL AND author_group <> '' ORDER BY author_group"
        )
    ]
    return {
        **browser.load_site_document_meta(),
        "source_workbook": metadata.get("source_workbook", ""),
        "source_path": metadata.get("source_path", ""),
        "record_count": int(metadata.get("record_count", "0")),
        "by_category": by_category,
        "categories": categories,
        "authors": authors,
        "evaluation_methodology": browser.evaluation_methodology(),
        "static_export": True,
    }


def build_cards(conn: sqlite3.Connection) -> dict[str, dict[str, object]]:
    cards: dict[str, dict[str, object]] = {}
    image_dir = OUT_DIR / "card-images"
    image_dir.mkdir(parents=True, exist_ok=True)
    for row in conn.execute("SELECT * FROM cards ORDER BY source_sheet, source_row"):
        card = browser.row_to_result(row)
        abilities = load_abilities(conn, card["id"])
        card["abilities"] = abilities
        card["units"] = browser.build_card_units(card, abilities)
        card.update(browser.load_review_layers(card.get("title")))
        card["structure_notes"] = browser.load_structure_notes(card.get("title"))
        image_path = browser.find_card_image(card)
        if image_path and image_path.exists():
            image_name = f"{card['id']}.png"
            shutil.copy2(image_path, image_dir / image_name)
            card["image_url"] = f"card-images/{image_name}"
        cards[str(card["id"])] = card
    return cards


def build_documents() -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for entry in browser.load_site_document_entries():
        documents.append(browser.site_document_payload(entry))
    return documents


def write_frontend() -> None:
    import time
    for filename in ["app.js", "styles.css"]:
        shutil.copy2(WEB_ROOT / filename, OUT_DIR / filename)
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    ts = int(time.time())
    html = re.sub(r'href="/styles\.css(?:\?[^"]*)?"', f'href="styles.css?v={ts}"', html)
    html = re.sub(
        r'<script src="/app\.js(?:\?[^"]*)?"></script>',
        f'<script src="static-data.js?v={ts}"></script>\n    <script src="app.js?v={ts}"></script>',
        html,
    )
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    with browser.connect() as conn:
        data = {
            "meta": build_meta(conn),
            "cards": build_cards(conn),
            "statistics": browser.load_json_file(browser.STATISTICS_PATH, {}),
            "document_meta": browser.load_site_document_meta(),
            "documents": build_documents(),
            "evaluation_entries": browser.evaluation_search_payload({}).get("results", []),
            "evaluation_stats": browser.evaluation_statistics_payload(),
        }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</script", "<\\/script")
    (OUT_DIR / "static-data.js").write_text(f"window.CARD_BROWSER_STATIC_DATA={payload};\n", encoding="utf-8")
    write_frontend()
    total_size = sum(path.stat().st_size for path in OUT_DIR.rglob("*") if path.is_file())
    print(OUT_DIR)
    print(f"files={sum(1 for path in OUT_DIR.rglob('*') if path.is_file())}")
    print(f"bytes={total_size}")


if __name__ == "__main__":
    main()
