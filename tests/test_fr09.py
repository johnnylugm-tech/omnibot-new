"""FR-09: PII masking L4."""
from __future__ import annotations


def test_fr09_pii_masks_email():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("Contact john@example.com for help")
    assert "john@example.com" not in result
    assert "[REDACTED]" in result


def test_fr09_pii_masks_phone():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("Call +1-555-123-4567 today")
    assert "+1-555-123-4567" not in result
    assert "[REDACTED]" in result


def test_fr09_pii_preserves_safe_text():
    from omnibot.processing.pii import PIIMasker
    text = "Hello, how can I help you?"
    assert PIIMasker.mask(text) == text
