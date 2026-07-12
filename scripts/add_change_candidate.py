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
    parser.add_argument("--candidate-type", default="revision", choices=["revision", "new_card", "rules_text", "other"])
    parser.add_argument("--design-goal", default="")
    parser.add_argument("--ai-position", default="uncertain", choices=["support", "caution", "oppose", "uncertain"])
    parser.add_argument("--rationale", default="")
    parser.add_argument("--current-snapshot", default="")
    parser.add_argument("--full-text", default="")
    parser.add_argument("--patch", action="append", default=[])
    parser.add_argument("--patch-note", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--strength-impact", default="")
    parser.add_argument("--flavor-fit", default="")
    parser.add_argument("--clarity", default="")
    parser.add_argument("--electronic-risk", action="append", default=[])
    parser.add_argument("--question", action="append", default=[])
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--status", default="draft")
    parser.add_argument("--dry-run", action="store_true", help="Print the candidate JSON without writing it.")
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
        "candidate_type": args.candidate_type,
        "card_title": args.card_title,
        "status": args.status,
        "request": args.request,
        "design_goal": args.design_goal,
        "ai_position": args.ai_position,
        "rationale": args.rationale,
        "current_snapshot": args.current_snapshot,
        "review": {
            "strength_impact": args.strength_impact,
            "flavor_fit": args.flavor_fit,
            "clarity": args.clarity,
            "rules_risks": args.risk,
            "electronic_risks": args.electronic_risk,
            "open_questions": args.question,
        },
        "proposed_full_text": args.full_text,
        "proposed_patch": args.patch,
        "patch_notes": args.patch_note,
        "author_decision_needed": args.question,
        "source_tasks": args.task or ["作者确认后修改PSD", "更新Excel", "重建数据库", "生成玩家更新说明"],
        "created_at": date.today().isoformat(),
    }
    if args.dry_run:
        print(json.dumps(candidate, ensure_ascii=False, indent=2))
    else:
        candidates.append(candidate)
        CHANGE_CANDIDATES_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(candidate["id"])


if __name__ == "__main__":
    main()
