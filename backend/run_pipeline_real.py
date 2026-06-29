import os
from dotenv import load_dotenv
load_dotenv()
from crawler import fetch_latest_news
from ai_agent import run_ai_analysis
from database import insert_news
import sqlite3

db_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\worldnews.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
conn.commit()
conn.close()

print("Fetching news...")
news_items = fetch_latest_news()
print("Running AI with REAL key...")
processed_news = run_ai_analysis(news_items)
print(f"Generated {len(processed_news)} news items.")
print("Inserting into DB...")
insert_news(processed_news)
print("Done!")