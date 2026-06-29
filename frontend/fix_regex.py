with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix the broken regex syntax
js = js.replace("news.impact_analysis.replace(/\n/g, '<br>');", r"news.impact_analysis.replace(/\n/g, '<br>');")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)
