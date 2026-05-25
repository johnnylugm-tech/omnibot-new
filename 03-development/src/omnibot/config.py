"""FR-21: Configuration loader and settings dataclass.

Loads and validates all required environment variables at startup.
Fail-fast on missing critical keys.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import cast

from omnibot.errors import ConfigError


# ---------------------------------------------------------------------------
# Settings dataclass
# ---------------------------------------------------------------------------


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    # Required — bot tokens / channel secrets
    telegram_bot_token: str
    line_channel_secret: str

    # Required — infrastructure
    database_url: str
    redis_url: str

    # Optional — rate limiter
    rate_limit_rps: int = field(default=100)
    rate_limit_window: int = field(default=60)

    # Optional — IP whitelist
    ip_whitelist_cidrs: str = field(default="")

    # Optional — application
    log_level: str = field(default="INFO")


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------


class ConfigLoader:
    """Loads and validates configuration from environment variables."""

    @staticmethod
    def from_env() -> Settings:
        """Load all settings from environment variables.

        Raises:
            ConfigError: If any required environment variable is missing.

        Returns:
            Settings instance populated from the environment.
        """
        missing = []

        telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")

        line_channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
        if not line_channel_secret:
            missing.append("LINE_CHANNEL_SECRET")

        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            missing.append("DATABASE_URL")

        redis_url = os.environ.get("REDIS_URL")
        if not redis_url:
            missing.append("REDIS_URL")

        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ConfigError(f"Missing required environment variables: {missing_list}")

        # Parse optional rate limit settings
        rate_limit_rps = _parse_int_or_raise(
            os.environ.get("RATE_LIMIT_RPS", ""), default=100
        )
        rate_limit_window = _parse_int_or_raise(
            os.environ.get("RATE_LIMIT_WINDOW", ""), default=60
        )

        return Settings(
            telegram_bot_token=cast(str, telegram_bot_token),
            line_channel_secret=cast(str, line_channel_secret),
            database_url=cast(str, database_url),
            redis_url=cast(str, redis_url),
            rate_limit_rps=rate_limit_rps,
            rate_limit_window=rate_limit_window,
            ip_whitelist_cidrs=os.environ.get("IP_WHITELIST_CIDRS", ""),
            log_level=os.environ.get("LOG_LEVEL", "INFO"),
        )


def get_database_url() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def _parse_int_or_raise(value: str, *, default: int) -> int:
    """Parse an integer from a string, falling back to default if empty."""
    if not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ConfigError(
            f"Invalid integer value for environment variable: {value!r}"
        )