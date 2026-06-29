import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT translated_title, summary FROM news ORDER BY id DESC LIMIT 2")
for row in c.fetchall():
    print(f"Title: {row[0]}")
    print(f"Summary: {row[1][:100]}...\n")
conn.close()
