"""FR-05: Verify LINE webhook signature via HMAC-SHA256 with Base64 digest.

SRS.md §FR-05:
  "Verify LINE webhook signature via HMAC-SHA256 with Base64 digest;
   reject invalid with 401"

Implementation function: LineWebhookVerifier.verify
"""

from __future__ import annotations

import base64
import hashlib
import hmac

CHANNEL_SECRET = "test_line_secret"
BODY = b'{"events":[{"type":"message","message":{"text":"hello"}}]}'
VALID_SIGNATURE = base64.b64encode(
    hmac.new(CHANNEL_SECRET.encode("utf-8"), BODY, hashlib.sha256).digest()
).decode()


# ---------------------------------------------------------------------------
# Test 1 — valid signature returns True
# ---------------------------------------------------------------------------

def test_fr05_line_valid_signature_returns_true():
    """FR-05: valid signature -> True."""
    from omnibot.security import LineWebhookVerifier

    verifier = LineWebhookVerifier(CHANNEL_SECRET)
    assert verifier.verify(BODY, VALID_SIGNATURE) is True


# ---------------------------------------------------------------------------
# Test 2 — tampered body returns False
# ---------------------------------------------------------------------------

def test_fr05_line_tampered_body_returns_false():
    """FR-05: tampered body -> False."""
    from omnibot.security import LineWebhookVerifier

    verifier = LineWebhookVerifier(CHANNEL_SECRET)
    tampered = b'{"events":[{"type":"message","message":{"text":"hacked"}}]}'
    assert verifier.verify(tampered, VALID_SIGNATURE) is False


# ---------------------------------------------------------------------------
# Test 3 — wrong secret returns False
# ---------------------------------------------------------------------------

def test_fr05_line_wrong_secret_returns_false():
    """FR-05: wrong secret -> False."""
    from omnibot.security import LineWebhookVerifier

    verifier = LineWebhookVerifier("wrong_secret")
    assert verifier.verify(BODY, VALID_SIGNATURE) is False


# ---------------------------------------------------------------------------
# Test 4 — uses hmac.compare_digest
# ---------------------------------------------------------------------------

def test_fr05_line_uses_hmac_compare_digest():
    """FR-05: verify uses hmac.compare_digest for timing safety."""
    import inspect
    from omnibot.security import LineWebhookVerifier

    source = inspect.getsource(LineWebhookVerifier.verify)
    assert "compare_digest" in source, "Must use hmac.compare_digest"
