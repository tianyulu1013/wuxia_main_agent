from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from audit_title_consistency import normalize_title, parse_aliases
from audit_update_log_against_excel import strip_heading_noise


ROOT = Path(__file__).resolve().parents[1]
RAW_CARDS = ROOT / "data" / "cards_raw" / "all_cards.jsonl"
LOG_JSON = ROOT / "data" / "update_logs" / "2025_update_log.json"
REPORT = ROOT / "docs" / "excel-sync-gap-report-v0.1.md"


def normalize_text(text: str) -> str:
    text = text.replace("（", "(").replace("）", ")")
    text = re.sub(r"\s+", "", text)
    return text


def meaningful_line(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) < 8:
        return False
    if re.fullmatch(r"[\d\s]+", stripped):
        return False
    return True


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def card_text(card: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["title", "life", "identity", "description", "relationships", "weapons", "source_work", "author_group", "gender"]:
        value = card.get(key)
        if value is None:
            value = card.get("fields", {}).get(key)
        if value is not None:
            parts.append(str(value))
    return "\n".join(parts)


def main() -> None:
    cards = load_jsonl(RAW_CARDS)
    log = json.loads(LOG_JSON.read_text(encoding="utf-8"))
    aliases = parse_aliases()

    by_exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_norm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        title = card.get("title")
        if isinstance(title, str) and title:
            by_exact[title].append(card)
            by_norm[normalize_title(title)].append(card)

    gaps: list[dict[str, Any]] = []
    covered: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    for entry in log["entries"]:
        raw_title = entry.get("title")
        if not raw_title:
            continue
        title = strip_heading_noise(raw_title)

        candidates = by_exact.get(title)
        if not candidates and title in aliases:
            candidates = by_exact.get(aliases[title])
        if not candidates:
            candidates = by_norm.get(normalize_title(title))
        if not candidates:
            unresolved.append(entry)
            continue

        card = candidates[0]
        excel_norm = normalize_text(card_text(card))

        after_lines: list[str] = []
        markdown_lines: list[str] = []
        for item in entry.get("body", []):
            after = item.get("after_text") or item.get("text") or ""
            for line in after.splitlines():
                if meaningful_line(line):
                    after_lines.append(line.strip())
            markdown = item.get("markdown") or item.get("text") or ""
            if markdown.strip():
                markdown_lines.append(markdown.strip())

        missing = [
            line for line in after_lines
            if normalize_text(line) and normalize_text(line) not in excel_norm
        ]

        result = {
            "date": entry.get("date"),
            "section": entry.get("section"),
            "log_title": raw_title,
            "excel_title": card.get("title"),
            "excel_source": card.get("source"),
            "missing_after_lines": missing,
            "after_lines": after_lines,
            "log_markdown": "\n".join(markdown_lines),
        }
        if missing:
            gaps.append(result)
        else:
            covered.append(result)

    lines = [
        "# Excel 同步缺口报告 v0.1",
        "",
        "本报告用更新日志中的“更新后文本片段”对照 Excel 当前文本。",
        "",
        "判定方式很保守：删除线内容视为旧文并忽略，加粗内容保留；如果更新后片段不出现在 Excel 对应卡文本中，就列为同步缺口候选。",
        "",
        "这不是最终裁定，只是帮作者优先看到最可能漏同步的卡。",
        "",
        "## 总览",
        "",
        f"- 日志条目数：{len(log['entries'])}",
        f"- 可定位 Excel 条目：{len(gaps) + len(covered)}",
        f"- 存在疑似同步缺口：{len(gaps)}",
        f"- 更新片段已在 Excel 中覆盖：{len(covered)}",
        f"- 暂未定位 Excel：{len(unresolved)}",
        "",
        "## 疑似需要同步到 Excel 的条目",
        "",
    ]

    for item in gaps:
        source = item["excel_source"]
        lines.extend(
            [
                f"### {item['date'] or '未标日期'} / {item['section'] or '未分类'} / {item['log_title']}",
                "",
                f"- Excel 候选：`{item['excel_title']}` ({source['sheet']}!{source['row']})",
                "- Excel 中未找到的更新后片段：",
            ]
        )
        for line in item["missing_after_lines"][:20]:
            lines.append(f"  - {line}")
        if len(item["missing_after_lines"]) > 20:
            lines.append(f"  - ... 还有 {len(item['missing_after_lines']) - 20} 条")
        lines.extend(["", "日志原文：", "", "```text", item["log_markdown"], "```", ""])

    lines.extend(["", "## 暂未定位 Excel 的日志条目", ""])
    if unresolved:
        for entry in unresolved:
            lines.append(
                f"- {entry.get('date') or '未标日期'} / {entry.get('section') or '未分类'} / `{entry.get('title')}`"
            )
    else:
        lines.append("- 无")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))


if __name__ == "__main__":
    main()
