with open("main.py", "r", encoding="utf-8") as f:
    code = f.read()

new_endpoint = """
@app.get("/api/available-dates")
def get_available_dates():
    dates = database.get_available_dates()
    return {"status": "success", "data": dates}

@app.post("/api/trigger")
"""

if "@app.get(\"/api/available-dates\")" not in code:
    code = code.replace("@app.post(\"/api/trigger\")", new_endpoint)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(code)
