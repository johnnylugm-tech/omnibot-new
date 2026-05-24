"""FR-06: UnifiedMessage, Platform, and MessageType definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


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


@dataclass(frozen=True)
class UnifiedResponse:
    """Cross-platform normalized outbound reply."""
    content: str
    source: str
    confidence: float
    knowledge_id: Optional[int] = None
    emotion_adjustment: Optional[str] = None


@dataclass
class ApiResponse(Generic[T]):
    """Generic API response wrapper."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class PaginatedResponse(ApiResponse[T]):
    """Paginated API response."""
    total: int = 0
    page: int = 1
    limit: int = 50
    has_next: bool = False
