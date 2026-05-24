"""Webhook signature verification — FR-04 (Telegram) + FR-05 (LINE)."""
from __future__ import annotations

from abc import ABC, abstractmethod
import base64
import hashlib
import hmac


class WebhookVerifier(ABC):
    @abstractmethod
    def verify(self, body: bytes, signature: str) -> bool: ...


class TelegramWebhookVerifier(WebhookVerifier):
    def __init__(self, bot_token: str):
        self.secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()

    def verify(self, body: bytes, signature: str) -> bool:
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)


class LineWebhookVerifier(WebhookVerifier):
    def __init__(self, channel_secret: str):
        self.channel_secret = channel_secret.encode("utf-8")

    def verify(self, body: bytes, signature: str) -> bool:
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)
