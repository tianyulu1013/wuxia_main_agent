from __future__ import annotations

import difflib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from audit_title_consistency import normalize_title, parse_aliases


ROOT = Path(__file__).resolve().parents[1]
RAW_CARDS = ROOT / "data" / "cards_raw" / "all_cards.jsonl"
LOG_JSON = ROOT / "data" / "update_logs" / "2025_update_log.json"
REPORT = ROOT / "docs" / "update-log-vs-excel-audit-v0.1.md"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def strip_heading_noise(title: str) -> str:
    title = title.strip()
    title = re.sub(r"\s+\d+(\s+\d+)*$", "", title)
    return title.strip()


def plain_body(entry: dict[str, Any]) -> str:
    return "\n".join(item["text"] for item in entry.get("body", []) if item.get("text")).strip()


def rich_body(entry: dict[str, Any]) -> str:
    return "\n".join(
        item.get("markdown") or item.get("text") or "" for item in entry.get("body", [])
    ).strip()


def main() -> None:
    cards = load_jsonl(RAW_CARDS)
    log = json.loads(LOG_JSON.read_text(encoding="utf-8"))
    aliases = parse_aliases()
    reverse_aliases = {value: key for key, value in aliases.items()}

    by_exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_norm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    titles: list[str] = []
    for card in cards:
        title = card.get("title")
        if isinstance(title, str) and title:
            by_exact[title].append(card)
            by_norm[normalize_title(title)].append(card)
            titles.append(title)

    results: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []

    for entry in log["entries"]:
        raw_title = entry.get("title")
        body = plain_body(entry)
        if not raw_title and not body:
            continue

        title = strip_heading_noise(raw_title or "")
        if not title:
            continue

        candidates: list[dict[str, Any]] = []
        method = None

        if title in by_exact:
            candidates = by_exact[title]
            method = "exact_title"
        elif title in aliases and aliases[title] in by_exact:
            candidates = by_exact[aliases[title]]
            method = "confirmed_alias"
        elif title in reverse_aliases and reverse_aliases[title] in by_exact:
            candidates = by_exact[reverse_aliases[title]]
            method = "confirmed_alias_reverse"
        elif normalize_title(title) in by_norm:
            candidates = by_norm[normalize_title(title)]
            method = "normalized_title"
        else:
            close = difflib.get_close_matches(title, titles, n=5, cutoff=0.58)
            if close:
                candidates = [by_exact[name][0] for name in close]
                method = "fuzzy_candidates"

        record = {
            "date": entry.get("date"),
            "section": entry.get("section"),
            "log_title": raw_title,
            "clean_title": title,
            "method": method,
            "body_markdown": rich_body(entry),
            "body_text": body,
            "candidate_cards": [
                {
                    "title": card.get("title"),
                    "category": card.get("category"),
                    "source": card.get("source"),
                    "description": card.get("fields", {}).get("description"),
                    "life": card.get("fields", {}).get("life"),
                    "identity": card.get("fields", {}).get("identity"),
                }
                for card in candidates
            ],
        }
        if method:
            results.append(record)
        else:
            unmatched.append(record)

    lines = [
        "# 更新日志 vs Excel 审计 v0.1",
        "",
        "本报告把 `2025更新日志.docx` 的结构化条目与 `已制作.xlsx` 导入结果进行匹配。",
        "",
        "目标不是自动改 Excel，而是找出哪些日志条目需要同步到 Excel，或需要作者确认对应卡。",
        "",
        "## 总览",
        "",
        f"- 日志条目数：{len(log['entries'])}",
        f"- 可匹配条目数：{len(results)}",
        f"- 未匹配条目数：{len(unmatched)}",
        "",
        "## 匹配方法统计",
        "",
    ]

    counts: dict[str, int] = defaultdict(int)
    for item in results:
        counts[item["method"]] += 1
    for method, count in sorted(counts.items()):
        lines.append(f"- `{method}`: {count}")

    lines.extend(["", "## 未匹配日志条目", ""])
    if unmatched:
        for item in unmatched:
            lines.append(
                f"- {item['date'] or '未标日期'} / {item['section'] or '未分类'} / `{item['log_title']}`"
            )
    else:
        lines.append("- 无")

    lines.extend(["", "## 需要同步检查的日志条目", ""])
    for item in results:
        title = item["log_title"]
        date = item["date"] or "未标日期"
        section = item["section"] or "未分类"
        lines.extend(["", f"### {date} / {section} / {title}", ""])
        lines.append(f"- 匹配方式：`{item['method']}`")
        if item["candidate_cards"]:
            lines.append("- Excel 候选：")
            for card in item["candidate_cards"]:
                source = card["source"]
                lines.append(
                    f"  - `{card['title']}` ({source['sheet']}!{source['row']}, `{card['category']}`)"
                )
        else:
            lines.append("- Excel 候选：无")
        if item["body_markdown"]:
            lines.extend(["", "日志正文：", "", "```text", item["body_markdown"], "```"])

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))


if __name__ == "__main__":
    main()
