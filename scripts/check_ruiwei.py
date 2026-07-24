import sqlite3
import json

conn = sqlite3.connect('data/cards.sqlite')
c = conn.cursor()
c.execute('SELECT life, title, description FROM cards WHERE title = ?', ('芮伟',))
row = c.fetchone()
print("Rui Wei raw SQL row:")
print(row)
conn.close()
