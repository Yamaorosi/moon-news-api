import sqlite3
import os
import json

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "libai.db")


# 🧠 DB接続（辞書アクセス可能）
def get_libai_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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


# 📖 全件取得（JSON復元済みで返す）
def get_all_poems():
    conn = get_libai_conn()
    cur = conn.cursor()

    rows = cur.execute("""
    SELECT id, title, data
    FROM poems
    ORDER BY id
    """).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            **json.loads(row["data"])
        }
        for row in rows
    ]


# 🔍 1件取得（JSON復元済み）
def get_poem_by_id(poem_id):
    conn = get_libai_conn()
    cur = conn.cursor()

    row = cur.execute("""
    SELECT id, title, data
    FROM poems
    WHERE id = ?
    """, (poem_id,)).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        **json.loads(row["data"])
    }


# 🧪 デバッグ用（中身確認）
def debug_print_all():
    poems = get_all_poems()
    for p in poems:
        print(p["id"], p["title"])
