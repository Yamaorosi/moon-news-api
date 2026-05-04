from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY")
print("API_KEY:", API_KEY)
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
        "country": "us",
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
