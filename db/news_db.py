#db/news_db.py

import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "news.db")

def get_news_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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


def seed_news_if_empty():
    conn = get_news_conn()
    cur = conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    conn.close()

    if count == 0:
        from services import fetch_and_store_news
        fetch_and_store_news()
        print("🌱 news seeded")
