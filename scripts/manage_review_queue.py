import json
import sqlite3
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

QUEUE_PATH = 'data/review/calibration_queue.json'
DB_PATH = 'data/cards.sqlite'

def load_queue():
    if not os.path.exists(QUEUE_PATH):
        print(f"Error: Queue file not found at {QUEUE_PATH}")
        sys.exit(1)
    with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queue(data):
    with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_card_text(title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT life, description FROM cards WHERE title = ?", (title,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"life": row[0], "description": row[1]}
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_review_queue.py [status | next | complete <name> | skip <name>]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'status':
        data = load_queue()
        print(f"=== Calibration Queue Status ===")
        print(f"Reviewed count: {len(data['reviewed'])}")
        print(f"Pending count:  {len(data['queue'])}")
        if data['reviewed']:
            print(f"Last reviewed:  {data['reviewed'][-1]}")
        if data['queue']:
            print(f"Up next:        {data['queue'][0]}")
            
    elif action == 'next':
        data = load_queue()
        if not data['queue']:
            print("No pending cards in the queue! Calibration complete!")
            sys.exit(0)
        next_card = data['queue'][0]
        print(f"NEXT_CARD_NAME: {next_card}")
        card_info = get_card_text(next_card)
        if card_info:
            print(f"Life: {card_info['life']}")
            print(f"Description:\n{card_info['description']}")
        else:
            print(f"Warning: Card '{next_card}' text not found in database!")

    elif action == 'complete':
        if len(sys.argv) < 3:
            print("Error: Please specify the card name to complete.")
            sys.exit(1)
        card_name = sys.argv[2]
        data = load_queue()
        
        # Remove from queue if present
        in_queue = False
        if card_name in data['queue']:
            data['queue'].remove(card_name)
            in_queue = True
            
        # Add to reviewed if not already present
        if card_name not in data['reviewed']:
            data['reviewed'].append(card_name)
            
        save_queue(data)
        if in_queue:
            print(f"Successfully moved '{card_name}' from pending to reviewed.")
        else:
            print(f"'{card_name}' was not in the pending queue, but marked as reviewed.")
            
    elif action == 'skip':
        if len(sys.argv) < 3:
            print("Error: Please specify the card name to skip.")
            sys.exit( Third)
        card_name = sys.argv[2]
        data = load_queue()
        if card_name in data['queue']:
            data['queue'].remove(card_name)
            data['queue'].append(card_name) # Move to the end of queue
            save_queue(data)
            print(f"Moved '{card_name}' to the end of the pending queue.")
        else:
            print(f"Card '{card_name}' not in the pending queue.")
            
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()
