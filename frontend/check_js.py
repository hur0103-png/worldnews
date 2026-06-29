import ast
import traceback

with open("app.js", "r", encoding="utf-8") as f:
    js_code = f.read()

# We can't parse JS with ast, but we can check if string interpolation is valid
print("Checking for obvious JS errors...")
lines = js_code.split("\n")
for i, line in enumerate(lines):
    if "${" in line and "`" not in line and not line.strip().startswith("//"):
        print(f"Warning: Line {i+1} might have invalid interpolation: {line}")
