# app.py

from flask import Flask, render_template, jsonify, request
from services import fetch_tech_news, get_all_poems, fetch_and_store_news
from db.news_db import init_news_db, get_news_conn, seed_news_if_empty
from db.libai_db import init_libai_db, seed_libai_if_empty, get_libai_conn
import os

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# --- 初期化 ---
init_news_db()
init_libai_db()

# --- seed（空なら入れる） ---
seed_libai_if_empty()
seed_news_if_empty()

print("🌱 seeds checked")



    
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
    conn = get_news_conn()
    cur = conn.cursor()
    # ASを使ってフロントが期待するキー名（publishedAt, description）に変える
    rows = cur.execute("""
        SELECT 
            title, 
            source, 
            url, 
            created_at AS publishedAt, 
            body AS description
        FROM news
        ORDER BY created_at DESC
        LIMIT 3
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

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

@app.route("/debug/count")
def debug_count():
    # 李白のカウント
    conn_l = get_libai_conn()
    count_l = conn_l.execute("SELECT COUNT(*) FROM poems").fetchone()[0]
    conn_l.close()
    
    # ニュースのカウント
    conn_n = get_news_conn()
    count_n = conn_n.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    conn_n.close()
    
    return {
        "libai_count": count_l,
        "news_count": count_n
    }



# --- app.run は必ず一番最後に書く！ ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
