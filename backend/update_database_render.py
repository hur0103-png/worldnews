code = """import sqlite3
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DB_URL = os.environ.get("DATABASE_URL")
DB_FILE = os.path.join(os.path.dirname(__file__), 'worldnews.db')

def get_connection():
    if DB_URL:
        return psycopg2.connect(DB_URL)
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def execute_query(conn, query, params=(), is_select=False):
    is_pg = bool(DB_URL)
    
    if is_pg:
        query = query.replace('?', '%s')
        query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        query = query.replace('substr(', 'substring(')
        cursor = conn.cursor(cursor_factory=RealDictCursor) if is_select else conn.cursor()
    else:
        if is_select:
            conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
    cursor.execute(query, params)
    return cursor

def init_db():
    conn = get_connection()
    execute_query(conn, '''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_title TEXT NOT NULL,
            original_url TEXT NOT NULL,
            translated_title TEXT NOT NULL,
            summary TEXT NOT NULL,
            category TEXT NOT NULL,
            published_date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            impact_analysis TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

def insert_news(news_list):
    conn = get_connection()
    for item in news_list:
        execute_query(conn, '''
            INSERT INTO news (original_title, original_url, translated_title, summary, category, published_date, created_at, impact_analysis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('original_title', ''),
            item.get('original_url', ''),
            item.get('translated_title', ''),
            item.get('summary', ''),
            item.get('category', ''),
            item.get('published_date', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            item.get('impact_analysis', '')
        ))
    conn.commit()
    conn.close()

def get_news_by_date(date_str):
    conn = get_connection()
    cursor = execute_query(conn, '''
        SELECT * FROM news 
        WHERE substr(created_at, 1, 10) = ?
        ORDER BY id DESC
    ''', (date_str,), is_select=True)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_available_dates():
    conn = get_connection()
    cursor = execute_query(conn, '''
        SELECT DISTINCT substr(created_at, 1, 10) as date
        FROM news
        ORDER BY date DESC
    ''', is_select=True)
    rows = cursor.fetchall()
    conn.close()
    return [row['date'] for row in rows]
"""

with open("database.py", "w", encoding="utf-8") as f:
    f.write(code)
