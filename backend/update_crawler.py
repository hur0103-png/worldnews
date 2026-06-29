import re

crawler_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\crawler.py'
with open(crawler_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Add imports
if 'import email.utils' not in code:
    code = "import email.utils\nfrom datetime import datetime, timezone, timedelta\n" + code

old_loop = """            for entry in feed.entries[:20]: # Top 20 from each feed
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                
                # Basic summary cleanup"""

new_loop = """            for entry in feed.entries[:20]: # Top 20 from each feed
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                
                # Filter old news (older than 36 hours to be safe with timezones)
                try:
                    if published:
                        pub_dt = email.utils.parsedate_to_datetime(published)
                        now = datetime.now(timezone.utc)
                        if now - pub_dt > timedelta(hours=36):
                            continue # Skip this old article
                except Exception as parse_e:
                    pass # If date parsing fails, let it pass rather than dropping everything
                
                # Basic summary cleanup"""

if "email.utils.parsedate_to_datetime" not in code:
    code = code.replace(old_loop, new_loop)

with open(crawler_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated crawler.py with datetime filter.")
