"""
FR-14: Health check endpoint tests.

NFR-06: reliability — health check < 500ms, returns HTTP 200 even when degraded.

TDD-RED: Tests written before full HTTP integration (FastAPI route) is wired up.
         health_check() function is tested directly with injected connectivity checks.
"""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from omnibot.infrastructure.health import health_check

# ---------------------------------------------------------------------------
# Correctness: status derivation
# ---------------------------------------------------------------------------

class TestHealthCheckStatus:

    def test_both_up_returns_healthy(self):
        result = health_check(check_postgres=lambda: True, check_redis=lambda: True)
        assert result["status"] == "healthy"
        assert result["postgres"] is True
        assert result["redis"] is True

    def test_postgres_down_returns_degraded(self):
        result = health_check(check_postgres=lambda: False, check_redis=lambda: True)
        assert result["status"] == "degraded"
        assert result["postgres"] is False
        assert result["redis"] is True

    def test_redis_down_returns_degraded(self):
        result = health_check(check_postgres=lambda: True, check_redis=lambda: False)
        assert result["status"] == "degraded"
        assert result["postgres"] is True
        assert result["redis"] is False

    def test_both_down_returns_unhealthy(self):
        result = health_check(check_postgres=lambda: False, check_redis=lambda: False)
        assert result["status"] == "unhealthy"
        assert result["postgres"] is False
        assert result["redis"] is False

    def test_response_includes_uptime_seconds(self):
        result = health_check(check_postgres=lambda: True, check_redis=lambda: True)
        assert "uptime_seconds" in result
        assert isinstance(result["uptime_seconds"], float)
        assert result["uptime_seconds"] >= 0.0

    def test_uptime_increases_between_calls(self):
        r1 = health_check(check_postgres=lambda: True, check_redis=lambda: True)
        time.sleep(0.01)
        r2 = health_check(check_postgres=lambda: True, check_redis=lambda: True)
        assert r2["uptime_seconds"] > r1["uptime_seconds"]


# ---------------------------------------------------------------------------
# NFR-06: always returns HTTP 200 even when degraded
# (tested at function level — HTTP layer wraps this with status 200 always)
# ---------------------------------------------------------------------------

class TestHealthCheckAlways200:

    def test_degraded_state_does_not_raise(self):
        """health_check() must not raise when a dependency is down."""
        try:
            health_check(check_postgres=lambda: False, check_redis=lambda: True)
        except Exception as exc:
            pytest.fail(f"health_check() raised {exc!r} on degraded state")

    def test_unhealthy_state_does_not_raise(self):
        """health_check() must not raise when both dependencies are down."""
        try:
            health_check(check_postgres=lambda: False, check_redis=lambda: False)
        except Exception as exc:
            pytest.fail(f"health_check() raised {exc!r} on unhealthy state")


# ---------------------------------------------------------------------------
# NFR-06: response time < 500ms
# CI tolerance: 1000ms (slow CI machines) with fast mocked dependencies.
# ---------------------------------------------------------------------------

class TestHealthCheckResponseTime:
    _CI_TIMEOUT_MS = 1000  # ms — NFR target is 500ms; CI tolerance 2×

    def test_healthy_response_within_ci_timeout(self):
        start = time.perf_counter()
        health_check(check_postgres=lambda: True, check_redis=lambda: True)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < self._CI_TIMEOUT_MS, (
            f"health_check() took {elapsed_ms:.1f}ms (CI limit {self._CI_TIMEOUT_MS}ms, "
            f"NFR-06 target 500ms)"
        )

    def test_degraded_response_within_ci_timeout(self):
        """Degraded path (one dep down) must also be fast — no blocking retries."""
        start = time.perf_counter()
        health_check(check_postgres=lambda: False, check_redis=lambda: True)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < self._CI_TIMEOUT_MS, (
            f"health_check() degraded path took {elapsed_ms:.1f}ms "
            f"(NFR-06 target 500ms)"
        )
