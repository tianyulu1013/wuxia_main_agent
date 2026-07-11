from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "psd_text_fragments.json"


def printable_ratio(text: str) -> float:
    if not text:
        return 0.0
    printable = sum(1 for ch in text if ch.isprintable() or ch in "\n\r\t")
    return printable / len(text)


def useful(text: str) -> bool:
    if len(text) < 2:
        return False
    if printable_ratio(text) < 0.85:
        return False
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_utf16(data: bytes, encoding: str) -> list[str]:
    strings: list[str] = []
    decoded = data.decode(encoding, errors="ignore")
    for candidate in re.findall(r"[\u4e00-\u9fffA-Za-z0-9，。；：？！【】（）《》、·“”\-\+\*/=×%~\s]{4,}", decoded):
        text = clean(candidate)
        if useful(text):
            strings.append(text)
    return strings


def extract_utf8(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="ignore")
    candidates = re.findall(r"[\u4e00-\u9fffA-Za-z0-9，。；：？！【】（）《》、·“”\-\+\*/=×%~\s]{4,}", text)
    return [clean(item) for item in candidates if useful(clean(item))]


def compact_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        if any(item != other and item in other for other in result):
            continue
        seen.add(item)
        result.append(item)
    return result


def main() -> None:
    paths = [Path(arg) for arg in sys.argv[1:]]
    output = {}
    for path in paths:
        data = path.read_bytes()
        fragments = []
        fragments.extend(extract_utf16(data, "utf-16-be"))
        fragments.extend(extract_utf16(data, "utf-16-le"))
        fragments.extend(extract_utf8(data))
        fragments = compact_unique([item for item in fragments if len(item) <= 3000])
        output[str(path)] = fragments

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))
    for path, fragments in output.items():
        print(path, len(fragments))


if __name__ == "__main__":
    main()
