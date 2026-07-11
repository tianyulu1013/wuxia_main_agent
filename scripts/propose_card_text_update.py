from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW_CARDS = ROOT / "data" / "cards_raw" / "all_cards.jsonl"
OUT_DIR = ROOT / "docs" / "card-update-proposals"
DATA_DIR = ROOT / "data" / "update_proposals"


def slug(text: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text, flags=re.UNICODE).strip("-")
    return value or "proposal"


def load_cards() -> list[dict[str, Any]]:
    return [json.loads(line) for line in RAW_CARDS.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--field", default="description")
    parser.add_argument("--find", required=True)
    parser.add_argument("--replace", required=True)
    parser.add_argument("--reason", default="")
    parser.add_argument("--assumption", default="")
    args = parser.parse_args()

    cards = [card for card in load_cards() if card.get("title") == args.title]
    if not cards:
        raise SystemExit(f"Card not found: {args.title}")
    if len(cards) > 1:
        locations = ", ".join(f"{c['source']['sheet']}!{c['source']['row']}" for c in cards)
        raise SystemExit(f"Multiple cards found: {args.title}: {locations}")

    card = cards[0]
    old_value = card.get("fields", {}).get(args.field)
    if not isinstance(old_value, str):
        raise SystemExit(f"Field is not text: {args.field}")
    if args.find not in old_value:
        raise SystemExit(f"Find text not found in {args.title}.{args.field}: {args.find}")

    new_value = old_value.replace(args.find, args.replace, 1)
    source = card["source"]
    proposal = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "title": args.title,
        "field": args.field,
        "source": source,
        "reason": args.reason,
        "assumption": args.assumption,
        "find": args.find,
        "replace": args.replace,
        "old_value": old_value,
        "new_value": new_value,
        "excel_patch": {
            "workbook": source["workbook"],
            "sheet": source["sheet"],
            "row": source["row"],
            "field": args.field,
            "new_value": new_value,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    base = slug(f"{args.title}-{args.field}")
    json_path = DATA_DIR / f"{base}.json"
    md_path = OUT_DIR / f"{base}.md"

    json_path.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# 单卡文本修改提案：{args.title}",
        "",
        "## 来源",
        "",
        f"- Excel：`{source['sheet']}!{source['row']}`",
        f"- 字段：`{args.field}`",
        "",
        "## 修改意见",
        "",
        f"- 理由：{args.reason or '未填写'}",
        f"- 假设：{args.assumption or '无'}",
        "",
        "## 精确替换",
        "",
        "旧片段：",
        "",
        "```text",
        args.find,
        "```",
        "",
        "新片段：",
        "",
        "```text",
        args.replace,
        "```",
        "",
        "## 新版字段全文候选",
        "",
        "```text",
        new_value,
        "```",
        "",
        "## 更新日志候选",
        "",
        f"### 修改 / {args.title}",
        "",
        "```text",
        args.replace,
        "```",
        "",
        "## Excel 补丁候选",
        "",
        f"- 将 `{source['sheet']}!{source['row']}` 的 `{args.field}` 更新为上方新版字段全文。",
        f"- 机器可读补丁：`{json_path.relative_to(ROOT)}`",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(str(md_path))
    print(str(json_path))


if __name__ == "__main__":
    main()
