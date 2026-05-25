"""FR-12: Basic escalation queue."""
from __future__ import annotations


class EscalationQueue:
    @staticmethod
    def enqueue(reason: str, message: dict) -> dict:
        """Create an escalation entry. Returns the entry dict."""
        return {
            "id": -1,
            "reason": reason,
            "message": message,
            "priority": 0,
            "status": "pending",
            "source": "escalate",
            "sla_deadline": None,
            "scope_type": "out_of_scope" if reason == "out_of_scope" else "unknown",
        }
