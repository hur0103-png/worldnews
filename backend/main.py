import typing
if hasattr(typing, '_eval_type'):
    _orig = typing._eval_type
    def _patched(*args, **kwargs):
        kwargs.pop('prefer_fwd_module', None)
        return _orig(*args, **kwargs)
    typing._eval_type = _patched

from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import database
import progress
import scheduler
import crawler
import ai_agent

load_dotenv()

app = FastAPI(title="World News Clipper API")

# Setup CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading
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


@app.get("/api/news")
def get_news(date: str):
    # date format expected: YYYY-MM-DD
    news = database.get_news_by_date(date)
    return {"status": "success", "date": date, "data": news}


@app.get("/api/available-dates")
def get_available_dates():
    dates = database.get_available_dates()
    return {"status": "success", "data": dates}

@app.get("/api/progress")
def get_progress():
    return progress.get_progress()

@app.post("/api/trigger")

def trigger_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(scheduler.run_news_pipeline)
    return {"status": "success", "message": "Pipeline triggered in background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)


# Serve static files
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, 'frontend')
if os.path.exists(frontend_path):
    app.mount('/', StaticFiles(directory=frontend_path, html=True), name='frontend')
