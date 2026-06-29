import re

app_js_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

old_impact_logic = """            impactContainer.innerHTML = `
                <h3 class="impact-title">AI Market Impact Analysis</h3>
                <div class="impact-content">${news.impact_analysis}</div>
            `;"""

new_impact_logic = """            let impactHtml = '';
            try {
                const impactObj = JSON.parse(news.impact_analysis);
                for (const [key, value] of Object.entries(impactObj)) {
                    impactHtml += `<h4>${key}</h4>`;
                    if (Array.isArray(value)) {
                        impactHtml += `<ul>${value.map(v => `<li>${v}</li>`).join('')}</ul>`;
                    } else {
                        impactHtml += `<p>${value}</p>`;
                    }
                }
            } catch (jsonError) {
                impactHtml = news.impact_analysis.replace(/\\n/g, '<br>');
            }
            
            impactContainer.innerHTML = `
                <h3 class="impact-title">AI Market Impact Analysis</h3>
                <div class="impact-content">${impactHtml}</div>
            `;"""

if "let impactHtml =" not in app_js:
    app_js = app_js.replace(old_impact_logic, new_impact_logic)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)

# Update CSS for h4 and ul
css_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
.impact-content h4 {
    color: #94a3b8;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-size: 1.15rem;
}
.impact-content ul {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}
.impact-content li {
    margin-bottom: 0.3rem;
}
"""
if ".impact-content h4" not in css:
    css += new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Cache bust
html_path = r'C:\Users\PC\.gemini\antigravity\worldnews\frontend\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'app\.js\?v=\d+', 'app.js?v=7', html)
html = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=7', html)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated JS and CSS for JSON impact_analysis rendering.")
