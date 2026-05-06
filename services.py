import requests
import os
import json
import re
from html import unescape
from db.libai_db import get_libai_conn
from db.news_db import get_news_conn


API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


# -------------------------
# 📰 ニュース取得（そのままOK）
# -------------------------
def fetch_tech_news():
    if not API_KEY:
        print("⚠️ NEWS_API_KEY not set")
        return []

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

    # HTMLエスケープ解除 (&quot; など)
    text = unescape(desc)

    # HTMLタグ除去（念のため）
    text = re.sub(r"<[^>]+>", "", text)

    # URL除去（RAGのノイズになりやすい）
    text = re.sub(r"https?://\S+", "", text)

    # 改行・タブ・多重スペースを1つにまとめる
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def fetch_and_store_news():
    print("🚀 fetch_and_store_news called")

    articles = fetch_tech_news()
    print("📰 fetched articles:", len(articles))

    conn = get_news_conn()
    cur = conn.cursor()

    for a in articles:
        summary = make_summary(a)
        print("➕ inserting:", a["title"])

        cur.execute("""
            INSERT OR IGNORE INTO news (title, body, source, url, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            a["title"],
            summary,
            a["source"],
            a["url"],
            a["publishedAt"]
        ))

    conn.commit()
    conn.close()
    print("✅ news commit done")


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

# -------------------------
# RAG下処理
# -------------------------
def build_libai_search_text(poem):
    parts = []

    parts.append(poem.get("title", ""))

    if poem.get("theme"):
        parts.append("テーマ: " + " ".join(poem["theme"]))

    if poem.get("emotion"):
        parts.append("感情: " + " ".join(poem["emotion"]))

    if poem.get("keywords"):
        parts.append("象徴: " + " ".join(poem["keywords"]))

    if poem.get("metaphor"):
        parts.append(
            "比喩: " + " ".join(poem["metaphor"].keys())
        )

    return " / ".join(parts)