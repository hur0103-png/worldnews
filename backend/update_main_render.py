import re

with open("main.py", "r", encoding="utf-8") as f:
    code = f.read()

# Update port binding
code = code.replace('port=8000', 'port=int(os.environ.get("PORT", 8000))')

# Update frontend_path to be dynamic
new_frontend = """
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, 'frontend')
"""
code = re.sub(r'frontend_path = r\'c:\\Users\\PC\\\.gemini\\antigravity\\worldnews\\frontend\'', new_frontend.strip(), code)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(code)
