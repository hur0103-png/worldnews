import sqlite3
db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("DELETE FROM news")
conn.commit()
print("Wiped database again to clear dummy news.")
conn.close()
