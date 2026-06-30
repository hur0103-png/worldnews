import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove the button with id="triggerBtn"
html = re.sub(r'<button id="triggerBtn".*?</button>', '', html, flags=re.DOTALL)

# Bump version to clear cache
html = re.sub(r'app\.js\?v=\d+', 'app.js?v=30', html)
html = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=30', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
