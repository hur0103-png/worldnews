import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

button_html = '<button id="triggerBtn" class="btn btn-primary" title="새로운 뉴스 수집" style="display: none; margin-left: 10px;">🔄 수동 업데이트</button>'

# Find the header-controls and add the button inside it
html = re.sub(
    r'(<div class="header-controls">[\s\S]*?<input type="text" id="datePicker".*?>)',
    rf'\1\n                    {button_html}',
    html
)

# Bump version
html = re.sub(r'app\.js\?v=\d+', 'app.js?v=31', html)
html = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=31', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update app.js
with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add DOMContentLoaded logic to check URL params
admin_check_js = """
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') === '1') {
        const triggerBtn = document.getElementById('triggerBtn');
        if (triggerBtn) {
            triggerBtn.style.display = 'inline-block';
        }
    }
});
"""

# Append to app.js if not already there
if "urlParams.get('admin')" not in js:
    js += "\n" + admin_check_js

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)
