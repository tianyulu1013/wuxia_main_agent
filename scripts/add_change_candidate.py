from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGE_CANDIDATES_PATH = ROOT / "data" / "change_candidates.json"


def slug(value: str) -> str:
    text = re.sub(r"\W+", "_", value, flags=re.UNICODE).strip("_")
    return text[:32] or "card"


def load_data() -> dict[str, object]:
    if not CHANGE_CANDIDATES_PATH.exists():
        return {"_schema": {"version": 1}, "candidates": []}
    return json.loads(CHANGE_CANDIDATES_PATH.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a card change candidate without touching source card data.")
    parser.add_argument("card_title")
    parser.add_argument("request")
    parser.add_argument("--rationale", default="")
    parser.add_argument("--full-text", default="")
    parser.add_argument("--patch-note", action="append", default=[])
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--status", default="draft")
    args = parser.parse_args()

    data = load_data()
    candidates = data.setdefault("candidates", [])
    if not isinstance(candidates, list):
        raise TypeError("change_candidates.json: candidates must be a list")

    today = date.today().isoformat().replace("-", "")
    prefix = f"change_{today}_{slug(args.card_title)}"
    next_number = 1 + sum(
        1
        for item in candidates
        if isinstance(item, dict) and str(item.get("id", "")).startswith(prefix)
    )
    candidate = {
        "id": f"{prefix}_{next_number:03d}",
        "card_title": args.card_title,
        "status": args.status,
        "request": args.request,
        "rationale": args.rationale,
        "proposed_full_text": args.full_text,
        "patch_notes": args.patch_note,
        "source_tasks": args.task or ["作者确认后修改PSD", "更新Excel", "重建数据库", "生成玩家更新说明"],
        "created_at": date.today().isoformat(),
    }
    candidates.append(candidate)
    CHANGE_CANDIDATES_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(candidate["id"])


if __name__ == "__main__":
    main()
