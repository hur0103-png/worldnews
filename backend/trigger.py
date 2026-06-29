import urllib.request

url = "http://127.0.0.1:8000/api/trigger"
req = urllib.request.Request(url, method="POST")
with urllib.request.urlopen(req) as response:
    print(response.read().decode())
