"""FR-21: Load and validate configuration from env vars; fail fast on missing keys.

SRS.md §FR-21:
  "Load and validate configuration from env vars: bot tokens, channel secrets,
   DB/Redis URLs, rate limiter settings; fail fast on missing keys."

Verification method (SRS):
  Unit test: all vars set -> correct Settings; missing critical key -> ConfigError

TEST_INVENTORY.yaml unit tests for FR-21:
  - test_fr21_settings_all_env_vars_set_creates_valid_config
  - test_fr21_missing_database_url_raises_config_error_with_key_list
  - test_fr21_optional_keys_use_defaults
  - test_fr21_config_validation_runs_at_startup_fail_fast
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

REQUIRED_ENV_KEYS = [
    "TELEGRAM_BOT_TOKEN",
    "LINE_CHANNEL_SECRET",
    "DATABASE_URL",
    "REDIS_URL",
]

OPTIONAL_ENV_KEYS = {
    "RATE_LIMIT_RPS": "100",
    "RATE_LIMIT_WINDOW": "60",
}


@pytest.fixture(autouse=True)
def _clean_env():
    """Ensure no omnibot env vars leak between tests."""
    all_keys = REQUIRED_ENV_KEYS + list(OPTIONAL_ENV_KEYS)
    for key in all_keys:
        os.environ.pop(key, None)


# ---------------------------------------------------------------------------
# Test 1 — all required env vars present -> valid Settings instance
# ---------------------------------------------------------------------------

def test_fr21_settings_all_env_vars_set_creates_valid_config():
    """FR-21: When every required env var is set, ConfigLoader.from_env()
    returns a Settings instance with the correct values."""

    # Import after fixture clears env — source doesn't exist yet, so this
    # import itself will fail (ImportError), which is the expected RED failure.
    from omnibot.config import ConfigLoader, Settings

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.update(OPTIONAL_ENV_KEYS)

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    assert isinstance(settings, Settings)
    assert settings.telegram_bot_token == "fake-telegram_bot_token"
    assert settings.line_channel_secret == "fake-line_channel_secret"
    assert settings.database_url == "fake-database_url"
    assert settings.redis_url == "fake-redis_url"


# ---------------------------------------------------------------------------
# Test 2 — missing DATABASE_URL raises ConfigError listing the key
# ---------------------------------------------------------------------------

def test_fr21_missing_database_url_raises_config_error_with_key_list():
    """FR-21: When a required env var is missing, ConfigLoader.from_env()
    raises ConfigError that names the missing key(s)."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.pop("DATABASE_URL")  # remove the critical key

    with patch.dict(os.environ, env, clear=False):
        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader.from_env()

    error_msg = str(exc_info.value).lower()
    assert "database_url" in error_msg, (
        f"ConfigError should mention the missing key 'DATABASE_URL'; "
        f"got: {exc_info.value}"
    )


# ---------------------------------------------------------------------------
# Test 3 — optional keys fall back to sensible defaults
# ---------------------------------------------------------------------------

def test_fr21_optional_keys_use_defaults():
    """FR-21: When optional env vars are absent, Settings uses defaults."""

    from omnibot.config import ConfigLoader  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    # Do NOT set RATE_LIMIT_RPS or RATE_LIMIT_WINDOW

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    assert hasattr(settings, "rate_limit_rps")
    assert settings.rate_limit_rps == 100, (
        f"Expected default rate_limit_rps=100, got {settings.rate_limit_rps}"
    )


# ---------------------------------------------------------------------------
# Test 4 — validation runs at startup and fails fast (no partial init)
# ---------------------------------------------------------------------------

def test_fr21_config_validation_runs_at_startup_fail_fast():
    """FR-21: Config validation must run during from_env() and raise before
    any Settings object is returned when required keys are missing."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.pop("TELEGRAM_BOT_TOKEN")

    with patch.dict(os.environ, env, clear=False):
        # Must raise — no Settings instance should be returned
        with pytest.raises(ConfigError):
            ConfigLoader.from_env()

    # If we reach here without the pytest.raises context raising, the test
    # fails because ConfigLoader.from_env() did NOT fail fast.
