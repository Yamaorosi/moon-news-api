# app.py
from flask import Flask, render_template, jsonify, request
from services import fetch_tech_news  # 作業員を呼び出す
from db.news_db import init_news_db
from db.libai_db import init_libai_db

app = Flask(__name__)

init_news_db()
init_libai_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({"status": "ok"})

@app.route("/news")
def news():
    # 実際の作業は職人（service）に任せて、結果をJSONで返すだけ
    data = fetch_tech_news()
    return jsonify(data)

@app.route("/article")
def article():
    url = request.args.get("url")
    return render_template("article.html", url=url)
