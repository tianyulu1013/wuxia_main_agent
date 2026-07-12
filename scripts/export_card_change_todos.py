from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "change_candidates.json"
OUTPUT = ROOT / "改卡TODO.md"
VISIBLE_STATUSES = {"draft", "needs_author_review", "approved"}


def block(text: object, language: str = "text") -> list[str]:
    value = str(text or "").strip()
    if not value:
        return []
    return [f"```{language}", value, "```", ""]


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    candidates = [
        item
        for item in data.get("candidates", [])
        if isinstance(item, dict) and item.get("status") in VISIBLE_STATUSES
    ]

    lines = [
        "# 改卡 TODO",
        "",
        "> 这是 `data/change_candidates.json` 的便于阅读和复制的生成视图。",
        "> 只显示有效改卡候选；不包含缩进、解析、卡面审计等工程 TODO。不要直接编辑本文件。",
        "",
        f"当前有效候选：{len(candidates)} 条。",
        "",
    ]

    for item in candidates:
        title = str(item.get("card_title") or "未命名")
        status = str(item.get("status") or "draft")
        lines.extend([
            f"## {title}",
            "",
            f"- ID：`{item.get('id', '')}`",
            f"- 状态：`{status}`",
            f"- 修改意图：{item.get('request', '')}",
            "",
        ])

        patches = item.get("proposed_patch") or []
        if patches:
            lines.extend(["### 修改对照", ""])
            for patch in patches:
                before, separator, after = str(patch).partition("→")
                if separator:
                    lines.extend(block(f"- {before.strip()}\n+ {after.strip()}", "diff"))
                else:
                    lines.extend(block(str(patch)))

        full_text = str(item.get("proposed_full_text") or "").strip()
        if full_text:
            lines.extend(["### 可直接粘贴", ""])
            lines.extend(block(full_text))

        questions = item.get("author_decision_needed") or []
        if questions:
            lines.extend(["### 尚待裁定", ""])
            lines.extend(f"- {question}" for question in questions)
            lines.append("")

        notes = item.get("patch_notes") or []
        if notes:
            lines.extend(["### 更新说明草稿", ""])
            lines.extend(f"- {note}" for note in notes)
            lines.append("")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
