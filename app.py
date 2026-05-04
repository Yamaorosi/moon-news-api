from flask import Flask

app = Flask(__name__)

@app.route("/healthz")
def health():
    return {"status": "ok"}
