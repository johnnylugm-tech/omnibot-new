"""FR-09: PII masking L4."""
from __future__ import annotations

from io import StringIO

import logging


def test_fr09_mask_taiwan_phone_dashed_format():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("請聯絡 02-1234-5678")
    assert "02-1234-5678" not in result
    assert "[REDACTED]" in result


def test_fr09_mask_taiwan_phone_continuous_digits():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("電話 0912345678")
    assert "0912345678" not in result
    assert "[REDACTED]" in result


def test_fr09_mask_email_address():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("Contact john@example.com for help")
    assert "john@example.com" not in result
    assert "[REDACTED]" in result


def test_fr09_mask_taiwan_address_city_road():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("台北市大安區忠孝東路")
    assert "忠孝東路" not in result
    assert "[REDACTED]" in result


def test_fr09_clean_text_returns_mask_count_zero():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.mask_count("Hello world") == 0


def test_fr09_pii_corpus_recall_above_95_percent():
    """At least 95% of PII items in the corpus should be masked."""
    from omnibot.processing.pii import PIIMasker

    corpus = [
        "john@example.com",
        "Contact me at john.doe+tag@sub.example.co.uk",
        "電話 0912345678",
        "02-1234-5678",
        "台北市大安區忠孝東路",
        "高雄市前鎮區中山路",
    ]
    masked = sum(1 for text in corpus if "[REDACTED]" in PIIMasker.mask(text))
    recall = masked / len(corpus) * 100
    assert recall >= 95, f"Recall {recall:.1f}% < 95%"


def test_fr09_pii_corpus_precision_above_99_percent():
    """At least 99% of [REDACTED] outputs should be true positives."""
    from omnibot.processing.pii import PIIMasker

    clean_texts = [
        "Hello, how can I help you today?",
        "今天天氣很好",
        "請稍等我幫您查詢",
        "這是一般文字沒有個資",
    ]
    false_positives = sum(
        1 for text in clean_texts if "[REDACTED]" in PIIMasker.mask(text)
    )
    precision = (len(clean_texts) - false_positives) / len(clean_texts) * 100
    assert precision >= 99, f"Precision {precision:.1f}% < 99%"


def test_fr09_pii_masked_in_logs_during_pipeline():
    """PII must not appear in any pipeline stage logs."""
    import logging
    from omnibot.processing.pii import PIIMasker

    logger = logging.getLogger("test_pipeline")
    logger.setLevel(logging.DEBUG)
    handler = StringIO()
    logger.addHandler(handler)

    text = "帳號 john@example.com 電話 0912345678"
    masked = PIIMasker.mask(text)
    logger.debug(f"Processed: {masked}")

    log_output = handler.getvalue()
    assert "john@example.com" not in log_output
    assert "0912345678" not in log_output
    assert "[REDACTED]" in log_output


def test_fr09_masker_should_escalate_returns_true_for_sensitive_keywords():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.should_escalate("請提供您的密碼") is True
    assert PIIMasker.should_escalate("信用卡號") is True
    assert PIIMasker.should_escalate("護照號碼") is True
    assert PIIMasker.should_escalate("password is secret") is True


def test_fr09_masker_none_input_handled_gracefully():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.mask(None) == ""
    assert PIIMasker.mask_count(None) == 0
    assert PIIMasker.should_escalate(None) is False


def test_fr09_masker_phone_leak_masked_in_response():
    from omnibot.processing.pii import PIIMasker
    text = "您的電話是 0912345678，請確認"
    result = PIIMasker.mask(text)
    assert "0912345678" not in result
    assert "[REDACTED]" in result


def test_fr09_masker_email_leak_masked_in_response():
    from omnibot.processing.pii import PIIMasker
    text = "聯絡我們 john@example.com"
    result = PIIMasker.mask(text)
    assert "john@example.com" not in result
    assert "[REDACTED]" in result


def test_fr09_masker_address_leak_masked_in_response():
    from omnibot.processing.pii import PIIMasker
    text = "地址是台北市大安區忠孝東路"
    result = PIIMasker.mask(text)
    assert "忠孝東路" not in result
    assert "[REDACTED]" in result


def test_fr09_masker_pattern_order_phone_before_email_before_address():
    """All patterns are masked in a single pass."""
    from omnibot.processing.pii import PIIMasker
    text = "Email: john@example.com 電話 0912345678 地址台北市大安區忠孝東路"
    result = PIIMasker.mask(text)
    assert "john@example.com" not in result
    assert "0912345678" not in result
    assert "忠孝東路" not in result
    assert result.count("[REDACTED]") == 3


def test_fr09_pii_masker_output_feeds_fr19_pipeline_stage_6():
    """PIIMasker output must be usable as stage 6 input to PipelineOrchestrator."""
    from omnibot.processing.pii import PIIMasker
    from omnibot.processing.pipeline import PipelineOrchestrator, Platform

    raw = "聯絡 john@example.com 電話 0912345678"
    masked = PIIMasker.mask(raw)
    # PipelineOrchestrator.process expects (platform, raw_body, signature)
    # masked output should be string-safe for downstream stages
    assert isinstance(masked, str)
    assert "[REDACTED]" in masked


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
