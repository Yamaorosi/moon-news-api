from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY")
print("API_KEY:", API_KEY)
if not API_KEY:
    print("❌ API_KEYが設定されてない")
BASE_URL = "https://newsapi.org/v2/top-headlines"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({"status": "ok"})


@app.route("/news")
def news():

    params = {
        "country": "jp",
        "category": "technology",
        "pageSize": 3,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    articles = response.json().get("articles", [])

    result = [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "publishedAt": a["publishedAt"]
        }
        for a in articles
    ]

    return jsonify(result)

@app.route("/article")
def article():
    url = request.args.get("url")
    return render_template("article.html", url=url)
