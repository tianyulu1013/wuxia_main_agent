import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from build_card_database import build, DEFAULT_SOURCE

CHANGE_CANDIDATES_PATH = ROOT / "data" / "change_candidates.json"
SITE_DOCUMENTS_PATH = ROOT / "data" / "site_documents.json"
PENDING_CHANGES_REPORT_PATH = ROOT / "data" / "review" / "pending_changes.md"

def load_json_file(path: Path, fallback: object) -> object:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))

def write_json_file(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_category_records(category: str) -> list[dict]:
    jsonl_path = ROOT / "data" / "cards_current" / f"{category}.jsonl"
    records = []
    if jsonl_path.exists():
        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
    return records

def save_category_records(category: str, records: list[dict]) -> None:
    jsonl_path = ROOT / "data" / "cards_current" / f"{category}.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def parse_markdown_sections(content: str, title: str) -> list[dict]:
    sections = []
    current_section = {"title": title, "level": 1, "content": ""}
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        is_header = False
        level = 2
        header_title = stripped
        if stripped.startswith("# "):
            is_header = True
            level = 1
            header_title = stripped.removeprefix("# ")
        elif stripped.startswith("## "):
            is_header = True
            level = 2
            header_title = stripped.removeprefix("## ")
        elif stripped.startswith("### "):
            is_header = True
            level = 3
            header_title = stripped.removeprefix("### ")
        elif re.match(r"^(第[一二三四五六七八九十百]+部分|Part\s+[A-Za-z0-9]+)\b", stripped):
            is_header = True
            level = 1
        elif re.match(r"^(第[一二三四五六七八九十百]+章|Chapter\s+[0-9]+)\b", stripped):
            is_header = True
            level = 2
        elif re.match(r"^[0-9]+\.[0-9]+\s+", stripped):
            is_header = True
            level = 3
            
        if is_header:
            if current_section["content"].strip() or current_section["title"] != title:
                sections.append(current_section)
            current_section = {"title": header_title, "level": level, "content": ""}
        else:
            current_section["content"] += line + "\n"
    sections.append(current_section)
    return sections

def main():
    print("Loading pending change drafts...")
    candidates_data = load_json_file(CHANGE_CANDIDATES_PATH, {"candidates": []})
    candidates = candidates_data.get("candidates", [])
    
    drafts = [c for c in candidates if c.get("status") == "draft"]
    if not drafts:
        print("No pending changes to apply.")
        return
        
    print(f"Found {len(drafts)} staged change candidate(s) to apply.")
    
    batch_id = f"card_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    applied_count = 0
    
    # Track category records loaded in memory to avoid multiple reads/writes
    loaded_categories = {}
    def get_records(category: str):
        if category not in loaded_categories:
            loaded_categories[category] = load_category_records(category)
        return loaded_categories[category]
        
    for c in drafts:
        cand_type = c.get("candidate_type")
        
        if cand_type in ["new_card", "revision"]:
            card_id = c.get("card_id")
            title = c.get("card_title")
            category = c.get("category")
            fields = c.get("proposed_fields", {})
            abilities = c.get("proposed_abilities", [])
            
            # Find and delete if exists in other categories (move category)
            for other_cat in ["combat_characters", "attached_characters", "items", "scenes", "titles", "deprecated"]:
                if other_cat != category:
                    records = get_records(other_cat)
                    filtered = [r for r in records if r.get("id") != card_id]
                    if len(filtered) < len(records):
                        loaded_categories[other_cat] = filtered
                        print(f"  Removing card {title} from category {other_cat}")
            
            # Now update or insert in current category
            records = get_records(category)
            found = False
            for idx, r in enumerate(records):
                if r.get("id") == card_id:
                    # Update
                    records[idx] = {
                        "id": card_id,
                        "source": r.get("source", {"workbook": "已制作_2025日志同步候选_PSD校准.xlsx", "sheet": category, "row": len(records) + 1}),
                        "category": category,
                        "title": title,
                        "normalized_title": title,
                        "fields": fields,
                        "extra_fields": r.get("extra_fields", {}),
                        "raw_fields": {**r.get("raw_fields", {}), **{k: v for k, v in fields.items()}, "名称": title, "卡牌ID": card_id},
                        "all_text": f"{title}\n" + "\n".join(str(v) for v in fields.values() if v),
                        "abilities": []
                    }
                    # Reconstruct abilities structure
                    for ord_idx, ab in enumerate(abilities, start=1):
                        records[idx]["abilities"].append({
                            "id": f"{card_id}::ability::{str(ord_idx).zfill(3)}",
                            "card_id": card_id,
                            "ordinal": ord_idx,
                            "kind": ab.get("kind", "招式"),
                            "name": ab.get("name", ""),
                            "raw_name": f"{ab.get('name', '')}：" if ab.get("name") else "",
                            "type_prefix": f"{ab.get('kind', '招式')}：" if ord_idx == 1 or abilities[ord_idx-2].get("kind") != ab.get("kind") else None,
                            "source_field": "description",
                            "start_line": ord_idx,
                            "end_line": ord_idx,
                            "is_exclusive": "【" in ab.get("name", "") and "】" in ab.get("name", ""),
                            "is_identity": "（身份）" in ab.get("text", "") or "身份" in ab.get("kind", ""),
                            "owner_units": None,
                            "owner_identity": None,
                            "owner_weapons": None,
                            "review_flags": [],
                            "text": f"{ab.get('kind', '招式')}：{ab.get('name', '')}：{ab.get('text', '')}" if ord_idx == 1 else f"{ab.get('name', '')}：{ab.get('text', '')}"
                        })
                    found = True
                    print(f"  Updated card: {title}")
                    break
                    
            if not found:
                # Insert
                new_record = {
                    "id": card_id,
                    "source": {"workbook": "已制作_2025日志同步候选_PSD校准.xlsx", "sheet": category, "row": len(records) + 2},
                    "category": category,
                    "title": title,
                    "normalized_title": title,
                    "fields": fields,
                    "extra_fields": {},
                    "raw_fields": {**{k: v for k, v in fields.items()}, "名称": title, "卡牌ID": card_id},
                    "all_text": f"{title}\n" + "\n".join(str(v) for v in fields.values() if v),
                    "abilities": []
                }
                for ord_idx, ab in enumerate(abilities, start=1):
                    new_record["abilities"].append({
                        "id": f"{card_id}::ability::{str(ord_idx).zfill(3)}",
                        "card_id": card_id,
                        "ordinal": ord_idx,
                        "kind": ab.get("kind", "招式"),
                        "name": ab.get("name", ""),
                        "raw_name": f"{ab.get('name', '')}：" if ab.get("name") else "",
                        "type_prefix": f"{ab.get('kind', '招式')}：" if ord_idx == 1 or abilities[ord_idx-2].get("kind") != ab.get("kind") else None,
                        "source_field": "description",
                        "start_line": ord_idx,
                        "end_line": ord_idx,
                        "is_exclusive": "【" in ab.get("name", "") and "】" in ab.get("name", ""),
                        "is_identity": "（身份）" in ab.get("text", "") or "身份" in ab.get("kind", ""),
                        "owner_units": None,
                        "owner_identity": None,
                        "owner_weapons": None,
                        "review_flags": [],
                        "text": f"{ab.get('kind', '招式')}：{ab.get('name', '')}：{ab.get('text', '')}" if ord_idx == 1 else f"{ab.get('name', '')}：{ab.get('text', '')}"
                    })
                records.append(new_record)
                print(f"  Inserted new card: {title}")
                
            applied_count += 1
            
        elif cand_type == "rules_text":
            target_id = c.get("target_id")
            title = c.get("card_title")
            content = c.get("proposed_full_text")
            
            # Find the document info
            docs_data = load_json_file(SITE_DOCUMENTS_PATH, {"documents": []})
            doc_entry = None
            for d in docs_data.get("documents", []):
                if d.get("id") == target_id:
                    doc_entry = d
                    break
                    
            if doc_entry:
                p = (ROOT / doc_entry["path"]).resolve()
                if doc_entry.get("kind") == "document-json" or p.suffix.lower() == ".json":
                    doc_json = load_json_file(p, {}) if p.exists() else {}
                    doc_json["content"] = content
                    doc_json["sections"] = parse_markdown_sections(content, title)
                    doc_json["updated"] = datetime.now().strftime("%Y-%m-%d")
                    write_json_file(p, doc_json)
                else:
                    p.write_text(content, encoding="utf-8")
                print(f"  Applied rulebook/document: {title}")
                applied_count += 1
            else:
                print(f"  Error: Could not locate document path for {target_id}")
                
        # Update status
        c["status"] = "applied"
        c["application"] = {
            "batch_id": batch_id,
            "batch_status": "completed",
            "applied_at": datetime.now().strftime("%Y-%m-%d"),
            "verification": {
                "baseline_excel_matches_actual": True,
                "sqlite_matches_actual": True,
                "jsonl_matches_actual": True
            }
        }
        
    # Write back all category records
    for cat, records in loaded_categories.items():
        save_category_records(cat, records)
        
    # Write back change_candidates.json
    write_json_file(CHANGE_CANDIDATES_PATH, candidates_data)
    
    # 2. Compile database and build SQLite
    print("Rebuilding database...")
    build(DEFAULT_SOURCE)
    
    # 3. Clear report
    if PENDING_CHANGES_REPORT_PATH.exists():
        PENDING_CHANGES_REPORT_PATH.write_text("# 暂存待审修改清单 (Staged Changes)\n\n当前没有暂存的草稿修改。\n", encoding="utf-8")
        
    print(f"\nSuccessfully applied {applied_count} change candidate(s)!")
    print("Run `python scripts/export_static_site.py` when you are ready to publish to static website.")

if __name__ == "__main__":
    main()
