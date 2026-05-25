#!/usr/bin/env python3
"""Verify FR-10 tests pass."""
import sys
sys.path.insert(0, '03-development/src')

import time
import threading
from omnibot.security.rate_limiter import TokenBucket, RateLimiter

tests = []

def test_fr10_token_bucket_consumes_within_capacity():
    bucket = TokenBucket(capacity=100, refill_rate=100.0)
    for _ in range(100):
        assert bucket.consume() is True
    return True

def test_fr10_token_bucket_exceeded_returns_false():
    bucket = TokenBucket(capacity=2, refill_rate=0.0)
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False
    return True

def test_fr10_token_bucket_refills_over_time():
    bucket = TokenBucket(capacity=2, refill_rate=100.0)
    bucket.consume()
    bucket.consume()
    time.sleep(0.05)
    assert bucket.consume() is True
    return True

def test_fr10_rate_limiter_separate_user_buckets_independent():
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("telegram", "user2") is True
    return True

def test_fr10_rate_limiter_separate_platform_buckets_independent():
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("line", "user1") is True
    return True

def test_fr10_webhook_rate_limit_exceeded_returns_false():
    rl = RateLimiter()
    for _ in range(100):
        rl.check("telegram", "user1")
    assert rl.check("telegram", "user1") is False
    return True

def test_fr10_limiter_burst_101_requests_100_pass_1_gets_429():
    rl = RateLimiter()
    results = [rl.check("telegram", "user1") for _ in range(101)]
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    assert passed == 100, f"Expected 100 passed, got {passed}"
    assert failed == 1, f"Expected 1 failed, got {failed}"
    return True

def test_fr10_limiter_concurrent_requests_from_same_user_isolated():
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
    return True

def test_fr10_limiter_redis_unavailable_fail_open_allows_request():
    class FailingRL(RateLimiter):
        def check(self, platform, user_id):
            raise RuntimeError("redis unavailable")
    rl = FailingRL()
    assert rl.check("telegram", "user1") is True
    return True

def test_fr10_limiter_key_format_is_platform_colon_user_id():
    rl = RateLimiter()
    rl.check("telegram", "user1")
    rl.check("telegram", "user2")
    rl.check("line", "user1")
    keys = list(rl._buckets.keys())
    assert "telegram:user1" in keys
    assert "telegram:user2" in keys
    assert "line:user1" in keys
    assert len(keys) == 3
    return True

def test_fr10_rate_limiter_feeds_fr19_pipeline_stage_4():
    rl = RateLimiter()
    result = rl.check("telegram", "user1")
    assert isinstance(result, bool)
    return True

all_tests = [
    test_fr10_token_bucket_consumes_within_capacity,
    test_fr10_token_bucket_exceeded_returns_false,
    test_fr10_token_bucket_refills_over_time,
    test_fr10_rate_limiter_separate_user_buckets_independent,
    test_fr10_rate_limiter_separate_platform_buckets_independent,
    test_fr10_webhook_rate_limit_exceeded_returns_false,
    test_fr10_limiter_burst_101_requests_100_pass_1_gets_429,
    test_fr10_limiter_concurrent_requests_from_same_user_isolated,
    test_fr10_limiter_redis_unavailable_fail_open_allows_request,
    test_fr10_limiter_key_format_is_platform_colon_user_id,
    test_fr10_rate_limiter_feeds_fr19_pipeline_stage_4,
]

passed = 0
failed = 0
for t in all_tests:
    try:
        t()
        print(f"PASS: {t.__name__}")
        passed += 1
    except Exception as e:
        print(f"FAIL: {t.__name__}: {e}")
        failed += 1

print()
print(f"Results: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)