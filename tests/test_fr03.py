"""FR-03: Accept LINE webhook POST, parse into immutable UnifiedMessage.

SRS.md §FR-03:
  "Accept LINE webhook POST, parse into UnifiedMessage with reply_token"

Implementation function: LineAdapter.parse_message

Verification method (SRS):
  Unit test: valid LINE JSON payload -> correct UnifiedMessage with reply_token;
             empty events -> handled gracefully
"""

from __future__ import annotations

import pytest


LINE_VALID_PAYLOAD = {
    "destination": "Uxxxxxxxx",
    "events": [
        {
            "type": "message",
            "message": {"type": "text", "id": "12345", "text": "Hello from LINE!"},
            "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
            "source": {"type": "user", "userId": "U123456"},
            "timestamp": 1462629479859,
            "mode": "active",
        }
    ],
}


# ---------------------------------------------------------------------------
# Test 1 — valid LINE payload -> UnifiedMessage
# ---------------------------------------------------------------------------

def test_fr03_line_valid_payload_returns_unified_message_with_reply_token():
    """FR-03 happy path."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = LineAdapter.parse_message(LINE_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.LINE
    assert result.platform_user_id == "U123456"
    assert result.content == "Hello from LINE!"
    assert result.reply_token == "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA"


# ---------------------------------------------------------------------------
# Test 2 — empty events handled gracefully
# ---------------------------------------------------------------------------

def test_fr03_line_empty_events_handled_gracefully():
    """FR-03: empty events array raises ValidationError."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    payload = {"destination": "Uxxxxxxxx", "events": []}

    with pytest.raises(ValidationError) as exc_info:
        LineAdapter.parse_message(payload)

    assert "events" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# Test 3 — missing events raises error
# ---------------------------------------------------------------------------

def test_fr03_line_missing_events_raises_error():
    """FR-03: missing events key raises ValidationError."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    with pytest.raises(ValidationError):
        LineAdapter.parse_message({})


# ---------------------------------------------------------------------------
# Test 4 — raw payload preserved
# ---------------------------------------------------------------------------

def test_fr03_line_raw_payload_preserved():
    """FR-03: raw LINE payload preserved in raw_payload field."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import UnifiedMessage

    result = LineAdapter.parse_message(LINE_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert result.raw_payload == LINE_VALID_PAYLOAD


# ---------------------------------------------------------------------------
# Test 5 — unsupported event type raises 422
# ---------------------------------------------------------------------------

def test_fr03_line_unsupported_event_type_raises_422():
    """FR-03: non-message event type raises ValidationError 422."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    payload = {
        "destination": "Uxxxxxxxx",
        "events": [
            {
                "type": "follow",
                "replyToken": "abc",
                "source": {"type": "user", "userId": "U123456"},
                "timestamp": 1462629479859,
                "mode": "active",
            }
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        LineAdapter.parse_message(payload)

    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# Test 6 — missing userId raises error
# ---------------------------------------------------------------------------

def test_fr03_line_missing_user_id_raises_error():
    """FR-03: missing source.userId raises ValidationError."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    payload = {
        "destination": "Uxxxxxxxx",
        "events": [
            {
                "type": "message",
                "message": {"type": "text", "id": "12345", "text": "Hello"},
                "replyToken": "abc",
                "source": {"type": "user"},
                "timestamp": 1462629479859,
                "mode": "active",
            }
        ],
    }

    with pytest.raises(ValidationError):
        LineAdapter.parse_message(payload)


# ---------------------------------------------------------------------------
# Test 7 — malformed unicode does not crash
# ---------------------------------------------------------------------------

def test_fr03_line_malformed_unicode_no_crash():
    """FR-03: malformed unicode handled without crash."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import UnifiedMessage

    payload = {
        "destination": "Uxxxxxxxx",
        "events": [
            {
                "type": "message",
                "message": {"type": "text", "id": "12345", "text": "Hello‮⁦world⁩"},
                "replyToken": "abc",
                "source": {"type": "user", "userId": "U123456"},
                "timestamp": 1462629479859,
                "mode": "active",
            }
        ],
    }

    result = LineAdapter.parse_message(payload)
    assert isinstance(result, UnifiedMessage)


# ---------------------------------------------------------------------------
# Test 8 — output feeds FR-19 pipeline
# ---------------------------------------------------------------------------

def test_fr03_line_output_feeds_fr19_pipeline():
    """FR-03 FR-19 integration: output consumed as UnifiedMessage."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = LineAdapter.parse_message(LINE_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.LINE
    assert result.platform_user_id == "U123456"
    assert result.reply_token is not None
    assert hasattr(result, "raw_payload")
    assert hasattr(result, "content")
