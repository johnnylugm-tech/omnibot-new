"""FR-12: Basic escalation queue."""
from __future__ import annotations


def test_fr12_escalation_enqueue_returns_entry():
    from omnibot.escalation.queue import EscalationQueue
    entry = EscalationQueue.enqueue("no_rule_match", {"text": "hello"})
    assert entry["reason"] == "no_rule_match"
    assert entry["status"] == "pending"
    assert entry["priority"] == 0
