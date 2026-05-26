"""FR-19: Core message processing pipeline."""

from __future__ import annotations

import json
import os

from omnibot.adapters.line import LineAdapter
from omnibot.adapters.telegram import TelegramAdapter
from omnibot.errors import ValidationError
from omnibot.escalation.queue import EscalationQueue
from omnibot.knowledge.matcher import KnowledgeMatcher
from omnibot.logging.logger import StructuredLogger
from omnibot.models import Platform, UnifiedResponse
from omnibot.processing.pii import PIIMasker
from omnibot.processing.sanitizer import InputSanitizer
from omnibot.security.rate_limiter import RateLimiter
from omnibot.security.verifiers import LineWebhookVerifier, TelegramWebhookVerifier

_logger = StructuredLogger(__name__)


def _telegram_verifier():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def _line_verifier():
    secret = os.environ.get("LINE_CHANNEL_SECRET", "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


class PipelineOrchestrator:
    """
    Orchestrates the 11-stage inbound message pipeline (FR-19).

    Stage order:
      1. IP Whitelist interception (placeholder — always allow)
      2. Webhook signature verification (bypassable for tests via _skip_signature_check)
      3. Platform adapter parse
      4. Rate limiter check
      5. Input sanitization L2
      6. PII masking L4
      7. Knowledge matching Layer 1
      8. Basic escalation (if no knowledge match)
      9. Construct UnifiedResponse
     10. Send reply via platform adapter (placeholder)
     11. Log completion via structured logger
    """

    def __init__(self):
        """Initialize the pipeline orchestrator with rate limiter and logger."""
        self._rate_limiter = RateLimiter()
        self._logger = _logger
        self._skip_signature_check = False

    def _verify_signature(self, platform, raw_body, signature):
        """Verify webhook signature; returns error response or None."""
        if self._skip_signature_check:
            return None
        if platform == Platform.TELEGRAM:
            verifier = _telegram_verifier()
            if verifier is None or not verifier.verify(raw_body, signature):
                return UnifiedResponse(content="", source="signature",
                                      confidence=0.0, status_code=401, platform=platform)
        elif platform == Platform.LINE:
            verifier = _line_verifier()
            if verifier is None or not verifier.verify(raw_body, signature):
                return UnifiedResponse(content="", source="signature",
                                      confidence=0.0, status_code=401, platform=platform)
        return None

    def _parse_message(self, platform, raw_body):
        """Parse platform-specific message; returns (message, platform_user_id)."""
        payload = json.loads(raw_body)
        if platform == Platform.TELEGRAM:
            msg = TelegramAdapter.parse_message(payload)
        elif platform == Platform.LINE:
            msg = LineAdapter.parse_message(payload)
        else:
            msg = None
        platform_user_id = msg.platform_user_id if msg else "unknown"
        return msg, platform_user_id

    def _check_rate_limit(self, platform, platform_user_id):
        """Check rate limit; returns error response or None."""
        if not self._rate_limiter.check(platform.value, platform_user_id):
            return UnifiedResponse(content="rate limited", source="rate_limit",
                                  confidence=0.0, status_code=429, platform=platform)
        return None

    def _process_content(self, msg):
        """Sanitize, mask PII, and match knowledge; returns match result dict or None."""
        if msg is None:
            text = ""
        else:
            text = InputSanitizer.sanitize(msg.content)
            text = PIIMasker.mask(text)
        rules = []
        return KnowledgeMatcher.match(text, rules)

    def _build_response(self, match_result, platform):
        """Build UnifiedResponse from match result or escalate."""
        if match_result is None:
            source, confidence, content = "escalate", 0.0, ""
            EscalationQueue.enqueue("out_of_scope", {"content": ""})
        else:
            source = match_result["source"]
            confidence = match_result["confidence"]
            content = match_result.get("answer", "")
        return UnifiedResponse(content=content, source=source, confidence=confidence,
                              status_code=200, platform=platform)

    def process(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        err = self._verify_signature(platform, raw_body, signature)
        if err:
            return err
        try:
            msg, platform_user_id = self._parse_message(platform, raw_body)
            err = self._check_rate_limit(platform, platform_user_id)
            if err:
                return err
            match_result = self._process_content(msg)
            resp = self._build_response(match_result, platform)
            self._logger.info("pipeline_done", platform=platform.value, source=resp.source)
            return resp
        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(content="", source="escalate", confidence=0.0,
                                  status_code=200, platform=platform)
        except ValidationError:
            return UnifiedResponse(content="", source="escalate", confidence=0.0,
                                  status_code=200, platform=platform)
        except Exception:
            return UnifiedResponse(content="", source="escalate", confidence=0.0,
                                  status_code=500, platform=platform)

    def _db_execute(self, data: dict):
        """Execute a DB operation (stub for testing)."""
        return {"ok": True}

    def _db_execute_with_retry(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc