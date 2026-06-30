import psycopg2

SUPABASE_URL = "postgresql://postgres.xlwogpavxqtykumzfzov:%2B3M7k%40E.L7gzVJh@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

pg_conn = psycopg2.connect(SUPABASE_URL)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("SELECT id, translated_title FROM news WHERE created_at LIKE '2026-06-30%' ORDER BY id ASC")
rows = pg_cursor.fetchall()
print(f"Total rows: {len(rows)}")
for r in rows[:5]:
    print(r)
print("...")
for r in rows[-5:]:
    print(r)
pg_conn.close()
