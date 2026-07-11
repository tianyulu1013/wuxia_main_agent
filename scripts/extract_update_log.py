from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import docx


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "2025更新日志.docx"
OUT_DIR = ROOT / "data" / "update_logs"
JSON_OUT = OUT_DIR / "2025_update_log.json"
MD_OUT = ROOT / "docs" / "2025-update-log-extract.md"


DATE_RE = re.compile(r"^\d{4}/\d{1,2}/\d{1,2}$")


def run_text(run: docx.text.run.Run) -> str:
    text = run.text.replace("\r\n", "\n").replace("\r", "\n")
    if not text:
        return ""
    if run.font.strike:
        text = f"~~{text}~~"
    if run.bold:
        text = f"**{text}**"
    if run.italic:
        text = f"*{text}*"
    return text


def paragraph_markdown(paragraph: docx.text.paragraph.Paragraph) -> str:
    return "".join(run_text(run) for run in paragraph.runs).strip()


def paragraph_after_text(paragraph: docx.text.paragraph.Paragraph) -> str:
    parts: list[str] = []
    for run in paragraph.runs:
        if run.font.strike:
            continue
        parts.append(run.text)
    return "".join(parts).replace("\r\n", "\n").replace("\r", "\n").strip()


def paragraph_before_text(paragraph: docx.text.paragraph.Paragraph) -> str:
    parts: list[str] = []
    for run in paragraph.runs:
        if run.bold:
            continue
        parts.append(run.text)
    return "".join(parts).replace("\r\n", "\n").replace("\r", "\n").strip()


def has_revision_marks(paragraph: docx.text.paragraph.Paragraph) -> bool:
    return any(bool(run.bold) or bool(run.font.strike) for run in paragraph.runs)


def heading_level(style_name: str) -> int | None:
    match = re.match(r"Heading\s+(\d+)", style_name)
    if not match:
        return None
    return int(match.group(1))


def classify_heading(text: str, level: int | None) -> str:
    if DATE_RE.match(text):
        return "date"
    if level == 2:
        return "section"
    if level and level >= 3:
        return "card_or_item"
    return "other_heading"


def extract() -> dict[str, Any]:
    document = docx.Document(SOURCE)
    entries: list[dict[str, Any]] = []
    current_date: str | None = None
    current_section: str | None = None
    current_entry: dict[str, Any] | None = None

    paragraph_records: list[dict[str, Any]] = []

    for index, paragraph in enumerate(document.paragraphs, start=1):
        text = paragraph.text.strip()
        markdown = paragraph_markdown(paragraph)
        if not text and not markdown:
            continue

        level = heading_level(paragraph.style.name)
        kind = classify_heading(text, level)
        runs = [
            {
                "text": run.text,
                "bold": bool(run.bold),
                "strike": bool(run.font.strike),
                "italic": bool(run.italic),
            }
            for run in paragraph.runs
            if run.text
        ]
        paragraph_records.append(
            {
                "paragraph": index,
                "style": paragraph.style.name,
                "heading_level": level,
                "kind": kind,
                "text": text,
                "markdown": markdown,
                "before_text": paragraph_before_text(paragraph),
                "after_text": paragraph_after_text(paragraph),
                "has_revision_marks": has_revision_marks(paragraph),
                "runs": runs,
            }
        )

        if kind == "date":
            current_date = text
            current_section = None
            current_entry = None
            continue

        if kind == "section":
            current_section = text
            current_entry = None
            continue

        if kind == "card_or_item":
            current_entry = {
                "date": current_date,
                "section": current_section,
                "title": text,
                "heading_paragraph": index,
                "style": paragraph.style.name,
                "body": [],
            }
            entries.append(current_entry)
            continue

        if current_entry is None:
            current_entry = {
                "date": current_date,
                "section": current_section,
                "title": None,
                "heading_paragraph": None,
                "style": None,
                "body": [],
            }
            entries.append(current_entry)

        current_entry["body"].append(
            {
                "paragraph": index,
                "text": text,
                "markdown": markdown,
                "before_text": paragraph_before_text(paragraph),
                "after_text": paragraph_after_text(paragraph),
                "has_revision_marks": has_revision_marks(paragraph),
                "runs": runs,
            }
        )

    return {
        "source": SOURCE.name,
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
        "paragraphs": paragraph_records,
    }


def write_markdown(data: dict[str, Any]) -> None:
    lines = [
        "# 2025 更新日志结构化抽取",
        "",
        f"- 来源：`{SOURCE.name}`",
        f"- 条目数：{len(data['entries'])}",
        "",
    ]

    current_date = object()
    current_section = object()
    for entry in data["entries"]:
        if entry["date"] != current_date:
            current_date = entry["date"]
            lines.extend(["", f"## {current_date or '未标日期'}", ""])
            current_section = object()

        if entry["section"] != current_section:
            current_section = entry["section"]
            lines.extend(["", f"### {current_section or '未分类'}", ""])

        title = entry["title"] or "未命名条目"
        lines.extend(["", f"#### {title}", ""])
        if not entry["body"]:
            lines.append("_无正文_")
        for item in entry["body"]:
            lines.append(item["markdown"] or item["text"])

    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = extract()
    JSON_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(data)
    print(str(JSON_OUT))
    print(str(MD_OUT))


if __name__ == "__main__":
    main()
