with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<link rel="stylesheet" href="styles.css?v=18">', 
                    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">\n    <link rel="stylesheet" href="styles.css?v=19">')
html = html.replace('<input type="date" id="datePicker" class="date-picker">', 
                    '<input type="text" id="datePicker" class="date-picker" placeholder="Select Date">')
html = html.replace('<script src="app.js?v=18"></script>', 
                    '<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>\n    <script src="app.js?v=19"></script>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
