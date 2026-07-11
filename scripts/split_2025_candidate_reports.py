from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "excel_patch_candidates" / "2025_full_pass_candidates.json"
OUT_DIR = ROOT / "docs" / "2025-log-review"


STATUS_TITLES = {
    "auto_replace_candidate": "精确替换候选",
    "append_row_candidate": "新增行候选",
    "needs_review": "需要人工确认",
    "unmatched": "未匹配 Excel",
    "already_synced": "看起来已同步",
}


def write_status_report(status: str, candidates: list[dict[str, Any]]) -> None:
    path = OUT_DIR / f"{status}.md"
    title = STATUS_TITLES.get(status, status)
    lines = [
        f"# 2025 更新日志：{title}",
        "",
        f"- 状态：`{status}`",
        f"- 条目数：{len(candidates)}",
        "",
    ]

    for index, item in enumerate(candidates, start=1):
        date = item.get("date") or "未标日期"
        section = item.get("section") or "未分类"
        title = item.get("log_title") or "未命名"
        lines.extend(["", f"## {index}. {date} / {section} / {title}", ""])
        lines.append(f"- 匹配方式：`{item.get('match_method')}`")

        if item.get("candidate_cards"):
            lines.append("- Excel 候选：")
            for card in item["candidate_cards"]:
                source = card["source"]
                lines.append(f"  - `{card['title']}` ({source['sheet']}!{source['row']}, `{card['category']}`)")
                if status == "needs_review":
                    lines.append("    - Excel 当前字段：")
                    for field, value in card.get("current_fields", {}).items():
                        text = str(value)
                        lines.append(f"      - `{field}`:")
                        lines.extend(["", "```text", text, "```", ""])

        for note in item.get("notes", []):
            lines.append(f"- 备注：{note}")

        if item.get("operations"):
            lines.extend(["", "替换候选：", ""])
            for op in item["operations"]:
                lines.append(f"- 字段：`{op['field']}`；定位：`{op['match_kind']}`；安全候选：`{op['safe_to_apply']}`")
                lines.extend(["", "旧：", "", "```text", op["before_text"], "```"])
                lines.extend(["", "新：", "", "```text", op["after_text"], "```", ""])

        if item.get("missing_after_lines"):
            lines.extend(["", "需要放入 Excel 的更新后片段：", ""])
            for line in item["missing_after_lines"]:
                lines.append(f"- {line}")

        if item.get("log_markdown") and status in {"append_row_candidate", "needs_review", "unmatched"}:
            lines.extend(["", "日志原文：", "", "```text", item["log_markdown"], "```"])

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    candidates = data["candidates"]
    for status in STATUS_TITLES:
        write_status_report(status, [item for item in candidates if item["status"] == status])
    print(str(OUT_DIR))


if __name__ == "__main__":
    main()
