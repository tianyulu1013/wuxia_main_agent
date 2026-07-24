from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CROP_ROOT = ROOT / "data" / "release_images" / "cards"
WEBP_ROOT = ROOT / "data" / "release_images" / "cards_webp"
HISTORY_ROOT = ROOT / "data" / "release_images" / "cards_history"
CROP_MANIFEST = ROOT / "data" / "release_images" / "card_crops.jsonl"
WEBP_MANIFEST = ROOT / "data" / "release_images" / "web_card_images.jsonl"
CARD_HISTORY = ROOT / "data" / "cards_history" / "card_versions.jsonl"
RELEASES = ROOT / "data" / "cards_history" / "releases.json"


def safe_filename(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = value.strip().strip(".")
    return value or "unnamed"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def crop_box(slot: int) -> tuple[int, int, int, int]:
    zero = slot - 1
    column = zero % 10
    row = zero // 10
    return column * 550, row * 900, (column + 1) * 550, (row + 1) * 900


def replace_or_append(records: list[dict], predicate, replacement: dict) -> None:
    indexes = [index for index, record in enumerate(records) if predicate(record)]
    if len(indexes) > 1:
        raise SystemExit(f"Expected at most one manifest record, found {len(indexes)}")
    if indexes:
        records[indexes[0]] = replacement
    else:
        records.append(replacement)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Selectively crop and register current WebP files for a release."
    )
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    spec_path = args.spec if args.spec.is_absolute() else ROOT / args.spec
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    release_id = spec["release_id"]
    source_release_version = spec["source_release_version"]
    quality = int(spec.get("webp_quality", 85))
    cards = spec["cards"]

    crop_records = read_jsonl(CROP_MANIFEST)
    webp_records = read_jsonl(WEBP_MANIFEST)
    history_records = read_jsonl(CARD_HISTORY)
    history_ids = {record["card_version_id"] for record in history_records}
    crop_by_title = {record["title"]: record for record in crop_records}
    generated_images: dict[str, dict] = {}

    source_images: dict[str, Image.Image] = {}
    try:
        for card in cards:
            title = card["title"]
            card_id = card["card_id"]
            source_rel = card["source_image"]
            source_path = ROOT / source_rel
            if source_rel not in source_images:
                image = Image.open(source_path).convert("RGB")
                if image.size != (5500, 6300):
                    raise SystemExit(
                        f"{source_rel} must be 5500x6300, got {image.size[0]}x{image.size[1]}"
                    )
                source_images[source_rel] = image

            if card.get("requires_history"):
                history_id = f"{card_id}@pre-{release_id}"
                history_path = HISTORY_ROOT / card_id / f"pre-{release_id}.webp"
                if history_id not in history_ids:
                    raise SystemExit(f"Missing historical card record: {history_id}")
                if not history_path.exists():
                    raise SystemExit(f"Missing historical WebP: {history_path}")

            old_crop = crop_by_title.get(title)
            if old_crop:
                crop_rel = Path(old_crop["crop_path"].replace("\\", "/"))
            else:
                crop_rel = (
                    Path("data")
                    / "release_images"
                    / "cards"
                    / card["release_deck"]
                    / f"{card['slot']:02d}_{safe_filename(title)}.png"
                )
            crop_path = ROOT / crop_rel
            crop_path.parent.mkdir(parents=True, exist_ok=True)

            box = crop_box(int(card["slot"]))
            crop = source_images[source_rel].crop(box)
            crop.save(crop_path, format="PNG")

            webp_rel = Path(str(crop_rel).replace("\\", "/")).relative_to(
                Path("data") / "release_images" / "cards"
            )
            webp_rel = (
                Path("data")
                / "release_images"
                / "cards_webp"
                / webp_rel.with_suffix(".webp")
            )
            webp_path = ROOT / webp_rel
            webp_path.parent.mkdir(parents=True, exist_ok=True)
            crop.save(webp_path, format="WEBP", quality=quality, method=6)

            crop_record = {
                "title": title,
                "card_id": card_id,
                "order_deck": card["order_deck"],
                "release_deck": card["release_deck"],
                "slot": card["slot"],
                "row": (int(card["slot"]) - 1) // 10 + 1,
                "column": (int(card["slot"]) - 1) % 10 + 1,
                "source_image": source_rel,
                "source_version": source_release_version,
                "crop_path": str(crop_rel).replace("\\", "/"),
                "box": list(box),
            }
            replace_or_append(
                crop_records,
                lambda record, title=title: record.get("title") == title,
                crop_record,
            )

            webp_record = {
                "card_id": card_id,
                "title": title,
                "source_path": str(crop_rel).replace("\\", "/"),
                "webp_path": str(webp_rel).replace("\\", "/"),
                "quality": quality,
                "width": 550,
                "height": 900,
                "source_bytes": crop_path.stat().st_size,
                "webp_bytes": webp_path.stat().st_size,
                "source_sha256": sha256(crop_path),
                "webp_sha256": sha256(webp_path),
                "source_release_version": source_release_version,
                "release_deck": card["release_deck"],
                "slot": card["slot"],
            }
            generated_images[card_id] = {
                "status": "current",
                "format": "webp",
                "path": webp_record["webp_path"],
                "sha256": webp_record["webp_sha256"],
                "width": 550,
                "height": 900,
                "quality": quality,
                "source_image": source_rel,
                "source_release_version": source_release_version,
                "slot": card["slot"],
                "crop_box": list(box),
            }
            replace_or_append(
                webp_records,
                lambda record, source=str(crop_rel).replace("\\", "/"): (
                    record.get("source_path", "").replace("\\", "/") == source
                ),
                webp_record,
            )
            print(
                f"{card['release_deck']} slot {card['slot']:02d} {title} "
                f"{webp_record['webp_sha256']}"
            )
    finally:
        for image in source_images.values():
            image.close()

    write_jsonl(CROP_MANIFEST, crop_records)
    write_jsonl(WEBP_MANIFEST, webp_records)

    releases_data = json.loads(RELEASES.read_text(encoding="utf-8"))
    releases = [
        release
        for release in releases_data["releases"]
        if release["release_id"] == release_id
    ]
    if len(releases) != 1:
        raise SystemExit(f"Expected one release registry entry for {release_id}")
    release = releases[0]
    registry_cards = {card["card_id"]: card for card in release["cards"]}
    for card in cards:
        registry_card = registry_cards.get(card["card_id"])
        if registry_card is None:
            raise SystemExit(f"Card missing from release registry: {card['title']}")
        registry_card["release_deck"] = card["release_deck"]
        registry_card["slot"] = card["slot"]
        registry_card["image"] = generated_images[card["card_id"]]
    release["affected_decks"] = sorted(
        set(release.get("affected_decks", []))
        | {card["release_deck"] for card in cards}
    )
    excluded_release_cards = spec.get("excluded_release_cards", [])
    image_status = (
        "complete_for_author_declared_scope"
        if excluded_release_cards
        else "complete"
    )
    release["image_update"] = {
        "status": image_status,
        "applied_at": date.today().isoformat(),
        "source_release_version": source_release_version,
        "card_count": len(cards),
        "cards": [
            {"card_id": card["card_id"], "title": card["title"]}
            for card in cards
        ],
        "excluded_release_cards": excluded_release_cards,
    }
    release["status"] = (
        "data_complete_images_complete_for_author_declared_scope"
        if excluded_release_cards
        else "complete"
    )
    release["images_applied_at"] = date.today().isoformat()
    RELEASES.write_text(
        json.dumps(releases_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"updated_cards={len(cards)}")
    print(CROP_MANIFEST)
    print(WEBP_MANIFEST)
    print(RELEASES)


if __name__ == "__main__":
    main()
