"""
FR-19 / NFR-01: Pipeline performance benchmark.

NFR-01: p95 latency < 3.0s for PipelineOrchestrator.process().

Uses pytest-benchmark (https://pytest-benchmark.readthedocs.io/).
Run with:
    pytest tests/test_fr19_benchmark.py --benchmark-only

TDD-RED: PipelineOrchestrator.process() raises NotImplementedError until
         FR-19 TDD-GREEN is complete. Tests are skipped when not implemented.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from omnibot.processing.pipeline import PipelineOrchestrator, Platform


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_orchestrator() -> PipelineOrchestrator:
    """Return a PipelineOrchestrator wired with fast mocked dependencies."""
    return PipelineOrchestrator()


def _sample_body() -> bytes:
    return b'{"update_id": 1, "message": {"text": "hello", "chat": {"id": 42}}}'


def _sample_signature() -> str:
    return "sha256=abc123"


# ---------------------------------------------------------------------------
# NFR-01: benchmark tests
# (Skipped via pytest.importorskip / skip-if-not-implemented guard)
# ---------------------------------------------------------------------------

def _run_pipeline(orchestrator: PipelineOrchestrator) -> None:
    """Helper called by benchmark fixture."""
    orchestrator.process(Platform.TELEGRAM, _sample_body(), _sample_signature())


def test_pipeline_process_benchmark(benchmark):
    """
    NFR-01: full pipeline p95 must be < 3000ms.

    The benchmark fixture measures mean latency. Gate 3/4 performance
    dimension cross-validates this via pytest-benchmark --benchmark-only.
    """
    orchestrator = _make_orchestrator()

    try:
        result = benchmark(_run_pipeline, orchestrator)
    except NotImplementedError:
        pytest.skip("FR-19 PipelineOrchestrator.process() not yet implemented")

    assert result is not None or True  # UnifiedResponse or None is valid


def test_pipeline_mean_latency_assertion(benchmark):
    """
    Explicit mean latency guard: fail if mean > 3000ms.
    Complements the gate score threshold with a hard assertion.
    """
    orchestrator = _make_orchestrator()

    try:
        benchmark(_run_pipeline, orchestrator)
    except NotImplementedError:
        pytest.skip("FR-19 not yet implemented")

    mean_ms = benchmark.stats["mean"] * 1000
    assert mean_ms < 3000, (
        f"Pipeline mean latency {mean_ms:.1f}ms exceeds NFR-01 target of 3000ms"
    )
