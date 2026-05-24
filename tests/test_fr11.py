"""FR-11: Layer 1 knowledge matching."""
from __future__ import annotations


RULES = [
    {"question": "What are your hours?", "answer": "We are open 9-5 Mon-Fri.",
     "category": "hours", "keywords": ["hours", "open", "close"]},
    {"question": "How do I return an item?",
     "answer": "You can return items within 30 days.",
     "category": "returns", "keywords": ["return", "refund"]},
]


def test_fr11_knowledge_match_returns_answer():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("What are your business hours?", RULES)
    assert result is not None
    assert "open" in result["answer"]


def test_fr11_knowledge_no_match_returns_none():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("Tell me about quantum physics", RULES)
    assert result is None


def test_fr11_knowledge_case_insensitive():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("HOW DO I RETURN AN ITEM please", RULES)
    assert result is not None
    assert "return" in result["answer"]
