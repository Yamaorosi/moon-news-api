#db/libai_db.py

import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "libai.db")

def get_libai_conn():
    return sqlite3.connect(DB_PATH)

def init_libai_db():
    conn = get_libai_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS poems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        text TEXT,
        dynasty TEXT,
        theme TEXT
    )
    """)
    conn.commit()
    conn.close()
