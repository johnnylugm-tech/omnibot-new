"""FR-11: Layer 1 rule-based knowledge matcher."""
from __future__ import annotations


class KnowledgeMatcher:
    @staticmethod
    def match(text: str, rules: list[dict]) -> dict | None:
        """Match text against keyword rules (case-insensitive substring)."""
        text_lower = text.lower()
        for rule in rules:
            for keyword in rule.get("keywords", []):
                if keyword.lower() in text_lower:
                    return {"question": rule.get("question", ""),
                            "answer": rule.get("answer", ""),
                            "category": rule.get("category", "general"),
                            "confidence": 0.8}
        return None
