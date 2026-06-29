import re

with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix polling logic
fixed_poll = """
let progressInterval = null;
let pollWaitTicks = 0;

function startProgressPolling() {
    if (progressInterval) return;
    
    const container = document.getElementById('progressContainer');
    const msg = document.getElementById('progressMessage');
    const time = document.getElementById('progressTime');
    const bar = document.getElementById('progressBar');
    const pct = document.getElementById('progressPercent');
    
    // Show immediately
    if (container) container.style.display = 'flex';
    if (msg) msg.textContent = '뉴스 수집을 준비 중입니다... (연결 대기중)';
    pollWaitTicks = 0;
    
    progressInterval = setInterval(async () => {
        try {
            const resp = await fetch('/api/progress');
            const data = await resp.json();
            
            if (data.is_running) {
                pollWaitTicks = 100; // it started running!
                if (container) container.style.display = 'flex';
                if (msg) msg.textContent = data.message || '뉴스 수집 중...';
                if (bar) bar.style.width = data.percent + '%';
                if (pct) pct.textContent = data.percent + '%';
                
                if (data.time_remaining > 0) {
                    if (time) time.textContent = `남은 시간: 약 ${data.time_remaining}초`;
                } else {
                    if (time) time.textContent = '마무리 중...';
                }
                
                if (data.percent >= 100) {
                    stopProgressPolling(container, true);
                }
            } else {
                // If it's not running, maybe it hasn't started yet.
                pollWaitTicks++;
                // Stop only if we waited more than 5 ticks and it's still not running
                if (pollWaitTicks > 5) {
                    stopProgressPolling(container, false);
                }
            }
        } catch (e) {
            console.error("Progress poll error", e);
        }
    }, 1000);
}
"""

js = re.sub(r'let progressInterval = null;\n\nfunction startProgressPolling\(\) \{.*?\n\}\n', fixed_poll, js, flags=re.DOTALL)

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)
