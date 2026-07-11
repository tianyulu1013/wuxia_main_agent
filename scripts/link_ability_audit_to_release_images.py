from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cards.sqlite"
CROPS = ROOT / "data" / "release_images" / "card_crops.jsonl"
REPORT = ROOT / "docs" / "ability-image-review.md"


def load_crops() -> dict[str, dict]:
    by_title: dict[str, dict] = {}
    if not CROPS.exists():
        return by_title
    with CROPS.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            by_title[row["title"]] = row
    return by_title


def crop_lookup_key(item: dict) -> str:
    if item.get("title") == "辟邪剑谱":
        return "辟邪剑法"
    if item.get("title") == "郭襄":
        if item.get("source_work") == "倚天屠龙记":
            return "郭襄（峨眉祖师）"
        if item.get("source_work") == "神雕侠侣":
            return "郭襄（小）"
    return item["title"]


def load_review_items() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT
              c.title,
              c.category,
              c.source_sheet,
              c.source_row,
              c.source_work,
              a.ordinal,
              a.kind,
              a.name,
              a.text,
              a.review_flags_json
            FROM card_abilities a
            JOIN cards c ON c.id = a.card_id
            WHERE
              a.review_flags_json LIKE '%inherited_named_ability%'
              OR a.review_flags_json LIKE '%missing_indent_for_inherited%'
              OR a.review_flags_json LIKE '%indented_implicit_word%'
            ORDER BY c.source_sheet, c.source_row, a.ordinal
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def compact(text: str, limit: int = 150) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else f"{text[:limit]}..."


def render_items(title: str, items: list[dict], crops: dict[str, dict], limit: int | None = None) -> tuple[list[str], int]:
    lines = ["", f"## {title}", "", f"- 数量：{len(items)}", ""]
    missing = 0
    shown = items if limit is None else items[:limit]
    for item in shown:
        crop = crops.get(crop_lookup_key(item))
        flags = ", ".join(json.loads(item["review_flags_json"]))
        lines.extend(
            [
                f"### {item['title']} / {item['source_sheet']}!{item['source_row']} / {item['name']}",
                "",
                f"- 当前判断：`{item['kind']}`",
                f"- 标记：`{flags}`",
                f"- 原文：{compact(item['text'])}",
            ]
        )
        if crop:
            crop_path = ROOT / crop["crop_path"]
            source_path = ROOT / crop["source_image"]
            lines.append(f"- 牌面图：[{Path(crop['crop_path']).name}]({crop_path.as_posix()})")
            lines.append(
                f"- Release：`{crop['source_version']}` / `{crop['release_deck']}` slot {crop['slot']} "
                f"(row {crop['row']}, col {crop['column']})；[整张牌堆图]({source_path.as_posix()})"
            )
        else:
            missing += 1
            lines.append("- 牌面图：未找到，可能是废弃卡或名称不一致")
        lines.append("")
    if limit is not None and len(items) > limit:
        lines.append(f"- 仅显示前 {limit} 条。")
    return lines, missing


def main() -> None:
    crops = load_crops()
    items = load_review_items()
    parsed_items = [(item, json.loads(item["review_flags_json"])) for item in items]
    missing_indent_items = [item for item, flags in parsed_items if "missing_indent_for_inherited" in flags]
    indented_word_items = [item for item, flags in parsed_items if "indented_implicit_word" in flags]
    inherited_items = [item for item, flags in parsed_items if "inherited_named_ability" in flags]

    lines = [
        "# 特技继承图像复核清单",
        "",
        "本报告把 `card_abilities` 中的结构可疑项连接到 release 单卡切图。",
        "用于查看牌面是否有空行、是否仍属于上一组类型，以及是否存在缩进漏写。",
        "",
        f"- 待复核继承特技：{len(inherited_items)}",
        f"- 继承但文本无缩进：{len(missing_indent_items)}",
        f"- 有缩进但按字处理：{len(indented_word_items)}",
        f"- 单卡切图索引：`{CROPS.relative_to(ROOT)}`",
        "",
    ]

    missing = 0
    section, section_missing = render_items("继承但文本无缩进", missing_indent_items, crops)
    lines.extend(section)
    missing += section_missing
    section, section_missing = render_items("有缩进但按字处理", indented_word_items, crops)
    lines.extend(section)
    missing += section_missing
    section, section_missing = render_items("全部继承特技", inherited_items, crops, limit=120)
    lines.extend(section)
    missing += section_missing

    lines.extend(["## 未找到切图数量", "", f"- {missing}", ""])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
