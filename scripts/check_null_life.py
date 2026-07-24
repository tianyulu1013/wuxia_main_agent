import sqlite3
import sys

conn = sqlite3.connect('data/cards.sqlite')
c = conn.cursor()
c.execute('SELECT title, life FROM cards WHERE category = ? AND (life IS NULL OR life = ?)', ('combat_characters', ''))
res = []
for row in c.fetchall():
    res.append(f"{row[0]}: {row[1]}")
    
sys.stdout.buffer.write(('\n'.join(res)).encode('utf-8'))
conn.close()
