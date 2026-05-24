"""Custom exception classes."""
from __future__ import annotations


class ValidationError(Exception):
    """Raised when a payload fails validation."""

    def __init__(self, message: str, status_code: int = 422) -> None:
        super().__init__(message)
        self.status_code = status_code
