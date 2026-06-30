import re

with open("ai_agent.py", "r", encoding="utf-8") as f:
    code = f.read()

new_api_check = """
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
"""

code = code.replace("""    api_key = os.environ.get("GOOGLE_API_KEY")\n    if not api_key:""", new_api_check.strip('\n'))

with open("ai_agent.py", "w", encoding="utf-8") as f:
    f.write(code)
