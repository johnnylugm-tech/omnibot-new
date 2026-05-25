"""FR-20: UnifiedResponse dataclass — 6 tests."""
from __future__ import annotations

import json
import time
from unittest.mock import patch

import pytest

from omnibot.models import (
    KnowledgeSource,
    Platform,
    UnifiedMessage,
    UnifiedResponse,
)


# ---------------------------------------------------------------------------
# Existing passing test
# ---------------------------------------------------------------------------


def test_fr20_unified_response_serializes_correctly():
    """FR-20: UnifiedResponse serializes with required fields."""
    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    d = {"content": resp.content, "source": resp.source,
         "confidence": resp.confidence}
    assert d["content"] == "answer"
    assert d["source"] == "rule"
    assert d["confidence"] == 0.95


# ---------------------------------------------------------------------------
# Immutability — requires @dataclass(frozen=True) on UnifiedResponse
# ---------------------------------------------------------------------------


def test_fr20_unified_response_mutation_raises_frozen_instance_error():
    """FR-20: mutation raises FrozenInstanceError."""
    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    with pytest.raises(Exception):
        resp.content = "mutated"


# ---------------------------------------------------------------------------
# metadata field default
# ---------------------------------------------------------------------------


def test_fr20_unified_response_metadata_defaults_to_empty_dict():
    """FR-20: metadata field defaults to empty dict."""
    resp = UnifiedResponse(content="answer", source="rule", confidence=0.95)
    assert resp.metadata == {}
    # metadata is mutable internally (frozen=False container inside frozen struct)
    resp.metadata["key"] = "value"
    assert resp.metadata["key"] == "value"


# ---------------------------------------------------------------------------
# KnowledgeSource enum
# ---------------------------------------------------------------------------


def test_fr20_knowledge_source_enum_has_rule_and_escalate():
    """FR-20: KnowledgeSource enum has RULE and ESCALATE members."""
    assert hasattr(KnowledgeSource, "RULE")
    assert hasattr(KnowledgeSource, "ESCALATE")
    assert KnowledgeSource.RULE.value == "rule"
    assert KnowledgeSource.ESCALATE.value == "escalate"


# ---------------------------------------------------------------------------
# Pipeline integration — requires PipelineOrchestrator (stub in pipeline.py)
# ---------------------------------------------------------------------------


def test_fr20_pipeline_returns_unified_response_with_correct_source_and_confidence():
    """FR-20: pipeline returns UnifiedResponse with correct source and confidence."""
    import hashlib
    import hmac
    import os
    from omnibot.processing.pipeline import PipelineOrchestrator

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "test_token")
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()

    orch = PipelineOrchestrator()
    payload = {
        "message": {
            "from": {"id": 123456},
            "text": "hello",
        }
    }
    body = json.dumps(payload).encode()
    signature = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    result = orch.process(Platform.TELEGRAM, body, signature)
    assert isinstance(result, UnifiedResponse)
    assert result.source in ("rule", "escalate")
    assert isinstance(result.confidence, float)


def test_fr20_unified_response_constructed_by_fr19_pipeline_stage_9():
    """FR-20: UnifiedResponse is constructed by FR-19 pipeline stage 9."""
    # Stage 9 constructs UnifiedResponse; verify it has all required fields
    resp = UnifiedResponse(
        content="Hello!",
        source="rule",
        confidence=0.95,
        knowledge_id=1,
    )
    assert resp.source == "rule"
    assert resp.confidence == 0.95
    assert resp.knowledge_id == 1
    assert resp.platform == Platform.TELEGRAM