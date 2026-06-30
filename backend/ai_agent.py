import os
import json
import time
import progress
from datetime import datetime
from google import genai

def run_ai_analysis(news_items):
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set. Using dummy data for testing.")
        return generate_dummy_news(news_items)
        
    client = genai.Client(api_key=api_key)
    current_year = datetime.now().year
    today_str = datetime.now().strftime("%Y-%m-%d")
    max_retries = 3
    
    # STAGE 1: Minimal Inputs (No summary)
    minimal_inputs = [
        {"original_id": i, "title": item["original_title"], "source": item.get("original_url", "")}
        for i, item in enumerate(news_items)
    ]
    
    stage1_prompt = f"""
    You are an expert financial analyst. Today's date is {today_str}.
    Analyze the following list of news headlines from global media outlets.
    
    CRITICAL RULES:
    1. Deduplicate: Many headlines cover the same event. Select only the best one.
    2. Select UP TO 45 news items (or all available if there are fewer than 45) that have the highest impact on global investment and macroeconomy.
    3. Output ONLY the selected item IDs as a JSON array. Do not translate or summarize yet.
    """
    
    stage1_schema = {
        "type": "OBJECT",
        "properties": {
            "selected_ids": {
                "type": "ARRAY",
                "items": {"type": "INTEGER"},
                "description": "List of selected news (up to 45) original_ids"
            }
        },
        "required": ["selected_ids"]
    }
    
    safety_settings = [
        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'}
    ]
    
    selected_ids = []
    for attempt in range(max_retries):
        try:
            print(f"Running Stage 1: Selecting 45 candidate IDs... (Attempt {attempt+1})")
            response1 = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[stage1_prompt, json.dumps(minimal_inputs, ensure_ascii=False)],
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': stage1_schema,
                    'safety_settings': safety_settings
                },
            )
            selected_ids = json.loads(response1.text).get("selected_ids", [])
            print(f"Stage 1 completed. Retrieved {len(selected_ids)} candidate IDs.")
            progress.update_progress(percent=45, message="AI가 각 기사를 한국어로 번역 및 핵심 요약 분석 중...", time_remaining=90)
            if not selected_ids:
                raise Exception("Stage 1 returned empty ID list.")
            break
        except Exception as e:
            print(f"Stage 1 error: {e}")
            if attempt == max_retries - 1:
                return generate_dummy_news(news_items)
            time.sleep(10)
            
    # STAGE 2: Full text processing for selected candidates
    stage2_inputs = [
        {"original_id": i, "title": news_items[i]["original_title"], "summary": news_items[i]["summary_text"], "url": news_items[i]["original_url"]}
        for i in selected_ids if i < len(news_items)
    ]
    
    stage2_prompt = f"""
    You are an expert financial and political analyst.
    From the provided {len(stage2_inputs)} news items, select UP TO 30 most critical items (or all if there are fewer than 30) for global investors.
    
    For each of the final items:
    1. Identify the primary country.
    2. Create a NEW, punchy title in Korean, prefixed with the 2-letter ISO country code in brackets (e.g., [US] 연준 금리 인하 시그널). Do NOT use category names in brackets.
    3. Summarize the core content into Korean strictly focusing on Economy/Investment impact.
       CRITICAL: 문체는 반드시 '한다', '했다', '이다' 등 평어체(한다체)로 작성할 것. '합니다', '했습니다' 등 높임말 절대 사용 금지.
       CRITICAL: 요약 내용 맨 마지막 줄에는 반드시 "출처: [매체명]" 형식으로 원본 뉴스 출처를 기재할 것.
    4. Categorize each item as either 'Economy' or 'Diplomacy/Politics'. Select UP TO 30 items total (or all available) based purely on their overall importance, regardless of category ratio.
    5. OUTPUT ORDER: You MUST return the final_news array strictly ordered by their importance and impact on international economy and investment, from MOST important (index 0) to LEAST important.
    """
    
    stage2_schema = {
        "type": "OBJECT",
        "properties": {
            "final_news": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "original_id": {"type": "INTEGER"},
                        "translated_title": {"type": "STRING"},
                        "summary": {"type": "STRING"},
                        "category": {"type": "STRING"}
                    },
                    "required": ["original_id", "translated_title", "summary", "category"]
                }
            }
        },
        "required": ["final_news"]
    }
        
    final_list = []
    for attempt in range(max_retries):
        try:
            print(f"Running Stage 2: Verifying and summarizing 30 items... (Attempt {attempt+1})")
            response2 = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[stage2_prompt, json.dumps(stage2_inputs, ensure_ascii=False)],
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': stage2_schema,
                    'safety_settings': safety_settings
                },
            )
            final_list = json.loads(response2.text).get("final_news", [])
            print(f"Stage 2 completed. Retrieved {len(final_list)} final items.")
            break
        except Exception as e:
            print(f"Stage 2 error: {e}")
            if attempt == max_retries - 1:
                return generate_dummy_news(news_items)
            time.sleep(10)
    
    processed_news = []
    for sel in final_list:
        orig_id = sel.get("original_id", 0)
        if orig_id < len(news_items):
            original = news_items[orig_id]
            processed_news.append({
                "original_title": original["original_title"],
                "original_url": original["original_url"],
                "published_date": original["published_date"],
                "translated_title": sel.get("translated_title", ""),
                "summary": sel.get("summary", ""),
                "category": sel.get("category", ""),
                "impact_analysis": ""
            })
    
    return processed_news[::-1]

def generate_dummy_news(news_items):
    processed = []
    for i in range(min(30, len(news_items))):
        category = "경제"
        source = news_items[i % len(news_items)] if news_items else {"original_title": f"Title {i}", "original_url": "#", "published_date": "2026-06-16"}
        
        processed.append({
            "original_title": source["original_title"],
            "original_url": source["original_url"],
            "published_date": source["published_date"],
            "translated_title": f"[US] 테스트 뉴스 제목 {i+1} - 글로벌 투자 동향",
            "summary": f"이 기사는 {category} 관련 글로벌 투자 동향 분석 테스트 요약본이다. 투자 시장에 미치는 영향을 주로 설명한다.\n\n출처: 테스트 미디어",
            "category": category,
            "impact_analysis": "- **거시경제 파급력**\n  - 금리 인상 사이클 조기 종료 가능성 시사\n  - 글로벌 인플레이션 압력 완화 기대\n- **투자 및 자산 배분 영향**\n  - 기술주 및 성장주 비중 확대 권고\n  - 안전자산 선호 심리 일시적 하락" 
        })
    return processed
