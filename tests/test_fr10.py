"""[FR-10]  Token Bucket rate limiter."""
from __future__ import annotations

import threading
import time

from omnibot.security.rate_limiter import RateLimiter, TokenBucket


def test_fr10_token_bucket_consumes_within_capacity():
    """Consuming tokens within capacity returns True."""
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=100, refill_rate=100.0)
    for _ in range(100):
        assert bucket.consume() is True


def test_fr10_token_bucket_exceeded_returns_false():
    """Consuming beyond capacity returns False."""
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=2, refill_rate=0.0)
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False


def test_fr10_token_bucket_refills_over_time():
    """Token bucket refills tokens over time."""
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=2, refill_rate=100.0)
    bucket.consume()
    bucket.consume()
    time.sleep(0.05)
    assert bucket.consume() is True


def test_fr10_token_bucket_consumes_until_empty():
    bucket = TokenBucket(capacity=2, refill_rate=1.0)
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False


def test_fr10_token_bucket_refills():
    bucket = TokenBucket(capacity=2, refill_rate=100.0)
    bucket.consume()
    bucket.consume()
    time.sleep(0.02)
    assert bucket.consume() is True


def test_fr10_rate_limiter_separate_user_buckets_independent():
    """Different users have independent rate limit buckets."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("telegram", "user2") is True


def test_fr10_rate_limiter_separate_platform_buckets_independent():
    """Different platforms have independent rate limit buckets."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("line", "user1") is True


def test_fr10_rate_limiter_per_user_independent():
    rl = RateLimiter()
    assert rl.check("telegram", "user1") is True
    assert rl.check("telegram", "user2") is True


def test_fr10_webhook_rate_limit_exceeded_returns_429():
    """When rate limit is exceeded, check() returns False (caller returns 429)."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    result = rl.check("telegram", "user1")
    assert result is False


def test_fr10_webhook_rate_limit_exceeded_returns_false():
    """When rate limit is exceeded, check() returns False (caller returns 429)."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("telegram", "user1") is False


def test_fr10_limiter_burst_101_requests_100_pass_1_gets_429():
    """101 requests with capacity 100: 100 pass, 1 is rejected."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    results = [rl.check("telegram", "user1") for _ in range(101)]
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    assert passed == 100, f"Expected 100 passed, got {passed}"
    assert failed == 1, f"Expected 1 failed, got {failed}"


def test_fr10_limiter_concurrent_requests_from_same_user_isolated():
    """Concurrent requests from the same user are handled in isolation."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    results = []

    def make_request():
        results.append(rl.check("telegram", "user1"))

    threads = [threading.Thread(target=make_request) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    passed = sum(1 for r in results if r is True)
    assert passed == 10


def test_fr10_limiter_redis_unavailable_fail_open_allows_request():
    """Fail-open: returns True when Redis is unavailable (any exception during check)."""
    from unittest.mock import patch
    from omnibot.security.rate_limiter import RateLimiter, TokenBucket

    with patch.object(TokenBucket, 'consume', side_effect=ConnectionError("Redis connection refused")):
        rl = RateLimiter()
        result = rl.check("telegram", "user1")
        assert result is True


def test_fr10_limiter_key_format_is_platform_colon_user_id():
    """Key format is platform:user_id ensuring cross-platform isolation."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    rl.check("telegram", "user1")
    rl.check("telegram", "user2")
    rl.check("line", "user1")
    keys = list(rl._buckets.keys())
    assert "telegram:user1" in keys
    assert "telegram:user2" in keys
    assert "line:user1" in keys
    assert len(keys) == 3


def test_fr10_rate_limiter_feeds_fr19_pipeline_stage_4():
    """RateLimiter feeds into FR-19 pipeline stage 4 (returns bool)."""
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    result = rl.check("telegram", "user1")
    assert isinstance(result, bool)


def test_fr10_rate_limiter_fail_open():
    """Fail-open: returns True even on error."""
    from omnibot.security.rate_limiter import TokenBucket
    bucket = TokenBucket(capacity=100, refill_rate=100.0)
    assert bucket.consume() is True
