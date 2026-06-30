with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the current triggerBtn with the correct one containing onclick
html = html.replace(
    '<button id="triggerBtn" class="btn btn-primary" title="새로운 뉴스 수집" style="display: none; margin-left: 10px;">🔄 수동 업데이트</button>',
    '<button id="triggerBtn" class="btn btn-primary" onclick="triggerPipeline()" title="수동 업데이트" style="display: none; margin-left: 10px; background-color: #007bff; color: white;">🔄 수동 업데이트</button>'
)

# Bump version again
html = html.replace("v=31", "v=32")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
