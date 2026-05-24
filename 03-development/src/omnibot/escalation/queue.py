"""FR-12: Basic escalation queue."""
from __future__ import annotations


class EscalationQueue:
    @staticmethod
    def enqueue(reason: str, message: dict) -> dict:
        """Create an escalation entry. Returns the entry dict."""
        return {
            "reason": reason,
            "message": message,
            "priority": 0,
            "status": "pending",
        }
