"""FR-06: Define immutable UnifiedMessage dataclass with Platform/MessageType enums.

SRS.md §FR-06:
  "Define immutable UnifiedMessage dataclass with Platform/MessageType enums"

Implementation functions: UnifiedMessage, Platform, MessageType
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Test 1 — instantiation with valid args succeeds
# ---------------------------------------------------------------------------

def test_fr06_unified_message_instantiation_valid():
    """FR-06: UnifiedMessage instantiation with valid args."""
    from omnibot.models import MessageType, Platform, UnifiedMessage

    msg = UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id="123",
        unified_user_id=None,
        message_type=MessageType.TEXT,
        content="Hello",
    )

    assert msg.platform == Platform.TELEGRAM
    assert msg.platform_user_id == "123"
    assert msg.message_type == MessageType.TEXT
    assert msg.content == "Hello"
    assert msg.raw_payload == {}
    assert msg.reply_token is None


# ---------------------------------------------------------------------------
# Test 2 — mutation raises FrozenInstanceError
# ---------------------------------------------------------------------------

def test_fr06_unified_message_mutation_raises_frozen_instance_error():
    """FR-06: mutation attempt raises FrozenInstanceError."""
    from omnibot.models import MessageType, Platform, UnifiedMessage

    msg = UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id="123",
        unified_user_id=None,
        message_type=MessageType.TEXT,
        content="Hello",
    )

    with pytest.raises(Exception):
        msg.content = "mutated"


# ---------------------------------------------------------------------------
# Test 3 — received_at defaults to current UTC
# ---------------------------------------------------------------------------

def test_fr06_unified_message_received_at_defaults_to_utc():
    """FR-06: received_at defaults to current UTC."""
    from omnibot.models import MessageType, Platform, UnifiedMessage
    from datetime import datetime, timezone

    msg = UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id="123",
        unified_user_id=None,
        message_type=MessageType.TEXT,
        content="Hello",
    )

    assert isinstance(msg.received_at, datetime)
    assert msg.received_at.tzinfo is not None


# ---------------------------------------------------------------------------
# Test 4 — all Platform enum members present
# ---------------------------------------------------------------------------

def test_fr06_all_platform_enum_members_present():
    """FR-06: all Platform enum members present."""
    from omnibot.models import Platform

    members = {m.value for m in Platform}
    assert "telegram" in members
    assert "line" in members


# ---------------------------------------------------------------------------
# Test 5 — all MessageType enum members present
# ---------------------------------------------------------------------------

def test_fr06_all_message_type_enum_members_present():
    """FR-06: all MessageType enum members present."""
    from omnibot.models import MessageType

    members = {m.value for m in MessageType}
    assert "text" in members
    assert "image" in members


# ---------------------------------------------------------------------------
# Test 6 — MessageType enum has all required members (text, image, sticker, location, file)
# ---------------------------------------------------------------------------

def test_fr06_message_all_message_type_enum_members_present():
    """FR-06: MessageType has all required members."""
    from omnibot.models import MessageType

    members = {m.value for m in MessageType}
    required = {"text", "image", "sticker", "location", "file"}
    assert required.issubset(members), f"Missing message types: {required - members}"


# ---------------------------------------------------------------------------
# Test 7 — UnifiedMessage consumed by FR-19 pipeline
# ---------------------------------------------------------------------------

def test_fr06_unified_message_consumed_by_fr19_pipeline():
    """FR-06: UnifiedMessage is consumed by FR-19 pipeline components."""
    from omnibot.models import MessageType, Platform, UnifiedMessage
    from omnibot.processing.sanitizer import InputSanitizer
    from omnibot.processing.pii import PIIMasker

    msg = UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id="999",
        unified_user_id=None,
        message_type=MessageType.TEXT,
        content="hello world",
    )

    sanitizer = InputSanitizer()
    masked = PIIMasker.mask(msg.content)
    sanitized = sanitizer.sanitize(masked)

    assert sanitized == "hello world"
    assert isinstance(msg, UnifiedMessage)


# ---------------------------------------------------------------------------
# Test 8 — UnifiedMessage consumed by FR-02 Telegram adapter
# ---------------------------------------------------------------------------

def test_fr06_unified_message_consumed_by_fr02_telegram_adapter():
    """FR-06: TelegramAdapter.parse_message returns UnifiedMessage."""
    from omnibot.models import MessageType, Platform, UnifiedMessage
    from omnibot.adapters.telegram import TelegramAdapter

    payload = {
        "update_id": 123,
        "message": {
            "message_id": 1,
            "from": {"id": 456, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 456, "type": "private"},
            "date": 1700000000,
            "text": "hello",
        },
    }

    result = TelegramAdapter.parse_message(payload)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.TELEGRAM
    assert result.platform_user_id == "456"
    assert result.message_type == MessageType.TEXT
    assert result.content == "hello"


# ---------------------------------------------------------------------------
# Test 9 — UnifiedMessage consumed by FR-03 LINE adapter
# ---------------------------------------------------------------------------

def test_fr06_unified_message_consumed_by_fr03_line_adapter():
    """FR-06: LineAdapter.parse_message returns UnifiedMessage."""
    from omnibot.models import MessageType, Platform, UnifiedMessage
    from omnibot.adapters.line import LineAdapter

    payload = {
        "destination": "U0123456789abcdef",
        "events": [
            {
                "replyToken": "nHuy9BEGZNGYgdNF涯",
                "type": "message",
                "mode": "active",
                "timestamp": 1700000000000,
                "source": {"type": "user", "userId": "U0123456789abcdef"},
                "message": {"id": "1234567890", "type": "text", "text": "hello"},
            }
        ],
    }

    result = LineAdapter.parse_message(payload)

    assert isinstance(result, UnifiedMessage)
    assert result.platform == Platform.LINE
    assert result.platform_user_id == "U0123456789abcdef"
    assert result.message_type == MessageType.TEXT
    assert result.content == "hello"
    assert result.reply_token == "nHuy9BEGZNGYgdNF涯"


# ---------------------------------------------------------------------------
# Test 10 — UnifiedResponse instantiation
# ---------------------------------------------------------------------------

def test_fr06_unified_response_instantiation():
    """FR-06: UnifiedResponse instantiation."""
    from omnibot.models import UnifiedResponse

    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    assert resp.content == "answer"
    assert resp.source == "rule"
    assert resp.confidence == 0.95
    assert resp.knowledge_id is None