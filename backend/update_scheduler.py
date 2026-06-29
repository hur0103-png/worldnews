import threading

with open("scheduler.py", "r", encoding="utf-8") as f:
    code = f.read()

new_logic = """import threading
is_running = False
is_running_lock = threading.Lock()

def run_news_pipeline():
    global is_running
    with is_running_lock:
        if is_running:
            print(f"[{datetime.now()}] Pipeline is already running. Skipping...")
            return
        is_running = True
        
    try:
        print(f"[{datetime.now()}] Starting news pipeline...")
        # 1. Fetch news
        raw_news = crawler.fetch_latest_news()
        print(f"Fetched {len(raw_news)} raw news items.")
        
        # 2. Process with Gemini
        processed_news = ai_agent.run_ai_analysis(raw_news)
        print(f"Processed {len(processed_news)} news items via Gemini.")
        
        # 3. Save to database
        database.insert_news(processed_news)
        print("Saved to database successfully.")
    finally:
        with is_running_lock:
            is_running = False
"""

# Replace the old def run_news_pipeline
import re
code = re.sub(r'def run_news_pipeline\(\):.*?print\("Saved to database successfully."\)', new_logic, code, flags=re.DOTALL)

with open("scheduler.py", "w", encoding="utf-8") as f:
    f.write(code)
