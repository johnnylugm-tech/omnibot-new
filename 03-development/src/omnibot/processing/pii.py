"""FR-09: PII masking L4."""
from __future__ import annotations

import re


class PIIMasker:
    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{6,8}\d")

    @staticmethod
    def mask(text: str) -> str:
        """Replace emails and phone numbers with '[REDACTED]'."""
        text = PIIMasker.EMAIL_RE.sub("[REDACTED]", text)
        text = PIIMasker.PHONE_RE.sub("[REDACTED]", text)
        return text
