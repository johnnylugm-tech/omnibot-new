"""[FR-02] Telegram webhook adapter.

Accepts Telegram Bot API webhook POST payloads and parses them into an
immutable UnifiedMessage.

Citations:
  - SRS.md FR-02: Accept Telegram webhook POST, parse into UnifiedMessage
  - SPEC.md lines 104-108 (Platform Adapter Layer architecture)
  - SPEC.md lines 412-451 (UnifiedMessage dataclass format)
"""
from __future__ import annotations

from omnibot.errors import ValidationError
from omnibot.models import MessageType, Platform, UnifiedMessage

UNPROCESSABLE_ENTITY = 422


class TelegramAdapter:
    @staticmethod
    def parse_message(payload: dict) -> UnifiedMessage:
        """[FR-02] Parse a Telegram Bot API update payload into UnifiedMessage.

        Supports both 'message' and 'edited_message' event types.
        Returns an immutable UnifiedMessage frozen dataclass.

        Raises:
            ValidationError (HTTP 422): When required fields (message,
                message.from.id, message.text) are missing or invalid.

        Citations:
          - SRS.md FR-02 verification: valid Telegram JSON -> UnifiedMessage
          - SPEC.md lines 412-451 (UnifiedMessage frozen dataclass fields)
        """
        telegram_msg = payload.get("message") or payload.get("edited_message")
        if telegram_msg is None:
            raise ValidationError(
                "Telegram payload missing required field: 'message'",
                status_code=UNPROCESSABLE_ENTITY,
            )

        sender = telegram_msg.get("from")
        if not sender or not sender.get("id"):
            raise ValidationError(
                "Telegram message missing required field: 'from.id'",
                status_code=UNPROCESSABLE_ENTITY,
            )

        text = telegram_msg.get("text")
        if text is None:
            raise ValidationError(
                "Telegram message has no 'text' field — unsupported message type",
                status_code=UNPROCESSABLE_ENTITY,
            )

        return UnifiedMessage(
            platform=Platform.TELEGRAM,
            platform_user_id=str(sender["id"]),
            unified_user_id=None,
            message_type=MessageType.TEXT,
            content=text,
            raw_payload=payload,
        )
