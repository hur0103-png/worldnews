with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove the button
html = html.replace('<button onclick="triggerPipeline()" class="btn-refresh">🔄 수동 업데이트</button>', '')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
