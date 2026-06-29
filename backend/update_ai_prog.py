import re

with open("ai_agent.py", "r", encoding="utf-8") as f:
    code = f.read()

if "import progress" not in code:
    code = code.replace("import time", "import time\nimport progress")

# After Stage 1 completes, update progress
code = code.replace('print(f"Stage 1 completed. Retrieved {len(selected_ids)} candidate IDs.")',
                    'print(f"Stage 1 completed. Retrieved {len(selected_ids)} candidate IDs.")\n            progress.update_progress(percent=45, message="AI가 각 기사를 한국어로 번역 및 핵심 요약 분석 중...", time_remaining=90)')

with open("ai_agent.py", "w", encoding="utf-8") as f:
    f.write(code)
