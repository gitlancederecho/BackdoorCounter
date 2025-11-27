# server.py
import os, time, logging, requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, send_from_directory
import time
_last_fetch_error = None
_last_success_ts = None

# Load the exact .env file even if CWD is weird
DOTENV_PATH = find_dotenv(usecwd=True)
load_dotenv(DOTENV_PATH, override=True)

def _clean(s: str | None) -> str | None:
    if s is None:
        return None
    # remove surrounding quotes and whitespace/newlines
    s = s.strip().strip('"').strip("'")
    return s

app = Flask(__name__, static_folder='.', static_url_path='')

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

# optional: sanity log once on startup
logging.basicConfig(level=logging.INFO)
logging.info(f".env path: {DOTENV_PATH or 'NOT FOUND'}")
logging.info(
    "IG_USER_ID=%s token_len=%s token_tail=%s",
    IG_USER_ID,
    len(IG_ACCESS_TOKEN) if IG_ACCESS_TOKEN else 0,
    (IG_ACCESS_TOKEN[-6:] if IG_ACCESS_TOKEN else None),
)

# Why: tiny in-memory cache so we call Instagram at most once per 40 seconds
_cache = {"ts": 0, "count": None}
TTL = 40  # seconds

def fetch_followers():
    global _last_fetch_error, _last_success_ts
    url = f"https://graph.facebook.com/v23.0/{IG_USER_ID}"
    params = {
        "fields": "followers_count",
        "access_token": IG_ACCESS_TOKEN,  # already cleaned
    }

    try:
        r = requests.get(url, timeout=10, params=params)
        if r.status_code != 200:
            logging.error("Graph non-200: %s %s", r.status_code, r.text)
        r.raise_for_status()
        data = r.json()
        count = int(data.get("followers_count", 0))
        _last_fetch_error = None
        _last_success_ts = int(time.time())
        return count
    except Exception as e:
        _last_fetch_error = str(e)
        raise

@app.route("/debug")
def debug():
    age = int(time.time() - (_cache.get("ts") or 0)) if _cache.get("ts") else None
    return jsonify({
        "cached_count": _cache.get("count"),
        "cached_seconds": age,
        "ttl": TTL,
        "last_success_ts": _last_success_ts,
        "last_fetch_error": _last_fetch_error,
        "env": {
            "ig_user_id": IG_USER_ID,
            "token_len": len(IG_ACCESS_TOKEN) if IG_ACCESS_TOKEN else 0,
            "token_head": (IG_ACCESS_TOKEN[:8] + "...") if IG_ACCESS_TOKEN else None,
            "dotenv_path": DOTENV_PATH,
            "cwd": os.getcwd()
        }
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

@app.route('/display')
def display():
    return send_from_directory('.', 'display.html')

if __name__ == "__main__":
    # Why: binds to localhost on port 5050 like you already use
    app.run(host="127.0.0.1", port=5050)