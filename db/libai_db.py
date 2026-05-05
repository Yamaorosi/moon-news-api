#db/libai_db.py

import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "libai.db")


# 🧠 DB接続
def get_libai_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ← 辞書っぽく扱えるようにする（超重要）
    return conn


# 🧱 テーブル初期化
def init_libai_db():
    conn = get_libai_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS poems (
        id INTEGER PRIMARY KEY,
        title TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


# 📖 全件取得
def get_all_poems():
    conn = get_libai_conn()
    cur = conn.cursor()

    rows = cur.execute("""
    SELECT id, title, data
    FROM poems
    ORDER BY id
    """).fetchall()

    conn.close()

    return rows


# 🔍 1件取得（将来用）
def get_poem_by_id(poem_id):
    conn = get_libai_conn()
    cur = conn.cursor()

    row = cur.execute("""
    SELECT id, title, data
    FROM poems
    WHERE id = ?
    """, (poem_id,)).fetchone()

    conn.close()
    return row
