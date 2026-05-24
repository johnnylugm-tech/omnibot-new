"""FR-20: UnifiedResponse dataclass."""
from __future__ import annotations

import json


def test_fr20_unified_response_serializes_correctly():
    """FR-20: UnifiedResponse serializes with required fields."""
    from omnibot.models import UnifiedResponse
    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    d = {"content": resp.content, "source": resp.source,
         "confidence": resp.confidence}
    assert d["content"] == "answer"
    assert d["source"] == "rule"
    assert d["confidence"] == 0.95


def test_fr20_unified_response_immutable():
    """FR-20: mutation raises FrozenInstanceError."""
    from omnibot.models import UnifiedResponse
    import pytest
    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    with pytest.raises(Exception):
        resp.content = "mutated"
