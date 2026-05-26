"""[FR-09] PII masking L4."""
from __future__ import annotations

import re


class PIIMasker:
    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{6,8}\d")
    TAIWAN_ADDRESS_RE = re.compile(
        r"[一-鿿]+(?:市|縣)[一-鿿]+(?:區|鎮|鄉)[一-鿿]+(?:路|街|大道)",  # noqa: E501
    )
    SENSITIVE_KEYWORDS = frozenset(["密碼", "信用卡", "身份證", "護照", "password", "credit card", "ssn"])

    @staticmethod
    def mask(text: str) -> str:
        """Replace emails and phone numbers with '[REDACTED]'."""
        if text is None:
            return ""
        text = PIIMasker.EMAIL_RE.sub("[REDACTED]", text)
        text = PIIMasker.PHONE_RE.sub("[REDACTED]", text)
        text = PIIMasker.TAIWAN_ADDRESS_RE.sub("[REDACTED]", text)
        return text

    @staticmethod
    def mask_count(text: str) -> int:
        """Return the number of PII redactions made."""
        if text is None:
            return 0
        return (
            len(PIIMasker.EMAIL_RE.findall(text))
            + len(PIIMasker.PHONE_RE.findall(text))
            + len(PIIMasker.TAIWAN_ADDRESS_RE.findall(text))
        )

    @staticmethod
    def should_escalate(text: str) -> bool:
        """Return True if text contains sensitive keywords requiring escalation."""
        if text is None:
            return False
        lower = text.lower()
        return any(kw.lower() in lower for kw in PIIMasker.SENSITIVE_KEYWORDS)
