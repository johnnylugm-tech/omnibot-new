#!/usr/bin/env python3
"""Run FR-09 tests manually to see pass/fail state."""
import sys
sys.path.insert(0, '03-development/src')

from io import StringIO
import logging

from omnibot.processing.pii import PIIMasker

def test_mask_taiwan_phone_dashed_format():
    result = PIIMasker.mask("請聯絡 02-1234-5678")
    assert "02-1234-5678" not in result, f"Phone not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_mask_taiwan_phone_dashed_format")

def test_mask_taiwan_phone_continuous_digits():
    result = PIIMasker.mask("電話 0912345678")
    assert "0912345678" not in result, f"Phone not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_mask_taiwan_phone_continuous_digits")

def test_mask_email_address():
    result = PIIMasker.mask("Contact john@example.com for help")
    assert "john@example.com" not in result, f"Email not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_mask_email_address")

def test_mask_taiwan_address_city_road():
    result = PIIMasker.mask("台北市大安區忠孝東路")
    assert "忠孝東路" not in result, f"Address not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_mask_taiwan_address_city_road")

def test_clean_text_returns_mask_count_zero():
    count = PIIMasker.mask_count("Hello world")
    assert count == 0, f"Expected 0, got {count}"
    print("PASS: test_clean_text_returns_mask_count_zero")

def test_pii_corpus_recall():
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
    print(f"Recall: {recall:.1f}% ({masked}/{len(corpus)})")
    for text in corpus:
        result = PIIMasker.mask(text)
        print(f"  '{text}' -> '{result}'")
    assert recall >= 95, f"Recall {recall:.1f}% < 95%"
    print("PASS: test_pii_corpus_recall")

def test_pii_corpus_precision():
    clean_texts = [
        "Hello, how can I help you today?",
        "今天天氣很好",
        "請稍等我幫您查詢",
        "這是一般文字沒有個資",
    ]
    false_positives = sum(1 for text in clean_texts if "[REDACTED]" in PIIMasker.mask(text))
    precision = (len(clean_texts) - false_positives) / len(clean_texts) * 100
    print(f"Precision: {precision:.1f}% ({len(clean_texts)-false_positives}/{len(clean_texts)})")
    for text in clean_texts:
        result = PIIMasker.mask(text)
        print(f"  '{text}' -> '{result}'")
    assert precision >= 99, f"Precision {precision:.1f}% < 99%"
    print("PASS: test_pii_corpus_precision")

def test_pii_masked_in_logs():
    logger = logging.getLogger("test_pipeline")
    logger.setLevel(logging.DEBUG)
    handler = StringIO()
    logger.addHandler(handler)

    text = "帳號 john@example.com 電話 0912345678"
    masked = PIIMasker.mask(text)
    logger.debug(f"Processed: {masked}")

    log_output = handler.getvalue()
    assert "john@example.com" not in log_output, f"Email leaked: {log_output}"
    assert "0912345678" not in log_output, f"Phone leaked: {log_output}"
    assert "[REDACTED]" in log_output, f"No REDACTED in log: {log_output}"
    print("PASS: test_pii_masked_in_logs")

def test_masker_should_escalate():
    assert PIIMasker.should_escalate("請提供您的密碼") is True
    assert PIIMasker.should_escalate("信用卡號") is True
    assert PIIMasker.should_escalate("護照號碼") is True
    assert PIIMasker.should_escalate("password is secret") is True
    print("PASS: test_masker_should_escalate")

def test_masker_none_input():
    assert PIIMasker.mask(None) == "", f"mask(None) = {PIIMasker.mask(None)!r}"
    assert PIIMasker.mask_count(None) == 0
    assert PIIMasker.should_escalate(None) is False
    print("PASS: test_masker_none_input")

def test_masker_phone_leak():
    text = "您的電話是 0912345678，請確認"
    result = PIIMasker.mask(text)
    assert "0912345678" not in result, f"Phone not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_masker_phone_leak")

def test_masker_email_leak():
    text = "聯絡我們 john@example.com"
    result = PIIMasker.mask(text)
    assert "john@example.com" not in result, f"Email not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_masker_email_leak")

def test_masker_address_leak():
    text = "地址是台北市大安區忠孝東路"
    result = PIIMasker.mask(text)
    assert "忠孝東路" not in result, f"Address not masked: {result}"
    assert "[REDACTED]" in result, f"No REDACTED: {result}"
    print("PASS: test_masker_address_leak")

def test_masker_pattern_order():
    text = "Email: john@example.com 電話 0912345678 地址台北市大安區忠孝東路"
    result = PIIMasker.mask(text)
    assert "john@example.com" not in result, f"Email not masked: {result}"
    assert "0912345678" not in result, f"Phone not masked: {result}"
    assert "忠孝東路" not in result, f"Address not masked: {result}"
    assert result.count("[REDACTED]") == 3, f"Expected 3 REDACTED, got {result.count('[REDACTED]')}: {result}"
    print("PASS: test_masker_pattern_order")

def test_masker_output_feeds_pipeline():
    from omnibot.processing.pii import PIIMasker
    masked = PIIMasker.mask("聯絡 john@example.com 電話 0912345678")
    assert isinstance(masked, str)
    assert "[REDACTED]" in masked
    print("PASS: test_masker_output_feeds_pipeline")

if __name__ == "__main__":
    tests = [
        test_mask_taiwan_phone_dashed_format,
        test_mask_taiwan_phone_continuous_digits,
        test_mask_email_address,
        test_mask_taiwan_address_city_road,
        test_clean_text_returns_mask_count_zero,
        test_pii_corpus_recall,
        test_pii_corpus_precision,
        test_pii_masked_in_logs,
        test_masker_should_escalate,
        test_masker_none_input,
        test_masker_phone_leak,
        test_masker_email_leak,
        test_masker_address_leak,
        test_masker_pattern_order,
        test_masker_output_feeds_pipeline,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\nResults: {passed} passed, {failed} failed")