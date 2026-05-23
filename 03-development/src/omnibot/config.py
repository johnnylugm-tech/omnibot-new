"""[FR-01] PostgreSQL database configuration.

Citations:
  - SPEC.md lines 1772-1787 (users table schema)
"""
from __future__ import annotations

import os
from typing import Final

DATABASE_URL_ENV_VAR: Final[str] = "DATABASE_URL"


def get_database_url() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if not url:
        raise ValueError(f"Environment variable {DATABASE_URL_ENV_VAR!r} is not set")
    return url