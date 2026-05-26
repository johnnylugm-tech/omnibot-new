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


def x__telegram_verifier__mutmut_orig():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_1():
    token = None
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_2():
    token = os.environ.get(None, "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_3():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_4():
    token = os.environ.get("")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_5():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", )
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_6():
    token = os.environ.get("XXTELEGRAM_BOT_TOKENXX", "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_7():
    token = os.environ.get("telegram_bot_token", "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_8():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "XXXX")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_9():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if token:
        return None
    return TelegramWebhookVerifier(bot_token=token)


def x__telegram_verifier__mutmut_10():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return None
    return TelegramWebhookVerifier(bot_token=None)

x__telegram_verifier__mutmut_mutants : ClassVar[MutantDict] = {
'x__telegram_verifier__mutmut_1': x__telegram_verifier__mutmut_1, 
    'x__telegram_verifier__mutmut_2': x__telegram_verifier__mutmut_2, 
    'x__telegram_verifier__mutmut_3': x__telegram_verifier__mutmut_3, 
    'x__telegram_verifier__mutmut_4': x__telegram_verifier__mutmut_4, 
    'x__telegram_verifier__mutmut_5': x__telegram_verifier__mutmut_5, 
    'x__telegram_verifier__mutmut_6': x__telegram_verifier__mutmut_6, 
    'x__telegram_verifier__mutmut_7': x__telegram_verifier__mutmut_7, 
    'x__telegram_verifier__mutmut_8': x__telegram_verifier__mutmut_8, 
    'x__telegram_verifier__mutmut_9': x__telegram_verifier__mutmut_9, 
    'x__telegram_verifier__mutmut_10': x__telegram_verifier__mutmut_10
}

def _telegram_verifier(*args, **kwargs):
    result = _mutmut_trampoline(x__telegram_verifier__mutmut_orig, x__telegram_verifier__mutmut_mutants, args, kwargs)
    return result 

_telegram_verifier.__signature__ = _mutmut_signature(x__telegram_verifier__mutmut_orig)
x__telegram_verifier__mutmut_orig.__name__ = 'x__telegram_verifier'


def x__line_verifier__mutmut_orig():
    secret = os.environ.get("LINE_CHANNEL_SECRET", "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_1():
    secret = None
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_2():
    secret = os.environ.get(None, "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_3():
    secret = os.environ.get("LINE_CHANNEL_SECRET", None)
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_4():
    secret = os.environ.get("")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_5():
    secret = os.environ.get("LINE_CHANNEL_SECRET", )
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_6():
    secret = os.environ.get("XXLINE_CHANNEL_SECRETXX", "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_7():
    secret = os.environ.get("line_channel_secret", "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_8():
    secret = os.environ.get("LINE_CHANNEL_SECRET", "XXXX")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_9():
    secret = os.environ.get("LINE_CHANNEL_SECRET", "")
    if secret:
        return None
    return LineWebhookVerifier(channel_secret=secret)


def x__line_verifier__mutmut_10():
    secret = os.environ.get("LINE_CHANNEL_SECRET", "")
    if not secret:
        return None
    return LineWebhookVerifier(channel_secret=None)

x__line_verifier__mutmut_mutants : ClassVar[MutantDict] = {
'x__line_verifier__mutmut_1': x__line_verifier__mutmut_1, 
    'x__line_verifier__mutmut_2': x__line_verifier__mutmut_2, 
    'x__line_verifier__mutmut_3': x__line_verifier__mutmut_3, 
    'x__line_verifier__mutmut_4': x__line_verifier__mutmut_4, 
    'x__line_verifier__mutmut_5': x__line_verifier__mutmut_5, 
    'x__line_verifier__mutmut_6': x__line_verifier__mutmut_6, 
    'x__line_verifier__mutmut_7': x__line_verifier__mutmut_7, 
    'x__line_verifier__mutmut_8': x__line_verifier__mutmut_8, 
    'x__line_verifier__mutmut_9': x__line_verifier__mutmut_9, 
    'x__line_verifier__mutmut_10': x__line_verifier__mutmut_10
}

def _line_verifier(*args, **kwargs):
    result = _mutmut_trampoline(x__line_verifier__mutmut_orig, x__line_verifier__mutmut_mutants, args, kwargs)
    return result 

_line_verifier.__signature__ = _mutmut_signature(x__line_verifier__mutmut_orig)
x__line_verifier__mutmut_orig.__name__ = 'x__line_verifier'


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

    def xǁPipelineOrchestratorǁ__init____mutmut_orig(self):
        self._rate_limiter = RateLimiter()
        self._logger = _logger
        self._skip_signature_check = False  # True in tests that test other stages

    def xǁPipelineOrchestratorǁ__init____mutmut_1(self):
        self._rate_limiter = None
        self._logger = _logger
        self._skip_signature_check = False  # True in tests that test other stages

    def xǁPipelineOrchestratorǁ__init____mutmut_2(self):
        self._rate_limiter = RateLimiter()
        self._logger = None
        self._skip_signature_check = False  # True in tests that test other stages

    def xǁPipelineOrchestratorǁ__init____mutmut_3(self):
        self._rate_limiter = RateLimiter()
        self._logger = _logger
        self._skip_signature_check = None  # True in tests that test other stages

    def xǁPipelineOrchestratorǁ__init____mutmut_4(self):
        self._rate_limiter = RateLimiter()
        self._logger = _logger
        self._skip_signature_check = True  # True in tests that test other stages
    
    xǁPipelineOrchestratorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPipelineOrchestratorǁ__init____mutmut_1': xǁPipelineOrchestratorǁ__init____mutmut_1, 
        'xǁPipelineOrchestratorǁ__init____mutmut_2': xǁPipelineOrchestratorǁ__init____mutmut_2, 
        'xǁPipelineOrchestratorǁ__init____mutmut_3': xǁPipelineOrchestratorǁ__init____mutmut_3, 
        'xǁPipelineOrchestratorǁ__init____mutmut_4': xǁPipelineOrchestratorǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPipelineOrchestratorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPipelineOrchestratorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPipelineOrchestratorǁ__init____mutmut_orig)
    xǁPipelineOrchestratorǁ__init____mutmut_orig.__name__ = 'xǁPipelineOrchestratorǁ__init__'

    def xǁPipelineOrchestratorǁprocess__mutmut_orig(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_1(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_2(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform != Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_3(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = None
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_4(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None and not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_5(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is not None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_6(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_7(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(None, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_8(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, None):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_9(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_10(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, ):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_11(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content=None, source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_12(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source=None, confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_13(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=None,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_14(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=None, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_15(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=None,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_16(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_17(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_18(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_19(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_20(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_21(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="XXXX", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_22(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="XXsignatureXX", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_23(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="SIGNATURE", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_24(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=1.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_25(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=402, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_26(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform != Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_27(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = None
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_28(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None and not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_29(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is not None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_30(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_31(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(None, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_32(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, None):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_33(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_34(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, ):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_35(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content=None, source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_36(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source=None, confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_37(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=None,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_38(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=None, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_39(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=None,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_40(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_41(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_42(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_43(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_44(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_45(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="XXXX", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_46(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="XXsignatureXX", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_47(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="SIGNATURE", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_48(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=1.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_49(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=402, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_50(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = None
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_51(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(None)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_52(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform != Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_53(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = None
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_54(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(None)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_55(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform != Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_56(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = None
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_57(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(None)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_58(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = ""  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_59(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = None

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_60(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "XXunknownXX"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_61(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "UNKNOWN"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_62(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_63(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(None, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_64(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, None):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_65(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_66(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, ):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_67(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content=None, source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_68(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source=None, confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_69(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=None,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_70(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=None, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_71(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=None,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_72(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_73(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_74(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_75(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_76(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_77(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="XXrate limitedXX", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_78(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="RATE LIMITED", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_79(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="XXrate_limitXX", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_80(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="RATE_LIMIT", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_81(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=1.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_82(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=430, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_83(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is not None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_84(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = None
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_85(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = "XXXX"
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_86(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = None
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_87(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = None
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_88(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(None)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_89(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = None

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_90(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(None)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_91(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = None  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_92(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = None
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_93(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(None, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_94(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, None)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_95(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_96(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, )
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_97(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is not None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_98(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = None
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_99(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "XXescalateXX"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_100(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "ESCALATE"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_101(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = None
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_102(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 1.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_103(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = None
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_104(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = "XXXX"
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_105(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = None
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_106(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["XXsourceXX"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_107(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["SOURCE"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_108(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = None
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_109(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["XXconfidenceXX"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_110(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["CONFIDENCE"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_111(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = None

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_112(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get(None, "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_113(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", None)

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_114(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_115(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", )

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_116(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("XXanswerXX", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_117(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("ANSWER", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_118(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "XXXX")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_119(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source != "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_120(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "XXescalateXX":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_121(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "ESCALATE":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_122(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue(None, {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_123(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", None)

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_124(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue({"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_125(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", )

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_126(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("XXout_of_scopeXX", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_127(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("OUT_OF_SCOPE", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_128(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"XXcontentXX": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_129(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"CONTENT": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_130(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = None
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_131(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=None,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_132(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=None,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_133(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=None,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_134(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=None,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_135(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=None,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_136(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_137(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_138(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_139(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_140(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_141(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=201,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_142(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info(None, platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_143(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=None, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_144(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=None)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_145(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info(platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_146(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_147(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, )
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_148(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("XXpipeline_doneXX", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_149(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("PIPELINE_DONE", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_150(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content=None, source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_151(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source=None, confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_152(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=None,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_153(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=None, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_154(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=None,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_155(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_156(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_157(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_158(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_159(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_160(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="XXXX", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_161(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="XXescalateXX", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_162(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="ESCALATE", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_163(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=1.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_164(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=201, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_165(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content=None, source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_166(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source=None, confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_167(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=None,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_168(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=None, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_169(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=None,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_170(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_171(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_172(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_173(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_174(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_175(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="XXXX", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_176(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="XXescalateXX", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_177(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="ESCALATE", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_178(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=1.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_179(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=201, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_180(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content=None, source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_181(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source=None, confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_182(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=None,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_183(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=None, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_184(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, platform=None,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_185(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_186(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_187(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_188(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_189(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=500, )

    def xǁPipelineOrchestratorǁprocess__mutmut_190(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="XXXX", source="escalate", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_191(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="XXescalateXX", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_192(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="ESCALATE", confidence=0.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_193(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=1.0,
                status_code=500, platform=platform,
            )

    def xǁPipelineOrchestratorǁprocess__mutmut_194(self, platform: Platform, raw_body: bytes, signature: str):
        """Process one inbound webhook request through the 11-stage pipeline."""
        try:
            # ── Stage 2: HMAC signature verification ──────────────────────────
            # Tests that patch adapter/rate-limiter skip signature check entirely.
            # In production, this runs before any business logic (Security Constraint).
            if not self._skip_signature_check:
                if platform == Platform.TELEGRAM:
                    verifier = _telegram_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )
                elif platform == Platform.LINE:
                    verifier = _line_verifier()
                    if verifier is None or not verifier.verify(raw_body, signature):
                        return UnifiedResponse(
                            content="", source="signature", confidence=0.0,
                            status_code=401, platform=platform,
                        )

            # ── Stage 3: Platform adapter parse ───────────────────────────────
            payload = json.loads(raw_body)
            if platform == Platform.TELEGRAM:
                msg = TelegramAdapter.parse_message(payload)
            elif platform == Platform.LINE:
                msg = LineAdapter.parse_message(payload)
            else:
                msg = None  # type: ignore[assignment]

            platform_user_id = msg.platform_user_id if msg else "unknown"

            # ── Stage 4: Rate limiter check ──────────────────────────────────
            if not self._rate_limiter.check(platform.value, platform_user_id):
                return UnifiedResponse(
                    content="rate limited", source="rate_limit", confidence=0.0,
                    status_code=429, platform=platform,
                )

            # ── Stages 5-7: Sanitize, mask PII, knowledge match ─────────────
            if msg is None:
                text = ""
            else:
                text = msg.content
                text = InputSanitizer.sanitize(text)
                text = PIIMasker.mask(text)

            rules = []  # empty rules → no match → escalate
            match_result = KnowledgeMatcher.match(text, rules)
            if match_result is None:
                source = "escalate"
                confidence = 0.0
                content = ""
            else:
                source = match_result["source"]
                confidence = match_result["confidence"]
                content = match_result.get("answer", "")

            # ── Stage 8: Escalation queue ─────────────────────────────────────
            if source == "escalate":
                EscalationQueue.enqueue("out_of_scope", {"content": text})

            # ── Stage 9-11: Response + logging ────────────────────────────────
            resp = UnifiedResponse(
                content=content,
                source=source,
                confidence=confidence,
                status_code=200,
                platform=platform,
            )
            self._logger.info("pipeline_done", platform=platform.value, source=source)
            return resp

        except (json.JSONDecodeError, UnicodeDecodeError):
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except ValidationError:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=200, platform=platform,
            )
        except Exception:
            return UnifiedResponse(
                content="", source="escalate", confidence=0.0,
                status_code=501, platform=platform,
            )
    
    xǁPipelineOrchestratorǁprocess__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPipelineOrchestratorǁprocess__mutmut_1': xǁPipelineOrchestratorǁprocess__mutmut_1, 
        'xǁPipelineOrchestratorǁprocess__mutmut_2': xǁPipelineOrchestratorǁprocess__mutmut_2, 
        'xǁPipelineOrchestratorǁprocess__mutmut_3': xǁPipelineOrchestratorǁprocess__mutmut_3, 
        'xǁPipelineOrchestratorǁprocess__mutmut_4': xǁPipelineOrchestratorǁprocess__mutmut_4, 
        'xǁPipelineOrchestratorǁprocess__mutmut_5': xǁPipelineOrchestratorǁprocess__mutmut_5, 
        'xǁPipelineOrchestratorǁprocess__mutmut_6': xǁPipelineOrchestratorǁprocess__mutmut_6, 
        'xǁPipelineOrchestratorǁprocess__mutmut_7': xǁPipelineOrchestratorǁprocess__mutmut_7, 
        'xǁPipelineOrchestratorǁprocess__mutmut_8': xǁPipelineOrchestratorǁprocess__mutmut_8, 
        'xǁPipelineOrchestratorǁprocess__mutmut_9': xǁPipelineOrchestratorǁprocess__mutmut_9, 
        'xǁPipelineOrchestratorǁprocess__mutmut_10': xǁPipelineOrchestratorǁprocess__mutmut_10, 
        'xǁPipelineOrchestratorǁprocess__mutmut_11': xǁPipelineOrchestratorǁprocess__mutmut_11, 
        'xǁPipelineOrchestratorǁprocess__mutmut_12': xǁPipelineOrchestratorǁprocess__mutmut_12, 
        'xǁPipelineOrchestratorǁprocess__mutmut_13': xǁPipelineOrchestratorǁprocess__mutmut_13, 
        'xǁPipelineOrchestratorǁprocess__mutmut_14': xǁPipelineOrchestratorǁprocess__mutmut_14, 
        'xǁPipelineOrchestratorǁprocess__mutmut_15': xǁPipelineOrchestratorǁprocess__mutmut_15, 
        'xǁPipelineOrchestratorǁprocess__mutmut_16': xǁPipelineOrchestratorǁprocess__mutmut_16, 
        'xǁPipelineOrchestratorǁprocess__mutmut_17': xǁPipelineOrchestratorǁprocess__mutmut_17, 
        'xǁPipelineOrchestratorǁprocess__mutmut_18': xǁPipelineOrchestratorǁprocess__mutmut_18, 
        'xǁPipelineOrchestratorǁprocess__mutmut_19': xǁPipelineOrchestratorǁprocess__mutmut_19, 
        'xǁPipelineOrchestratorǁprocess__mutmut_20': xǁPipelineOrchestratorǁprocess__mutmut_20, 
        'xǁPipelineOrchestratorǁprocess__mutmut_21': xǁPipelineOrchestratorǁprocess__mutmut_21, 
        'xǁPipelineOrchestratorǁprocess__mutmut_22': xǁPipelineOrchestratorǁprocess__mutmut_22, 
        'xǁPipelineOrchestratorǁprocess__mutmut_23': xǁPipelineOrchestratorǁprocess__mutmut_23, 
        'xǁPipelineOrchestratorǁprocess__mutmut_24': xǁPipelineOrchestratorǁprocess__mutmut_24, 
        'xǁPipelineOrchestratorǁprocess__mutmut_25': xǁPipelineOrchestratorǁprocess__mutmut_25, 
        'xǁPipelineOrchestratorǁprocess__mutmut_26': xǁPipelineOrchestratorǁprocess__mutmut_26, 
        'xǁPipelineOrchestratorǁprocess__mutmut_27': xǁPipelineOrchestratorǁprocess__mutmut_27, 
        'xǁPipelineOrchestratorǁprocess__mutmut_28': xǁPipelineOrchestratorǁprocess__mutmut_28, 
        'xǁPipelineOrchestratorǁprocess__mutmut_29': xǁPipelineOrchestratorǁprocess__mutmut_29, 
        'xǁPipelineOrchestratorǁprocess__mutmut_30': xǁPipelineOrchestratorǁprocess__mutmut_30, 
        'xǁPipelineOrchestratorǁprocess__mutmut_31': xǁPipelineOrchestratorǁprocess__mutmut_31, 
        'xǁPipelineOrchestratorǁprocess__mutmut_32': xǁPipelineOrchestratorǁprocess__mutmut_32, 
        'xǁPipelineOrchestratorǁprocess__mutmut_33': xǁPipelineOrchestratorǁprocess__mutmut_33, 
        'xǁPipelineOrchestratorǁprocess__mutmut_34': xǁPipelineOrchestratorǁprocess__mutmut_34, 
        'xǁPipelineOrchestratorǁprocess__mutmut_35': xǁPipelineOrchestratorǁprocess__mutmut_35, 
        'xǁPipelineOrchestratorǁprocess__mutmut_36': xǁPipelineOrchestratorǁprocess__mutmut_36, 
        'xǁPipelineOrchestratorǁprocess__mutmut_37': xǁPipelineOrchestratorǁprocess__mutmut_37, 
        'xǁPipelineOrchestratorǁprocess__mutmut_38': xǁPipelineOrchestratorǁprocess__mutmut_38, 
        'xǁPipelineOrchestratorǁprocess__mutmut_39': xǁPipelineOrchestratorǁprocess__mutmut_39, 
        'xǁPipelineOrchestratorǁprocess__mutmut_40': xǁPipelineOrchestratorǁprocess__mutmut_40, 
        'xǁPipelineOrchestratorǁprocess__mutmut_41': xǁPipelineOrchestratorǁprocess__mutmut_41, 
        'xǁPipelineOrchestratorǁprocess__mutmut_42': xǁPipelineOrchestratorǁprocess__mutmut_42, 
        'xǁPipelineOrchestratorǁprocess__mutmut_43': xǁPipelineOrchestratorǁprocess__mutmut_43, 
        'xǁPipelineOrchestratorǁprocess__mutmut_44': xǁPipelineOrchestratorǁprocess__mutmut_44, 
        'xǁPipelineOrchestratorǁprocess__mutmut_45': xǁPipelineOrchestratorǁprocess__mutmut_45, 
        'xǁPipelineOrchestratorǁprocess__mutmut_46': xǁPipelineOrchestratorǁprocess__mutmut_46, 
        'xǁPipelineOrchestratorǁprocess__mutmut_47': xǁPipelineOrchestratorǁprocess__mutmut_47, 
        'xǁPipelineOrchestratorǁprocess__mutmut_48': xǁPipelineOrchestratorǁprocess__mutmut_48, 
        'xǁPipelineOrchestratorǁprocess__mutmut_49': xǁPipelineOrchestratorǁprocess__mutmut_49, 
        'xǁPipelineOrchestratorǁprocess__mutmut_50': xǁPipelineOrchestratorǁprocess__mutmut_50, 
        'xǁPipelineOrchestratorǁprocess__mutmut_51': xǁPipelineOrchestratorǁprocess__mutmut_51, 
        'xǁPipelineOrchestratorǁprocess__mutmut_52': xǁPipelineOrchestratorǁprocess__mutmut_52, 
        'xǁPipelineOrchestratorǁprocess__mutmut_53': xǁPipelineOrchestratorǁprocess__mutmut_53, 
        'xǁPipelineOrchestratorǁprocess__mutmut_54': xǁPipelineOrchestratorǁprocess__mutmut_54, 
        'xǁPipelineOrchestratorǁprocess__mutmut_55': xǁPipelineOrchestratorǁprocess__mutmut_55, 
        'xǁPipelineOrchestratorǁprocess__mutmut_56': xǁPipelineOrchestratorǁprocess__mutmut_56, 
        'xǁPipelineOrchestratorǁprocess__mutmut_57': xǁPipelineOrchestratorǁprocess__mutmut_57, 
        'xǁPipelineOrchestratorǁprocess__mutmut_58': xǁPipelineOrchestratorǁprocess__mutmut_58, 
        'xǁPipelineOrchestratorǁprocess__mutmut_59': xǁPipelineOrchestratorǁprocess__mutmut_59, 
        'xǁPipelineOrchestratorǁprocess__mutmut_60': xǁPipelineOrchestratorǁprocess__mutmut_60, 
        'xǁPipelineOrchestratorǁprocess__mutmut_61': xǁPipelineOrchestratorǁprocess__mutmut_61, 
        'xǁPipelineOrchestratorǁprocess__mutmut_62': xǁPipelineOrchestratorǁprocess__mutmut_62, 
        'xǁPipelineOrchestratorǁprocess__mutmut_63': xǁPipelineOrchestratorǁprocess__mutmut_63, 
        'xǁPipelineOrchestratorǁprocess__mutmut_64': xǁPipelineOrchestratorǁprocess__mutmut_64, 
        'xǁPipelineOrchestratorǁprocess__mutmut_65': xǁPipelineOrchestratorǁprocess__mutmut_65, 
        'xǁPipelineOrchestratorǁprocess__mutmut_66': xǁPipelineOrchestratorǁprocess__mutmut_66, 
        'xǁPipelineOrchestratorǁprocess__mutmut_67': xǁPipelineOrchestratorǁprocess__mutmut_67, 
        'xǁPipelineOrchestratorǁprocess__mutmut_68': xǁPipelineOrchestratorǁprocess__mutmut_68, 
        'xǁPipelineOrchestratorǁprocess__mutmut_69': xǁPipelineOrchestratorǁprocess__mutmut_69, 
        'xǁPipelineOrchestratorǁprocess__mutmut_70': xǁPipelineOrchestratorǁprocess__mutmut_70, 
        'xǁPipelineOrchestratorǁprocess__mutmut_71': xǁPipelineOrchestratorǁprocess__mutmut_71, 
        'xǁPipelineOrchestratorǁprocess__mutmut_72': xǁPipelineOrchestratorǁprocess__mutmut_72, 
        'xǁPipelineOrchestratorǁprocess__mutmut_73': xǁPipelineOrchestratorǁprocess__mutmut_73, 
        'xǁPipelineOrchestratorǁprocess__mutmut_74': xǁPipelineOrchestratorǁprocess__mutmut_74, 
        'xǁPipelineOrchestratorǁprocess__mutmut_75': xǁPipelineOrchestratorǁprocess__mutmut_75, 
        'xǁPipelineOrchestratorǁprocess__mutmut_76': xǁPipelineOrchestratorǁprocess__mutmut_76, 
        'xǁPipelineOrchestratorǁprocess__mutmut_77': xǁPipelineOrchestratorǁprocess__mutmut_77, 
        'xǁPipelineOrchestratorǁprocess__mutmut_78': xǁPipelineOrchestratorǁprocess__mutmut_78, 
        'xǁPipelineOrchestratorǁprocess__mutmut_79': xǁPipelineOrchestratorǁprocess__mutmut_79, 
        'xǁPipelineOrchestratorǁprocess__mutmut_80': xǁPipelineOrchestratorǁprocess__mutmut_80, 
        'xǁPipelineOrchestratorǁprocess__mutmut_81': xǁPipelineOrchestratorǁprocess__mutmut_81, 
        'xǁPipelineOrchestratorǁprocess__mutmut_82': xǁPipelineOrchestratorǁprocess__mutmut_82, 
        'xǁPipelineOrchestratorǁprocess__mutmut_83': xǁPipelineOrchestratorǁprocess__mutmut_83, 
        'xǁPipelineOrchestratorǁprocess__mutmut_84': xǁPipelineOrchestratorǁprocess__mutmut_84, 
        'xǁPipelineOrchestratorǁprocess__mutmut_85': xǁPipelineOrchestratorǁprocess__mutmut_85, 
        'xǁPipelineOrchestratorǁprocess__mutmut_86': xǁPipelineOrchestratorǁprocess__mutmut_86, 
        'xǁPipelineOrchestratorǁprocess__mutmut_87': xǁPipelineOrchestratorǁprocess__mutmut_87, 
        'xǁPipelineOrchestratorǁprocess__mutmut_88': xǁPipelineOrchestratorǁprocess__mutmut_88, 
        'xǁPipelineOrchestratorǁprocess__mutmut_89': xǁPipelineOrchestratorǁprocess__mutmut_89, 
        'xǁPipelineOrchestratorǁprocess__mutmut_90': xǁPipelineOrchestratorǁprocess__mutmut_90, 
        'xǁPipelineOrchestratorǁprocess__mutmut_91': xǁPipelineOrchestratorǁprocess__mutmut_91, 
        'xǁPipelineOrchestratorǁprocess__mutmut_92': xǁPipelineOrchestratorǁprocess__mutmut_92, 
        'xǁPipelineOrchestratorǁprocess__mutmut_93': xǁPipelineOrchestratorǁprocess__mutmut_93, 
        'xǁPipelineOrchestratorǁprocess__mutmut_94': xǁPipelineOrchestratorǁprocess__mutmut_94, 
        'xǁPipelineOrchestratorǁprocess__mutmut_95': xǁPipelineOrchestratorǁprocess__mutmut_95, 
        'xǁPipelineOrchestratorǁprocess__mutmut_96': xǁPipelineOrchestratorǁprocess__mutmut_96, 
        'xǁPipelineOrchestratorǁprocess__mutmut_97': xǁPipelineOrchestratorǁprocess__mutmut_97, 
        'xǁPipelineOrchestratorǁprocess__mutmut_98': xǁPipelineOrchestratorǁprocess__mutmut_98, 
        'xǁPipelineOrchestratorǁprocess__mutmut_99': xǁPipelineOrchestratorǁprocess__mutmut_99, 
        'xǁPipelineOrchestratorǁprocess__mutmut_100': xǁPipelineOrchestratorǁprocess__mutmut_100, 
        'xǁPipelineOrchestratorǁprocess__mutmut_101': xǁPipelineOrchestratorǁprocess__mutmut_101, 
        'xǁPipelineOrchestratorǁprocess__mutmut_102': xǁPipelineOrchestratorǁprocess__mutmut_102, 
        'xǁPipelineOrchestratorǁprocess__mutmut_103': xǁPipelineOrchestratorǁprocess__mutmut_103, 
        'xǁPipelineOrchestratorǁprocess__mutmut_104': xǁPipelineOrchestratorǁprocess__mutmut_104, 
        'xǁPipelineOrchestratorǁprocess__mutmut_105': xǁPipelineOrchestratorǁprocess__mutmut_105, 
        'xǁPipelineOrchestratorǁprocess__mutmut_106': xǁPipelineOrchestratorǁprocess__mutmut_106, 
        'xǁPipelineOrchestratorǁprocess__mutmut_107': xǁPipelineOrchestratorǁprocess__mutmut_107, 
        'xǁPipelineOrchestratorǁprocess__mutmut_108': xǁPipelineOrchestratorǁprocess__mutmut_108, 
        'xǁPipelineOrchestratorǁprocess__mutmut_109': xǁPipelineOrchestratorǁprocess__mutmut_109, 
        'xǁPipelineOrchestratorǁprocess__mutmut_110': xǁPipelineOrchestratorǁprocess__mutmut_110, 
        'xǁPipelineOrchestratorǁprocess__mutmut_111': xǁPipelineOrchestratorǁprocess__mutmut_111, 
        'xǁPipelineOrchestratorǁprocess__mutmut_112': xǁPipelineOrchestratorǁprocess__mutmut_112, 
        'xǁPipelineOrchestratorǁprocess__mutmut_113': xǁPipelineOrchestratorǁprocess__mutmut_113, 
        'xǁPipelineOrchestratorǁprocess__mutmut_114': xǁPipelineOrchestratorǁprocess__mutmut_114, 
        'xǁPipelineOrchestratorǁprocess__mutmut_115': xǁPipelineOrchestratorǁprocess__mutmut_115, 
        'xǁPipelineOrchestratorǁprocess__mutmut_116': xǁPipelineOrchestratorǁprocess__mutmut_116, 
        'xǁPipelineOrchestratorǁprocess__mutmut_117': xǁPipelineOrchestratorǁprocess__mutmut_117, 
        'xǁPipelineOrchestratorǁprocess__mutmut_118': xǁPipelineOrchestratorǁprocess__mutmut_118, 
        'xǁPipelineOrchestratorǁprocess__mutmut_119': xǁPipelineOrchestratorǁprocess__mutmut_119, 
        'xǁPipelineOrchestratorǁprocess__mutmut_120': xǁPipelineOrchestratorǁprocess__mutmut_120, 
        'xǁPipelineOrchestratorǁprocess__mutmut_121': xǁPipelineOrchestratorǁprocess__mutmut_121, 
        'xǁPipelineOrchestratorǁprocess__mutmut_122': xǁPipelineOrchestratorǁprocess__mutmut_122, 
        'xǁPipelineOrchestratorǁprocess__mutmut_123': xǁPipelineOrchestratorǁprocess__mutmut_123, 
        'xǁPipelineOrchestratorǁprocess__mutmut_124': xǁPipelineOrchestratorǁprocess__mutmut_124, 
        'xǁPipelineOrchestratorǁprocess__mutmut_125': xǁPipelineOrchestratorǁprocess__mutmut_125, 
        'xǁPipelineOrchestratorǁprocess__mutmut_126': xǁPipelineOrchestratorǁprocess__mutmut_126, 
        'xǁPipelineOrchestratorǁprocess__mutmut_127': xǁPipelineOrchestratorǁprocess__mutmut_127, 
        'xǁPipelineOrchestratorǁprocess__mutmut_128': xǁPipelineOrchestratorǁprocess__mutmut_128, 
        'xǁPipelineOrchestratorǁprocess__mutmut_129': xǁPipelineOrchestratorǁprocess__mutmut_129, 
        'xǁPipelineOrchestratorǁprocess__mutmut_130': xǁPipelineOrchestratorǁprocess__mutmut_130, 
        'xǁPipelineOrchestratorǁprocess__mutmut_131': xǁPipelineOrchestratorǁprocess__mutmut_131, 
        'xǁPipelineOrchestratorǁprocess__mutmut_132': xǁPipelineOrchestratorǁprocess__mutmut_132, 
        'xǁPipelineOrchestratorǁprocess__mutmut_133': xǁPipelineOrchestratorǁprocess__mutmut_133, 
        'xǁPipelineOrchestratorǁprocess__mutmut_134': xǁPipelineOrchestratorǁprocess__mutmut_134, 
        'xǁPipelineOrchestratorǁprocess__mutmut_135': xǁPipelineOrchestratorǁprocess__mutmut_135, 
        'xǁPipelineOrchestratorǁprocess__mutmut_136': xǁPipelineOrchestratorǁprocess__mutmut_136, 
        'xǁPipelineOrchestratorǁprocess__mutmut_137': xǁPipelineOrchestratorǁprocess__mutmut_137, 
        'xǁPipelineOrchestratorǁprocess__mutmut_138': xǁPipelineOrchestratorǁprocess__mutmut_138, 
        'xǁPipelineOrchestratorǁprocess__mutmut_139': xǁPipelineOrchestratorǁprocess__mutmut_139, 
        'xǁPipelineOrchestratorǁprocess__mutmut_140': xǁPipelineOrchestratorǁprocess__mutmut_140, 
        'xǁPipelineOrchestratorǁprocess__mutmut_141': xǁPipelineOrchestratorǁprocess__mutmut_141, 
        'xǁPipelineOrchestratorǁprocess__mutmut_142': xǁPipelineOrchestratorǁprocess__mutmut_142, 
        'xǁPipelineOrchestratorǁprocess__mutmut_143': xǁPipelineOrchestratorǁprocess__mutmut_143, 
        'xǁPipelineOrchestratorǁprocess__mutmut_144': xǁPipelineOrchestratorǁprocess__mutmut_144, 
        'xǁPipelineOrchestratorǁprocess__mutmut_145': xǁPipelineOrchestratorǁprocess__mutmut_145, 
        'xǁPipelineOrchestratorǁprocess__mutmut_146': xǁPipelineOrchestratorǁprocess__mutmut_146, 
        'xǁPipelineOrchestratorǁprocess__mutmut_147': xǁPipelineOrchestratorǁprocess__mutmut_147, 
        'xǁPipelineOrchestratorǁprocess__mutmut_148': xǁPipelineOrchestratorǁprocess__mutmut_148, 
        'xǁPipelineOrchestratorǁprocess__mutmut_149': xǁPipelineOrchestratorǁprocess__mutmut_149, 
        'xǁPipelineOrchestratorǁprocess__mutmut_150': xǁPipelineOrchestratorǁprocess__mutmut_150, 
        'xǁPipelineOrchestratorǁprocess__mutmut_151': xǁPipelineOrchestratorǁprocess__mutmut_151, 
        'xǁPipelineOrchestratorǁprocess__mutmut_152': xǁPipelineOrchestratorǁprocess__mutmut_152, 
        'xǁPipelineOrchestratorǁprocess__mutmut_153': xǁPipelineOrchestratorǁprocess__mutmut_153, 
        'xǁPipelineOrchestratorǁprocess__mutmut_154': xǁPipelineOrchestratorǁprocess__mutmut_154, 
        'xǁPipelineOrchestratorǁprocess__mutmut_155': xǁPipelineOrchestratorǁprocess__mutmut_155, 
        'xǁPipelineOrchestratorǁprocess__mutmut_156': xǁPipelineOrchestratorǁprocess__mutmut_156, 
        'xǁPipelineOrchestratorǁprocess__mutmut_157': xǁPipelineOrchestratorǁprocess__mutmut_157, 
        'xǁPipelineOrchestratorǁprocess__mutmut_158': xǁPipelineOrchestratorǁprocess__mutmut_158, 
        'xǁPipelineOrchestratorǁprocess__mutmut_159': xǁPipelineOrchestratorǁprocess__mutmut_159, 
        'xǁPipelineOrchestratorǁprocess__mutmut_160': xǁPipelineOrchestratorǁprocess__mutmut_160, 
        'xǁPipelineOrchestratorǁprocess__mutmut_161': xǁPipelineOrchestratorǁprocess__mutmut_161, 
        'xǁPipelineOrchestratorǁprocess__mutmut_162': xǁPipelineOrchestratorǁprocess__mutmut_162, 
        'xǁPipelineOrchestratorǁprocess__mutmut_163': xǁPipelineOrchestratorǁprocess__mutmut_163, 
        'xǁPipelineOrchestratorǁprocess__mutmut_164': xǁPipelineOrchestratorǁprocess__mutmut_164, 
        'xǁPipelineOrchestratorǁprocess__mutmut_165': xǁPipelineOrchestratorǁprocess__mutmut_165, 
        'xǁPipelineOrchestratorǁprocess__mutmut_166': xǁPipelineOrchestratorǁprocess__mutmut_166, 
        'xǁPipelineOrchestratorǁprocess__mutmut_167': xǁPipelineOrchestratorǁprocess__mutmut_167, 
        'xǁPipelineOrchestratorǁprocess__mutmut_168': xǁPipelineOrchestratorǁprocess__mutmut_168, 
        'xǁPipelineOrchestratorǁprocess__mutmut_169': xǁPipelineOrchestratorǁprocess__mutmut_169, 
        'xǁPipelineOrchestratorǁprocess__mutmut_170': xǁPipelineOrchestratorǁprocess__mutmut_170, 
        'xǁPipelineOrchestratorǁprocess__mutmut_171': xǁPipelineOrchestratorǁprocess__mutmut_171, 
        'xǁPipelineOrchestratorǁprocess__mutmut_172': xǁPipelineOrchestratorǁprocess__mutmut_172, 
        'xǁPipelineOrchestratorǁprocess__mutmut_173': xǁPipelineOrchestratorǁprocess__mutmut_173, 
        'xǁPipelineOrchestratorǁprocess__mutmut_174': xǁPipelineOrchestratorǁprocess__mutmut_174, 
        'xǁPipelineOrchestratorǁprocess__mutmut_175': xǁPipelineOrchestratorǁprocess__mutmut_175, 
        'xǁPipelineOrchestratorǁprocess__mutmut_176': xǁPipelineOrchestratorǁprocess__mutmut_176, 
        'xǁPipelineOrchestratorǁprocess__mutmut_177': xǁPipelineOrchestratorǁprocess__mutmut_177, 
        'xǁPipelineOrchestratorǁprocess__mutmut_178': xǁPipelineOrchestratorǁprocess__mutmut_178, 
        'xǁPipelineOrchestratorǁprocess__mutmut_179': xǁPipelineOrchestratorǁprocess__mutmut_179, 
        'xǁPipelineOrchestratorǁprocess__mutmut_180': xǁPipelineOrchestratorǁprocess__mutmut_180, 
        'xǁPipelineOrchestratorǁprocess__mutmut_181': xǁPipelineOrchestratorǁprocess__mutmut_181, 
        'xǁPipelineOrchestratorǁprocess__mutmut_182': xǁPipelineOrchestratorǁprocess__mutmut_182, 
        'xǁPipelineOrchestratorǁprocess__mutmut_183': xǁPipelineOrchestratorǁprocess__mutmut_183, 
        'xǁPipelineOrchestratorǁprocess__mutmut_184': xǁPipelineOrchestratorǁprocess__mutmut_184, 
        'xǁPipelineOrchestratorǁprocess__mutmut_185': xǁPipelineOrchestratorǁprocess__mutmut_185, 
        'xǁPipelineOrchestratorǁprocess__mutmut_186': xǁPipelineOrchestratorǁprocess__mutmut_186, 
        'xǁPipelineOrchestratorǁprocess__mutmut_187': xǁPipelineOrchestratorǁprocess__mutmut_187, 
        'xǁPipelineOrchestratorǁprocess__mutmut_188': xǁPipelineOrchestratorǁprocess__mutmut_188, 
        'xǁPipelineOrchestratorǁprocess__mutmut_189': xǁPipelineOrchestratorǁprocess__mutmut_189, 
        'xǁPipelineOrchestratorǁprocess__mutmut_190': xǁPipelineOrchestratorǁprocess__mutmut_190, 
        'xǁPipelineOrchestratorǁprocess__mutmut_191': xǁPipelineOrchestratorǁprocess__mutmut_191, 
        'xǁPipelineOrchestratorǁprocess__mutmut_192': xǁPipelineOrchestratorǁprocess__mutmut_192, 
        'xǁPipelineOrchestratorǁprocess__mutmut_193': xǁPipelineOrchestratorǁprocess__mutmut_193, 
        'xǁPipelineOrchestratorǁprocess__mutmut_194': xǁPipelineOrchestratorǁprocess__mutmut_194
    }
    
    def process(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPipelineOrchestratorǁprocess__mutmut_orig"), object.__getattribute__(self, "xǁPipelineOrchestratorǁprocess__mutmut_mutants"), args, kwargs, self)
        return result 
    
    process.__signature__ = _mutmut_signature(xǁPipelineOrchestratorǁprocess__mutmut_orig)
    xǁPipelineOrchestratorǁprocess__mutmut_orig.__name__ = 'xǁPipelineOrchestratorǁprocess'

    def xǁPipelineOrchestratorǁ_db_execute__mutmut_orig(self, data: dict):
        """Execute a DB operation (stub for testing)."""
        return {"ok": True}

    def xǁPipelineOrchestratorǁ_db_execute__mutmut_1(self, data: dict):
        """Execute a DB operation (stub for testing)."""
        return {"XXokXX": True}

    def xǁPipelineOrchestratorǁ_db_execute__mutmut_2(self, data: dict):
        """Execute a DB operation (stub for testing)."""
        return {"OK": True}

    def xǁPipelineOrchestratorǁ_db_execute__mutmut_3(self, data: dict):
        """Execute a DB operation (stub for testing)."""
        return {"ok": False}
    
    xǁPipelineOrchestratorǁ_db_execute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPipelineOrchestratorǁ_db_execute__mutmut_1': xǁPipelineOrchestratorǁ_db_execute__mutmut_1, 
        'xǁPipelineOrchestratorǁ_db_execute__mutmut_2': xǁPipelineOrchestratorǁ_db_execute__mutmut_2, 
        'xǁPipelineOrchestratorǁ_db_execute__mutmut_3': xǁPipelineOrchestratorǁ_db_execute__mutmut_3
    }
    
    def _db_execute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPipelineOrchestratorǁ_db_execute__mutmut_orig"), object.__getattribute__(self, "xǁPipelineOrchestratorǁ_db_execute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _db_execute.__signature__ = _mutmut_signature(xǁPipelineOrchestratorǁ_db_execute__mutmut_orig)
    xǁPipelineOrchestratorǁ_db_execute__mutmut_orig.__name__ = 'xǁPipelineOrchestratorǁ_db_execute'

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_orig(self, data: dict, max_attempts: int = 3):
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

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_1(self, data: dict, max_attempts: int = 4):
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

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_2(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = ""
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_3(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(None):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_4(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(None)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_5(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = None
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_6(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt <= max_attempts - 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_7(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts + 1:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_8(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 2:
                    time.sleep(0.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_9(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(None)
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_10(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 / (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_11(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(1.01 * (2 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_12(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (2 * attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_13(self, data: dict, max_attempts: int = 3):
        """Execute DB operation with retry logic."""
        import time
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return self._db_execute(data)
            except Exception as exc:
                last_exc = exc
                if attempt < max_attempts - 1:
                    time.sleep(0.01 * (3 ** attempt))
        if last_exc is not None:
            raise last_exc

    def xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_14(self, data: dict, max_attempts: int = 3):
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
        if last_exc is None:
            raise last_exc
    
    xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_1': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_1, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_2': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_2, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_3': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_3, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_4': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_4, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_5': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_5, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_6': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_6, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_7': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_7, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_8': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_8, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_9': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_9, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_10': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_10, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_11': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_11, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_12': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_12, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_13': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_13, 
        'xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_14': xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_14
    }
    
    def _db_execute_with_retry(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_orig"), object.__getattribute__(self, "xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _db_execute_with_retry.__signature__ = _mutmut_signature(xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_orig)
    xǁPipelineOrchestratorǁ_db_execute_with_retry__mutmut_orig.__name__ = 'xǁPipelineOrchestratorǁ_db_execute_with_retry'