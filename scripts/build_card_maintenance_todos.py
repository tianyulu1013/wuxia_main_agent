from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT_PATH = ROOT / "data" / "review" / "card_maintenance_todos.json"


def clean_markdown_text(value: str) -> str:
    text = value.strip()
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = text.replace("`", "")
    return text.strip()


def add_todo(todos: dict[str, list[dict[str, object]]], title: str, item: dict[str, object]) -> None:
    title = title.strip()
    if not title:
        return
    todos.setdefault(title, []).append(item)


def parse_face_todos(todos: dict[str, list[dict[str, object]]]) -> int:
    path = REPORTS / "1-card-face-todo.md"
    if not path.exists():
        return 0
    current_section = ""
    current: dict[str, object] | None = None
    current_title = ""
    created = 0

    def flush() -> None:
        nonlocal current, current_title, created
        if current is not None and current_title:
            add_todo(todos, current_title, current)
            created += 1
        current = None
        current_title = ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            flush()
            current_section = line.removeprefix("## ").strip()
            continue
        if line.startswith("- "):
            flush()
            head = clean_markdown_text(line[2:])
            if " / " in head:
                title, subject = head.split(" / ", 1)
            else:
                title, subject = head, ""
            current_title = title.strip()
            current = {
                "kind": "card_face_todo",
                "source_report": "reports/1-card-face-todo.md",
                "section": current_section,
                "subject": subject.strip(),
                "summary": f"{current_section}：{subject.strip() or current_title}",
                "details": [],
            }
            continue
        if current is not None and line.startswith("  - "):
            detail = clean_markdown_text(line[4:])
            if detail:
                current.setdefault("details", []).append(detail)
    flush()
    return created


def parse_text_audit_todos(todos: dict[str, list[dict[str, object]]]) -> int:
    path = REPORTS / "2-card-text-audit-todos.md"
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    current_source = ""
    created = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## 📖 来源作品："):
            current_source = line.split("：", 1)[-1].strip()
            i += 1
            continue
        match = re.match(r"^### 🎴 \[([^\]]+)\] (.+)$", line)
        if not match:
            i += 1
            continue
        category, title = match.groups()
        i += 1
        issues: list[str] = []
        while i < len(lines):
            if lines[i].startswith("### 🎴 ") or lines[i].startswith("## 📖 "):
                break
            if lines[i].startswith("- "):
                issue = clean_markdown_text(lines[i][2:])
                if issue:
                    issues.append(issue)
            i += 1
        if issues:
            add_todo(
                todos,
                title.strip(),
                {
                    "kind": "card_text_audit",
                    "source_report": "reports/2-card-text-audit-todos.md",
                    "section": current_source,
                    "category": category.strip(),
                    "summary": f"文案审计发现 {len(issues)} 项疑点",
                    "details": issues,
                },
            )
            created += 1
    return created


def main() -> None:
    todos: dict[str, list[dict[str, object]]] = {}
    face_count = parse_face_todos(todos)
    text_count = parse_text_audit_todos(todos)
    payload = {
        "_schema": {
            "version": 1,
            "purpose": "卡牌维护待办层：记录 reports 中的卡面排版、缺冒号、缩进、文案审计等待办。不得视为牌面源数据或强度评语。",
            "sources": [
                "reports/1-card-face-todo.md",
                "reports/2-card-text-audit-todos.md",
            ],
        },
        "summary": {
            "cards_with_todos": len(todos),
            "face_todo_items": face_count,
            "text_audit_items": text_count,
        },
        "todos": dict(sorted(todos.items(), key=lambda item: item[0])),
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
