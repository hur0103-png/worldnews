import re

# 1. Update index.html
html_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

summary_div = '<div id="detailSummary" class="detail-summary">\n            뉴스 요약 내용...\n        </div>'
new_summary_div = summary_div + '\n        <div id="detailImpact" class="detail-impact" style="display: none;"></div>'

html = html.replace(summary_div, new_summary_div)
html = re.sub(r'app\.js\?v=\d+', 'app.js?v=6', html)
html = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=6', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.js
app_js_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

old_open_modal = """    document.getElementById('detailTitle').textContent = news.translated_title || news.original_title;
    document.getElementById('detailSummary').textContent = news.summary || '요약 내용이 없습니다.';
    document.getElementById('detailLink').href = news.original_url;"""

new_open_modal = """    document.getElementById('detailTitle').textContent = news.translated_title || news.original_title;
    document.getElementById('detailSummary').textContent = news.summary || '요약 내용이 없습니다.';
    document.getElementById('detailLink').href = news.original_url;

    // Defensive rendering of AI Market Impact Analysis
    const impactContainer = document.getElementById('detailImpact');
    try {
        if (news.impact_analysis && news.impact_analysis.trim() !== '') {
            impactContainer?.style?.setProperty('display', 'block');
            impactContainer.innerHTML = `
                <h3 class="impact-title">AI Market Impact Analysis</h3>
                <div class="impact-content">${news.impact_analysis}</div>
            `;
        } else {
            impactContainer?.style?.setProperty('display', 'none');
        }
    } catch (e) {
        console.error("Failed to render impact analysis", e);
        if(impactContainer) impactContainer.style.display = 'none';
    }"""

app_js = app_js.replace(old_open_modal, new_open_modal)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)

# 3. Update styles.css
css_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_styles = """
/* AI Impact Analysis */
.detail-impact {
    background: rgba(15, 23, 42, 0.6);
    border-left: 4px solid var(--primary);
    padding: 1.5rem 2rem;
    border-radius: 0 12px 12px 0;
    margin-bottom: 3rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.impact-title {
    color: #60a5fa;
    font-size: 1.3rem;
    margin-bottom: 1.2rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.impact-title::before {
    content: '⚡';
    font-size: 1.2rem;
}

.impact-content {
    color: #f1f5f9;
    font-size: 1.1rem;
    line-height: 1.8;
    white-space: pre-wrap;
}
"""

css += new_styles

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated frontend for impact_analysis.")
