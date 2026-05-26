"""FR-03: LINE webhook adapter."""
from omnibot.errors import ValidationError
from omnibot.models import MessageType, Platform, UnifiedMessage

UNPROCESSABLE_ENTITY = 422
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class LineAdapter:
    """Parse LINE Messaging API webhook payloads into UnifiedMessage."""

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
