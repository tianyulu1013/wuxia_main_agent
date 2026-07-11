from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TIMELINE_JSON = ROOT / "data" / "excel_patch_candidates" / "2025_card_timeline_sync.json"
REPORT = ROOT / "docs" / "2025-clear-excel-diff-report.md"


def main() -> None:
    data = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
    timelines = data["timelines"]

    rows: list[dict[str, object]] = []
    for item in timelines:
        for fragment in item.get("near_match_fragments") or []:
            changes = fragment.get("diff_summary") or []
            if not changes:
                continue
            rows.append(
                {
                    "title": item["title"],
                    "date": fragment.get("date") or "未标日期",
                    "log_title": fragment.get("log_title") or "",
                    "similarity": fragment.get("excel_similarity"),
                    "changes": changes,
                }
            )

    lines = [
        "# 2025 Excel 明确差异清单",
        "",
        "这个文件只列机器已经能读出来的差异，目的是避免人工在两段长文本里找字。",
        "",
        "判断原则：这里不是最终自动改 Excel 的授权清单，但其中“缺少/多出/写作不同”的事实通常说明 Excel 没有同步到日志。",
        "",
        f"- 明确差异条目数：{len(rows)}",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"## {row['title']}",
                "",
                f"- 日志：{row['date']} / {row['log_title']} / 相似度 {row['similarity']}",
                "- 具体差异：",
            ]
        )
        for change in row["changes"]:
            lines.append(f"  - {change['summary']}")
            context = change.get("context")
            if context:
                lines.append(f"    - Excel 位置：`{context}`")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))


if __name__ == "__main__":
    main()
