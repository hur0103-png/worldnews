import re

with open("scheduler.py", "r", encoding="utf-8") as f:
    code = f.read()

# Add import progress
if "import progress" not in code:
    code = code.replace("import database", "import database\nimport progress")

# Modify run_news_pipeline
new_func = """def run_news_pipeline():
    global is_running
    with is_running_lock:
        if is_running:
            print(f"[{datetime.now()}] Pipeline is already running. Skipping...")
            return
        is_running = True
        
    try:
        progress.update_progress(is_running=True, percent=0, message="수집 초기화 중...", time_remaining=150)
        print(f"[{datetime.now()}] Starting news pipeline...")
        
        # 1. Fetch news
        progress.update_progress(percent=5, message="전 세계 48개 매체에서 실시간 속보 수집 중...", time_remaining=145)
        raw_news = crawler.fetch_latest_news()
        print(f"Fetched {len(raw_news)} raw news items.")
        
        # 2. Process with Gemini
        progress.update_progress(percent=15, message="AI가 가장 파급력 높은 뉴스를 선별 중...", time_remaining=130)
        processed_news = ai_agent.run_ai_analysis(raw_news)
        print(f"Processed {len(processed_news)} news items via Gemini.")
        
        # 3. Save to database
        progress.update_progress(percent=95, message="분석 완료. 데이터베이스 저장 중...", time_remaining=5)
        database.insert_news(processed_news)
        print("Saved to database successfully.")
        
        progress.update_progress(percent=100, message="수집 완료!", time_remaining=0)
    except Exception as e:
        progress.update_progress(percent=100, message=f"오류 발생: {str(e)[:50]}", time_remaining=0)
        print(f"Error in pipeline: {e}")
    finally:
        with is_running_lock:
            is_running = False
        import time
        time.sleep(3) # Let UI show 100% for 3 seconds before resetting
        progress.update_progress(is_running=False, percent=0, message="대기 중", time_remaining=0)"""

code = re.sub(r'def run_news_pipeline\(\):.*?(?=def start_scheduler)', new_func + '\n\n', code, flags=re.DOTALL)

with open("scheduler.py", "w", encoding="utf-8") as f:
    f.write(code)
