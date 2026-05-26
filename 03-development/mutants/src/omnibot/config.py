"""FR-21: Configuration loader and settings dataclass.

Loads and validates all required environment variables at startup.
Fail-fast on missing critical keys.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import cast

from omnibot.errors import ConfigError
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


def x_get_database_url__mutmut_orig() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_1() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = None
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_2() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get(None)
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_3() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("XXDATABASE_URLXX")
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_4() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("database_url")
    if not url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_5() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if url:
        raise ConfigError("DATABASE_URL environment variable is not set")
    return url


def x_get_database_url__mutmut_6() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError(None)
    return url


def x_get_database_url__mutmut_7() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError("XXDATABASE_URL environment variable is not setXX")
    return url


def x_get_database_url__mutmut_8() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError("database_url environment variable is not set")
    return url


def x_get_database_url__mutmut_9() -> str:
    """Return the DATABASE_URL environment variable.

    Raises:
        ConfigError: If the variable is not set.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ConfigError("DATABASE_URL ENVIRONMENT VARIABLE IS NOT SET")
    return url

x_get_database_url__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_database_url__mutmut_1': x_get_database_url__mutmut_1, 
    'x_get_database_url__mutmut_2': x_get_database_url__mutmut_2, 
    'x_get_database_url__mutmut_3': x_get_database_url__mutmut_3, 
    'x_get_database_url__mutmut_4': x_get_database_url__mutmut_4, 
    'x_get_database_url__mutmut_5': x_get_database_url__mutmut_5, 
    'x_get_database_url__mutmut_6': x_get_database_url__mutmut_6, 
    'x_get_database_url__mutmut_7': x_get_database_url__mutmut_7, 
    'x_get_database_url__mutmut_8': x_get_database_url__mutmut_8, 
    'x_get_database_url__mutmut_9': x_get_database_url__mutmut_9
}

def get_database_url(*args, **kwargs):
    result = _mutmut_trampoline(x_get_database_url__mutmut_orig, x_get_database_url__mutmut_mutants, args, kwargs)
    return result 

get_database_url.__signature__ = _mutmut_signature(x_get_database_url__mutmut_orig)
x_get_database_url__mutmut_orig.__name__ = 'x_get_database_url'


def x__parse_int_or_raise__mutmut_orig(value: str, *, default: int) -> int:
    """Parse an integer from a string, falling back to default if empty."""
    if not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ConfigError(
            f"Invalid integer value for environment variable: {value!r}"
        )


def x__parse_int_or_raise__mutmut_1(value: str, *, default: int) -> int:
    """Parse an integer from a string, falling back to default if empty."""
    if value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ConfigError(
            f"Invalid integer value for environment variable: {value!r}"
        )


def x__parse_int_or_raise__mutmut_2(value: str, *, default: int) -> int:
    """Parse an integer from a string, falling back to default if empty."""
    if not value.strip():
        return default
    try:
        return int(None)
    except ValueError:
        raise ConfigError(
            f"Invalid integer value for environment variable: {value!r}"
        )


def x__parse_int_or_raise__mutmut_3(value: str, *, default: int) -> int:
    """Parse an integer from a string, falling back to default if empty."""
    if not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ConfigError(
            None
        )

x__parse_int_or_raise__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_int_or_raise__mutmut_1': x__parse_int_or_raise__mutmut_1, 
    'x__parse_int_or_raise__mutmut_2': x__parse_int_or_raise__mutmut_2, 
    'x__parse_int_or_raise__mutmut_3': x__parse_int_or_raise__mutmut_3
}

def _parse_int_or_raise(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_int_or_raise__mutmut_orig, x__parse_int_or_raise__mutmut_mutants, args, kwargs)
    return result 

_parse_int_or_raise.__signature__ = _mutmut_signature(x__parse_int_or_raise__mutmut_orig)
x__parse_int_or_raise__mutmut_orig.__name__ = 'x__parse_int_or_raise'