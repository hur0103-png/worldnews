import psycopg2

SUPABASE_URL = "postgresql://postgres.xlwogpavxqtykumzfzov:%2B3M7k%40E.L7gzVJh@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

pg_conn = psycopg2.connect(SUPABASE_URL)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("DELETE FROM news WHERE original_title LIKE 'Test News Title %'")
deleted_count = pg_cursor.rowcount
pg_conn.commit()

print(f"Deleted {deleted_count} dummy records.")
pg_conn.close()
