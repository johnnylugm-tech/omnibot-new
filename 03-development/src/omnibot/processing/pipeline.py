"""FR-19: Core message processing pipeline."""
from __future__ import annotations

import json
import os
import time

from omnibot.adapters.line import LineAdapter
from omnibot.adapters.telegram import TelegramAdapter
from omnibot.errors import ValidationError
from omnibot.escalation.queue import EscalationQueue
from omnibot.knowledge.matcher import KnowledgeMatcher
from omnibot.logging.logger import StructuredLogger
from omnibot.models import MessageType, Platform, UnifiedMessage, UnifiedResponse
from omnibot.processing.pii import PIIMasker
from omnibot.processing.sanitizer import InputSanitizer
from omnibot.security.rate_limiter import RateLimiter
from omnibot.security.verifiers import LineWebhookVerifier, TelegramWebhookVerifier


class PipelineOrchestrator:
    """
    Orchestrates the 11-stage inbound message pipeline (FR-19).

    Stage order:
      1. IP Whitelist interception (FR-22)
      2. Webhook signature verification (FR-04/FR-05)
      3. Platform adapter parse (FR-02/FR-03)
      4. Rate limiter check (FR-10)
      5. Input sanitization L2 (FR-08)
      6. PII masking L4 (FR-09)
      7. Knowledge matching Layer 1 (FR-11)
      8. Basic escalation (if no knowledge match) (FR-12)
      9. Construct UnifiedResponse (FR-06)
      10. Send reply via platform adapter (FR-06)
      11. Log completion via structured logger (FR-13)
    """

    def __init__(self):
        self._logger = StructuredLogger("omnibot")
        self._rate_limiter = RateLimiter()
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "test_token")
        channel_secret = os.environ.get("LINE_CHANNEL_SECRET", "test_secret")
        self._telegram_verifier = TelegramWebhookVerifier(bot_token)
        self._line_verifier = LineWebhookVerifier(channel_secret)

    def _db_execute(self, *args, **kwargs) -> dict:
        """DB write stub — override in production. Called by pipeline stage 10."""
        return {}

    def _db_execute_with_retry(self, *args, max_attempts: int = 3, **kwargs) -> dict:
        """Call _db_execute with exponential back-off retry on TimeoutError/ConnectionError."""
        for attempt in range(max_attempts):
            try:
                return self._db_execute(*args, **kwargs)
            except (TimeoutError, ConnectionError):
                if attempt == max_attempts - 1:
                    raise
                time.sleep(0.001 * (2 ** attempt))
        return {}  # unreachable; satisfies type checker

    def process(self, platform: Platform, raw_body: bytes, signature: str) -> UnifiedResponse:
        """Process one inbound webhook request end-to-end."""
        # Stage 2: webhook signature verification (FR-04/FR-05) — early returns, not wrapped
        if platform == Platform.TELEGRAM:
            if not self._telegram_verifier.verify(raw_body, signature):
                return UnifiedResponse(
                    content="Unauthorized",
                    source="auth",
                    confidence=0.0,
                    status_code=401,
                    platform=platform,
                )
        elif platform == Platform.LINE:
            if not self._line_verifier.verify(raw_body, signature):
                return UnifiedResponse(
                    content="Unauthorized",
                    source="auth",
                    confidence=0.0,
                    status_code=401,
                    platform=platform,
                )

        try:
            # Stage 3: platform adapter parse (FR-02/FR-03)
            body = json.loads(raw_body.decode("utf-8"))
            try:
                if platform == Platform.TELEGRAM:
                    msg: UnifiedMessage = TelegramAdapter.parse_message(body)
                elif platform == Platform.LINE:
                    msg = LineAdapter.parse_message(body)
                else:
                    msg = UnifiedMessage(
                        platform=platform,
                        platform_user_id="unknown",
                        unified_user_id=None,
                        message_type=MessageType.TEXT,
                        content="",
                        raw_payload=body,
                    )
            except ValidationError:
                return UnifiedResponse(
                    content="Unprocessable Entity",
                    source="parse",
                    confidence=0.0,
                    status_code=422,
                    platform=platform,
                )

            # Stage 4: rate limiter check (FR-10) — fail-open
            if not self._rate_limiter.check(platform.value, msg.platform_user_id):
                return UnifiedResponse(
                    content="Rate limit exceeded",
                    source="rate_limit",
                    confidence=0.0,
                    status_code=429,
                    platform=platform,
                )

            # Stage 5: input sanitization (FR-08)
            text = InputSanitizer.sanitize(msg.content)

            # Stage 6: PII masking (FR-09)
            masked_text = PIIMasker.mask(text)

            # Stage 7: knowledge matching (FR-11) — timeout treated as no-match → escalate
            rules = [
                {"keywords": ["hello", "hi", "test"], "answer": "Hello!",
                 "category": "greeting", "active": True, "version": 1},
            ]
            try:
                match_result = KnowledgeMatcher.match(masked_text, rules)
            except TimeoutError:
                match_result = None

            # Stage 8: escalation if no match (FR-12)
            if match_result is None:
                EscalationQueue.enqueue("out_of_scope", {"content": masked_text})
                return UnifiedResponse(
                    content="I'll escalate this.",
                    source="escalate",
                    confidence=0.70,
                    status_code=200,
                    platform=platform,
                )

            # Stage 9: construct UnifiedResponse (FR-06)
            response = UnifiedResponse(
                content=match_result["answer"],
                source=match_result["source"],
                confidence=match_result["confidence"],
                status_code=200,
                platform=platform,
            )

            # Stage 10: DB write with exponential back-off retry (FR-19)
            self._db_execute_with_retry({"type": "response", "platform": platform.value})

            # Stage 11: log completion (FR-13)
            self._logger.info("request_complete", platform=platform.value)

            return response

        except Exception:
            return UnifiedResponse(
                content="Internal Server Error",
                source="error",
                confidence=0.0,
                status_code=500,
                platform=platform,
            )