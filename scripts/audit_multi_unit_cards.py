from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"
REPORT = ROOT / "docs" / "multi-unit-card-audit.md"


TITLE_HINTS = (
    "二老",
    "二岛主",
    "三人组",
    "四大",
    "三才",
    "七子",
    "七怪",
    "夫妻",
    "夫妇",
    "兄弟",
    "姐妹",
    "父子",
    "父女",
    "母女",
    "师徒",
    "双",
    "两",
)

IDENTITY_HINTS = (
    "两人",
    "二人",
    "三人",
    "四人",
    "七人",
    "两个",
    "三个",
    "四个",
    "七个",
    "人物",
    "同时",
    "共享",
)

NAME_LIFE_NAME = re.compile(r"^[\u4e00-\u9fff·]{2,8}\d{3,5}[\u4e00-\u9fff·（）()]{2,}")


def load_rows() -> tuple[list[sqlite3.Row], dict[str, list[sqlite3.Row]]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cards = conn.execute(
            """
            SELECT *
            FROM cards
            WHERE category IN ('combat_characters', 'attached_characters')
            ORDER BY source_sheet, source_row
            """
        ).fetchall()
        abilities = conn.execute(
            """
            SELECT c.id AS card_id, c.title, c.source_sheet, c.source_row,
                   a.ordinal, a.kind, a.name, a.text, a.owner_units_json
            FROM card_abilities a
            JOIN cards c ON c.id = a.card_id
            ORDER BY c.source_sheet, c.source_row, a.ordinal
            """
        ).fetchall()
    finally:
        conn.close()

    by_card: dict[str, list[sqlite3.Row]] = {}
    for ability in abilities:
        by_card.setdefault(ability["card_id"], []).append(ability)
    return list(cards), by_card


def card_text(card: sqlite3.Row, abilities: list[sqlite3.Row]) -> str:
    parts = [
        card["title"] or "",
        card["life"] or "",
        card["identity"] or "",
        card["description"] or "",
        card["relationships"] or "",
    ]
    parts.extend(str(row["text"] or "") for row in abilities)
    return "\n".join(parts)


def owners(row: sqlite3.Row) -> list[str]:
    raw = row["owner_units_json"]
    if not raw:
        return []
    return json.loads(raw)


def detect_reasons(card: sqlite3.Row, abilities: list[sqlite3.Row]) -> list[str]:
    title = card["title"] or ""
    identity = card["identity"] or ""
    description = card["description"] or ""
    reasons: list[str] = []
    if any(hint in title for hint in TITLE_HINTS):
        reasons.append("标题疑似多人")
    if any(hint in identity for hint in IDENTITY_HINTS):
        reasons.append("身份栏疑似多人")
    if any(hint in description for hint in ("可同时", "同时出战", "任一位出战", "全部死亡", "均存活", "共享一个生命")):
        reasons.append("描述疑似多人机制")
    if card["life"] and len(re.findall(r"\d{3,5}", str(card["life"]))) >= 2:
        reasons.append("生命栏有多个数值")
    if card["life"] and re.search(r"\*\s*[2-9]", str(card["life"])):
        reasons.append("生命栏疑似多个单位")
    if any(NAME_LIFE_NAME.match(str(row["text"] or "")) for row in abilities):
        reasons.append("特技文本出现“人名+血量+特技名”格式")
    if any(owners(row) for row in abilities):
        reasons.append("已有所属人物字段")
    return reasons


def main() -> None:
    cards, abilities_by_card = load_rows()
    candidates = []
    for card in cards:
        abilities = abilities_by_card.get(card["id"], [])
        reasons = detect_reasons(card, abilities)
        if reasons:
            candidates.append((card, abilities, reasons))

    lines = [
        "# 多人一卡候选审计",
        "",
        "这份报告只用于识别哪些卡可能需要 `所属人物`。单人卡默认所属本人，不需要填写。",
        "",
        f"- 候选卡数：{len(candidates)}",
        "",
        "## 已有所属人物",
        "",
    ]

    owned = [(card, abilities, reasons) for card, abilities, reasons in candidates if any(owners(row) for row in abilities)]
    if not owned:
        lines.append("- 无")
    for card, abilities, reasons in owned:
        lines.extend(["", f"### {card['title']} / {card['source_sheet']}!{card['source_row']}", ""])
        lines.append(f"- 识别原因：{'、'.join(reasons)}")
        for row in abilities:
            unit_names = owners(row)
            if unit_names:
                lines.append(f"- `{row['kind']}` / `{row['name'] or '未命名'}`：所属人物 = {', '.join(unit_names)}")

    lines.extend(["", "## 需要作者裁定", ""])
    unresolved = [(card, abilities, reasons) for card, abilities, reasons in candidates if not any(owners(row) for row in abilities)]
    if not unresolved:
        lines.append("- 无")
    for index, (card, abilities, reasons) in enumerate(unresolved, start=1):
        lines.extend(
            [
                "",
                f"### M{index:03d} {card['title']} / {card['source_sheet']}!{card['source_row']}",
                "",
                f"- 识别原因：{'、'.join(reasons)}",
                f"- 生命：{card['life'] or '—'}",
                f"- 身份：{card['identity'] or '—'}",
                "- 当前特技：",
            ]
        )
        for row in abilities:
            text = re.sub(r"\s+", " ", str(row["text"] or "")).strip()
            if len(text) > 90:
                text = text[:90] + "..."
            lines.append(f"  - `{row['kind']}` / `{row['name'] or '未命名'}`：{text}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
