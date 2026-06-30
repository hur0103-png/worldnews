import re

with open("ai_agent.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace generate_dummy_news fallback with returning an empty list
code = code.replace("return generate_dummy_news(news_items)", "return []")

with open("ai_agent.py", "w", encoding="utf-8") as f:
    f.write(code)
