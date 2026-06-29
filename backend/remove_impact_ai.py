with open("ai_agent.py", "r", encoding="utf-8") as f:
    code = f.read()

# Remove step 5 from prompt
code = code.replace("""    5. GENERATE AN AI MARKET IMPACT ANALYSIS for each item. This analysis must be EXTREMELY CONCISE, totaling exactly 3 bullet points.
       - 거시경제 파급력 (Macroeconomic Impact): Provide 1 bullet point analyzing the core shift.
       - 투자 및 자산 배분 영향 (Investment Impact): Provide 1 or 2 bullet points with direct, actionable asset class insights.
       Maintain a sharp, authoritative tone of a premium institutional fund manager. DO NOT exceed 3 lines total.
    6. OUTPUT ORDER: You MUST return the final_news array strictly ordered by their importance and impact on international economy and investment, from MOST important (index 0) to LEAST important.""", 
"""    5. OUTPUT ORDER: You MUST return the final_news array strictly ordered by their importance and impact on international economy and investment, from MOST important (index 0) to LEAST important.""")

# Remove impact_analysis from schema
code = code.replace(',\n                        "impact_analysis": {"type": "STRING"}', "")
code = code.replace(', "impact_analysis"]', "]")

# Replace impact_analysis in response extraction
code = code.replace('"impact_analysis": sel.get("impact_analysis", "")', '"impact_analysis": ""')

# Replace dummy impact analysis
code = code.replace('''"- **거시경제 파급력**\n  - 금리 인상 사이클 조기 종료 가능성 부상\n  - 글로벌 인플레이션 압력 완화 기대\n- **투자 및 자산 배분 영향**\n  - 성장주 비중 확대 권고\n  - 자본 차익 실현 후 현금 확보 유리"''', '""')

with open("ai_agent.py", "w", encoding="utf-8") as f:
    f.write(code)
