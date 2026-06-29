with open("styles.css", "r", encoding="utf-8") as f:
    css = f.read()

# Fix the broken quote and weird characters
css = css.replace("content: '??;", "content: '✨';")
css = css.replace("?목??감싸??박스???래?명", "제목을 감싸는 박스 아래 공백")
css = css.replace("?자가 커질?록 ??많이 벌어집니??", "숫자가 커질수록 더 많이 벌어집니다")

with open("styles.css", "w", encoding="utf-8") as f:
    f.write(css)
