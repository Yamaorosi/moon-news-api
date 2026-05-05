# services.py
import requests
import os
from db.libai_db import get_libai_conn

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_tech_news():
    """News APIから技術ニュースを取得して整形する作業"""
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

    # 必要なデータだけを抽出する加工処理
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

def get_all_poems():
    conn = get_libai_conn()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT title, text, dynasty, theme
        FROM poems
    """).fetchall()
    conn.close()

    poems = []
    for r in rows:
        poems.append({
            "title": r[0],
            "text": r[1],
            "dynasty": r[2],
            "theme": r[3]
        })

    return poems
