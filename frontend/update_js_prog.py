import re

with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add polling functions
polling_funcs = """
let progressInterval = null;

function startProgressPolling() {
    if (progressInterval) return;
    
    const container = document.getElementById('progressContainer');
    const msg = document.getElementById('progressMessage');
    const time = document.getElementById('progressTime');
    const bar = document.getElementById('progressBar');
    const pct = document.getElementById('progressPercent');
    
    progressInterval = setInterval(async () => {
        try {
            const resp = await fetch('/api/progress');
            const data = await resp.json();
            
            if (data.is_running) {
                container.style.display = 'flex';
                msg.textContent = data.message || '뉴스 수집 중...';
                bar.style.width = data.percent + '%';
                pct.textContent = data.percent + '%';
                
                if (data.time_remaining > 0) {
                    time.textContent = `남은 시간: 약 ${data.time_remaining}초`;
                } else {
                    time.textContent = '마무리 중...';
                }
                
                if (data.percent >= 100) {
                    stopProgressPolling(container, true);
                }
            } else {
                stopProgressPolling(container, false);
            }
        } catch (e) {
            console.error("Progress poll error", e);
        }
    }, 1000);
}

function stopProgressPolling(container, wasRunning) {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    if (wasRunning) {
        setTimeout(() => {
            if (container) container.style.display = 'none';
            // Refresh news if we are looking at today
            const dp = document.getElementById('datePicker');
            if (dp && dp.value) {
                fetchNews(dp.value);
            }
        }, 3000);
    } else {
        if (container) container.style.display = 'none';
    }
}
"""

if "startProgressPolling" not in js:
    js = polling_funcs + "\n" + js

# Call startProgressPolling on DOMContentLoaded
js = js.replace("fetchNews(todayStr);", "fetchNews(todayStr);\n    startProgressPolling();")

# Call startProgressPolling on manual trigger
js = js.replace("alert('뉴스 수집이 백그라운드에서 시작되었습니다. 약 2~3분 뒤 새로고침 해주세요.');", 
                "startProgressPolling();")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)
