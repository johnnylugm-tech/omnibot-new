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


# ---------------------------------------------------------------------------
# Test 9 — adapter in pipeline context
# ---------------------------------------------------------------------------

def test_fr03_line_adapter_in_pipeline():
    """FR-03: LineAdapter integrates as a pipeline stage."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = LineAdapter.parse_message(LINE_VALID_PAYLOAD)

    # Pipeline contract: returns UnifiedMessage
    assert isinstance(result, UnifiedMessage)
    # Pipeline contract: reply_token preserved for reply routing
    assert result.reply_token is not None
    # Pipeline contract: platform identified correctly
    assert result.platform == Platform.LINE
    # Pipeline contract: content present for downstream LLM
    assert isinstance(result.content, str)
    assert len(result.content) > 0


# ---------------------------------------------------------------------------
# Test 10 — adapter parse with invalid JSON raises error
# ---------------------------------------------------------------------------

def test_fr03_adapter_parse_invalid_json_raises_error():
    """FR-03: non-dict input raises error."""
    from omnibot.adapters.line import LineAdapter

    invalid_inputs = ["not a dict", [1, 2, 3], 42, None, b"bytes"]

    for bad_input in invalid_inputs:
        try:
            LineAdapter.parse_message(bad_input)
            assert False, f"Expected error for input: {bad_input!r}"
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Test 11 — raw payload preserved in UnifiedMessage
# ---------------------------------------------------------------------------

def test_fr03_adapter_parse_raw_payload_preserved_in_unified_message():
    """FR-03: raw_payload in UnifiedMessage matches original dict."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import UnifiedMessage

    payload = {
        "destination": "Uxxxxxxxx",
        "events": [
            {
                "type": "message",
                "message": {"type": "text", "id": "99999", "text": "Payload test"},
                "replyToken": "tok_abc",
                "source": {"type": "user", "userId": "U_test"},
                "timestamp": 1600000000000,
                "mode": "active",
            }
        ],
    }

    result = LineAdapter.parse_message(payload)
    assert isinstance(result, UnifiedMessage)
    assert result.raw_payload == payload


# ---------------------------------------------------------------------------
# Test 12 — unexpected event type handled gracefully
# ---------------------------------------------------------------------------

def test_fr03_adapter_parse_unexpected_event_type_graceful():
    """FR-03: unsupported event types raise ValidationError without crash."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    for event_type in ("follow", "unfollow", "join", "leave", "postback", "beacon"):
        payload = {
            "destination": "Uxxxxxxxx",
            "events": [
                {
                    "type": event_type,
                    "replyToken": "tok",
                    "source": {"type": "user", "userId": "U123"},
                    "timestamp": 1462629479859,
                    "mode": "active",
                }
            ],
        }
        with pytest.raises(ValidationError):
            LineAdapter.parse_message(payload)


# ---------------------------------------------------------------------------
# Test 13 — missing message field returns 422
# ---------------------------------------------------------------------------

def test_fr03_adapter_parse_missing_message_field_returns_422():
    """FR-03: event with no message field raises 422."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError

    # Event without a 'message' key at all
    payload = {
        "destination": "Uxxxxxxxx",
        "events": [
            {
                "type": "message",
                "replyToken": "tok",
                "source": {"type": "user", "userId": "U123"},
                "timestamp": 1462629479859,
                "mode": "active",
            }
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        LineAdapter.parse_message(payload)

    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# Test 14 — malformed unicode does not crash (adapter variant)
# ---------------------------------------------------------------------------

def test_fr03_adapter_parse_malformed_unicode_no_crash():
    """FR-03: adapter handles unicode edge cases without crash."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import UnifiedMessage

    tricky_texts = [
        "Hello​world",          # zero-width space
        "😀",               # surrogate pair (emoji)
        "Café",                  # composed character
        "\x00null\x00byte",      # embedded nulls
    ]

    for text in tricky_texts:
        payload = {
            "destination": "Uxxxxxxxx",
            "events": [
                {
                    "type": "message",
                    "message": {"type": "text", "id": "12345", "text": text},
                    "replyToken": "abc",
                    "source": {"type": "user", "userId": "U123456"},
                    "timestamp": 1462629479859,
                    "mode": "active",
                }
            ],
        }
        result = LineAdapter.parse_message(payload)
        assert isinstance(result, UnifiedMessage)
        assert isinstance(result.content, str)


# ---------------------------------------------------------------------------
# Test 15 — output feeds FR-19 pipeline (pipeline variant)
# ---------------------------------------------------------------------------

def test_fr03_parse_output_feeds_fr19_pipeline_as_unified_message():
    """FR-03 FR-19 integration: parse_message output is pipeline-ready."""
    from omnibot.adapters.line import LineAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = LineAdapter.parse_message(LINE_VALID_PAYLOAD)

    # Pipeline requirements for FR-19 (LLM routing)
    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.LINE
    assert result.platform_user_id is not None
    assert result.reply_token is not None
    assert result.message_type is not None
    assert isinstance(result.content, str)

    # Simulate downstream FR-19 consumption
    pipeline_input = {
        "platform": result.platform.value,
        "user_id": result.platform_user_id,
        "content": result.content,
        "reply_token": result.reply_token,
    }
    assert pipeline_input["platform"] == "line"
    assert pipeline_input["user_id"] == "U123456"
    assert pipeline_input["content"] == "Hello from LINE!"
    assert pipeline_input["reply_token"] == "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA"
