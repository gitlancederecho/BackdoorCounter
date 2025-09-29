from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
import requests, os

from dotenv import load_dotenv
load_dotenv()

IG_USER_ID    = os.getenv("IG_USER_ID")
ACCESS_TOKEN  = os.getenv("IG_ACCESS_TOKEN")

app = Flask(__name__)
CORS(app)  # allow browser fetch from file:// or other origins

@app.route("/count")
def count():
    if not IG_USER_ID or not ACCESS_TOKEN:
        return jsonify({"error": "Missing IG_USER_ID or IG_ACCESS_TOKEN", "count": None}), 500
    try:
        url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}"
        params = {"fields": "followers_count", "access_token": ACCESS_TOKEN}
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        followers = int(data.get("followers_count", 0))
        return jsonify({"count": followers})
    except Exception as e:
        return jsonify({"error": str(e), "count": None}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)

@app.route("/")
def home():
    return "BackdoorCounter is running. Try /count"