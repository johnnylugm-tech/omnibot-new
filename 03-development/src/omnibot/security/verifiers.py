"""Webhook signature verification — FR-04 (Telegram) + FR-05 (LINE)."""

import base64
import hashlib
import hmac
from abc import ABC, abstractmethod


class WebhookVerifier(ABC):
    """Abstract base for webhook signature verification."""

    @abstractmethod
    def verify(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""


class TelegramWebhookVerifier(WebhookVerifier):
    """Verify Telegram webhook request signatures."""

    def __init__(self, bot_token: str):
        self.secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()

    def verify(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)


class LineWebhookVerifier(WebhookVerifier):
    """Verify LINE Messaging API webhook request signatures."""

    def __init__(self, channel_secret: str):
        self.channel_secret = channel_secret.encode("utf-8")

    def verify(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)
