import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT DATE(created_at), count(*) FROM news GROUP BY DATE(created_at)")
print(c.fetchall())
conn.close()
