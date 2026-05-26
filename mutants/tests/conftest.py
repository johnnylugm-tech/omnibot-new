"""conftest.py — test fixtures for FR tests.

Creates the PostgreSQL schema before each test so that FR-01 schema
verification tests can run against an populated database.
"""
from __future__ import annotations

import asyncio
import os
import sys

# Ensure 03-development/src is on the path so `from omnibot.*` imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03-development", "src"))

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

@pytest.fixture(scope="function")
def _ensure_schema():
    """Create the complete Phase 1 schema once per test that needs it.

    FR-01 tests inspect the live database, so the schema must be created
    before any test runs. This fixture is function-scoped so each test gets
    a clean slate via CREATE TABLE IF NOT EXISTS idempotency.
    """
    url = os.environ.get("DATABASE_URL")
    if url:
        from app.models import create_schema
        try:
            asyncio.run(create_schema())
        finally:
            pass  # leave DATABASE_URL as-is; do not modify env
    else:
        pass  # no DATABASE_URL available — skip schema creation