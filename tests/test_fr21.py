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


# ---------------------------------------------------------------------------
# Test 5 — application starts with valid config and env
# ---------------------------------------------------------------------------

def test_fr21_application_starts_with_valid_config_and_env():
    """FR-21: When all required env vars are set, the application starts
    cleanly with a valid Settings object returned by ConfigLoader.from_env()."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.update(OPTIONAL_ENV_KEYS)

    with patch.dict(os.environ, env, clear=False):
        # Should NOT raise
        settings = ConfigLoader.from_env()
        assert settings is not None

    # Verify all required attributes are accessible
    assert settings.telegram_bot_token == "fake-telegram_bot_token"
    assert settings.line_channel_secret == "fake-line_channel_secret"
    assert settings.database_url == "fake-database_url"
    assert settings.redis_url == "fake-redis_url"


# ---------------------------------------------------------------------------
# Test 6 — invalid rate limit capacity string raises ConfigError
# ---------------------------------------------------------------------------

def test_fr21_rate_limit_capacity_invalid_string_raises_error():
    """FR-21: When RATE_LIMIT_RPS or RATE_LIMIT_WINDOW contains an invalid
    integer string, ConfigLoader.from_env() raises ConfigError."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env["RATE_LIMIT_RPS"] = "not_a_number"  # invalid
    env["RATE_LIMIT_WINDOW"] = "60"

    with patch.dict(os.environ, env, clear=False):
        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader.from_env()

    error_msg = str(exc_info.value)
    assert "Invalid integer value" in error_msg
    assert "RATE_LIMIT_RPS" in error_msg or "not_a_number" in error_msg


# ---------------------------------------------------------------------------
# Test 7 — empty IP whitelist CIDRs defaults to empty string
# ---------------------------------------------------------------------------

def test_fr21_empty_ip_whitelist_cidrs_defaults_to_empty_string():
    """FR-21: When IP_WHITELIST_CIDRS is not set, the Settings attribute
    defaults to an empty string."""

    from omnibot.config import ConfigLoader  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    # Do NOT set IP_WHITELIST_CIDRS

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    assert hasattr(settings, "ip_whitelist_cidrs")
    assert settings.ip_whitelist_cidrs == "", (
        f"Expected default ip_whitelist_cidrs='', got {settings.ip_whitelist_cidrs!r}"
    )


# ---------------------------------------------------------------------------
# Test 8 — config provides settings to FR-04/FR-05 signature verifiers
# ---------------------------------------------------------------------------

def test_fr21_config_provides_settings_to_fr04_fr05_signature_verifiers():
    """FR-21: Settings carries telegram_bot_token and line_channel_secret
    that FR-04 (Telegram HMAC) and FR-05 (LINE HMAC) signature verifiers need."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.update(OPTIONAL_ENV_KEYS)

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    # Verify FR-04/FR-05 signature verifier inputs are present
    assert settings.telegram_bot_token == "fake-telegram_bot_token"
    assert settings.line_channel_secret == "fake-line_channel_secret"


# ---------------------------------------------------------------------------
# Test 9 — config provides settings to FR-10 rate limiter
# ---------------------------------------------------------------------------

def test_fr21_config_provides_settings_to_fr10_rate_limiter():
    """FR-21: Settings carries rate_limit_rps and rate_limit_window
    that the FR-10 token-bucket rate limiter requires."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env["RATE_LIMIT_RPS"] = "50"
    env["RATE_LIMIT_WINDOW"] = "30"

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    assert settings.rate_limit_rps == 50
    assert settings.rate_limit_window == 30


# ---------------------------------------------------------------------------
# Test 10 — config provides settings to FR-22 IP whitelist
# ---------------------------------------------------------------------------

def test_fr21_config_provides_settings_to_fr22_ip_whitelist():
    """FR-21: Settings carries ip_whitelist_cidrs that the FR-22
    IP whitelist middleware requires."""

    from omnibot.config import ConfigLoader  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env["IP_WHITELIST_CIDRS"] = "192.168.1.0/24,10.0.0.0/8"

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    assert settings.ip_whitelist_cidrs == "192.168.1.0/24,10.0.0.0/8"


# ---------------------------------------------------------------------------
# Test 11 — config provides database URL to FR-01 models
# ---------------------------------------------------------------------------

def test_fr21_config_provides_database_url_to_fr01_models():
    """FR-21: Settings carries database_url that the FR-01 models
    (PostgreSQL schema) require via get_database_url()."""

    from omnibot.config import ConfigLoader, get_database_url  # noqa: F811
    from omnibot.errors import ConfigError  # noqa: F811

    env = {k: f"fake-{k.lower()}" for k in REQUIRED_ENV_KEYS}
    env.update(OPTIONAL_ENV_KEYS)

    with patch.dict(os.environ, env, clear=False):
        settings = ConfigLoader.from_env()

    # FR-01 models use get_database_url() to access the DB connection string
    db_url = get_database_url()
    assert db_url == "fake-database_url"
    assert settings.database_url == "fake-database_url"
