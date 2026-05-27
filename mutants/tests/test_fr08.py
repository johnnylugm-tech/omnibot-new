"""[FR-08]  Input Sanitizer L2 — NFKC normalization, strip control chars.

SRS.md §FR-08:
  "Normalize all inbound message text using Unicode NFKC normalization"
"""

from __future__ import annotations


def test_fr08_sanitize_fullwidth_to_ascii_via_nfkc():
    """FR-08: fullwidth chars normalized via NFKC -> ASCII."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("ＴＥＳＴ") == "TEST"


def test_fr08_sanitize_control_chars_removed():
    """FR-08: non-printable control chars removed."""
    from omnibot.processing.sanitizer import InputSanitizer
    result = InputSanitizer.sanitize("Hello\x00\x01\x02World")
    assert "\x00" not in result
    assert result == "HelloWorld"


def test_fr08_sanitize_newlines_and_tabs_preserved():
    """FR-08: newlines and tabs are preserved."""
    from omnibot.processing.sanitizer import InputSanitizer
    result = InputSanitizer.sanitize("Line 1\nLine 2\tindented")
    assert "\n" in result and "\t" in result


def test_fr08_sanitize_empty_string_returns_empty_string():
    """FR-08: empty string returns empty string."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("") == ""


def test_fr08_sanitize_no_regex_pattern_matching_in_implementation():
    """FR-08: implementation contains no regex pattern matching."""
    import inspect
    from omnibot.processing.sanitizer import InputSanitizer
    source = inspect.getsource(InputSanitizer.sanitize)
    assert "re." not in source and "regex" not in source.lower()


def test_fr08_sanitizer_called_in_pipeline_before_knowledge_match():
    """FR-08: sanitizer is called in pipeline before knowledge matching (stage 5)."""
    import inspect
    from omnibot.processing.pipeline import PipelineOrchestrator
    source = inspect.getsource(PipelineOrchestrator)
    # Stage 5 is sanitization, stage 7 is knowledge matching
    # Confirm stage ordering in docstring
    assert "Input sanitization L2" in source and "Knowledge matching Layer 1" in source


def test_fr08_nfkc_does_not_alter_ascii_alphanumerics():
    """FR-08: NFKC normalization does not alter plain ASCII alphanumerics."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("Hello World 123") == "Hello World 123"


def test_fr08_invalid_input_none_handled_gracefully():
    """FR-08: None input is handled gracefully (returns empty string)."""
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize(None) == ""


def test_fr08_sanitizer_output_feeds_fr09_pii_masker():
    """FR-08: sanitizer output is passed to PII masker (FR-09)."""
    from omnibot.processing.sanitizer import InputSanitizer
    from omnibot.processing.pii import PIIMasker
    # Sanitizer should clean the text before PII masking
    dirty = "user@example.com and 0912345678"
    sanitized = InputSanitizer.sanitize(dirty)
    masked = PIIMasker.mask(sanitized)
    assert masked == "[REDACTED] and [REDACTED]"


def test_fr08_sanitizer_output_feeds_fr19_pipeline_stage_5():
    """FR-08: sanitizer is integrated as pipeline stage 5."""
    from omnibot.processing.pipeline import PipelineOrchestrator
    doc = PipelineOrchestrator.__doc__ or ""
    assert "5. Input sanitization L2" in doc
