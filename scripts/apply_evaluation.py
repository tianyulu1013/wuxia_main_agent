import json
import os
import sys

def main():
    db_path = 'data/review/card_evaluations.json'
    payload_path = 'data/review/eval_payload.json'
    
    if not os.path.exists(payload_path):
        print(f"Error: Payload file {payload_path} not found")
        sys.exit(1)
        
    if not os.path.exists(db_path):
        print(f"Error: DB file {db_path} not found")
        sys.exit(1)
        
    with open(payload_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
        
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    updates_count = 0
    for update in payload:
        title = update.get('card_title')
        strength = update.get('strength_score')
        generality = update.get('generality_score')
        full_text = update.get('full_text')
        
        found = False
        for entry in db['entries']:
            if entry['card_title'] == title:
                if strength is not None:
                    entry['strength_score'] = strength
                if generality is not None:
                    entry['generality_score'] = generality
                if full_text is not None:
                    entry['full_text'] = full_text
                found = True
                updates_count += 1
                print(f"Successfully updated evaluations DB entry for: {title}")
                break
        if not found:
            print(f"Warning: Card '{title}' not found in evaluations DB")
            
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    # Clean up the payload file to prevent re-running
    try:
        os.remove(payload_path)
        print("Cleaned up payload file.")
    except Exception as e:
        print(f"Warning: Could not clean up payload file: {e}")
        
    print(f"Done. Applied {updates_count} updates.")

if __name__ == '__main__':
    main()
