import requests
import os
import json
from db.libai_db import get_libai_conn
from db.news_db import get_news_conn


API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


# -------------------------
# 📰 ニュース取得（そのままOK）
# -------------------------
def fetch_tech_news():
    if not API_KEY:
        return {"error": "API_KEYが設定されてない"}, 500

    params = {
        "country": "us",
        "category": "technology",
        "pageSize": 3,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    articles = response.json().get("articles", [])

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "publishedAt": a["publishedAt"],
            "description": a.get("description", "")
        }
        for a in articles
    ]


# -------------------------
# 📖 詩データ取得（完成形）
# -------------------------
def get_all_poems():
    conn = get_libai_conn()
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT id, title, data
        FROM poems
        ORDER BY id
    """).fetchall()

    conn.close()

    poems = []

    for r in rows:
        try:
            data = json.loads(r["data"]) if r["data"] else {}
        except json.JSONDecodeError:
            data = {}

        poems.append({
            "id": r["id"],
            "title": r["title"],
            **data
        })

    return poems



# -------------------------
# バッチ処理
# -------------------------
def make_summary(article):
    desc = article.get("description") or ""
    return desc.replace("\n", " ").strip()


def fetch_and_store_news():
    articles = fetch_tech_news()

    conn = get_news_conn()
    cur = conn.cursor()

    for a in articles:
        summary = make_summary(a)

        cur.execute("""
            INSERT INTO news (title, description, summary, source, publishedAt)
            VALUES (?, ?, ?, ?, ?)
        """, (
            a["title"],
            a["description"],
            summary,
            a["source"],
            a["publishedAt"]
        ))

    conn.commit()
    conn.close()



# -------------------------
# 🔍 将来用：単体取得
# -------------------------
def get_poem_by_id(poem_id):
    conn = get_libai_conn()
    cur = conn.cursor()

    row = cur.execute("""
        SELECT id, title, data
        FROM poems
        WHERE id = ?
    """, (poem_id,)).fetchone()

    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        **json.loads(row["data"])
    }
