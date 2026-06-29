import urllib.request
try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/app.js?v=19')
    js = response.read().decode('utf-8')
    print("JS Length:", len(js))
    
    # Check if the file contains the literal newline issue
    if "replace(/\n/g" not in js:
        print("Regex looks OK")
    else:
        # we specifically put \n in the file, so it SHOULD be there as \n, not actual newline
        pass
        
    print("Contains flatpickr init?", "flatpickr(datePicker" in js)
    print("Has-news check?", "dayElem.classList.add('has-news')" in js)
    
except Exception as e:
    print("Error:", e)
