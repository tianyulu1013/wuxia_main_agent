from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "release_images" / "cards"
OUTPUT_ROOT = ROOT / "data" / "release_images" / "cards_webp"
MANIFEST = ROOT / "data" / "release_images" / "web_card_images.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WebP derivatives for current card images.")
    parser.add_argument("--quality", type=int, default=85)
    args = parser.parse_args()
    if not 1 <= args.quality <= 100:
        raise SystemExit("--quality must be between 1 and 100")

    source_paths = sorted(SOURCE_ROOT.rglob("*.png"))
    if not source_paths:
        raise SystemExit(f"No PNG card images found under {SOURCE_ROOT}")

    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True)

    records: list[dict[str, object]] = []
    for source_path in source_paths:
        relative_path = source_path.relative_to(SOURCE_ROOT).with_suffix(".webp")
        output_path = OUTPUT_ROOT / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source_path) as image:
            converted = image.convert("RGB") if image.mode != "RGB" else image
            converted.save(output_path, format="WEBP", quality=args.quality, method=6)
            width, height = image.size
        records.append(
            {
                "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                "webp_path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
                "quality": args.quality,
                "width": width,
                "height": height,
                "source_bytes": source_path.stat().st_size,
                "webp_bytes": output_path.stat().st_size,
                "source_sha256": sha256(source_path),
                "webp_sha256": sha256(output_path),
            }
        )

    MANIFEST.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    source_bytes = sum(int(record["source_bytes"]) for record in records)
    webp_bytes = sum(int(record["webp_bytes"]) for record in records)
    print(OUTPUT_ROOT)
    print(f"images={len(records)}")
    print(f"quality={args.quality}")
    print(f"source_bytes={source_bytes}")
    print(f"webp_bytes={webp_bytes}")
    print(f"savings_pct={(1 - webp_bytes / source_bytes) * 100:.2f}")


if __name__ == "__main__":
    main()
