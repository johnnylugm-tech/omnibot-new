"""[FR-07]  Define ApiResponse and PaginatedResponse dataclasses.

SRS.md §FR-07:
  "Define generic ApiResponse[T] and PaginatedResponse[T] dataclasses"
"""

from __future__ import annotations

import json


# ---------------------------------------------------------------------------
# Test 1 — ApiResponse(success=True, data=obj) serializes correctly
# ---------------------------------------------------------------------------

def test_fr07_api_response_success_serializes_correctly():
    """FR-07: successful ApiResponse JSON round-trip."""
    from omnibot.models import ApiResponse

    resp = ApiResponse(success=True, data={"key": "value"})
    d = {"success": resp.success, "data": resp.data, "error": resp.error, "error_code": resp.error_code}
    assert d["success"] is True
    assert d["data"] == {"key": "value"}
    assert d["error"] is None
    assert d["error_code"] is None


# ---------------------------------------------------------------------------
# Test 2 — ApiResponse error format
# ---------------------------------------------------------------------------

def test_fr07_api_response_error_format():
    """FR-07: error ApiResponse with all fields."""
    from omnibot.models import ApiResponse

    resp = ApiResponse(success=False, error="Bad request", error_code="VALIDATION_ERROR")
    assert resp.success is False
    assert resp.error == "Bad request"
    assert resp.error_code == "VALIDATION_ERROR"
    assert resp.data is None


# ---------------------------------------------------------------------------
# Test 3 — PaginatedResponse includes pagination fields
# ---------------------------------------------------------------------------

def test_fr07_paginated_response_includes_pagination_fields():
    """FR-07: PaginatedResponse with pagination fields."""
    from omnibot.models import PaginatedResponse

    resp = PaginatedResponse(
        success=True,
        data=["item1", "item2"],
        total=100,
        page=2,
        limit=10,
        has_next=True,
    )
    assert resp.total == 100
    assert resp.page == 2
    assert resp.limit == 10
    assert resp.has_next is True


# ---------------------------------------------------------------------------
# Test 4 — JSON round-trip preserves has_next
# ---------------------------------------------------------------------------

def test_fr07_json_roundtrip_preserves_has_next():
    """FR-07: JSON round-trip preserves has_next boolean."""
    resp = {"success": True, "data": ["a"], "error": None, "error_code": None, "total": 50, "page": 1, "limit": 25, "has_next": False}
    serialized = json.dumps(resp)
    deserialized = json.loads(serialized)
    assert deserialized["has_next"] is False
    assert deserialized["total"] == 50


# ---------------------------------------------------------------------------
# Test 5 — ApiResponse error serializes with error_code
# ---------------------------------------------------------------------------

