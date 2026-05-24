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

def test_fr06_unified_message_instantiation_succeeds():
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

def test_fr06_unified_message_mutation_raises_error():
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

def test_fr06_platform_enum_all_members():
    """FR-06: all Platform enum members present."""
    from omnibot.models import Platform

    members = {m.value for m in Platform}
    assert "telegram" in members
    assert "line" in members


# ---------------------------------------------------------------------------
# Test 5 — all MessageType enum members present
# ---------------------------------------------------------------------------

def test_fr06_message_type_enum_all_members():
    """FR-06: all MessageType enum members present."""
    from omnibot.models import MessageType

    members = {m.value for m in MessageType}
    assert "text" in members
    assert "image" in members


# ---------------------------------------------------------------------------
# Test 6 — UnifiedResponse instantiation
# ---------------------------------------------------------------------------

def test_fr06_unified_response_instantiation():
    """FR-06: UnifiedResponse instantiation."""
    from omnibot.models import UnifiedResponse

    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    assert resp.content == "answer"
    assert resp.source == "rule"
    assert resp.confidence == 0.95
    assert resp.knowledge_id is None
