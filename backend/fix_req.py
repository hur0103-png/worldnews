with open("requirements.txt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("google-generativeai==0.3.1", "google-genai==2.8.0")

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(content)
