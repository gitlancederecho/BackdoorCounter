from __future__ import annotations
import time
import logging
from typing import Optional, Callable

class FollowerCache:
    """In-memory TTL cache for the follower count."""

    def __init__(self, ttl_seconds: int = 40):
        self.ttl = ttl_seconds
        self._ts: float = 0.0
        self._count: Optional[int] = None
        self.last_error: Optional[str] = None
        self.last_success_ts: Optional[int] = None

    def get(self) -> Optional[int]:
        return self._count

    def age(self) -> Optional[int]:
        if not self._ts:
            return None
        return int(time.time() - self._ts)

    def is_stale(self) -> bool:
        if self._count is None:
            return True
        if not self._ts:
            return True
        return (time.time() - self._ts) > self.ttl

    def refresh(self, fetcher: Callable[[], int]) -> int:
        try:
            count = fetcher()
            self._count = count
            self._ts = time.time()
            self.last_error = None
            self.last_success_ts = int(self._ts)
            return count
        except Exception as e:
            logging.exception("fetch_followers failed")
            self.last_error = str(e)
            # keep old value
            return self._count or 0

    def get_or_refresh(self, fetcher: Callable[[], int]) -> int:
        if self.is_stale():
            return self.refresh(fetcher)
        return self._count or 0
