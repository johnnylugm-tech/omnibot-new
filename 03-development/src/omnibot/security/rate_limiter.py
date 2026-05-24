"""FR-10: Token bucket rate limiter."""
from __future__ import annotations

import time


class TokenBucket:
    def __init__(self, capacity: int = 100, refill_rate: float = 100.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def consume(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False


class RateLimiter:
    def __init__(self):
        self._buckets: dict[str, TokenBucket] = {}

    def check(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = TokenBucket()
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True
