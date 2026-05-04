from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/news")
def news():
    return jsonify({
        "fact": [],
        "structure": [],
        "sensation": []
    })
