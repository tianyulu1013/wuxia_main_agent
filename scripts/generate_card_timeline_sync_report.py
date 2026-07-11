from __future__ import annotations

import difflib
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from audit_excel_sync_gaps import normalize_text


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_JSON = ROOT / "data" / "excel_patch_candidates" / "2025_full_pass_candidates.json"
REPORT = ROOT / "docs" / "2025-card-timeline-sync-report.md"
JSON_OUT = ROOT / "data" / "excel_patch_candidates" / "2025_card_timeline_sync.json"


def parse_date(value: str | None) -> tuple[int, int, int]:
    if not value:
        return (0, 0, 0)
    try:
        dt = datetime.strptime(value, "%Y/%m/%d")
        return (dt.year, dt.month, dt.day)
    except ValueError:
        return (0, 0, 0)


def meaningful(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 6:
        return False
    if re.fullmatch(r"[\d\s]+", stripped):
        return False
    return True


def card_key(candidate: dict[str, Any]) -> str:
    if candidate["status"] == "append_row_candidate":
        return f"new::{candidate.get('clean_title') or candidate.get('log_title')}"
    cards = candidate.get("candidate_cards") or []
    if cards:
        card = cards[0]
        source = card.get("source") or {}
        return f"{source.get('sheet')}!{source.get('row')}::{card.get('title')}"
    return f"unmatched::{candidate.get('clean_title') or candidate.get('log_title')}"


def excel_text(candidate: dict[str, Any]) -> str:
    cards = candidate.get("candidate_cards") or []
    if not cards:
        return ""
    fields = cards[0].get("current_fields") or {}
    return "\n".join(str(value) for value in fields.values() if value is not None)


def closest_excel_paragraph(fragment: str, excel_now: str) -> tuple[float, str]:
    fragment_norm = normalize_text(fragment)
    if not fragment_norm:
        return 0.0, ""

    paragraphs = [part for part in re.split(r"\n+", excel_now) if part.strip()]
    best = 0.0
    best_paragraph = ""
    for paragraph in paragraphs:
        paragraph_norm = normalize_text(paragraph)
        if not paragraph_norm:
            continue
        if fragment_norm in paragraph_norm:
            return 1.0, paragraph
        score = difflib.SequenceMatcher(None, fragment_norm, paragraph_norm).ratio()
        if score > best:
            best = score
            best_paragraph = paragraph
    return best, best_paragraph


def compact_text(text: str, limit: int = 28) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def local_context(text: str, start: int, end: int, radius: int = 12) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    prefix = "..." if left > 0 else ""
    suffix = "..." if right < len(text) else ""
    return prefix + text[left:right] + suffix


def diff_summary(expected: str, actual: str) -> list[dict[str, str]]:
    """Describe what Excel must change to match the log fragment."""
    if not expected or not actual:
        return []

    matcher = difflib.SequenceMatcher(None, actual, expected)
    changes: list[dict[str, str]] = []
    for tag, actual_start, actual_end, expected_start, expected_end in matcher.get_opcodes():
        if tag == "equal":
            continue

        actual_part = actual[actual_start:actual_end]
        expected_part = expected[expected_start:expected_end]
        context_start = min(actual_start, actual_end)
        context_end = max(actual_start, actual_end)
        context = local_context(actual, context_start, context_end)

        if tag == "delete":
            changes.append(
                {
                    "kind": "delete_from_excel",
                    "text": actual_part,
                    "summary": f"Excel 多出“{compact_text(actual_part)}”，应删除。",
                    "context": context,
                }
            )
        elif tag == "insert":
            insert_at = actual_start
            context = local_context(actual, insert_at, insert_at)
            changes.append(
                {
                    "kind": "insert_into_excel",
                    "text": expected_part,
                    "summary": f"Excel 缺少“{compact_text(expected_part)}”，应加入。",
                    "context": context,
                }
            )
        elif tag == "replace":
            changes.append(
                {
                    "kind": "replace_in_excel",
                    "text": expected_part,
                    "summary": f"Excel 写作“{compact_text(actual_part)}”，日志要求“{compact_text(expected_part)}”。",
                    "context": context,
                }
            )
    return changes


def expected_fragments(candidate: dict[str, Any]) -> list[str]:
    fragments: list[str] = []
    for op in candidate.get("operations") or []:
        after = op.get("after_text")
        if after and meaningful(after):
            fragments.append(after)
    for line in candidate.get("missing_after_lines") or []:
        if line and meaningful(line):
            fragments.append(line)
    return fragments


def main() -> None:
    data = json.loads(CANDIDATES_JSON.read_text(encoding="utf-8"))
    candidates = data["candidates"]

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        grouped[card_key(candidate)].append(candidate)

    timelines: list[dict[str, Any]] = []
    for key, items in grouped.items():
        items.sort(key=lambda item: parse_date(item.get("date")))
        display_title = items[-1].get("clean_title") or items[-1].get("log_title")
        cards = items[-1].get("candidate_cards") or []
        excel_now = excel_text(items[-1])
        excel_norm = normalize_text(excel_now)

        missing_fragments: list[dict[str, Any]] = []
        near_match_fragments: list[dict[str, Any]] = []
        present_fragments: list[dict[str, Any]] = []

        for item in items:
            for fragment in expected_fragments(item):
                similarity, closest = closest_excel_paragraph(fragment, excel_now)
                fragment_record = {
                    "date": item.get("date"),
                    "section": item.get("section"),
                    "log_title": item.get("log_title"),
                    "fragment": fragment,
                    "source_status": item.get("status"),
                    "excel_similarity": round(similarity, 4),
                    "closest_excel_text": closest,
                    "diff_summary": diff_summary(fragment, closest),
                }
                if normalize_text(fragment) in excel_norm:
                    present_fragments.append(fragment_record)
                elif similarity >= 0.90:
                    near_match_fragments.append(fragment_record)
                else:
                    missing_fragments.append(fragment_record)

        if key.startswith("new::"):
            timeline_status = "append_row_candidate"
        elif key.startswith("unmatched::"):
            timeline_status = "unmatched"
        elif missing_fragments or near_match_fragments:
            timeline_status = "timeline_missing_fragments"
        else:
            timeline_status = "timeline_covered"

        timelines.append(
            {
                "key": key,
                "title": display_title,
                "status": timeline_status,
                "entries": [
                    {
                        "date": item.get("date"),
                        "section": item.get("section"),
                        "log_title": item.get("log_title"),
                        "candidate_status": item.get("status"),
                        "notes": item.get("notes", []),
                    }
                    for item in items
                ],
                "candidate_cards": cards,
                "missing_fragments": missing_fragments,
                "near_match_fragments": near_match_fragments,
                "present_fragments_count": len(present_fragments),
                "excel_current_text": excel_now,
            }
        )

    timelines.sort(key=lambda item: (item["status"], item["title"] or ""))
    JSON_OUT.write_text(json.dumps({"timelines": timelines}, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = defaultdict(int)
    for item in timelines:
        counts[item["status"]] += 1

    lines = [
        "# 2025 按卡时间线同步报告",
        "",
        "本报告按卡聚合 2025 更新日志，按时间顺序检查每张卡的累计改动是否已经体现在 Excel 当前文本中。",
        "",
        "它解决的问题是：旧日志修改技能 A，后续日志修改技能 B；即使 B 已同步，也仍能看到 A 是否漏同步。",
        "",
        "注意：相似但不完全相同的片段仍算缺失，并会显示“日志要求”和“Excel 最接近文本”。例如日志删除了“立即”，Excel 仍保留“立即”，就是需要改。",
        "",
        "阅读方式：优先看“具体差异”。这里会直接写出 Excel 多了什么、少了什么、哪里写法不同；后面的两段原文只是校验材料。",
        "",
        "## 总览",
        "",
        f"- 涉及卡/新作/未匹配主题数：{len(timelines)}",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"- `{status}`: {count}")

    for status in ["timeline_missing_fragments", "append_row_candidate", "unmatched"]:
        selected = [item for item in timelines if item["status"] == status]
        lines.extend(["", f"## {status}", ""])
        if not selected:
            lines.append("- 无")
            continue
        for item in selected:
            lines.extend(["", f"### {item['title']}", ""])
            if item.get("candidate_cards"):
                lines.append("- Excel 候选：")
                for card in item["candidate_cards"]:
                    source = card.get("source") or {}
                    lines.append(f"  - `{card.get('title')}` ({source.get('sheet')}!{source.get('row')}, `{card.get('category')}`)")
            lines.append("- 时间线：")
            for entry in item["entries"]:
                lines.append(
                    f"  - {entry.get('date') or '未标日期'} / {entry.get('section') or '未分类'} / "
                    f"{entry.get('log_title')} / `{entry.get('candidate_status')}`"
                )
            if item["missing_fragments"]:
                lines.extend(["", "Excel 当前文本中尚未找到的累计更新片段：", ""])
                for fragment in item["missing_fragments"]:
                    lines.append(
                        f"- {fragment.get('date') or '未标日期'} / {fragment.get('log_title')} "
                        f"(相似度 {fragment.get('excel_similarity')}): {fragment['fragment']}"
                    )
            if item.get("near_match_fragments"):
                lines.extend(["", "相似但有差异，不能视为已同步：", ""])
                for fragment in item["near_match_fragments"]:
                    lines.append(
                        f"- {fragment.get('date') or '未标日期'} / {fragment.get('log_title')} "
                        f"(相似度 {fragment.get('excel_similarity')})"
                    )
                    if fragment.get("diff_summary"):
                        lines.append("  - 具体差异：")
                        for change in fragment["diff_summary"]:
                            lines.append(f"    - {change['summary']}")
                            if change.get("context"):
                                lines.append(f"      - Excel 位置：`{change['context']}`")
                    lines.extend(["", "日志要求：", "", "```text", fragment["fragment"], "```"])
                    lines.extend(["", "Excel 最接近文本：", "", "```text", fragment.get("closest_excel_text") or "", "```"])
            if status == "timeline_missing_fragments":
                lines.extend(["", "Excel 当前文本：", "", "```text", item["excel_current_text"], "```"])

    lines.extend(["", "## 输出文件", "", f"- `{JSON_OUT.relative_to(ROOT)}`", ""])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))
    print(str(JSON_OUT))


if __name__ == "__main__":
    main()
