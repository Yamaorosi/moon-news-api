# app.py
from flask import Flask, render_template, jsonify, request
from services import fetch_tech_news, get_all_poems,fetch_and_store_news
from db.news_db import init_news_db,get_news_conn
from db.libai_db import init_libai_db
import os

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# 初期化
init_news_db()
init_libai_db()

from scripts.insert_libai import insert_poems
try:
    insert_poems()
    print("✅ Startup: DB seeding completed.")
except Exception as e:
    print(f"❌ Startup: Seeding failed: {e}")
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({"status": "ok"})
    
@app.route("/debug/libai")
def debug_libai():
    poems = get_all_poems()
    return jsonify(poems)
    
@app.route("/news")
def news():
    data = fetch_tech_news()
    return jsonify(data)

@app.route("/article")
def article():
    url = request.args.get("url")
    return render_template("article.html", url=url)

# --- ここから李白関連のエンドポイント ---

@app.route("/libai/list")
def libai_list():
    poems = get_all_poems()
    return jsonify(poems)

@app.route("/debug/seed-libai")
def debug_seed_libai():
    from scripts.insert_libai import insert_poems
    try:
        insert_poems()
        return "✔ データの投入に成功したよ！ /libai/list を確認してみて。"
    except Exception as e:
        return f"❌ 失敗: {e}"


@app.route("/update-news")
def update_news():
    try:
        fetch_and_store_news()
        return {"status": "ok"}
    except Exception as e:
        print("ERROR:", e)
        return {"status": "error", "message": str(e)}, 500


        
@app.route("/debug/news")
def debug_news():
    conn = get_news_conn()
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT id, title, body, source, url, created_at
        FROM news
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [
        dict(r) for r in rows
    ]

# --- app.run は必ず一番最後に書く！ ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
