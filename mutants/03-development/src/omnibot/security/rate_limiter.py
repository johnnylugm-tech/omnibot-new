"""[FR-10] Token bucket rate limiter."""
from __future__ import annotations

import time
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class TokenBucket:
    """Token bucket algorithm for rate limiting."""

    def xǁTokenBucketǁ__init____mutmut_orig(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_1(self, capacity: int = 101, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_2(self, capacity: int = 100, refill_rate: float = 101.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_3(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = None
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_4(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = None
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_5(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = None
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_6(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(None)
        self._last_refill = time.monotonic()

    def xǁTokenBucketǁ__init____mutmut_7(self, capacity: int = 100, refill_rate: float = 100.0):
        """Initialize token bucket with capacity and refill rate."""
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = None
    
    xǁTokenBucketǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁ__init____mutmut_1': xǁTokenBucketǁ__init____mutmut_1, 
        'xǁTokenBucketǁ__init____mutmut_2': xǁTokenBucketǁ__init____mutmut_2, 
        'xǁTokenBucketǁ__init____mutmut_3': xǁTokenBucketǁ__init____mutmut_3, 
        'xǁTokenBucketǁ__init____mutmut_4': xǁTokenBucketǁ__init____mutmut_4, 
        'xǁTokenBucketǁ__init____mutmut_5': xǁTokenBucketǁ__init____mutmut_5, 
        'xǁTokenBucketǁ__init____mutmut_6': xǁTokenBucketǁ__init____mutmut_6, 
        'xǁTokenBucketǁ__init____mutmut_7': xǁTokenBucketǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTokenBucketǁ__init____mutmut_orig)
    xǁTokenBucketǁ__init____mutmut_orig.__name__ = 'xǁTokenBucketǁ__init__'

    def xǁTokenBucketǁconsume__mutmut_orig(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_1(self, tokens: int = 2) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_2(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = None
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_3(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = None
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_4(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now + self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_5(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = None
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_6(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(None, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_7(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, None)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_8(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_9(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, )
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_10(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens - elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_11(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed / self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_12(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = None
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_13(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens > tokens:
            self._tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_14(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens = tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_15(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens += tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_16(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return False
        return False

    def xǁTokenBucketǁconsume__mutmut_17(self, tokens: int = 1) -> bool:
        """Consume tokens. Returns True if allowed, False if rate limited."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return True
    
    xǁTokenBucketǁconsume__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁconsume__mutmut_1': xǁTokenBucketǁconsume__mutmut_1, 
        'xǁTokenBucketǁconsume__mutmut_2': xǁTokenBucketǁconsume__mutmut_2, 
        'xǁTokenBucketǁconsume__mutmut_3': xǁTokenBucketǁconsume__mutmut_3, 
        'xǁTokenBucketǁconsume__mutmut_4': xǁTokenBucketǁconsume__mutmut_4, 
        'xǁTokenBucketǁconsume__mutmut_5': xǁTokenBucketǁconsume__mutmut_5, 
        'xǁTokenBucketǁconsume__mutmut_6': xǁTokenBucketǁconsume__mutmut_6, 
        'xǁTokenBucketǁconsume__mutmut_7': xǁTokenBucketǁconsume__mutmut_7, 
        'xǁTokenBucketǁconsume__mutmut_8': xǁTokenBucketǁconsume__mutmut_8, 
        'xǁTokenBucketǁconsume__mutmut_9': xǁTokenBucketǁconsume__mutmut_9, 
        'xǁTokenBucketǁconsume__mutmut_10': xǁTokenBucketǁconsume__mutmut_10, 
        'xǁTokenBucketǁconsume__mutmut_11': xǁTokenBucketǁconsume__mutmut_11, 
        'xǁTokenBucketǁconsume__mutmut_12': xǁTokenBucketǁconsume__mutmut_12, 
        'xǁTokenBucketǁconsume__mutmut_13': xǁTokenBucketǁconsume__mutmut_13, 
        'xǁTokenBucketǁconsume__mutmut_14': xǁTokenBucketǁconsume__mutmut_14, 
        'xǁTokenBucketǁconsume__mutmut_15': xǁTokenBucketǁconsume__mutmut_15, 
        'xǁTokenBucketǁconsume__mutmut_16': xǁTokenBucketǁconsume__mutmut_16, 
        'xǁTokenBucketǁconsume__mutmut_17': xǁTokenBucketǁconsume__mutmut_17
    }
    
    def consume(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_mutants"), args, kwargs, self)
        return result 
    
    consume.__signature__ = _mutmut_signature(xǁTokenBucketǁconsume__mutmut_orig)
    xǁTokenBucketǁconsume__mutmut_orig.__name__ = 'xǁTokenBucketǁconsume'


class RateLimiter:
    """Per-platform per-user rate limiter with token bucket algorithm."""

    def xǁRateLimiterǁ__init____mutmut_orig(self):
        """Initialize rate limiter with empty bucket map."""
        self._buckets: dict[str, TokenBucket] = {}

    def xǁRateLimiterǁ__init____mutmut_1(self):
        """Initialize rate limiter with empty bucket map."""
        self._buckets: dict[str, TokenBucket] = None
    
    xǁRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimiterǁ__init____mutmut_1': xǁRateLimiterǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRateLimiterǁ__init____mutmut_orig)
    xǁRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁRateLimiterǁ__init__'

    def xǁRateLimiterǁcheck__mutmut_orig(self, platform: str, user_id: str) -> bool:
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

    def xǁRateLimiterǁcheck__mutmut_1(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = None
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = TokenBucket()
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_2(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = None
            if bucket is None:
                bucket = TokenBucket()
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_3(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = self._buckets.get(None)
            if bucket is None:
                bucket = TokenBucket()
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_4(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = self._buckets.get(key)
            if bucket is not None:
                bucket = TokenBucket()
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_5(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = None
                self._buckets[key] = bucket
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_6(self, platform: str, user_id: str) -> bool:
        """Check rate limit. Returns True if allowed, False if exceeded.
        Fail-open: returns True on any unexpected error."""
        try:
            key = f"{platform}:{user_id}"
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = TokenBucket()
                self._buckets[key] = None
            return bucket.consume()
        except Exception:
            return True

    def xǁRateLimiterǁcheck__mutmut_7(self, platform: str, user_id: str) -> bool:
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
            return False
    
    xǁRateLimiterǁcheck__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimiterǁcheck__mutmut_1': xǁRateLimiterǁcheck__mutmut_1, 
        'xǁRateLimiterǁcheck__mutmut_2': xǁRateLimiterǁcheck__mutmut_2, 
        'xǁRateLimiterǁcheck__mutmut_3': xǁRateLimiterǁcheck__mutmut_3, 
        'xǁRateLimiterǁcheck__mutmut_4': xǁRateLimiterǁcheck__mutmut_4, 
        'xǁRateLimiterǁcheck__mutmut_5': xǁRateLimiterǁcheck__mutmut_5, 
        'xǁRateLimiterǁcheck__mutmut_6': xǁRateLimiterǁcheck__mutmut_6, 
        'xǁRateLimiterǁcheck__mutmut_7': xǁRateLimiterǁcheck__mutmut_7
    }
    
    def check(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimiterǁcheck__mutmut_orig"), object.__getattribute__(self, "xǁRateLimiterǁcheck__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check.__signature__ = _mutmut_signature(xǁRateLimiterǁcheck__mutmut_orig)
    xǁRateLimiterǁcheck__mutmut_orig.__name__ = 'xǁRateLimiterǁcheck'
