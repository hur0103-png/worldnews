import sqlite3
import time

db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("Waiting for database to populate...")
for _ in range(60):
    c.execute("SELECT count(*) FROM news")
    count = c.fetchone()[0]
    if count > 0:
        print(f"Success! Found {count} items.")
        break
    time.sleep(2)
else:
    print("Timeout waiting for data.")
conn.close()
