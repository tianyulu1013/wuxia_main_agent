import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "review" / "combat_baselines.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def print_json(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Query calibrated combat-character baselines without loading all workcards."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    title_parser = subparsers.add_parser("title", help="Query one exact card title.")
    title_parser.add_argument("title")

    function_parser = subparsers.add_parser(
        "function", help="Query entries containing a function tag."
    )
    function_parser.add_argument("tag")

    subparsers.add_parser("list", help="List available calibrated titles and tags.")

    args = parser.parse_args()
    data = load_data()
    entries = data["entries"]

    if args.command == "title":
        if args.title not in entries:
            raise SystemExit(f"No calibrated baseline found for: {args.title}")
        print_json(
            {
                "white_reference": data["white_reference"],
                "entry": entries[args.title],
            }
        )
        return

    if args.command == "function":
        matches = {
            title: entry
            for title, entry in entries.items()
            if args.tag in entry.get("function_tags", [])
        }
        print_json(
            {
                "query_tag": args.tag,
                "white_reference": data["white_reference"],
                "matches": matches,
            }
        )
        return

    tags = sorted(
        {
            tag
            for entry in entries.values()
            for tag in entry.get("function_tags", [])
        }
    )
    print_json({"titles": sorted(entries), "function_tags": tags})


if __name__ == "__main__":
    main()
