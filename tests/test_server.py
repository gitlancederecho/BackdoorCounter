import time
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import create_app
import backend.cache as cache_mod


def build_app():
    return create_app(ttl=2)  # small TTL for faster test refresh behavior


def test_healthz():
    app = build_app()
    with app.test_client() as client:
        resp = client.get("/healthz")
        assert resp.status_code == 200
        assert resp.data == b"ok"


def test_count_caching(monkeypatch):
    calls = {"n": 0}

    def fake_fetch():
        calls["n"] += 1
        # Return a different number each call to prove caching works
        return 1000 + calls["n"]
    app = build_app()
    client_obj = app.config['ig_client']
    cache = app.config['follower_cache']

    monkeypatch.setattr(client_obj, "fetch_followers", fake_fetch)

    first = app.test_client().get("/count").get_json()
    assert first["count"] >= 1001  # first call value
    assert first["cached_seconds"] == 0
    # Wait a tiny moment (< TTL) but not enough to expire cache
    time.sleep(0.05)
    second = app.test_client().get("/count").get_json()

    # fetch_followers should have been called only once due to caching
    assert calls["n"] == 1, f"fetch_followers called {calls['n']} times"
    assert second["count"] == first["count"]  # unchanged within TTL
    assert 0 <= second["cached_seconds"] <= app.config['ttl']
