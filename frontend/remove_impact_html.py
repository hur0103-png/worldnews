import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove detailImpact div
html = html.replace('<div id="detailImpact" class="detail-impact" style="display: none;"></div>', '')
html = html.replace('v=19', 'v=20')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
