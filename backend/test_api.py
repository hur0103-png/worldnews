import urllib.request
from datetime import datetime

today_str = datetime.now().strftime("%Y-%m-%d")
url = f"http://127.0.0.1:8000/api/news?date={today_str}"
print(f"Fetching {url}...")
try:
    with urllib.request.urlopen(url, timeout=5) as response:
        print("Status:", response.status)
        data = response.read()
        print("Data length:", len(data))
except Exception as e:
    print("Error:", e)
