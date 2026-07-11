from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

from check_tts_slot_orders import parse_orders


ROOT = Path(__file__).resolve().parents[1]
ORDER_DOC = ROOT / "docs" / "tts-slot-orders-v0.1.md"
LATEST_DECKS = ROOT / "data" / "release_images" / "latest_decks.json"
OUT_DIR = ROOT / "data" / "release_images" / "cards"
MANIFEST = ROOT / "data" / "release_images" / "card_crops.jsonl"
REPORT = ROOT / "docs" / "release-card-crops.md"


ORDER_TO_RELEASE_DECK = {
    "场景": "场景",
    "金庸1": "金庸1",
    "金庸2": "金庸2",
    "金庸3": "金庸3",
    "古龙1": "古龙1",
    "古龙2": "古龙2",
    "黄易1": "黄易1",
    "温瑞安1": "温瑞安1",
    "黄易温瑞安": "温瑞安2",
    "其他": "其他1",
    "现代": "现代1",
}


def safe_filename(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = value.strip().strip(".")
    return value or "unnamed"


def load_latest_decks() -> dict[str, dict]:
    data = json.loads(LATEST_DECKS.read_text(encoding="utf-8"))
    return {item["key"]: item for item in data["latest_decks"]}


def crop_box(slot_index: int, card_width: int, card_height: int, columns: int) -> tuple[int, int, int, int]:
    zero = slot_index - 1
    column = zero % columns
    row = zero // columns
    left = column * card_width
    top = row * card_height
    return left, top, left + card_width, top + card_height


def build_crops() -> list[dict]:
    orders = parse_orders(ORDER_DOC.read_text(encoding="utf-8"))
    latest = load_latest_decks()
    records: list[dict] = []

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for order_deck, names in orders.items():
        release_deck = ORDER_TO_RELEASE_DECK.get(order_deck)
        if not release_deck:
            continue
        deck_info = latest.get(release_deck)
        if not deck_info:
            continue

        image_path = ROOT / deck_info["path"]
        deck_out = OUT_DIR / release_deck
        deck_out.mkdir(parents=True, exist_ok=True)

        with Image.open(image_path) as image:
            for slot, title in enumerate(names, start=1):
                if slot > deck_info["columns"] * deck_info["rows"]:
                    break
                box = crop_box(slot, deck_info["card_width"], deck_info["card_height"], deck_info["columns"])
                crop = image.crop(box)
                crop_path = deck_out / f"{slot:02d}_{safe_filename(title)}.png"
                crop.save(crop_path)
                records.append(
                    {
                        "title": title,
                        "order_deck": order_deck,
                        "release_deck": release_deck,
                        "slot": slot,
                        "row": (slot - 1) // deck_info["columns"] + 1,
                        "column": (slot - 1) % deck_info["columns"] + 1,
                        "source_image": deck_info["path"],
                        "source_version": deck_info["version"],
                        "crop_path": str(crop_path.relative_to(ROOT)),
                        "box": box,
                    }
                )

    return records


def write_outputs(records: list[dict]) -> None:
    with MANIFEST.open("w", encoding="utf-8", newline="\n") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False))
            fh.write("\n")

    by_deck: dict[str, list[dict]] = {}
    for record in records:
        by_deck.setdefault(record["release_deck"], []).append(record)

    lines = [
        "# Release 单卡切图索引",
        "",
        "本报告按 TTS 顺序表和最新 release 牌堆索引，把 10×7 release PNG 切成单卡图片。",
        "",
        f"- 切图总数：{len(records)}",
        f"- Manifest：`{MANIFEST.relative_to(ROOT)}`",
        f"- 单卡目录：`{OUT_DIR.relative_to(ROOT)}`",
        "",
        "## 牌堆统计",
        "",
        "| Release 牌堆 | 卡数 | 来源版本 | 来源顺序名 |",
        "|---|---:|---|---|",
    ]
    for deck in sorted(by_deck):
        rows = by_deck[deck]
        versions = sorted({row["source_version"] for row in rows})
        order_decks = sorted({row["order_deck"] for row in rows})
        lines.append(f"| {deck} | {len(rows)} | {', '.join(versions)} | {', '.join(order_decks)} |")

    lines.extend(["", "## 样例", ""])
    for record in records[:20]:
        lines.append(
            f"- `{record['title']}` -> `{record['crop_path']}` "
            f"({record['release_deck']} slot {record['slot']})"
        )

    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    records = build_crops()
    write_outputs(records)
    print(MANIFEST)
    print(REPORT)


if __name__ == "__main__":
    main()
