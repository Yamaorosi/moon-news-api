from fastapi import FastAPI
import requests

app = FastAPI()

import os

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

params = {
    "country": "us",
    "category": "technology",
    "pageSize": 5,
    "apiKey": API_KEY
}

@app.get("/news")
def get_news():
    response = requests.get(BASE_URL, params=params)
    articles = response.json().get("articles", [])

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "publishedAt": a["publishedAt"]
        }
        for a in articles
    ]