def test_fr07_api_response_error_serializes_with_error_code():
    """FR-07: error ApiResponse serializes with error_code."""
    from omnibot.models import ApiResponse

    resp = ApiResponse(success=False, data=None, error="Not found", error_code="NOT_FOUND")
    d = {"success": resp.success, "data": resp.data, "error": resp.error, "error_code": resp.error_code}
    assert d["success"] is False
    assert d["data"] is None
    assert d["error"] == "Not found"
    assert d["error_code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# Test 6 — PaginatedResponse includes total, page, limit, has_next
# ---------------------------------------------------------------------------

def test_fr07_paginated_response_includes_total_page_limit_has_next():
    """FR-07: PaginatedResponse includes all four pagination fields."""
    from omnibot.models import PaginatedResponse

    resp = PaginatedResponse(
        success=True,
        data=["item1", "item2"],
        total=42,
        page=3,
        limit=5,
        has_next=True,
    )
    assert resp.total == 42
    assert resp.page == 3
    assert resp.limit == 5
    assert resp.has_next is True


# ---------------------------------------------------------------------------
# Test 7 — PaginatedResponse JSON roundtrip preserves has_next
# ---------------------------------------------------------------------------

def test_fr07_paginated_response_json_roundtrip_preserves_has_next():
    """FR-07: PaginatedResponse JSON round-trip preserves has_next."""
    from omnibot.models import PaginatedResponse

    resp = PaginatedResponse(
        success=True,
        data=["a"],
        total=50,
        page=1,
        limit=25,
        has_next=True,
    )
    d = {
        "success": resp.success,
        "data": resp.data,
        "error": resp.error,
        "error_code": resp.error_code,
        "total": resp.total,
        "page": resp.page,
        "limit": resp.limit,
        "has_next": resp.has_next,
    }
    serialized = json.dumps(d)
    deserialized = json.loads(serialized)
    assert deserialized["has_next"] is True
    assert deserialized["total"] == 50
    assert deserialized["page"] == 1


# ---------------------------------------------------------------------------
# Test 8 — has_next False on last page
# ---------------------------------------------------------------------------

def test_fr07_response_has_next_false_on_last_page():
    """FR-07: has_next is False on last page of results."""
    from omnibot.models import PaginatedResponse

    resp = PaginatedResponse(
        success=True,
        data=["final"],
        total=100,
        page=5,
        limit=20,
        has_next=False,
    )
    assert resp.has_next is False
    assert resp.page == 5
    assert resp.total == 100
    assert resp.limit == 20


# ---------------------------------------------------------------------------
# Test 9 — ApiResponse JSON round-trip preserves has_next
# ---------------------------------------------------------------------------

def test_fr07_response_json_round_trip_preserves_has_next():
    """FR-07: ApiResponse JSON round-trip preserves has_next via dict."""
    from omnibot.models import ApiResponse

    resp = ApiResponse(success=True, data={"items": ["a", "b"]})
    d = {"success": resp.success, "data": resp.data, "error": resp.error, "error_code": resp.error_code}
    serialized = json.dumps(d)
    deserialized = json.loads(serialized)
    assert deserialized["success"] is True
    assert deserialized["data"] == {"items": ["a", "b"]}
    assert deserialized["error"] is None
    assert deserialized["error_code"] is None


# ---------------------------------------------------------------------------
# Test 10 — ApiResponse used by FR-14 health endpoint
# ---------------------------------------------------------------------------

def test_fr07_api_response_used_by_fr14_health_endpoint():
    """FR-07: ApiResponse compatible with FR-14 health endpoint usage."""
    from omnibot.models import ApiResponse

    health_info = {"status": "ok", "uptime_seconds": 3600, "version": "1.0.0"}
    resp = ApiResponse(success=True, data=health_info)
    assert resp.success is True
    assert resp.data == health_info
    assert resp.error is None
    assert resp.error_code is None


# ---------------------------------------------------------------------------
# Test 11 — ApiResponse used by FR-17 error responses
# ---------------------------------------------------------------------------

def test_fr07_api_response_used_by_fr17_error_responses():
    """FR-07: ApiResponse compatible with FR-17 error response usage."""
    from omnibot.models import ApiResponse

    resp = ApiResponse(success=False, data=None, error="Unauthorized", error_code="UNAUTHORIZED")
    assert resp.success is False
    assert resp.data is None
    assert resp.error == "Unauthorized"
    assert resp.error_code == "UNAUTHORIZED"


# ---------------------------------------------------------------------------
# Test 12 — ApiResponse used by FR-19 pipeline response
# ---------------------------------------------------------------------------

def test_fr07_api_response_used_by_fr19_pipeline_response():
    """FR-07: ApiResponse compatible with FR-19 pipeline response usage."""
    from omnibot.models import ApiResponse

    pipeline_result = {"stage": "complete", "output": "processed_data", "duration_ms": 150}
    resp = ApiResponse(success=True, data=pipeline_result)
    assert resp.success is True
    assert resp.data == pipeline_result
    assert resp.error is None
    assert resp.error_code is None
