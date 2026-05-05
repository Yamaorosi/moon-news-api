#/scripts/insert_libai.py

import json
import os
from db.libai_db import get_libai_conn

# JSONファイルの場所
BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "data", "libai.json")

def load_poems():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_poems():
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
    insert_poems()
    print("✔ libai.json をDBに投入完了")
