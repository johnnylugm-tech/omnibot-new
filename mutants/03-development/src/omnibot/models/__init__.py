"""[FR-06] UnifiedMessage, Platform, and MessageType definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")
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


class Platform(Enum):
    TELEGRAM = "telegram"
    LINE = "line"
    MESSENGER = "messenger"    # Phase 2
    WHATSAPP = "whatsapp"      # Phase 2


class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    STICKER = "sticker"
    LOCATION = "location"
    FILE = "file"


@dataclass(frozen=True)
class UnifiedMessage:
    """Cross-platform normalized inbound message (immutable)."""
    platform: Platform
    platform_user_id: str
    unified_user_id: Optional[str]
    message_type: MessageType
    content: str
    raw_payload: dict = field(default_factory=dict)
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reply_token: Optional[str] = None


class KnowledgeSource(Enum):
    RULE = "rule"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class UnifiedResponse:
    """Cross-platform normalized outbound reply (immutable)."""
    content: str
    source: str
    confidence: float
    status_code: int = 200
    platform: Platform = Platform.TELEGRAM
    knowledge_id: Optional[int] = None
    emotion_adjustment: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ApiResponse(Generic[T]):
    """Generic API response wrapper."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class PaginatedResponse(ApiResponse[List[T]], Generic[T]):
    """Paginated API response."""
    total: int = 0
    page: int = 1
    limit: int = 20
    has_next: bool = False
