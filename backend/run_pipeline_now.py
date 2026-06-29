import ai_agent
import crawler
import database

print("Fetching news...")
news = crawler.fetch_latest_news()
print(f"Fetched {len(news)} items.")

print("Running AI...")
try:
    res = ai_agent.select_and_translate_news(news)
    print(f"Result length: {len(res)}")
    database.insert_news(res)
    print("Inserted into DB.")
except Exception as e:
    print(f"Error: {e}")
