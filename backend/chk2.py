import psycopg2

SUPABASE_URL = "postgresql://postgres.xlwogpavxqtykumzfzov:%2B3M7k%40E.L7gzVJh@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

pg_conn = psycopg2.connect(SUPABASE_URL)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("SELECT translated_title, summary FROM news WHERE created_at LIKE '2026-06-30%' LIMIT 2")
print(pg_cursor.fetchall())
pg_conn.close()
