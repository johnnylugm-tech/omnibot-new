"""FR-03: LINE webhook adapter."""
from __future__ import annotations

from omnibot.errors import ValidationError
from omnibot.models import MessageType, Platform, UnifiedMessage

UNPROCESSABLE_ENTITY = 422


class LineAdapter:
    @staticmethod
    def parse_message(payload: dict) -> UnifiedMessage:
        """Parse a LINE Messaging API webhook payload into UnifiedMessage.

        Raises ValidationError (HTTP 422) when required fields are missing.
        """
        events = payload.get("events")
        if not events:
            raise ValidationError(
                "LINE payload has no 'events' array",
                status_code=UNPROCESSABLE_ENTITY,
            )

        event = events[0]
        event_type = event.get("type", "")
        if event_type != "message":
            raise ValidationError(
                f"LINE event type '{event_type}' is not supported",
                status_code=UNPROCESSABLE_ENTITY,
            )

        message = event.get("message") or {}
        text = message.get("text")
        if text is None:
            raise ValidationError(
                "LINE message has no 'text' field — unsupported message type",
                status_code=UNPROCESSABLE_ENTITY,
            )

        source = event.get("source") or {}
        platform_user_id = source.get("userId")
        if not platform_user_id:
            raise ValidationError(
                "LINE event missing required field: 'source.userId'",
                status_code=UNPROCESSABLE_ENTITY,
            )

        reply_token = event.get("replyToken")

        return UnifiedMessage(
            platform=Platform.LINE,
            platform_user_id=str(platform_user_id),
            unified_user_id=None,
            message_type=MessageType.TEXT,
            content=text,
            raw_payload=payload,
            reply_token=reply_token,
        )
