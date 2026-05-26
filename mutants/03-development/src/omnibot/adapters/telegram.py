"""[FR-02] Telegram webhook adapter.

Accepts Telegram Bot API webhook POST payloads and parses them into an
immutable UnifiedMessage.

Citations:
  - SRS.md FR-02: Accept Telegram webhook POST, parse into UnifiedMessage
  - SPEC.md lines 104-108 (Platform Adapter Layer architecture)
  - SPEC.md lines 412-451 (UnifiedMessage dataclass format)
"""
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
