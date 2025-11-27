from __future__ import annotations
import os
import logging
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv, find_dotenv

from .instagram_client import InstagramClient
from .cache import FollowerCache

def create_app(ttl: int = 40) -> Flask:
    dotenv_path = find_dotenv(usecwd=True)
    load_dotenv(dotenv_path, override=True)

    ig_user_id = os.getenv("IG_USER_ID") or ""
    ig_access_token = os.getenv("IG_ACCESS_TOKEN") or ""

    logging.basicConfig(level=logging.INFO)
    logging.info(".env path: %s", dotenv_path or "NOT FOUND")
    logging.info(
        "IG_USER_ID=%s token_len=%s token_tail=%s",
        ig_user_id,
        len(ig_access_token) if ig_access_token else 0,
        (ig_access_token[-6:] if ig_access_token else None),
    )

    app = Flask(__name__, static_folder='.', static_url_path='')

    client = InstagramClient(ig_user_id, ig_access_token)
    cache = FollowerCache(ttl)

    # store references on app.config for access in tests / routes
    app.config['ig_client'] = client
    app.config['follower_cache'] = cache
    app.config['ttl'] = ttl

    @app.get('/count')
    def count():
        value = cache.get_or_refresh(client.fetch_followers)
        age = cache.age() or 0
        return jsonify({"count": value, "cached_seconds": age})

    @app.get('/debug')
    def debug():
        age = cache.age()
        return jsonify({
            "cached_count": cache.get(),
            "cached_seconds": age,
            "ttl": cache.ttl,
            "last_success_ts": cache.last_success_ts,
            "last_fetch_error": cache.last_error,
            "env": {
                "ig_user_id": ig_user_id,
                "token_len": len(ig_access_token) if ig_access_token else 0,
                "token_head": (ig_access_token[:8] + "...") if ig_access_token else None,
                "dotenv_path": dotenv_path,
                "cwd": os.getcwd()
            }
        })

    @app.get('/healthz')
    def healthz():
        return "ok", 200

    @app.route('/display')
    def display():
        return send_from_directory('.', 'display.html')

    return app
