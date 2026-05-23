"""conftest.py — test fixtures for FR tests.

Creates the PostgreSQL schema before each test so that FR-01 schema
verification tests can run against an populated database.
"""
from __future__ import annotations

import asyncio
import os

import pytest


# ---------------------------------------------------------------------------
# Database URL helper
# ---------------------------------------------------------------------------

def _require_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL not set — cannot run DB integration tests")
    return url


# ---------------------------------------------------------------------------
# Schema creation fixture (autouse for DB-dependent tests)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function", autouse=True)
def _ensure_schema():
    """Create the complete Phase 1 schema once per test that needs it.

    FR-01 tests inspect the live database, so the schema must be created
    before any test runs. This fixture is function-scoped so each test gets
    a clean slate via CREATE TABLE IF NOT EXISTS idempotency.
    """
    url = _require_database_url()
    if not url:
        return  # skipped — no DB available

    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03-development", "src"))

    from omnibot.db import create_schema
    from omnibot.config import get_database_url

    # Suppress ConfigError if DATABASE_URL is missing from env
    # by providing a dummy value so the import succeeds.
    original_env = os.environ.get("DATABASE_URL")
    if not original_env:
        os.environ["DATABASE_URL"] = url

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_schema())
    finally:
        if original_env is None:
            os.environ.pop("DATABASE_URL", None)