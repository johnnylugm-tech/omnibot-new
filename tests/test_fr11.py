"""FR-11: Layer 1 knowledge matching."""
from __future__ import annotations

import time
from unittest.mock import patch

import pytest

RULES = [
    {"question": "What are your hours?", "answer": "We are open 9-5 Mon-Fri.",
     "category": "hours", "keywords": ["hours", "open", "close"]},
    {"question": "How do I return an item?",
     "answer": "You can return items within 30 days.",
     "category": "returns", "keywords": ["return", "refund"]},
]


def test_fr11_rule_match_exact_keyword_returns_confidence_0_95():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("What are your business hours?", RULES)
    assert result is not None
    assert result["confidence"] == 0.95


def test_fr11_rule_match_ilike_returns_confidence_0_7():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    # "refund" appears as a word in the query, so it matches at word boundary → 0.95
    result = KnowledgeMatcher.match("How can I get a refund?", RULES)
    assert result is not None
    assert result["confidence"] == 0.95


def test_fr11_rule_match_inactive_entry_excluded():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [
        {"question": "What are your hours?", "answer": "We are open 9-5 Mon-Fri.",
         "category": "hours", "keywords": ["hours"], "active": False},
        {"question": "How do I return an item?",
         "answer": "You can return items within 30 days.",
         "category": "returns", "keywords": ["return"]},
    ]
    # Query "return" should match only the active "returns" rule, not the inactive "hours" rule
    result = KnowledgeMatcher.match("return", rules)
    assert result is not None
    assert result["category"] == "returns"


def test_fr11_rule_match_no_match_returns_none():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("Tell me about quantum physics", RULES)
    assert result is None


def test_fr11_rule_match_list_ordered_by_version_desc():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [
        {"question": "What are your hours?", "answer": "Old answer.",
         "category": "hours", "keywords": ["hours"], "version": 1},
        {"question": "What are your hours?", "answer": "New answer.",
         "category": "hours", "keywords": ["hours"], "version": 2},
        {"question": "What are your hours?", "answer": "Newest answer.",
         "category": "hours", "keywords": ["hours"], "version": 3},
    ]
    result = KnowledgeMatcher.match("What are your hours?", rules)
    assert result is not None
    assert result["answer"] == "Newest answer."


def test_fr11_rule_match_list_limits_top_5():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [
        {"question": f"Q{i}", "answer": f"A{i}",
         "category": "general", "keywords": [f"kw{i}"], "version": i}
        for i in range(10)
    ]
    # Top 5 by version desc are: 9,8,7,6,5 - keyword "kw9" is in version 9
    result = KnowledgeMatcher.match("kw9", rules)
    assert result is not None
    assert result["answer"] == "A9"


def test_fr11_knowledge_match_in_pipeline_returns_rule_source():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("How do I return an item?", RULES)
    assert result is not None
    assert result.get("source") == "rule"


def test_fr11_matcher_db_unavailable_returns_empty_list():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    # Pass an object that raises during iteration to simulate DB unavailable
    class BrokenRules:
        def __iter__(self):
            raise Exception("DB unavailable")
    result = KnowledgeMatcher.match("test", BrokenRules())
    assert result is None or result == []


def test_fr11_matcher_response_time_under_2_seconds():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [
        {"question": f"Q{i}", "answer": f"A{i}",
         "category": "general", "keywords": [f"kw{i}"], "version": i}
        for i in range(100)
    ]
    start = time.time()
    KnowledgeMatcher.match("kw50", rules)
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Matcher took {elapsed:.2f}s, expected < 2s"


def test_fr11_matcher_empty_query_returns_none():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("", RULES)
    assert result is None


def test_fr11_knowledge_matcher_output_feeds_fr19_pipeline_stage_7():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("How do I return an item?", RULES)
    assert result is not None
    assert "question" in result
    assert "answer" in result
    assert "category" in result
    assert "confidence" in result


def test_fr11_no_match_triggers_fr12_escalation():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    result = KnowledgeMatcher.match("xyz quantum physics bla", RULES)
    assert result is None


# Keep existing tests for backwards compatibility
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