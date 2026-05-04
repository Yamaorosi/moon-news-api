from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"status": "ok", "message": "moon-news-api is running"}