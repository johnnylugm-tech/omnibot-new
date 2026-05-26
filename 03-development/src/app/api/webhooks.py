"""FR-02/FR-03/FR-14: HTTP transport layer — webhook and health endpoints.

Routes:
  POST /api/v1/webhook/telegram  (FR-02)
  POST /api/v1/webhook/line      (FR-03)
  GET  /api/v1/health            (FR-14)

Citations:
  - SRS.md §FR-02, §FR-03, §FR-14
  - SAD.md §2.1 app.api.webhooks
"""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, Response

from omnibot.infrastructure.health import health_check
from omnibot.models import Platform
from omnibot.processing.pipeline import PipelineOrchestrator

app = FastAPI(title="OmniBot", version="1.0.0")
_pipeline = PipelineOrchestrator()


@app.post("/api/v1/webhook/telegram")
async def webhook_telegram(request: Request) -> Response:
    """Accept Telegram Bot API webhook POST and process through pipeline."""
    raw_body = await request.body()
    signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    result = _pipeline.process(Platform.TELEGRAM, raw_body, signature)
    return Response(
        content=result.content,
        status_code=result.status_code,
        media_type="application/json",
    )


@app.post("/api/v1/webhook/line")
async def webhook_line(request: Request) -> Response:
    """Accept LINE webhook POST and process through pipeline."""
    raw_body = await request.body()
    signature = request.headers.get("X-Line-Signature", "")
    result = _pipeline.process(Platform.LINE, raw_body, signature)
    return Response(
        content=result.content,
        status_code=result.status_code,
        media_type="application/json",
    )


@app.get("/api/v1/health")
async def health() -> dict[str, Any]:
    """Return composite health status (FR-14)."""
    return health_check()
