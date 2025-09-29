# server.py
import os, time, requests
from dotenv import load_dotenv
from flask import Flask, jsonify

# Why: loads IG_USER_ID and IG_ACCESS_TOKEN from your .env file
load_dotenv()

app = Flask(__name__)

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

# Why: tiny in-memory cache so we call Instagram at most once per minute
_cache = {"ts": 0, "count": None}
TTL = 60  # seconds

def fetch_followers():
    """Call Instagram Graph API and return the follower count as int."""
    url = f"https://graph.instagram.com/{IG_USER_ID}"
    params = {"fields": "followers_count", "access_token": IG_ACCESS_TOKEN}
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return int(data.get("followers_count", 0))

@app.get("/count")
def count():
    """Serve the follower count, using cache if it is fresh."""
    now = time.time()
    if _cache["count"] is None or now - _cache["ts"] > TTL:
        try:
            _cache["count"] = fetch_followers()
            _cache["ts"] = now
        except Exception:
            # keep last good value if API fails, otherwise 0
            _cache["count"] = _cache["count"] or 0
    age = int(now - _cache["ts"])
    return jsonify({"count": _cache["count"], "cached_seconds": age})

@app.get("/healthz")
def healthz():
    """Quick check that the Flask app is running."""
    return "ok", 200

if __name__ == "__main__":
    # Why: binds to localhost on port 5050 like you already use
    app.run(host="127.0.0.1", port=5050)
