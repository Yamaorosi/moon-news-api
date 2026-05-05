#db/libai_db.py

import sqlite3
import os
import json

# データベースファイルの保存場所を決める
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "libai.db")


def get_libai_conn():
    """
    【DB接続】SQLiteに繋ぐための関数
    """
    conn = sqlite3.connect(DB_PATH)
    # row["id"] のようにカラム名でデータを取り出せるようになる
    conn.row_factory = sqlite3.Row
    return conn


def init_libai_db():
    """
    【初期化】データを保存する「テーブル（表）」を作る
    """
    conn = get_libai_conn()
    cur = conn.cursor()

    # poemsテーブルがなければ作成（id, タイトル, JSONデータ本体の3つ）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS poems (
        id INTEGER PRIMARY KEY,
        title TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_all_poems():
    """
    【全件取得】DBにある全ての詩を、使いやすい形式（リスト）で返す
    """
    conn = get_libai_conn()
    cur = conn.cursor()

    # id順に並べて全部取得
    rows = cur.execute("""
    SELECT id, title, data
    FROM poems
    ORDER BY id
    """).fetchall()

    conn.close()

    # 取り出したデータを加工してリストにする
    return [
        {
            "id": row["id"],
            "title": row["title"],
            **json.loads(row["data"])
        }
        for row in rows
    ]



def get_poem_by_id(poem_id):
    """
    【検索】指定したIDの詩を1件だけ探して返す
    """
    conn = get_libai_conn()
    cur = conn.cursor()

    # ? を使うことで、安全に検索（SQLインジェクション対策）
    row = cur.execute("""
    SELECT id, title, data
    FROM poems
    WHERE id = ?
    """, (poem_id,)).fetchone()

    conn.close()

    # 見つからなかったら Noneを返す
    if row is None:
        return None

    # 見つかった場合は辞書形式にして返す
    return {
        "id": row["id"],
        "title": row["title"],
        **json.loads(row["data"])
    }



def debug_print_all():
    """
    【デバッグ】正しく保存されているかコンソールに表示して確認する用
    """
    poems = get_all_poems()
    for p in poems:
        print(p["id"], p["title"])
