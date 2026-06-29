import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("DELETE FROM news WHERE translated_title LIKE '%테스트 뉴스 제목%'")
deleted = c.rowcount
conn.commit()
print(f"Deleted {deleted} dummy news items.")
conn.close()
