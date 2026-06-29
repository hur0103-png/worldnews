import asyncio
from crawler import fetch_latest_news
from ai_agent import run_ai_analysis
from database import insert_news

print("Fetching news...")
news_items = fetch_latest_news()
print("Running AI...")
processed_news = run_ai_analysis(news_items)
print("Inserting into DB...")
insert_news(processed_news)
print("Done!")
