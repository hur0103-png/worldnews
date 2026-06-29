with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Check for syntax
if "impactContainer" in js:
    print("Error: impactContainer still present!")
else:
    print("impactContainer successfully removed.")
    
if "detail.style.display = 'block';" in js:
    print("Display block is intact.")

