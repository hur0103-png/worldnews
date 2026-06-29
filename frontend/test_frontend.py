import urllib.request
try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/')
    html = response.read().decode('utf-8')
    print("HTML Length:", len(html))
    print("Contains v=16?", "v=16" in html)
    
    response = urllib.request.urlopen('http://127.0.0.1:8000/app.js?v=16')
    js = response.read().decode('utf-8')
    print("JS Length:", len(js))
    print("Contains Syntax Error?", "${hours}:;" in js)
    print("Contains Korean Text?", "불러오는 중" in js)
except Exception as e:
    print("Error:", e)
