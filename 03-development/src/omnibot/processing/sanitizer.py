"""[FR-08] Input Sanitizer L2 — Unicode NFKC normalization."""
from __future__ import annotations

import unicodedata


class InputSanitizer:
    @staticmethod
    def sanitize(text: str) -> str:
        """Normalize input text using NFKC, strip control chars (except \n, \t)."""
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKC", text)
        cleaned = "".join(ch for ch in normalized if ch.isprintable() or ch in ("\n", "\t"))
        return cleaned
