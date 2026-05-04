from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/news")
def news():
   return jsonify({
    "fact": "米国株が上昇",
    "structure": "AI期待と地政学",
    "sensation": "都市の光が揺れる"
})
