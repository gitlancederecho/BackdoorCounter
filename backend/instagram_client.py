from __future__ import annotations
import time
import logging
import requests

class InstagramClient:
    """Thin wrapper around the Instagram Graph API for follower counts."""

    def __init__(self, user_id: str, access_token: str, version: str = "v23.0"):
        self.user_id = user_id
        self.access_token = access_token
        self.version = version
        self.base_url = f"https://graph.facebook.com/{self.version}/{self.user_id}"

    def fetch_followers(self, timeout: int = 10) -> int:
        params = {"fields": "followers_count", "access_token": self.access_token}
        r = requests.get(self.base_url, params=params, timeout=timeout)
        if r.status_code != 200:
            logging.error("Graph non-200: %s %s", r.status_code, r.text)
        r.raise_for_status()
        data = r.json()
        return int(data.get("followers_count", 0))
