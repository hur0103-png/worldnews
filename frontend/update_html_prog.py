import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

progress_ui = """
    <!-- Progress Bar UI (Initially Hidden) -->
    <div id="progressContainer" class="progress-container" style="display: none;">
        <div class="progress-status">
            <span id="progressMessage">뉴스 수집을 준비 중입니다...</span>
            <span id="progressTime" class="progress-time">남은 시간: 계산 중</span>
        </div>
        <div class="progress-bar-bg">
            <div id="progressBar" class="progress-bar-fill"></div>
        </div>
        <div id="progressPercent" class="progress-percent">0%</div>
    </div>
"""

# Insert progress UI right before the news-grid
if "progressContainer" not in html:
    html = html.replace('<div id="newsGrid"', progress_ui + '\n    <div id="newsGrid"')

html = html.replace('v=20', 'v=21')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
