from __future__ import annotations

import json
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"
CROPS = ROOT / "data" / "release_images" / "card_crops.jsonl"
REPORT = ROOT / "docs" / "ability-layout-risk-report.md"
ADJUDICATIONS = ROOT / "docs" / "ability-layout-adjudications.json"


ACTION_FLAGS = [
    "typed_name_without_colon",
    "typed_line_without_name",
    "nested_named_line_without_indent",
    "missing_indent_for_inherited",
]


def load_crops() -> dict[str, dict[str, Any]]:
    crops: dict[str, dict[str, Any]] = {}
    if not CROPS.exists():
        return crops
    with CROPS.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            crops[row["title"]] = row
    return crops


def load_adjudications() -> dict[str, dict[str, Any]]:
    if not ADJUDICATIONS.exists():
        return {}
    return json.loads(ADJUDICATIONS.read_text(encoding="utf-8"))


def crop_lookup_key(item: dict[str, Any]) -> str:
    if item.get("title") == "辟邪剑谱":
        return "辟邪剑法"
    if item.get("title") == "郭襄":
        if item.get("source_work") == "倚天屠龙记":
            return "郭襄（峨眉祖师）"
        if item.get("source_work") == "神雕侠侣":
            return "郭襄（小）"
    return item["title"]


def load_abilities() -> list[dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT
              c.id AS card_id,
              c.title,
              c.category,
              c.source_sheet,
              c.source_row,
              c.source_work,
              c.author_group,
              a.ordinal,
              a.kind,
              a.name,
              a.raw_name,
              a.type_prefix,
              a.start_line,
              a.end_line,
              a.text,
              a.review_flags_json
            FROM card_abilities a
            JOIN cards c ON c.id = a.card_id
            ORDER BY c.source_sheet, c.source_row, a.ordinal
            """
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["review_flags"] = json.loads(item.pop("review_flags_json"))
            result.append(item)
        return result
    finally:
        conn.close()


def compact(text: Any, limit: int = 180) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    return value if len(value) <= limit else f"{value[:limit]}..."


def has_flag(item: dict[str, Any], flag: str) -> bool:
    return flag in item.get("review_flags", [])


def action_labels(item: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    if has_flag(item, "typed_name_without_colon") or has_flag(item, "typed_line_without_name"):
        labels.append("补冒号/修特技名")
    if has_flag(item, "nested_named_line_without_indent"):
        labels.append("子项补缩进")
    elif has_flag(item, "missing_indent_for_inherited"):
        labels.append("独立特技补缩进")
    return labels


def is_actionable(item: dict[str, Any]) -> bool:
    if has_flag(item, "known_unnamed_ability"):
        return False
    return bool(action_labels(item))


def ability_key(item: dict[str, Any]) -> str:
    return f"{item['card_id']}::{int(item['ordinal']):03d}"


def apply_action_codes(items: list[dict[str, Any]], adjudications: dict[str, dict[str, Any]]) -> None:
    for index, item in enumerate(items, start=1):
        key = ability_key(item)
        item["action_code"] = adjudications.get(key, {}).get("code") or f"A{index:03d}"
        item["adjudication"] = adjudications.get(key)


def should_show_action(item: dict[str, Any]) -> bool:
    adjudication = item.get("adjudication") or {}
    return adjudication.get("decision") != "false_positive"


def crop_lines(item: dict[str, Any], crops: dict[str, dict[str, Any]]) -> list[str]:
    crop = crops.get(crop_lookup_key(item))
    if not crop:
        return ["- 牌面图：未找到，可能是废弃卡或名称不一致"]
    crop_path = ROOT / crop["crop_path"]
    source_path = ROOT / crop["source_image"]
    return [
        f"- 牌面图：[{Path(crop['crop_path']).name}]({crop_path.as_posix()})",
        (
            f"- Release：`{crop['source_version']}` / `{crop['release_deck']}` "
            f"slot {crop['slot']} (row {crop['row']}, col {crop['column']})；"
            f"[整张牌堆图]({source_path.as_posix()})"
        ),
    ]


def group_key(item: dict[str, Any]) -> tuple[str, int, str]:
    return (item["source_sheet"], int(item["source_row"]), item["title"])


def render_action_groups(items: list[dict[str, Any]], crops: dict[str, dict[str, Any]]) -> list[str]:
    groups: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(group_key(item), []).append(item)

    lines = ["", "## 待修改清单", "", f"- 卡牌数：{len(groups)}", f"- 条目数：{len(items)}"]
    item_index = 1
    sorted_groups = sorted(groups.items(), key=lambda pair: (pair[0][0], pair[0][1], pair[0][2]))
    for group_index, (_, group_items) in enumerate(sorted_groups, start=1):
        first = group_items[0]
        card_code = f"C{group_index:03d}"
        lines.extend(
            [
                "",
                f"### {card_code} {first['title']} / {first['source_sheet']}!{first['source_row']}",
                "",
            ]
        )
        if first.get("source_work"):
            lines.append(f"- 出处：{first['source_work']}")
        lines.extend(crop_lines(first, crops))
        for item in group_items:
            item_code = item.get("action_code") or f"A{item_index:03d}"
            item_index += 1
            flags = ", ".join(item.get("review_flags", [])) or "无"
            labels = "、".join(action_labels(item))
            name = item.get("name") or "未识别名称"
            adjudication = item.get("adjudication") or {}
            lines.extend(
                [
                    f"- `{item_code}` `{labels}`：`{item['kind']}` / {name}",
                    f"  - 标记：`{flags}`",
                    f"  - 原文：{compact(item.get('text'), 220)}",
                ]
            )
            if adjudication.get("decision") == "confirmed":
                lines.append(f"  - 裁定：{adjudication.get('note', '作者已确认需要修改。')}")
    return lines


def render_items(
    title: str,
    items: list[dict[str, Any]],
    crops: dict[str, dict[str, Any]],
    *,
    limit: int | None = None,
    note: str = "",
) -> list[str]:
    lines = ["", f"## {title}", "", f"- 数量：{len(items)}"]
    if note:
        lines.extend(["", note])
    shown = items if limit is None else items[:limit]
    for item in shown:
        flags = ", ".join(item.get("review_flags", [])) or "无"
        lines.extend(
            [
                "",
                f"### {item['title']} / {item['source_sheet']}!{item['source_row']} / {item.get('name') or '未识别名称'}",
                "",
                f"- 当前判断：`{item['kind']}`",
                f"- 标记：`{flags}`",
                f"- 原文：{compact(item.get('text'))}",
            ]
        )
        lines.extend(crop_lines(item, crops))
    if limit is not None and len(items) > limit:
        lines.extend(["", f"- 仅显示前 {limit} 条；完整数据见 `data/cards_current/abilities.jsonl`。"])
    return lines


def main() -> None:
    crops = load_crops()
    adjudications = load_adjudications()
    abilities = load_abilities()
    flag_counts = Counter(flag for item in abilities for flag in item.get("review_flags", []))

    action_candidates = [item for item in abilities if is_actionable(item)]
    apply_action_codes(action_candidates, adjudications)
    action_items = [item for item in action_candidates if should_show_action(item)]
    action_flag_counts = Counter(flag for item in action_items for flag in item.get("review_flags", []))
    action_cards = {group_key(item) for item in action_items}

    lines = [
        "# 特技卡面排版待整理清单",
        "",
        "这个报告只列 PSD / release 牌面排版待整理项目。数据库和 Excel 的结构正确性不以此报告为准。",
        "",
        "## 总览",
        "",
        f"- 特技/说明块总数：{len(abilities)}",
        f"- 已按作者裁定隐藏误报：{len(action_candidates) - len(action_items)}",
        f"- 待修改卡牌数：{len(action_cards)}",
        f"- 待修改条目数：{len(action_items)}",
        "",
        "## 待修改标记统计",
        "",
    ]
    for flag, count in action_flag_counts.most_common():
        lines.append(f"- `{flag}`: {count}")
    if not action_flag_counts:
        lines.append("- 无")

    lines.extend(render_action_groups(action_items, crops))

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
