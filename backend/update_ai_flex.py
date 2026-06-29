import re

ai_path = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\ai_agent.py'
with open(ai_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Stage 1 modifications
code = code.replace("2. Select EXACTLY 45 news items", "2. Select UP TO 45 news items (or all available if there are fewer than 45)")
code = code.replace('List of exactly 45 selected news', 'List of selected news (up to 45)')

# Stage 2 modifications
code = code.replace("select the top 30 most critical items", "select UP TO 30 most critical items (or all if there are fewer than 30)")
code = code.replace("For each of the final 30 items:", "For each of the final items:")

old_s2_rule4 = "4. Categorize each item as either 'Economy' or 'Diplomacy/Politics'. Select exactly 30 items total based purely on their overall importance, regardless of category ratio."
new_s2_rule4 = "4. Categorize each item as either 'Economy' or 'Diplomacy/Politics'. Select UP TO 30 items total (or all available) based purely on their overall importance, regardless of category ratio."
code = code.replace(old_s2_rule4, new_s2_rule4)

# Dummy update
old_dummy_len = "for i in range(30):"
new_dummy_len = "for i in range(min(30, len(news_items))):"
code = code.replace(old_dummy_len, new_dummy_len)

with open(ai_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated ai_agent.py for flexible item counts.")
