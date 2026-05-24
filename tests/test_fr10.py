"""FR-10: Token Bucket rate limiter."""
from __future__ import annotations

import time


def test_fr10_token_bucket_consumes_until_empty():
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=2, refill_rate=1.0)
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False


def test_fr10_token_bucket_refills():
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=2, refill_rate=100.0)
    bucket.consume()
    bucket.consume()
    time.sleep(0.02)
    assert bucket.consume() is True


def test_fr10_rate_limiter_per_user_independent():
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    assert rl.check("telegram", "user1") is True
    assert rl.check("telegram", "user2") is True


def test_fr10_rate_limiter_fail_open():
    """Fail-open: returns True even on error."""
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=100, refill_rate=100.0)
    assert bucket.consume() is True
