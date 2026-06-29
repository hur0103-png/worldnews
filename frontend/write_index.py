content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World News Clipper - 글로벌 경제/외교 인사이트</title>
    <meta name="description" content="전 세계 100대 매체의 핵심 뉴스를 큐레이션하여 제공합니다.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css?v=16">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header header-container">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">🌍</span>
                    <h1>World News Clipper</h1>
                </div>
                <div class="header-controls">
                    <input type="date" id="datePicker" class="date-picker">
                </div>
                <div class="header-actions">
                    <button id="triggerBtn" class="btn btn-primary" title="새로운 뉴스 수집">
                        수동 업데이트
                    </button>
                </div>
            </div>
        </div>

        <!-- Main Grid -->
        <div id="newsGrid" class="news-grid">
            <!-- News cards will be dynamically injected here -->
        </div>

        <!-- Detail View -->
        <div id="newsDetail" class="news-detail" style="display: none;">
            <button id="backBtn" class="btn btn-outline back-btn">&larr; 목록으로 돌아가기</button>
            
            <h2 id="detailTitle" class="detail-title">뉴스 제목</h2>
            <div id="detailSummary" class="detail-summary">
                뉴스 요약 내용...
            </div>
            <div id="detailSource" class="news-source" style="display: none;"></div>
            <div id="detailImpact" class="detail-impact" style="display: none;"></div>
            <div class="detail-footer">
                <a id="detailLink" href="#" target="_blank" class="btn btn-primary">원문 기사 보러가기</a>
            </div>
        </div>
    </div>
    <script src="app.js?v=16"></script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
