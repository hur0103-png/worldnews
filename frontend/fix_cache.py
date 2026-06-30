with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add cache buster to fetch calls
js = js.replace("fetch('/api/available-dates')", "fetch(`/api/available-dates?t=${new Date().getTime()}`)")
js = js.replace("fetch(`/api/news?date=${date}`)", "fetch(`/api/news?date=${date}&t=${new Date().getTime()}`)")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace("v=32", "v=33")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
