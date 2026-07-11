from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "release_images"
OUT_DIR = ROOT / "data" / "release_images"
INDEX_JSON = OUT_DIR / "latest_decks.json"
REPORT = ROOT / "docs" / "release-image-index.md"


SKIP_NAME_PATTERNS = [
    re.compile(r"table", re.I),
    re.compile(r"卡背"),
    re.compile(r"规则"),
    re.compile(r"剧本"),
    re.compile(r"^httpcloud", re.I),
]


@dataclass
class ReleaseImage:
    key: str
    version: str
    version_sort: list[int]
    path: str
    filename: str
    width: int
    height: int
    columns: int
    rows: int
    card_width: int
    card_height: int


def version_sort_key(name: str) -> list[int]:
    match = re.match(r"^(\d+(?:\.\d+)*)", name)
    if not match:
        return [0]
    return [int(part) for part in match.group(1).split(".")]


def should_skip(path: Path) -> bool:
    stem = path.stem
    return any(pattern.search(stem) for pattern in SKIP_NAME_PATTERNS)


def normalize_deck_key(path: Path, version: str) -> str | None:
    name = path.stem.strip()
    name = re.sub(r"^\d+(?:\.\d+)*(?:[-_ ]*)", "", name).strip()
    name = re.sub(r"[-_ ]+", "", name)
    if not name:
        return None
    if re.match(r"^温瑞安黄易0*2$", name):
        return "温瑞安2"

    match = re.match(r"^(.+?)(0*\d+)$", name)
    if match:
        base, number = match.groups()
        number_int = int(number)
        if base == "场景" and number_int == 1:
            return "场景"
        return f"{base}{number_int}"
    return name


def iter_release_dirs() -> Iterable[Path]:
    if not RELEASE_ROOT.exists():
        return []
    return sorted(
        [path for path in RELEASE_ROOT.iterdir() if path.is_dir()],
        key=lambda path: version_sort_key(path.name),
    )


def image_grid_size(width: int, height: int) -> tuple[int, int]:
    if width % 10 == 0 and height % 7 == 0:
        return 10, 7
    return 1, 1


def build_index() -> tuple[list[ReleaseImage], dict[str, ReleaseImage]]:
    all_images: list[ReleaseImage] = []
    latest: dict[str, ReleaseImage] = {}

    for release_dir in iter_release_dirs():
        version = release_dir.name
        sort_key = version_sort_key(version)
        for path in sorted(release_dir.glob("*.png")):
            if should_skip(path):
                continue
            key = normalize_deck_key(path, version)
            if not key:
                continue
            with Image.open(path) as image:
                width, height = image.size
            columns, rows = image_grid_size(width, height)
            item = ReleaseImage(
                key=key,
                version=version,
                version_sort=sort_key,
                path=str(path.relative_to(ROOT)),
                filename=path.name,
                width=width,
                height=height,
                columns=columns,
                rows=rows,
                card_width=width // columns,
                card_height=height // rows,
            )
            all_images.append(item)
            previous = latest.get(key)
            if previous is None or sort_key > previous.version_sort:
                latest[key] = item

    for key in list(latest):
        numbered_key = f"{key}1"
        if not re.search(r"\d+$", key) and numbered_key in latest:
            del latest[key]

    return all_images, latest


def write_outputs(all_images: list[ReleaseImage], latest: dict[str, ReleaseImage]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "release_root": str(RELEASE_ROOT.relative_to(ROOT)),
        "image_count": len(all_images),
        "latest_deck_count": len(latest),
        "latest_decks": [asdict(latest[key]) for key in sorted(latest)],
    }
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Release 图片索引",
        "",
        "本索引按版本号从新到旧回退：同一牌堆取出现过的最高版本 PNG。",
        "",
        f"- Release 根目录：`{RELEASE_ROOT.relative_to(ROOT)}`",
        f"- PNG 总数：{len(all_images)}",
        f"- 最新牌堆数：{len(latest)}",
        f"- JSON：`{INDEX_JSON.relative_to(ROOT)}`",
        "",
        "## 最新牌堆",
        "",
        "| 牌堆 | 版本 | 文件 | 尺寸 | 网格 | 单卡 |",
        "|---|---|---|---:|---:|---:|",
    ]
    for key in sorted(latest):
        item = latest[key]
        lines.append(
            f"| {key} | {item.version} | `{item.path}` | "
            f"{item.width}×{item.height} | {item.columns}×{item.rows} | "
            f"{item.card_width}×{item.card_height} |"
        )

    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    all_images, latest = build_index()
    write_outputs(all_images, latest)
    print(INDEX_JSON)
    print(REPORT)


if __name__ == "__main__":
    main()
