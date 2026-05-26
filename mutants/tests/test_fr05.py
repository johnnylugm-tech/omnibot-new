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


# ---------------------------------------------------------------------------
# Test 5 — uses compare_digest (timing-safe comparison)
# ---------------------------------------------------------------------------

def test_fr05_line_uses_compare_digest_timing_safe():
    """FR-05: verify uses hmac.compare_digest for timing-safe comparison."""
    import inspect
    from omnibot.security import LineWebhookVerifier

    source = inspect.getsource(LineWebhookVerifier.verify)
    assert "compare_digest" in source, "Must use hmac.compare_digest for timing safety"


# ---------------------------------------------------------------------------
# Test 6 — webhook invalid signature returns 401
# ---------------------------------------------------------------------------

def test_fr05_line_webhook_invalid_signature_returns_401():
    """FR-05: invalid LINE signature -> AUTH_INVALID_SIGNATURE maps to HTTP 401."""
    from omnibot.errors.codes import AUTH_INVALID_SIGNATURE, HTTP_STATUS_MAP

    assert AUTH_INVALID_SIGNATURE == "AUTH_INVALID_SIGNATURE"
    assert HTTP_STATUS_MAP[AUTH_INVALID_SIGNATURE] == 401


# ---------------------------------------------------------------------------
# Test 7 — uses both HMAC and compare_digest for timing safety
# ---------------------------------------------------------------------------

def test_fr05_line_uses_hmac_compare_digest_for_timing_safety():
    """FR-05: verify uses both hmac.new and hmac.compare_digest for timing safety."""
    import inspect
    from omnibot.security import LineWebhookVerifier

    source = inspect.getsource(LineWebhookVerifier.verify)
    assert "hmac.new" in source or "hmac.digest" in source, (
        "Must use HMAC for signature computation"
    )
    assert "compare_digest" in source, (
        "Must use hmac.compare_digest for timing-safe comparison"
    )


# ---------------------------------------------------------------------------
# Test 8 — AUTH_INVALID_SIGNATURE error code maps to 401 (NP-01)
# ---------------------------------------------------------------------------

def test_fr05_line_invalid_signature_returns_401_auth_invalid_signature():
    """FR-05 NP-01: AUTH_INVALID_SIGNATURE error code -> HTTP 401."""
    from omnibot.errors.codes import AUTH_INVALID_SIGNATURE, HTTP_STATUS_MAP
    from omnibot.security import LineWebhookVerifier

    verifier = LineWebhookVerifier(CHANNEL_SECRET)
    # Verify that an invalid signature is rejected
    assert verifier.verify(BODY, "invalid_base64_signature==") is False
    # And that the corresponding error code maps to 401
    assert HTTP_STATUS_MAP[AUTH_INVALID_SIGNATURE] == 401


# ---------------------------------------------------------------------------
# Test 9 — timing difference below 5ms (NP-08)
# ---------------------------------------------------------------------------

def test_fr05_line_timing_difference_below_5ms():
    """FR-05 NP-08: timing delta between valid/invalid signature < 5ms."""
    import timeit
    from omnibot.security import LineWebhookVerifier

    verifier = LineWebhookVerifier(CHANNEL_SECRET)
    invalid_sig = base64.b64encode(b"wrong" * 8).decode()
    iterations = 200

    valid_time = timeit.timeit(
        lambda: verifier.verify(BODY, VALID_SIGNATURE), number=iterations
    )
    invalid_time = timeit.timeit(
        lambda: verifier.verify(BODY, invalid_sig), number=iterations
    )

    avg_delta_ms = (abs(valid_time - invalid_time) / iterations) * 1000
    assert avg_delta_ms < 5, (
        f"Timing delta {avg_delta_ms:.3f}ms exceeds 5ms threshold"
    )


# ---------------------------------------------------------------------------
# Test 10 — signature verification feeds pipeline stage 2
# ---------------------------------------------------------------------------

def test_fr05_signature_feeds_fr19_pipeline_stage_2():
    """FR-05→FR-19: LineWebhookVerifier.verify has the correct interface for pipeline stage 2."""
    import inspect
    from omnibot.security import LineWebhookVerifier, WebhookVerifier

    method = LineWebhookVerifier.verify
    sig = inspect.signature(method)
    param_names = list(sig.parameters.keys())

    assert "body" in param_names, "Stage 2 must accept body bytes"
    assert "signature" in param_names, "Stage 2 must accept signature string"
    assert sig.return_annotation is bool, "Stage 2 must return bool"
    assert issubclass(LineWebhookVerifier, WebhookVerifier), (
        "Must implement WebhookVerifier for pipeline compatibility"
    )
