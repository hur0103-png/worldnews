with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("v=17", "v=18")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
