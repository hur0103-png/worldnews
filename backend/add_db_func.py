with open("database.py", "r", encoding="utf-8") as f:
    code = f.read()

new_func = """
def get_available_dates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT substr(created_at, 1, 10) as date
        FROM news
        ORDER BY date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
"""

if "def get_available_dates" not in code:
    with open("database.py", "a", encoding="utf-8") as f:
        f.write("\n" + new_func + "\n")
