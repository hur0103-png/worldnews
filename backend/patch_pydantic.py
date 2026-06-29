import re

pydantic_file = r'C:\Users\PC\.gemini\antigravity\worldnews\backend\venv\Lib\site-packages\pydantic\_internal\_typing_extra.py'
with open(pydantic_file, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("prefer_fwd_module=True,", "")

with open(pydantic_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched pydantic.")
