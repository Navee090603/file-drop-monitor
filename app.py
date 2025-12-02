# app.py
import os
import json
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__)
SHARED_SECRET = "1234"
DATA_PATH = os.path.join(os.path.dirname(__file__), "latest.json")

def load_latest():
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_latest(d):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(load_latest())

@app.route("/update", methods=["POST"])
def update():
    print("HIT /update")
    token = request.headers.get("X-File-Drop-Token", "")
    print("TOKEN:", token)
    if token != SHARED_SECRET:
        print("TOKEN FAIL")
        return abort(401)

    payload = request.get_json(force=True, silent=True)
    print("PAYLOAD:", payload)

    filename = payload.get("filename")
    size_bytes = payload.get("size_bytes")
    ts = payload.get("timestamp_iso")

    save_latest({
        "filename": filename,
        "size_bytes": size_bytes,
        "timestamp_iso": ts
    })

    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(debug=True)
