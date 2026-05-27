"""
[FR-14] Health check endpoint.

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


def x__default_check_postgres__mutmut_orig() -> bool:
    """Check PostgreSQL reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "health.py: postgres connectivity check not implemented"
    )


def x__default_check_postgres__mutmut_1() -> bool:
    """Check PostgreSQL reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        None
    )


def x__default_check_postgres__mutmut_2() -> bool:
    """Check PostgreSQL reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "XXhealth.py: postgres connectivity check not implementedXX"
    )


def x__default_check_postgres__mutmut_3() -> bool:
    """Check PostgreSQL reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "HEALTH.PY: POSTGRES CONNECTIVITY CHECK NOT IMPLEMENTED"
    )

x__default_check_postgres__mutmut_mutants : ClassVar[MutantDict] = {
'x__default_check_postgres__mutmut_1': x__default_check_postgres__mutmut_1, 
    'x__default_check_postgres__mutmut_2': x__default_check_postgres__mutmut_2, 
    'x__default_check_postgres__mutmut_3': x__default_check_postgres__mutmut_3
}

def _default_check_postgres(*args, **kwargs):
    result = _mutmut_trampoline(x__default_check_postgres__mutmut_orig, x__default_check_postgres__mutmut_mutants, args, kwargs)
    return result 

_default_check_postgres.__signature__ = _mutmut_signature(x__default_check_postgres__mutmut_orig)
x__default_check_postgres__mutmut_orig.__name__ = 'x__default_check_postgres'


def x__default_check_redis__mutmut_orig() -> bool:
    """Check Redis reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "health.py: redis connectivity check not implemented"
    )


def x__default_check_redis__mutmut_1() -> bool:
    """Check Redis reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        None
    )


def x__default_check_redis__mutmut_2() -> bool:
    """Check Redis reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "XXhealth.py: redis connectivity check not implementedXX"
    )


def x__default_check_redis__mutmut_3() -> bool:
    """Check Redis reachability. Replaced in tests via dependency injection."""
    raise NotImplementedError(  # pragma: no cover — infrastructure stub, replaced via DI in tests
        "HEALTH.PY: REDIS CONNECTIVITY CHECK NOT IMPLEMENTED"
    )

x__default_check_redis__mutmut_mutants : ClassVar[MutantDict] = {
'x__default_check_redis__mutmut_1': x__default_check_redis__mutmut_1, 
    'x__default_check_redis__mutmut_2': x__default_check_redis__mutmut_2, 
    'x__default_check_redis__mutmut_3': x__default_check_redis__mutmut_3
}

def _default_check_redis(*args, **kwargs):
    result = _mutmut_trampoline(x__default_check_redis__mutmut_orig, x__default_check_redis__mutmut_mutants, args, kwargs)
    return result 

_default_check_redis.__signature__ = _mutmut_signature(x__default_check_redis__mutmut_orig)
x__default_check_redis__mutmut_orig.__name__ = 'x__default_check_redis'


def x_health_check__mutmut_orig(
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


def x_health_check__mutmut_1(
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
    postgres_ok = None
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


def x_health_check__mutmut_2(
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
    redis_ok = None

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


def x_health_check__mutmut_3(
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

    if postgres_ok or redis_ok:
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


def x_health_check__mutmut_4(
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
        status = None
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


def x_health_check__mutmut_5(
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
        status = "XXhealthyXX"
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


def x_health_check__mutmut_6(
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
        status = "HEALTHY"
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


def x_health_check__mutmut_7(
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
    elif postgres_ok and redis_ok:
        status = "degraded"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_8(
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
        status = None
    else:
        status = "unhealthy"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_9(
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
        status = "XXdegradedXX"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_10(
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
        status = "DEGRADED"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_11(
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
        status = None

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_12(
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
        status = "XXunhealthyXX"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_13(
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
        status = "UNHEALTHY"

    return {
        "status": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_14(
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
        "XXstatusXX": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_15(
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
        "STATUS": status,
        "postgres": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_16(
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
        "XXpostgresXX": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_17(
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
        "POSTGRES": postgres_ok,
        "redis": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_18(
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
        "XXredisXX": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_19(
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
        "REDIS": redis_ok,
        "uptime_seconds": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_20(
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
        "XXuptime_secondsXX": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_21(
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
        "UPTIME_SECONDS": round(time.monotonic() - _START_TIME, 3),
    }


def x_health_check__mutmut_22(
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
        "uptime_seconds": round(None, 3),
    }


def x_health_check__mutmut_23(
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
        "uptime_seconds": round(time.monotonic() - _START_TIME, None),
    }


def x_health_check__mutmut_24(
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
        "uptime_seconds": round(3),
    }


def x_health_check__mutmut_25(
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
        "uptime_seconds": round(time.monotonic() - _START_TIME, ),
    }


def x_health_check__mutmut_26(
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
        "uptime_seconds": round(time.monotonic() + _START_TIME, 3),
    }


def x_health_check__mutmut_27(
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
        "uptime_seconds": round(time.monotonic() - _START_TIME, 4),
    }

x_health_check__mutmut_mutants : ClassVar[MutantDict] = {
'x_health_check__mutmut_1': x_health_check__mutmut_1, 
    'x_health_check__mutmut_2': x_health_check__mutmut_2, 
    'x_health_check__mutmut_3': x_health_check__mutmut_3, 
    'x_health_check__mutmut_4': x_health_check__mutmut_4, 
    'x_health_check__mutmut_5': x_health_check__mutmut_5, 
    'x_health_check__mutmut_6': x_health_check__mutmut_6, 
    'x_health_check__mutmut_7': x_health_check__mutmut_7, 
    'x_health_check__mutmut_8': x_health_check__mutmut_8, 
    'x_health_check__mutmut_9': x_health_check__mutmut_9, 
    'x_health_check__mutmut_10': x_health_check__mutmut_10, 
    'x_health_check__mutmut_11': x_health_check__mutmut_11, 
    'x_health_check__mutmut_12': x_health_check__mutmut_12, 
    'x_health_check__mutmut_13': x_health_check__mutmut_13, 
    'x_health_check__mutmut_14': x_health_check__mutmut_14, 
    'x_health_check__mutmut_15': x_health_check__mutmut_15, 
    'x_health_check__mutmut_16': x_health_check__mutmut_16, 
    'x_health_check__mutmut_17': x_health_check__mutmut_17, 
    'x_health_check__mutmut_18': x_health_check__mutmut_18, 
    'x_health_check__mutmut_19': x_health_check__mutmut_19, 
    'x_health_check__mutmut_20': x_health_check__mutmut_20, 
    'x_health_check__mutmut_21': x_health_check__mutmut_21, 
    'x_health_check__mutmut_22': x_health_check__mutmut_22, 
    'x_health_check__mutmut_23': x_health_check__mutmut_23, 
    'x_health_check__mutmut_24': x_health_check__mutmut_24, 
    'x_health_check__mutmut_25': x_health_check__mutmut_25, 
    'x_health_check__mutmut_26': x_health_check__mutmut_26, 
    'x_health_check__mutmut_27': x_health_check__mutmut_27
}

def health_check(*args, **kwargs):
    result = _mutmut_trampoline(x_health_check__mutmut_orig, x_health_check__mutmut_mutants, args, kwargs)
    return result 

health_check.__signature__ = _mutmut_signature(x_health_check__mutmut_orig)
x_health_check__mutmut_orig.__name__ = 'x_health_check'
