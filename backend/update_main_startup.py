import re

with open("main.py", "r", encoding="utf-8") as f:
    code = f.read()

new_startup = """import threading
from datetime import datetime

@app.on_event("startup")
def on_startup():
    database.init_db()
    scheduler.start_scheduler()
    
    # Auto-fetch on startup if no news exists for today
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_news = database.get_news_by_date(today_str)
    if not today_news:
        print(f"[{datetime.now()}] No news found for today ({today_str}). Starting automatic catch-up fetch...")
        threading.Thread(target=scheduler.run_news_pipeline).start()
"""

code = re.sub(r'@app\.on_event\("startup"\)\ndef on_startup\(\):\n    database\.init_db\(\)\n    scheduler\.start_scheduler\(\)', new_startup, code)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(code)
