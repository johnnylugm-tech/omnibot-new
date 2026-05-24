"""FR-04: Verify Telegram webhook signature via HMAC-SHA256.

SRS.md §FR-04:
  "Verify Telegram webhook signature via HMAC-SHA256; reject invalid with 401"

Implementation function: TelegramWebhookVerifier.verify
"""

from __future__ import annotations

import hashlib
import hmac

import pytest


BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
BODY = b'{"update_id":123,"message":{"text":"hello"}}'
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode("utf-8")).digest()
VALID_SIGNATURE = hmac.new(SECRET_KEY, BODY, hashlib.sha256).hexdigest()


# ---------------------------------------------------------------------------
# Test 1 — valid signature returns True
# ---------------------------------------------------------------------------

def test_fr04_telegram_valid_signature_returns_true():
    """FR-04: valid signature -> True."""
    from omnibot.security import TelegramWebhookVerifier

    verifier = TelegramWebhookVerifier(BOT_TOKEN)
    assert verifier.verify(BODY, VALID_SIGNATURE) is True


# ---------------------------------------------------------------------------
# Test 2 — tampered body returns False
# ---------------------------------------------------------------------------

def test_fr04_telegram_tampered_body_returns_false():
    """FR-04: tampered body -> False."""
    from omnibot.security import TelegramWebhookVerifier

    verifier = TelegramWebhookVerifier(BOT_TOKEN)
    tampered = b'{"update_id":999,"message":{"text":"hacked"}}'
    assert verifier.verify(tampered, VALID_SIGNATURE) is False


# ---------------------------------------------------------------------------
# Test 3 — wrong signature returns False
# ---------------------------------------------------------------------------

def test_fr04_telegram_wrong_signature_returns_false():
    """FR-04: wrong signature -> False."""
    from omnibot.security import TelegramWebhookVerifier

    verifier = TelegramWebhookVerifier(BOT_TOKEN)
    assert verifier.verify(BODY, "deadbeef") is False


# ---------------------------------------------------------------------------
# Test 4 — uses hmac.compare_digest
# ---------------------------------------------------------------------------

def test_fr04_telegram_uses_hmac_compare_digest():
    """FR-04: verify uses hmac.compare_digest for timing safety."""
    import inspect
    from omnibot.security import TelegramWebhookVerifier

    source = inspect.getsource(TelegramWebhookVerifier.verify)
    assert "compare_digest" in source, "Must use hmac.compare_digest"


# ---------------------------------------------------------------------------
# Test 5 — different bot tokens produce different results
# ---------------------------------------------------------------------------

def test_fr04_telegram_different_tokens_produce_different_results():
    """FR-04: different bot tokens produce different signatures."""
    from omnibot.security import TelegramWebhookVerifier

    v1 = TelegramWebhookVerifier(BOT_TOKEN)
    v2 = TelegramWebhookVerifier("other_token")

    assert v1.verify(BODY, VALID_SIGNATURE) is True
    assert v2.verify(BODY, VALID_SIGNATURE) is False
