import sys
sys.path.insert(0, '03-development/src')
from omnibot.security.rate_limiter import TokenBucket, RateLimiter

# Test 1: token bucket basic
bucket = TokenBucket(capacity=100, refill_rate=100.0)
results = [bucket.consume() for _ in range(100)]
print(f'Test 1 - 100 consumes: {all(results)} (expected True)')

# Test 2: exceeded returns False
bucket2 = TokenBucket(capacity=2, refill_rate=0.0)
r1 = bucket2.consume()
r2 = bucket2.consume()
r3 = bucket2.consume()
print(f'Test 2 - exceed capacity: {r1}, {r2}, {r3} (expected True, True, False)')

# Test 3: separate user buckets
rl = RateLimiter()
for _ in range(100):
    rl.check('telegram', 'user1')
result = rl.check('telegram', 'user2')
print(f'Test 3 - separate user buckets: {result} (expected True)')

# Test 4: key format
rl2 = RateLimiter()
rl2.check('telegram', 'user1')
rl2.check('telegram', 'user2')
rl2.check('line', 'user1')
keys = list(rl2._buckets.keys())
print(f'Test 4 - keys: {sorted(keys)} (expected [line:user1, telegram:user1, telegram:user2])')

# Test 5: Redis fail-open
class FakeRedisUnavailableError(Exception):
    pass
class FailingRateLimiter(RateLimiter):
    def check(self, platform, user_id):
        raise FakeRedisUnavailableError('connection refused')
rl3 = FailingRateLimiter()
try:
    result = rl3.check('telegram', 'user1')
    print(f'Test 5 - fail-open: {result} (expected True, but got {result})')
except Exception as e:
    print(f'Test 5 - fail-open: EXCEPTION {type(e).__name__}: {e} (expected True)')

# Test 6: 101 burst, 100 pass, 1 fail
rl4 = RateLimiter()
results2 = [rl4.check('telegram', 'user1') for _ in range(101)]
passed = sum(1 for r in results2 if r is True)
failed = sum(1 for r in results2 if r is False)
print(f'Test 6 - burst 101: passed={passed}, failed={failed} (expected 100, 1)')

print('Done')