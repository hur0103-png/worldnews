import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT translated_title FROM news ORDER BY id DESC LIMIT 5")
for row in c.fetchall():
    print(row[0])
conn.close()
