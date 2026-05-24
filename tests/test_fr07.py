"""FR-07: Define ApiResponse and PaginatedResponse dataclasses.

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
