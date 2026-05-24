"""FR-17: Standardized error codes."""
from __future__ import annotations


def test_fr17_all_error_codes_defined():
    from omnibot.errors.codes import (
        AUTH_INVALID_SIGNATURE, RATE_LIMIT_EXCEEDED,
        KNOWLEDGE_NOT_FOUND, VALIDATION_ERROR, INTERNAL_ERROR,
    )
    assert AUTH_INVALID_SIGNATURE == "AUTH_INVALID_SIGNATURE"
    assert RATE_LIMIT_EXCEEDED == "RATE_LIMIT_EXCEEDED"
    assert KNOWLEDGE_NOT_FOUND == "KNOWLEDGE_NOT_FOUND"
    assert VALIDATION_ERROR == "VALIDATION_ERROR"
    assert INTERNAL_ERROR == "INTERNAL_ERROR"


def test_fr17_error_codes_map_to_http_status():
    from omnibot.errors.codes import HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP["AUTH_INVALID_SIGNATURE"] == 401
    assert HTTP_STATUS_MAP["RATE_LIMIT_EXCEEDED"] == 429
    assert HTTP_STATUS_MAP["KNOWLEDGE_NOT_FOUND"] == 404
    assert HTTP_STATUS_MAP["VALIDATION_ERROR"] == 422
    assert HTTP_STATUS_MAP["INTERNAL_ERROR"] == 500
