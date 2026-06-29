with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

# The block to remove starts from "const impactContainer" to "detail.style.display = 'block';"
import re
new_js = re.sub(r'const impactContainer = document\.getElementById\(\'detailImpact\'\);.*?detail\.style\.display = \'block\';', "detail.style.display = 'block';", js, flags=re.DOTALL)

with open("app.js", "w", encoding="utf-8") as f:
    f.write(new_js)
