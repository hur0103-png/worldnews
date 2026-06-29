import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT translated_title, summary FROM news ORDER BY id DESC LIMIT 1")
row = c.fetchone()
if row:
    print(f"Title: {row[0].encode('utf-8', 'replace').decode('utf-8')}")
    print(f"Summary: {row[1].encode('utf-8', 'replace').decode('utf-8')}")
conn.close()
