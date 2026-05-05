import json
import os
import sys

# scripts/ から db/ を読み込む
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.libai_db import get_libai_conn, init_libai_db


# JSONファイルの場所
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
JSON_PATH = os.path.join(ROOT_DIR, "data", "libai.json")


def load_poems():
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError(f"JSONが見つからないよ: {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def insert_poems():
    init_libai_db()

    poems = load_poems()
    conn = get_libai_conn()
    cur = conn.cursor()

    for p in poems:
        cur.execute("""
        INSERT OR IGNORE INTO poems (id, title, data)
        VALUES (?, ?, ?)
        """, (
            p["id"],
            p["title"],
            json.dumps(p, ensure_ascii=False)
        ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    try:
        insert_poems()
        print("✔ libai.json をDBに投入完了")
    except Exception as e:
        print(f"❌ 失敗: {e}")
