# app.py
from flask import Flask, render_template, jsonify, request
from services import fetch_tech_news, get_all_poems
from db.news_db import init_news_db
from db.libai_db import init_libai_db

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


init_news_db()
init_libai_db()

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
    # 実際の作業は職人（service）に任せて、結果をJSONで返すだけ
    data = fetch_tech_news()
    return jsonify(data)

@app.route("/article")
def article():
    url = request.args.get("url")
    return render_template("article.html", url=url)


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
