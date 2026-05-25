"""FR-11: Layer 1 rule-based knowledge matcher."""
from __future__ import annotations

import re


class KnowledgeMatcher:
    @staticmethod
    def match(text: str, rules: list[dict]) -> dict | None:
        """Match text against keyword rules (case-insensitive substring).

        Confidence tiers:
        - 0.95: exact keyword boundary match (word-boundary match)
        - 0.70: ILIKE-style partial substring match
        - inactive rules are skipped
        - results ordered by version desc, top-5 limit
        - empty query returns None
        """
        if not text:
            return None

        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))

        # Filter out inactive rules
        active_rules = [r for r in rules if r.get("active", True)]

        for rule in sorted(active_rules, key=lambda r: r.get("version", 0), reverse=True)[:5]:
            for keyword in rule.get("keywords", []):
                kw_lower = keyword.lower()
                if kw_lower in text_lower:
                    # Determine confidence tier
                    if kw_lower in words or re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower):
                        confidence = 0.95
                    else:
                        confidence = 0.70
                    return {
                        "question": rule.get("question", ""),
                        "answer": rule.get("answer", ""),
                        "category": rule.get("category", "general"),
                        "confidence": confidence,
                        "source": "rule",
                    }
        return None
