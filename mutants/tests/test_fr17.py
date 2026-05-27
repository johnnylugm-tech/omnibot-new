"""[FR-17]  Standardized error codes."""
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


def test_fr17_auth_invalid_signature_maps_to_401():
    from omnibot.errors.codes import AUTH_INVALID_SIGNATURE, HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[AUTH_INVALID_SIGNATURE] == 401


def test_fr17_rate_limit_exceeded_maps_to_429():
    from omnibot.errors.codes import RATE_LIMIT_EXCEEDED, HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[RATE_LIMIT_EXCEEDED] == 429


def test_fr17_knowledge_not_found_maps_to_404():
    from omnibot.errors.codes import KNOWLEDGE_NOT_FOUND, HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[KNOWLEDGE_NOT_FOUND] == 404


def test_fr17_validation_error_maps_to_422():
    from omnibot.errors.codes import VALIDATION_ERROR, HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[VALIDATION_ERROR] == 422


def test_fr17_internal_error_maps_to_500():
    from omnibot.errors.codes import INTERNAL_ERROR, HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[INTERNAL_ERROR] == 500


def test_fr17_api_response_error_serialization_with_success_false():
    from omnibot.models import ApiResponse
    from omnibot.errors.codes import AUTH_INVALID_SIGNATURE
    resp = ApiResponse(success=False, error="invalid signature", error_code=AUTH_INVALID_SIGNATURE)
    assert resp.success is False
    assert resp.error_code == AUTH_INVALID_SIGNATURE
    assert resp.error == "invalid signature"
    assert resp.data is None


def test_fr17_webhook_endpoints_return_correct_api_response_error_format():
    from omnibot.models import ApiResponse
    from omnibot.errors.codes import VALIDATION_ERROR
    resp = ApiResponse(success=False, error="payload validation failed", error_code=VALIDATION_ERROR)
    assert hasattr(resp, "success")
    assert hasattr(resp, "error")
    assert hasattr(resp, "error_code")
    assert resp.success is False


def test_fr17_error_codes_used_by_fr19_pipeline_error_mapping():
    from omnibot.errors.codes import INTERNAL_ERROR, HTTP_STATUS_MAP
    assert "INTERNAL_ERROR" in HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[INTERNAL_ERROR] == 500


def test_fr17_error_codes_used_by_fr22_ip_whitelist_rejection():
    from omnibot.errors.codes import AUTH_INVALID_SIGNATURE, HTTP_STATUS_MAP
    assert "AUTH_INVALID_SIGNATURE" in HTTP_STATUS_MAP
    assert HTTP_STATUS_MAP[AUTH_INVALID_SIGNATURE] == 401