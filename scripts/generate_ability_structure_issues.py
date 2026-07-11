from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from generate_ability_layout_report import compact, crop_lines, group_key, load_abilities, load_crops


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "ability-structure-issues-report.md"


STRUCTURE_FLAGS = {
    "typed_line_without_name",
    "typed_name_without_colon",
    "nested_named_line",
    "unnamed_star_line",
    "indented_implicit_word",
    "named_free_text",
}

IGNORE_FLAGS = {
    "known_unnamed_ability",
    "author_confirmed_structure",
}


def has_flag(item: dict[str, Any], flag: str) -> bool:
    return flag in item.get("review_flags", [])


def issue_labels(item: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    if has_flag(item, "typed_line_without_name"):
        labels.append("类型行未识别出特技名")
    if has_flag(item, "typed_name_without_colon"):
        labels.append("显式类型后疑似缺冒号")
    if has_flag(item, "nested_named_line"):
        labels.append("含命名子项/可能被合并")
    if has_flag(item, "unnamed_star_line"):
        labels.append("* 行未识别出特技名")
    if has_flag(item, "indented_implicit_word"):
        labels.append("缩进的字特技/可能继承类型")
    if has_flag(item, "named_free_text"):
        labels.append("说明文字疑似带特技名")
    return labels


def is_structure_issue(item: dict[str, Any]) -> bool:
    flags = set(item.get("review_flags", []))
    if flags & IGNORE_FLAGS:
        return False
    return bool(flags & STRUCTURE_FLAGS)


def priority(item: dict[str, Any]) -> int:
    if has_flag(item, "typed_line_without_name") or has_flag(item, "typed_name_without_colon"):
        return 1
    if has_flag(item, "nested_named_line"):
        return 2
    return 3


def render_issue_groups(items: list[dict[str, Any]], crops: dict[str, dict[str, Any]]) -> list[str]:
    groups: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(group_key(item), []).append(item)

    lines = ["", "## 结构问题清单", "", f"- 卡牌数：{len(groups)}", f"- 条目数：{len(items)}"]
    issue_index = 1
    for group_index, (_, group_items) in enumerate(
        sorted(groups.items(), key=lambda pair: (pair[0][0], pair[0][1], pair[0][2])),
        start=1,
    ):
        first = group_items[0]
        lines.extend(
            [
                "",
                f"### D{group_index:03d} {first['title']} / {first['source_sheet']}!{first['source_row']}",
                "",
            ]
        )
        if first.get("source_work"):
            lines.append(f"- 出处：{first['source_work']}")
        lines.extend(crop_lines(first, crops))
        for item in sorted(group_items, key=lambda entry: (priority(entry), int(entry["ordinal"]))):
            code = f"S{issue_index:03d}"
            issue_index += 1
            labels = "、".join(issue_labels(item))
            flags = ", ".join(item.get("review_flags", [])) or "无"
            name = item.get("name") or "未识别名称"
            lines.extend(
                [
                    f"- `{code}` `{labels}`：当前解析为 `{item['kind']}` / {name}",
                    f"  - 优先级：P{priority(item)}",
                    f"  - 标记：`{flags}`",
                    f"  - 原文：{compact(item.get('text'), 260)}",
                ]
            )
    return lines


def main() -> None:
    crops = load_crops()
    abilities = load_abilities()
    issues = [item for item in abilities if is_structure_issue(item)]
    flag_counts = Counter(flag for item in issues for flag in item.get("review_flags", []) if flag in STRUCTURE_FLAGS)
    priority_counts = Counter(priority(item) for item in issues)

    lines = [
        "# 数据库特技结构问题报告",
        "",
        "这个报告只列可能影响数据库理解的项目：特技名、类型、子项合并、未命名特技等。",
        "单纯卡面缩进/排版问题不列在这里；那类问题属于 PSD 或牌面整理。",
        "",
        "## 总览",
        "",
        f"- 特技/说明块总数：{len(abilities)}",
        f"- 结构问题条目数：{len(issues)}",
        f"- P1：{priority_counts.get(1, 0)} 条，直接影响特技名或类型解析",
        f"- P2：{priority_counts.get(2, 0)} 条，需要确认子项合并是否正确",
        f"- P3：{priority_counts.get(3, 0)} 条，低频边界情况",
        "",
        "## 标记统计",
        "",
    ]
    for flag, count in flag_counts.most_common():
        lines.append(f"- `{flag}`: {count}")
    if not flag_counts:
        lines.append("- 无")

    lines.extend(render_issue_groups(issues, crops))
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
