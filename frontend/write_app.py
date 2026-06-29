content = """let allNews = [];

document.addEventListener('DOMContentLoaded', () => {
    const datePicker = document.getElementById('datePicker');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    datePicker.value = `${yyyy}-${mm}-${dd}`;
    
    fetchNews(datePicker.value);
    
    datePicker.addEventListener('change', (e) => fetchNews(e.target.value));
    
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
        
        document.getElementById('datePicker').value = todayStr;
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
        fetchNews(todayStr);
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

    const impactContainer = document.getElementById('detailImpact');
    try {
        if (news.impact_analysis && news.impact_analysis.trim() !== '') {
            impactContainer?.style?.setProperty('display', 'block');
            let impactHtml = '';
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
                impactHtml = news.impact_analysis.replace(/\n/g, '<br>');
            }
            
            impactContainer.innerHTML = `
                <h3 class="impact-title">AI Market Impact Analysis</h3>
                <div class="impact-content">${impactHtml}</div>
            `;
        } else {
            impactContainer?.style?.setProperty('display', 'none');
        }
    } catch (e) {
        console.error("Failed to render impact analysis", e);
        if(impactContainer) impactContainer.style.display = 'none';
    }
    
    detail.style.display = 'block';
    window.scrollTo(0, 0);
}

function closeDetail() {
    document.getElementById('newsDetail').style.display = 'none';
    document.getElementById('newsGrid').style.display = 'flex';
    window.scrollTo(0, savedScrollY);
}
"""

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)
