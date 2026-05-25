"""Custom exception classes."""
from __future__ import annotations


class ConfigError(ValueError):
    """Raised when required configuration keys are missing."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ValidationError(Exception):
    """Raised when a payload fails validation."""

    def __init__(self, message: str, status_code: int = 422) -> None:
        super().__init__(message)
        self.status_code = status_code


class IPWhitelistError(Exception):
    """Raised when IP whitelist contains invalid CIDR at startup."""

    def __init__(self, invalid_cidrs: list[str]) -> None:
        self.invalid_cidrs = invalid_cidrs
        super().__init__(f"Invalid CIDR in whitelist config: {invalid_cidrs}")
