import re

with open("main.py", "r", encoding="utf-8") as f:
    code = f.read()

if "import progress" not in code:
    code = code.replace("import database", "import database\nimport progress")

new_endpoint = """@app.get("/api/progress")
def get_progress():
    return progress.get_progress()

@app.post("/api/trigger")"""

code = code.replace('@app.post("/api/trigger")', new_endpoint)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(code)
