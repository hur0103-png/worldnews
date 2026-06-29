import re

# 1. Update app.js
app_js_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

old_card_html = """        card.innerHTML = `
            <h3 class="card-title">${index + 1}. ${news.translated_title || news.original_title}</h3>
        `;"""

new_card_html = """        let displayDate = news.published_date || '';
        if (displayDate.length > 25) {
            displayDate = new Date(displayDate).toLocaleString();
        }
        
        card.innerHTML = `
            <h3 class="card-title">
                ${index + 1}. ${news.translated_title || news.original_title}
                <span class="title-date">${displayDate}</span>
            </h3>
        `;"""

app_js = app_js.replace(old_card_html, new_card_html)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)

# 2. Update styles.css
css_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
.title-date {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 400;
    margin-left: 0.8rem;
    background: rgba(255,255,255,0.05);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    vertical-align: middle;
    display: inline-block;
}
"""
if ".title-date" not in css:
    css += new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Cache bust
html_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'app\.js\?v=\d+', 'app.js?v=8', html)
html = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=8', html)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Added title-date to UI.")
