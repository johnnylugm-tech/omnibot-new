"""FR-08: Input Sanitizer L2 — NFKC normalization, strip control chars.

SRS.md §FR-08:
  "Normalize all inbound message text using Unicode NFKC normalization"
"""

from __future__ import annotations


def test_fr08_sanitizer_fullwidth_to_ascii():
    """FR-08: fullwidth chars -> ASCII via NFKC."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("ＴＥＳＴ") == "TEST"


def test_fr08_sanitizer_control_chars_removed():
    """FR-08: non-printable control chars removed."""
    from omnibot.processing.sanitizer import InputSanitizer
    result = InputSanitizer.sanitize("Hello\x00\x01\x02World")
    assert "\x00" not in result
    assert result == "HelloWorld"


def test_fr08_sanitizer_newlines_preserved():
    """FR-08: newlines and tabs preserved."""
    from omnibot.processing.sanitizer import InputSanitizer
    result = InputSanitizer.sanitize("Line 1\nLine 2\tindented")
    assert "\n" in result
    assert "\t" in result


def test_fr08_sanitizer_empty_string():
    """FR-08: empty string returns empty string."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("") == ""


def test_fr08_sanitizer_ascii_unchanged():
    """FR-08: ASCII alphanumerics unchanged."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("Hello World 123") == "Hello World 123"


def test_fr08_sanitizer_no_regex():
    """FR-08: no regex pattern matching in implementation."""
    import inspect
    from omnibot.processing.sanitizer import InputSanitizer
    source = inspect.getsource(InputSanitizer.sanitize)
    assert "re." not in source and "regex" not in source.lower()
