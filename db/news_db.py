import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "news.db")

def get_news_conn():
    return sqlite3.connect(DB_PATH)

def init_news_db():
    conn = get_news_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        body TEXT,
        source TEXT,
        url TEXT UNIQUE,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()
