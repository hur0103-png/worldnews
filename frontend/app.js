

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

let allNews = [];

document.addEventListener('DOMContentLoaded', async () => {
    const datePicker = document.getElementById('datePicker');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayStr = `${yyyy}-${mm}-${dd}`;
    
    let availableDates = [];
    try {
        const resp = await fetch('/api/available-dates');
        const data = await resp.json();
        if (data.status === 'success') {
            availableDates = data.data;
        }
    } catch (e) {
        console.error("Failed to fetch available dates", e);
    }

    flatpickr(datePicker, {
        defaultDate: todayStr,
        onChange: function(selectedDates, dateStr, instance) {
            fetchNews(dateStr);
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const dateObj = dayElem.dateObj;
            const y = dateObj.getFullYear();
            const m = String(dateObj.getMonth() + 1).padStart(2, '0');
            const d = String(dateObj.getDate()).padStart(2, '0');
            const cellDateStr = `${y}-${m}-${d}`;
            
            if (availableDates.includes(cellDateStr)) {
                dayElem.classList.add('has-news');
            }
        }
    });
    
    fetchNews(todayStr);
    startProgressPolling();
    
    document.getElementById('triggerBtn').addEventListener('click', () => {
        if(confirm('새로운 뉴스를 강제로 수집하시겠습니까? (Gemini API 호출 발생)')) {
            triggerPipeline();
        }
    });
    
    document.getElementById('backBtn').addEventListener('click', closeDetail);
    document.querySelector('.logo').addEventListener('click', () => {
        closeDetail();
        
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        const todayStr = `${yyyy}-${mm}-${dd}`;
        
        document.getElementById('datePicker')._flatpickr.setDate(todayStr);
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
        fetchNews(todayStr);
    startProgressPolling();
    });
});

async function fetchNews(date) {
    const grid = document.getElementById('newsGrid');
    grid.innerHTML = '<div class="loading">뉴스를 불러오는 중입니다...</div>';
    
    try {
        const response = await fetch(`/api/news?date=${date}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            allNews = data.data;
            renderNews();
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        grid.innerHTML = `<div class="empty-state">뉴스 데이터를 불러오는데 실패했습니다.<br>${error.message}</div>`;
        console.error(error);
    }
}

async function triggerPipeline() {
    try {
        const response = await fetch('/api/trigger', { method: 'POST' });
        const data = await response.json();
        alert('백그라운드에서 뉴스 수집이 시작되었습니다. 잠시 후 새로고침 해보세요.');
    } catch (error) {
        alert('업데이트 시작 실패!');
    }
}

function renderNews() {
    const grid = document.getElementById('newsGrid');
    grid.innerHTML = '';
    allNews = allNews.slice(0, 30);

    let filteredNews = allNews;
    
    if (filteredNews.length === 0) {
        grid.innerHTML = '<div class="empty-state">해당 날짜의 뉴스가 없습니다.</div>';
        return;
    }
    
    filteredNews.forEach((news, index) => {
        const card = document.createElement('div');
        card.className = 'news-card';
        card.onclick = () => openModal(news);
        
        let displayDate = news.published_date || '';
        if (displayDate) {
            const dateObj = new Date(displayDate);
            if (!isNaN(dateObj)) {
                const hours = String(dateObj.getHours()).padStart(2, '0');
                const minutes = String(dateObj.getMinutes()).padStart(2, '0');
                displayDate = `${hours}:${minutes}`;
            }
        }
        
        card.innerHTML = `
            <h3 class="card-title">
                ${index + 1}. ${news.translated_title || news.original_title}
                <span class="title-date">${displayDate}</span>
            </h3>
        `;
        
        grid.appendChild(card);
    });
}

let savedScrollY = 0;

function openModal(news) {
    savedScrollY = window.scrollY;
    
    document.getElementById('newsGrid').style.display = 'none';
    const detail = document.getElementById('newsDetail');
    
    document.getElementById('detailTitle').textContent = news.translated_title || news.original_title;
    
    let summaryText = news.summary || '요약이 없습니다.';
    let sourceText = '';
    const sourceIndex = summaryText.lastIndexOf('출처:');
    if (sourceIndex !== -1) {
        sourceText = summaryText.substring(sourceIndex);
        summaryText = summaryText.substring(0, sourceIndex).trim();
    }
    
    document.getElementById('detailSummary').textContent = summaryText;
    
    const sourceEl = document.getElementById('detailSource');
    if (sourceEl) {
        sourceEl.textContent = sourceText;
        sourceEl.style.display = sourceText ? 'block' : 'none';
    }
    
    document.getElementById('detailLink').href = news.original_url;

    detail.style.display = 'block';
    window.scrollTo(0, 0);
}

function closeDetail() {
    document.getElementById('newsDetail').style.display = 'none';
    document.getElementById('newsGrid').style.display = 'flex';
    window.scrollTo(0, savedScrollY);
}


document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') === '1') {
        const triggerBtn = document.getElementById('triggerBtn');
        if (triggerBtn) {
            triggerBtn.style.display = 'inline-block';
        }
    }
});
