# server.py
import os, time, logging, requests
from dotenv import load_dotenv
from flask import Flask, jsonify
import time
_last_fetch_error = None
_last_success_ts = None

# Why: loads IG_USER_ID and IG_ACCESS_TOKEN from your .env file
load_dotenv()

app = Flask(__name__)

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

# optional: sanity log once on startup
logging.basicConfig(level=logging.INFO)
logging.info(f"IG_USER_ID={IG_USER_ID} token_len={len(IG_ACCESS_TOKEN) if IG_ACCESS_TOKEN else 0}")

# Why: tiny in-memory cache so we call Instagram at most once per minute
_cache = {"ts": 0, "count": None}
TTL = 60  # seconds

def fetch_followers():
    global _last_fetch_error, _last_success_ts
    url = f"https://graph.facebook.com/v23.0/{IG_USER_ID}"
    params = {"fields": "followers_count", "access_token": IG_ACCESS_TOKEN}
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        count = int(data.get("followers_count", 0))
        _last_fetch_error = None
        _last_success_ts = int(time.time())
        return count
    except Exception as e:
        _last_fetch_error = str(e)
        raise

from flask import jsonify

@app.route("/debug")
def debug():
    age = int(time.time() - (_cache.get("ts") or 0)) if _cache.get("ts") else None
    return jsonify({
        "cached_count": _cache.get("count"),
        "cached_seconds": age,
        "ttl": TTL,
        "last_success_ts": _last_success_ts,
        "last_fetch_error": _last_fetch_error
    })

@app.get("/count")
def count():
    now = time.time()
    try:
        if _cache["count"] is None or now - _cache["ts"] > TTL:
            n = fetch_followers()
            _cache["count"] = n
            _cache["ts"] = now
    except Exception as e:
        logging.exception("fetch_followers failed")
        # do not overwrite a good cached value on error

    age = int(now - _cache["ts"]) if _cache["ts"] else 0
    return jsonify({"count": _cache["count"] or 0, "cached_seconds": age})

@app.get("/healthz")
def healthz():
    """Quick check that the Flask app is running."""
    return "ok", 200

if __name__ == "__main__":
    # Why: binds to localhost on port 5050 like you already use
    app.run(host="127.0.0.1", port=5050)
