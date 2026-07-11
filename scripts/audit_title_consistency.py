from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import check_tts_slot_orders


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "cards_raw" / "all_cards.jsonl"
RULINGS = ROOT / "docs" / "card-name-rulings-v0.1.md"
ORDER_DOC = ROOT / "docs" / "tts-slot-orders-v0.1.md"
REPORT = ROOT / "docs" / "title-consistency-audit-v0.1.md"


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", "", title.replace("（", "(").replace("）", ")"))


def load_records() -> list[dict[str, Any]]:
    return [json.loads(line) for line in RAW.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_aliases() -> dict[str, str]:
    aliases: dict[str, str] = {}
    in_alias_table = False
    for line in RULINGS.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 3."):
            in_alias_table = True
            continue
        if in_alias_table and line.startswith("## "):
            break
        if not in_alias_table or not line.startswith("| `"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        display = cells[0].strip("`")
        asset = cells[1].strip("`")
        if display and asset and display != "TTS/展示名":
            aliases[display] = asset
    return aliases


def main() -> None:
    records = load_records()
    orders = check_tts_slot_orders.parse_orders(ORDER_DOC.read_text(encoding="utf-8"))
    aliases = parse_aliases()

    excel_exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    excel_norm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        title = record.get("title")
        if isinstance(title, str) and title:
            excel_exact[title].append(record)
            excel_norm[normalize_title(title)].append(record)

    tts_entries: list[dict[str, Any]] = []
    for deck, names in orders.items():
        if deck == "说明":
            continue
        for index, name in enumerate(names, start=1):
            tts_entries.append({"deck": deck, "slot": index, "name": name})

    no_excel_match: list[dict[str, Any]] = []
    alias_resolved: list[dict[str, Any]] = []
    normalized_resolved: list[dict[str, Any]] = []
    exact_matches = 0

    for entry in tts_entries:
        name = entry["name"]
        if name in excel_exact:
            exact_matches += 1
            continue

        alias = aliases.get(name)
        if alias and alias in excel_exact:
            alias_resolved.append({**entry, "resolved_by": alias})
            continue

        norm = normalize_title(name)
        if norm in excel_norm:
            normalized_resolved.append(
                {**entry, "resolved_by": excel_norm[norm][0]["title"]}
            )
            continue

        no_excel_match.append(entry)

    tts_names = {entry["name"] for entry in tts_entries}
    alias_assets = set(aliases.values())
    alias_displays = set(aliases.keys())
    tts_norm = {normalize_title(name) for name in tts_names}
    tts_norm |= {normalize_title(name) for name in alias_assets}
    tts_norm |= {normalize_title(name) for name in alias_displays}

    excel_not_in_tts: list[dict[str, Any]] = []
    for record in records:
        title = record.get("title")
        if not isinstance(title, str) or not title:
            continue
        if normalize_title(title) not in tts_norm:
            excel_not_in_tts.append(record)

    lines = [
        "# 标题一致性审计 v0.1",
        "",
        "本报告比较 `已制作.xlsx` 导入结果、TTS 顺序表和已确认别名裁定。",
        "",
        "## 总览",
        "",
        f"- Excel 记录数：{len(records)}",
        f"- TTS slot 数：{len(tts_entries)}",
        f"- TTS 名称精确匹配 Excel：{exact_matches}",
        f"- 通过裁定表别名匹配：{len(alias_resolved)}",
        f"- 通过括号/空格归一化匹配：{len(normalized_resolved)}",
        f"- TTS 中暂未匹配 Excel：{len(no_excel_match)}",
        f"- Excel 中暂未出现在 TTS/别名中的记录：{len(excel_not_in_tts)}",
        "",
        "## 通过裁定表别名匹配",
        "",
    ]
    if alias_resolved:
        for item in alias_resolved:
            lines.append(
                f"- `{item['deck']}` slot {item['slot']}: `{item['name']}` -> `{item['resolved_by']}`"
            )
    else:
        lines.append("- 无")

    lines.extend(["", "## 通过归一化匹配", ""])
    if normalized_resolved:
        for item in normalized_resolved:
            lines.append(
                f"- `{item['deck']}` slot {item['slot']}: `{item['name']}` -> `{item['resolved_by']}`"
            )
    else:
        lines.append("- 无")

    lines.extend(["", "## TTS 中暂未匹配 Excel", ""])
    if no_excel_match:
        for item in no_excel_match:
            lines.append(f"- `{item['deck']}` slot {item['slot']}: `{item['name']}`")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## Excel 中暂未出现在 TTS/别名中的记录",
            "",
            "说明：这里不一定是错误，可能是附加人物、废弃、Excel 保留项、不同命名或暂未发布。",
            "",
        ]
    )
    for record in excel_not_in_tts[:120]:
        source = record["source"]
        lines.append(
            f"- `{record['title']}` ({source['sheet']}!{source['row']}, `{record['category']}`)"
        )
    if len(excel_not_in_tts) > 120:
        lines.append(f"- ... 还有 {len(excel_not_in_tts) - 120} 条未显示")

    lines.extend(["", "## 下一步建议", ""])
    lines.append("- 先处理 `TTS 中暂未匹配 Excel`，因为这通常是名称不一致或 Excel 未同步。")
    lines.append("- `Excel 中暂未出现在 TTS/别名中` 暂时只作为线索，不急着全部修。")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(str(REPORT))


if __name__ == "__main__":
    main()
