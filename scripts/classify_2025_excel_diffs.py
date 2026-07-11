from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TIMELINE_JSON = ROOT / "data" / "excel_patch_candidates" / "2025_card_timeline_sync.json"
JSON_OUT = ROOT / "data" / "excel_patch_candidates" / "2025_diff_classification.json"
REPORT = ROOT / "docs" / "2025-diff-classification-report.md"


FORMAT_TOKENS = {"：", ":", "；", ";", "，", ",", "。", ".", " ", "\n", "\t"}
FORMAT_MARKERS = {"（身份）", "(身份)"}


def parse_date(value: str | None) -> tuple[int, int, int]:
    if not value:
        return (0, 0, 0)
    try:
        dt = datetime.strptime(value, "%Y/%m/%d")
        return (dt.year, dt.month, dt.day)
    except ValueError:
        return (0, 0, 0)


def is_format_text(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if stripped in FORMAT_MARKERS:
        return True
    return all(char in FORMAT_TOKENS for char in stripped)


def field_for_text(card: dict[str, Any], paragraph: str) -> str | None:
    fields = card.get("current_fields") or {}
    for name, value in fields.items():
        if value is not None and paragraph in str(value):
            return name
    return None


def classification_for(changes: list[dict[str, str]], superseded: bool) -> tuple[str, str]:
    if superseded:
        return "D_旧日志已被后续同段覆盖", "同一张卡同一段文本有更晚日志，旧段不应作为当前补丁。"

    changed_texts = [change.get("text", "") for change in changes]
    if changed_texts and all(is_format_text(text) for text in changed_texts):
        return "B_格式位置差异", "只涉及标点、空白或身份标记位置，先不自动改。"

    total_chars = sum(len(text.strip()) for text in changed_texts)
    semantic_replaces = [change for change in changes if change.get("kind") == "replace_in_excel" and not is_format_text(change.get("text", ""))]
    if len(changes) <= 2 and total_chars <= 24 and len(semantic_replaces) <= 1:
        return "A_可直接同步候选", "差异短且定位在同一段，可用日志段替换 Excel 当前段。"

    if len(changes) <= 3 and total_chars <= 36 and not any(len(text.strip()) > 22 for text in changed_texts):
        return "A_可直接同步候选", "差异较短且定位清楚，可用日志段替换 Excel 当前段。"

    return "C_需要规则裁定", "差异较多或语义跨度较大，需要确认日志是否代表最终文本。"


def main() -> None:
    data = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
    timelines = data["timelines"]

    latest_by_title_and_paragraph: dict[tuple[str, str], tuple[int, int, int]] = {}
    for item in timelines:
        title = item.get("title") or ""
        for fragment in item.get("near_match_fragments") or []:
            closest = fragment.get("closest_excel_text") or ""
            if not closest:
                continue
            key = (title, closest)
            date_key = parse_date(fragment.get("date"))
            if date_key > latest_by_title_and_paragraph.get(key, (0, 0, 0)):
                latest_by_title_and_paragraph[key] = date_key

    records: list[dict[str, Any]] = []
    for item in timelines:
        title = item.get("title") or ""
        card = (item.get("candidate_cards") or [{}])[0]
        source = card.get("source") or {}
        for fragment in item.get("near_match_fragments") or []:
            changes = fragment.get("diff_summary") or []
            if not changes:
                continue
            closest = fragment.get("closest_excel_text") or ""
            date_key = parse_date(fragment.get("date"))
            superseded = latest_by_title_and_paragraph.get((title, closest), date_key) > date_key
            category, reason = classification_for(changes, superseded)
            field_name = field_for_text(card, closest) if closest else None
            records.append(
                {
                    "title": title,
                    "date": fragment.get("date"),
                    "log_title": fragment.get("log_title"),
                    "category": category,
                    "reason": reason,
                    "similarity": fragment.get("excel_similarity"),
                    "sheet": source.get("sheet"),
                    "row": source.get("row"),
                    "field": field_name,
                    "changes": changes,
                    "excel_text": closest,
                    "log_text": fragment.get("fragment") or "",
                    "patch": {
                        "old_text": closest,
                        "new_text": fragment.get("fragment") or "",
                    }
                    if category == "A_可直接同步候选" and field_name
                    else None,
                }
            )

    duplicate_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["category"] != "A_可直接同步候选" or not record.get("patch"):
            continue
        key = (
            record.get("title"),
            record.get("date"),
            record.get("sheet"),
            record.get("row"),
            record.get("field"),
            record["patch"]["old_text"],
        )
        duplicate_groups[key].append(record)

    for duplicates in duplicate_groups.values():
        if len(duplicates) <= 1:
            continue
        keep = max(duplicates, key=lambda record: len(record["patch"]["new_text"]))
        for record in duplicates:
            if record is keep:
                continue
            record["category"] = "D_重复候选已合并"
            record["reason"] = "同一日期、同一单元格、同一旧段产生多个候选；已保留信息更完整的一条。"
            record["patch"] = None

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["category"]].append(record)

    JSON_OUT.write_text(json.dumps({"records": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    order = ["A_可直接同步候选", "B_格式位置差异", "C_需要规则裁定", "D_旧日志已被后续同段覆盖", "D_重复候选已合并"]
    lines = [
        "# 2025 差异分级报告",
        "",
        "这个报告把机器已读出的近似差异分成可直接同步、格式位置差异、需要规则裁定、旧日志覆盖四类。",
        "",
        "A 类仍然只是候选补丁；下一步会写入 Excel 副本，不覆盖原始 `已制作.xlsx`。",
        "",
        "## 总览",
        "",
    ]
    for category in order:
        lines.append(f"- {category}: {len(grouped.get(category, []))}")

    for category in order:
        lines.extend(["", f"## {category}", ""])
        records_in_category = grouped.get(category, [])
        if not records_in_category:
            lines.append("- 无")
            continue
        for record in records_in_category:
            loc = f"{record.get('sheet')}!{record.get('row')}"
            field = record.get("field") or "未定位字段"
            lines.extend(
                [
                    f"### {record['title']}",
                    "",
                    f"- 日志：{record.get('date') or '未标日期'} / {record.get('log_title') or ''} / 相似度 {record.get('similarity')}",
                    f"- Excel：{loc} / 字段 `{field}`",
                    f"- 判断：{record['reason']}",
                    "- 具体差异：",
                ]
            )
            for change in record["changes"]:
                lines.append(f"  - {change['summary']}")
                if change.get("context"):
                    lines.append(f"    - Excel 位置：`{change['context']}`")
            if category in {"A_可直接同步候选", "C_需要规则裁定"}:
                lines.extend(
                    [
                        "",
                        "Excel 当前段：",
                        "",
                        "```text",
                        record["excel_text"],
                        "```",
                        "",
                        "日志要求段：",
                        "",
                        "```text",
                        record["log_text"],
                        "```",
                    ]
                )
            lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))
    print(str(JSON_OUT))


if __name__ == "__main__":
    main()
