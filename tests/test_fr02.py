"""[FR-02]  Accept Telegram Bot API webhook POST, parse into immutable UnifiedMessage.

SRS.md §FR-02:
  "Accept Telegram webhook POST, parse into UnifiedMessage."

Implementation function: TelegramAdapter.parse_message

Verification method (SRS):
  Unit test: valid Telegram JSON payload -> correct UnifiedMessage;
             invalid -> raises descriptive error

TEST_SPEC.md §FR-02 test cases (10 total):
  1. test_fr02_telegram_valid_payload_returns_unified_message
  2. test_fr02_telegram_missing_fields_raises_descriptive_error
  3. test_fr02_telegram_adapter_in_pipeline
  4. test_fr02_adapter_parse_empty_body_handled_gracefully
  5. test_fr02_adapter_parse_raw_payload_preserved_in_unified_message
  6. test_fr02_adapter_parse_unexpected_payload_structure_graceful
  7. test_fr02_adapter_parse_invalid_message_type_returns_422
  8. test_fr02_adapter_parse_malformed_unicode_no_crash
  9. test_fr02_parse_output_feeds_fr19_pipeline_as_unified_message
  10. test_fr02_missing_from_id_raises_descriptive_error
"""

from __future__ import annotations

import pytest


TELEGRAM_VALID_PAYLOAD = {
    "update_id": 123456789,
    "message": {
        "message_id": 1,
        "from": {
            "id": 123456789,
            "is_bot": False,
            "first_name": "Test",
            "last_name": "User",
            "language_code": "en",
        },
        "chat": {
            "id": 123456789,
            "type": "private",
        },
        "date": 1700000000,
        "text": "Hello, world!",
    },
}


# ---------------------------------------------------------------------------
# Test 1 — valid Telegram payload -> UnifiedMessage
# ---------------------------------------------------------------------------

def test_fr02_telegram_valid_payload_returns_unified_message():
    """FR-02 happy path."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = TelegramAdapter.parse_message(TELEGRAM_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.TELEGRAM
    assert result.platform_user_id == "123456789"
    assert result.content == "Hello, world!"


# ---------------------------------------------------------------------------
# Test 2 — missing required fields raises descriptive error
# ---------------------------------------------------------------------------

def test_fr02_telegram_missing_fields_raises_descriptive_error():
    """FR-02: missing message field raises ValidationError."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError

    payload = {"update_id": 123456789}

    with pytest.raises(ValidationError) as exc_info:
        TelegramAdapter.parse_message(payload)

    assert "message" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# Test 3 — TelegramAdapter used in the FR-19 pipeline
# ---------------------------------------------------------------------------

def test_fr02_telegram_adapter_in_pipeline():
    """FR-02 integration: TelegramAdapter.parse_message is callable
    by the FR-19 pipeline at stage 3 (Parse)."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import UnifiedMessage

    assert hasattr(TelegramAdapter, "parse_message")

    result = TelegramAdapter.parse_message(TELEGRAM_VALID_PAYLOAD)
    assert isinstance(result, UnifiedMessage)


# ---------------------------------------------------------------------------
# Test 4 — empty body handled gracefully
# ---------------------------------------------------------------------------

def test_fr02_adapter_parse_empty_body_handled_gracefully():
    """FR-02: empty dict raises ValidationError with descriptive message."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        TelegramAdapter.parse_message({})

    error_msg = str(exc_info.value).lower()
    assert any(field in error_msg for field in ("message", "update_id", "missing", "required"))


# ---------------------------------------------------------------------------
# Test 5 — raw payload preserved in UnifiedMessage
# ---------------------------------------------------------------------------

def test_fr02_adapter_parse_raw_payload_preserved_in_unified_message():
    """FR-02 validation: raw Telegram payload preserved in raw_payload field."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import UnifiedMessage

    result = TelegramAdapter.parse_message(TELEGRAM_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert hasattr(result, "raw_payload"), "UnifiedMessage must have raw_payload field"
    assert result.raw_payload == TELEGRAM_VALID_PAYLOAD


# ---------------------------------------------------------------------------
# Test 6 — unexpected payload structure handled gracefully
# ---------------------------------------------------------------------------

def test_fr02_adapter_parse_unexpected_payload_structure_graceful():
    """FR-02: edited_message is handled gracefully (returns UnifiedMessage)."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import UnifiedMessage

    edited_payload = {
        "update_id": 999999999,
        "edited_message": {
            "message_id": 2,
            "from": {"id": 987654321, "is_bot": False, "first_name": "Editor"},
            "chat": {"id": 987654321, "type": "private"},
            "date": 1700000001,
            "text": "Edited text",
            "edit_date": 1700000002,
        },
    }

    result = TelegramAdapter.parse_message(edited_payload)
    assert isinstance(result, UnifiedMessage)


# ---------------------------------------------------------------------------
# Test 7 — invalid message type returns 422
# ---------------------------------------------------------------------------

def test_fr02_adapter_parse_invalid_message_type_returns_422():
    """FR-02: photo message (no text) raises ValidationError with status_code=422."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError

    photo_payload = {
        "update_id": 555555555,
        "message": {
            "message_id": 3,
            "from": {"id": 111111111, "is_bot": False, "first_name": "PhotoUser"},
            "chat": {"id": 111111111, "type": "private"},
            "date": 1700000003,
            "photo": [{"file_id": "abc123", "width": 640, "height": 480}],
        },
    }

    with pytest.raises(ValidationError) as exc_info:
        TelegramAdapter.parse_message(photo_payload)

    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# Test 8 — malformed unicode does not crash
# ---------------------------------------------------------------------------

def test_fr02_adapter_parse_malformed_unicode_no_crash():
    """FR-02 NP-08: malformed unicode handled without crash."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import UnifiedMessage

    mixed_unicode_payload = {
        "update_id": 777777777,
        "message": {
            "message_id": 4,
            "from": {"id": 222222222, "is_bot": False, "first_name": "Unicode"},
            "chat": {"id": 222222222, "type": "private"},
            "date": 1700000004,
            "text": "Hello‮⁦world⁩߿",
        },
    }

    result = TelegramAdapter.parse_message(mixed_unicode_payload)
    assert isinstance(result, UnifiedMessage)


# ---------------------------------------------------------------------------
# Test 9 — output feeds FR-19 pipeline as UnifiedMessage
# ---------------------------------------------------------------------------

def test_fr02_parse_output_feeds_fr19_pipeline_as_unified_message():
    """FR-02 FR-19 integration: output consumed as UnifiedMessage by pipeline stage 3."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.models import Platform, UnifiedMessage

    result = TelegramAdapter.parse_message(TELEGRAM_VALID_PAYLOAD)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.TELEGRAM
    assert hasattr(result, "content")
    assert hasattr(result, "platform_user_id")
    assert hasattr(result, "raw_payload")
    # Immutable — verify mutation raises
    with pytest.raises(Exception):
        result.platform_user_id = "mutated"


# ---------------------------------------------------------------------------
# Test 10 — missing from.id raises descriptive error
# ---------------------------------------------------------------------------

def test_fr02_missing_from_id_raises_descriptive_error():
    """FR-02: message with no 'from' field raises ValidationError mentioning from.id."""
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError

    payload = {
        "update_id": 111111111,
        "message": {
            "message_id": 1,
            "chat": {"id": 999999999, "type": "private"},
            "date": 1700000000,
            "text": "Hello",
        },
    }

    with pytest.raises(ValidationError) as exc_info:
        TelegramAdapter.parse_message(payload)

    assert "from.id" in str(exc_info.value).lower()
    assert exc_info.value.status_code == 422
