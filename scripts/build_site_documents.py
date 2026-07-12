from __future__ import annotations

import json
from pathlib import Path

import serve_card_browser as browser


OUT_DIR = browser.ROOT / "data" / "site_documents"


def build_payload(entry: dict[str, object]) -> dict[str, object]:
    source_path = str(entry.get("source_path") or entry.get("path") or "")
    source_entry = {**entry, "path": source_path}
    path = browser.document_path(source_entry)
    kind = str(entry.get("kind") or "").lower()
    suffix = path.suffix.lower()
    if str(entry.get("source_path") or ""):
        kind = path.suffix.removeprefix(".").lower()
    content = ""
    sections: list[dict[str, object]] = []
    if path.exists() and (kind == "docx" or suffix == ".docx"):
        blocks = browser.read_docx_blocks(path)
        content = browser.blocks_to_text(blocks)
        sections = browser.blocks_to_sections(blocks)
    elif path.exists() and (kind in {"markdown", "md"} or suffix == ".md"):
        content = path.read_text(encoding="utf-8")
        sections = browser.read_markdown_sections(path)
    elif path.exists():
        content = path.read_text(encoding="utf-8")
    display_kind = path.suffix.removeprefix(".").lower() or str(entry.get("kind") or "")
    return {
        "id": entry["id"],
        "title": entry["title"],
        "group": entry.get("group", ""),
        "kind": display_kind,
        "source_path": source_path,
        "description": entry.get("description", ""),
        "version": entry.get("version", ""),
        "updated": entry.get("updated", ""),
        "content": content,
        "sections": sections,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for entry in browser.load_site_document_entries():
        payload = build_payload(entry)
        out_path = OUT_DIR / f"{entry['id']}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{out_path} sections={len(payload['sections'])}")


if __name__ == "__main__":
    main()
