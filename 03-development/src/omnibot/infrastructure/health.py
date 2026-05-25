"""
FR-14: Health check endpoint.

GET /api/v1/health → {"status": "healthy|degraded|unhealthy", "postgres": bool, "redis": bool, "uptime_seconds": float}

- healthy:   both postgres and redis reachable
- degraded:  one of them down (always returns HTTP 200)
- unhealthy: both down (always returns HTTP 200)

NFR-06: response time < 500ms even when degraded.
"""
from __future__ import annotations

import time
from typing import Callable

# Module-level start time for uptime_seconds calculation
_START_TIME: float = time.monotonic()


def _default_check_postgres() -> bool:
    """Check PostgreSQL reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "health.py: postgres connectivity check not implemented"
    )


def _default_check_redis() -> bool:
    """Check Redis reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "health.py: redis connectivity check not implemented"
    )


def health_check(
    *,
    check_postgres: Callable[[], bool] = _default_check_postgres,
    check_redis: Callable[[], bool] = _default_check_redis,
) -> dict:
    """
    Return the health payload dict.  HTTP layer adds status code 200.

    Args:
        check_postgres: Injectable callable for DB reachability (default: real check).
        check_redis: Injectable callable for Redis reachability (default: real check).

    Returns:
        {"status": str, "postgres": bool, "redis": bool, "uptime_seconds": float}
    """
    postgres_ok = check_postgres()
    redis_ok = check_redis()

    if postgres_ok and redis_ok:
        status = "healthy"
    elif postgres_ok or redis_ok:
        status = "degraded"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }
