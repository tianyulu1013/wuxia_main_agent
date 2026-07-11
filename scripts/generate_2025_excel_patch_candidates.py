from __future__ import annotations

import difflib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_title_consistency import normalize_title, parse_aliases
from audit_update_log_against_excel import strip_heading_noise


ROOT = Path(__file__).resolve().parents[1]
RAW_CARDS = ROOT / "data" / "cards_raw" / "all_cards.jsonl"
LOG_JSON = ROOT / "data" / "update_logs" / "2025_update_log.json"
OUT_DIR = ROOT / "data" / "excel_patch_candidates"
JSON_OUT = OUT_DIR / "2025_full_pass_candidates.json"
JSONL_OUT = OUT_DIR / "2025_full_pass_candidates.jsonl"
REPORT = ROOT / "docs" / "2025-full-log-pass-report.md"

TEXT_FIELDS = [
    "identity",
    "description",
    "relationships",
    "weapons",
    "traits",
    "source_work",
    "author_group",
    "gender",
    "item_category",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def norm_text(text: str) -> str:
    text = text.replace("（", "(").replace("）", ")")
    text = text.replace("×", "*")
    return re.sub(r"\s+", "", text)


def meaningful(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 6:
        return False
    if re.fullmatch(r"[\d\s]+", stripped):
        return False
    return True


def load_cards() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    cards = load_jsonl(RAW_CARDS)
    by_exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_norm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        title = card.get("title")
        if isinstance(title, str) and title:
            by_exact[title].append(card)
            by_norm[normalize_title(title)].append(card)
    return cards, by_exact, by_norm


def match_card(
    title: str,
    by_exact: dict[str, list[dict[str, Any]]],
    by_norm: dict[str, list[dict[str, Any]]],
    aliases: dict[str, str],
    all_titles: list[str],
) -> tuple[str | None, list[dict[str, Any]]]:
    if title in by_exact:
        return "exact_title", by_exact[title]
    if title in aliases and aliases[title] in by_exact:
        return "confirmed_alias", by_exact[aliases[title]]
    norm = normalize_title(title)
    if norm in by_norm:
        return "normalized_title", by_norm[norm]
    close = difflib.get_close_matches(title, all_titles, n=5, cutoff=0.62)
    if close:
        return "fuzzy_candidates", [by_exact[name][0] for name in close]
    return None, []


def card_field_values(card: dict[str, Any]) -> dict[str, str]:
    fields = card.get("fields", {})
    values: dict[str, str] = {}
    for key in TEXT_FIELDS:
        value = fields.get(key)
        if value is not None:
            values[key] = str(value)
    life = fields.get("life")
    if life is not None:
        values["life"] = str(life)
    return values


def locate_text(card: dict[str, Any], needle: str) -> tuple[str | None, str | None]:
    if not needle:
        return None, None
    for field, value in card_field_values(card).items():
        if needle in value:
            return field, "exact"
    normalized_needle = norm_text(needle)
    if not normalized_needle:
        return None, None
    for field, value in card_field_values(card).items():
        if normalized_needle in norm_text(value):
            return field, "normalized"
    return None, None


def after_lines(entry: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for body in entry.get("body", []):
        text = body.get("after_text") or body.get("text") or ""
        for line in text.splitlines():
            if meaningful(line):
                result.append(line.strip())
    return result


def full_card_text(card: dict[str, Any]) -> str:
    return "\n".join(card_field_values(card).values())


def build_candidate(entry: dict[str, Any], match_method: str | None, cards: list[dict[str, Any]]) -> dict[str, Any]:
    title = strip_heading_noise(entry.get("title") or "")
    section = entry.get("section")
    base = {
        "date": entry.get("date"),
        "section": section,
        "log_title": entry.get("title"),
        "clean_title": title,
        "match_method": match_method,
        "status": None,
        "notes": [],
        "candidate_cards": [
            {
                "title": card.get("title"),
                "category": card.get("category"),
                "source": card.get("source"),
                "current_fields": card_field_values(card),
            }
            for card in cards
        ],
        "operations": [],
        "missing_after_lines": [],
        "log_markdown": "\n".join(
            item.get("markdown") or item.get("text") or "" for item in entry.get("body", [])
        ).strip(),
    }

    if section == "新作":
        base["status"] = "append_row_candidate"
        if cards and match_method not in {"fuzzy_candidates"}:
            base["notes"].append("日志标记为新作，但 Excel 中已有同名或同归一化标题；可能已经新增过。")
        elif cards:
            base["notes"].append("日志标记为新作；模糊候选只作参考，不应覆盖旧卡。")
        else:
            base["notes"].append("日志标记为新作，应作为新增行候选。")
        return base

    if not cards:
        base["status"] = "unmatched"
        base["notes"].append("日志标题暂未匹配到 Excel 记录。")
        return base

    if match_method == "fuzzy_candidates" or len(cards) > 1:
        base["status"] = "needs_review"
        base["notes"].append("只找到模糊候选或多个候选，需要作者确认对应卡。")
        return base

    card = cards[0]
    excel_norm = norm_text(full_card_text(card))
    operations: list[dict[str, Any]] = []
    missing: list[str] = []
    already_present = 0
    rich_paragraphs = 0

    for body in entry.get("body", []):
        before = (body.get("before_text") or body.get("text") or "").strip()
        after = (body.get("after_text") or body.get("text") or "").strip()
        if not meaningful(after):
            continue

        if norm_text(after) in excel_norm:
            already_present += 1
            continue

        if body.get("has_revision_marks"):
            rich_paragraphs += 1
            field, match_kind = locate_text(card, before)
            operations.append(
                {
                    "operation": "replace_text",
                    "field": field,
                    "match_kind": match_kind,
                    "before_text": before,
                    "after_text": after,
                    "safe_to_apply": bool(field and match_kind == "exact"),
                    "source": card.get("source"),
                }
            )
        else:
            missing.append(after)

    base["operations"] = operations
    base["missing_after_lines"] = missing

    if not operations and not missing:
        base["status"] = "already_synced"
        base["notes"].append(f"{already_present} 个更新后片段已在 Excel 中。")
    elif operations and all(op["safe_to_apply"] for op in operations) and not missing:
        base["status"] = "auto_replace_candidate"
        base["notes"].append("所有修订段落都能在 Excel 中精确定位旧片段。")
    else:
        base["status"] = "needs_review"
        if operations:
            unsafe = [op for op in operations if not op["safe_to_apply"]]
            if unsafe:
                base["notes"].append("部分修订段落无法在 Excel 中精确定位旧片段。")
        if missing:
            base["notes"].append("存在没有明确旧片段的更新后文本，需要人工决定替换位置或是否整段覆盖。")
        if rich_paragraphs == 0 and missing:
            base["notes"].append("日志条目没有加粗/删除线修订标记，不能自动生成安全替换。")

    return base


def write_report(candidates: list[dict[str, Any]]) -> None:
    status_counts = Counter(item["status"] for item in candidates)
    section_counts = Counter(item.get("section") or "未分类" for item in candidates)

    lines = [
        "# 2025 更新日志全量过表报告",
        "",
        "本报告全量处理 `2025更新日志.docx`，把每个日志条目与 Excel 导入结果对照，生成 Excel 更新候选。",
        "",
        "状态说明：",
        "",
        "- `already_synced`：更新后文本已能在 Excel 中找到。",
        "- `auto_replace_candidate`：带修订标记，旧片段能在 Excel 中精确定位，可作为自动替换候选，但仍需作者确认后执行。",
        "- `needs_review`：需要作者确认对应卡、替换位置或是否整段覆盖。",
        "- `append_row_candidate`：日志分类为新作，应新增一行；模糊候选只作避免误覆盖的参考。",
        "- `unmatched`：暂未匹配到 Excel 记录。",
        "",
        "## 总览",
        "",
        f"- 总候选条目：{len(candidates)}",
    ]
    for status, count in status_counts.most_common():
        lines.append(f"- `{status}`: {count}")

    lines.extend(["", "## 分类统计", ""])
    for section, count in section_counts.most_common():
        lines.append(f"- {section}: {count}")

    for status in ["auto_replace_candidate", "append_row_candidate", "needs_review", "unmatched"]:
        items = [item for item in candidates if item["status"] == status]
        lines.extend(["", f"## {status}", ""])
        if not items:
            lines.append("- 无")
            continue
        for item in items:
            date = item.get("date") or "未标日期"
            section = item.get("section") or "未分类"
            title = item.get("log_title") or "未命名"
            lines.extend(["", f"### {date} / {section} / {title}", ""])
            lines.append(f"- 匹配方式：`{item.get('match_method')}`")
            if item["candidate_cards"]:
                lines.append("- Excel 候选：")
                for card in item["candidate_cards"]:
                    source = card["source"]
                    lines.append(f"  - `{card['title']}` ({source['sheet']}!{source['row']}, `{card['category']}`)")
                    if status == "needs_review":
                        lines.append("    - Excel 当前字段：")
                        for field, value in card.get("current_fields", {}).items():
                            text = str(value).replace("\n", " / ")
                            if len(text) > 500:
                                text = text[:500] + "..."
                            lines.append(f"      - `{field}`: {text}")
            for note in item.get("notes", []):
                lines.append(f"- 备注：{note}")
            if item.get("operations"):
                lines.append("- 替换候选：")
                for op in item["operations"]:
                    lines.append(
                        f"  - field=`{op['field']}` match=`{op['match_kind']}` safe={op['safe_to_apply']}"
                    )
                    lines.append("    - 旧：`" + op["before_text"].replace("`", "\\`")[:180] + "`")
                    lines.append("    - 新：`" + op["after_text"].replace("`", "\\`")[:180] + "`")
            if item.get("missing_after_lines"):
                lines.append("- 需要放入 Excel 的更新后片段：")
                for line in item["missing_after_lines"][:8]:
                    lines.append(f"  - {line}")
                if len(item["missing_after_lines"]) > 8:
                    lines.append(f"  - ... 还有 {len(item['missing_after_lines']) - 8} 条")

    lines.extend(
        [
            "",
            "## 输出文件",
            "",
            f"- `{JSON_OUT.relative_to(ROOT)}`",
            f"- `{JSONL_OUT.relative_to(ROOT)}`",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards, by_exact, by_norm = load_cards()
    all_titles = [card["title"] for card in cards if isinstance(card.get("title"), str)]
    aliases = parse_aliases()
    log = json.loads(LOG_JSON.read_text(encoding="utf-8"))

    candidates: list[dict[str, Any]] = []
    for entry in log["entries"]:
        title = entry.get("title")
        if not title:
            continue
        clean = strip_heading_noise(title)
        method, matched_cards = match_card(clean, by_exact, by_norm, aliases, all_titles)
        candidates.append(build_candidate(entry, method, matched_cards))

    JSON_OUT.write_text(
        json.dumps(
            {
                "source_log": LOG_JSON.name,
                "source_cards": RAW_CARDS.name,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "candidates": candidates,
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    with JSONL_OUT.open("w", encoding="utf-8", newline="\n") as fh:
        for candidate in candidates:
            fh.write(json.dumps(candidate, ensure_ascii=False, default=str))
            fh.write("\n")

    write_report(candidates)
    print(str(JSON_OUT))
    print(str(REPORT))


if __name__ == "__main__":
    main()
