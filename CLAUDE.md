# Project: omnibot-new

## Methodology Handoff
- Framework: harness-methodology v2.4.0
- Quality Manifest: .methodology/quality_manifest.json
- Active Phase: P3 (Implementation)
- Last Gate: Gate 1 (per-FR, ongoing)
- Reviewer Chain: hermes,gemini  (P1–P2 A/B; Hermes optional)

## FR Registry
| FR ID | Description | Gate 1 Status | Gate 1 Score |
|-------|-------------|---------------|--------------|
| FR-01 | PostgreSQL schema — users/conversations/messages/knowledge_base/... | PASS | 89 |
| FR-02 | Telegram webhook handler | PASS | 100 |
| FR-03 | LINE webhook handler | PASS | 100 |
| FR-04 | Telegram HMAC signature verification | PASS | 100 |
| FR-05 | LINE HMAC signature verification | PASS | 100 |
| FR-06 | Unified message ingestion (multi-platform → DB) | PASS | 100 |
| FR-07 | REST API response builder | PASS | 100 |
| FR-08 | Input sanitizer (fullwidth → ASCII, script injection) | PASS | 100 |
| FR-09 | PII masker (Taiwan phone/ID/email) | PENDING | — |
| FR-10 | Token-bucket rate limiter | PENDING | — |
| FR-11 | AI response pipeline (OpenAI + fallback) | PENDING | — |
| FR-12 | Health check endpoint (/health) | PENDING | — |
| FR-13 | Structured JSON logger | PENDING | — |
| FR-14 | Graceful shutdown handler | PENDING | — |
| FR-15 | Docker Compose stack | PENDING | — |
| FR-16 | Ruff zero-violation enforcement | PENDING | — |
| FR-17 | DB schema migration runner | PENDING | — |
| FR-18 | Request-ID correlation middleware | PENDING | — |
| FR-19 | AI pipeline latency metrics (p95 < 3s) | PENDING | — |
| FR-20 | Cyclomatic complexity guard (CC ≤ 10) | PENDING | — |
| FR-21 | Escalation queue worker | PENDING | — |
| FR-22 | IP whitelist middleware | PENDING | — |

## Architecture Constraints
- No synchronous I/O in main thread
- Security validation before business logic (HMAC → sanitize → process)
- PII masking before any external AI call
- All webhook secrets via environment variables, never hardcoded

## High-Risk Modules
- 03-development/src/omnibot/security/ (HMAC verification — must never skip)
- 03-development/src/omnibot/processing/pii.py (PII masking — recall ≥ 95%)

## Open Issues (Top Priority)
- FR-09 Gate 1 FAIL: test_coverage dim failing (score 67, threshold 80)
- FR-10 Gate 1 FAIL: test_coverage dim failing (score 67, threshold 80)

## NFR → Dimension Mapping
| NFR | Dimension | Target |
|-----|-----------|--------|
| NFR-01 | performance | p95 < 3.0s (pipeline latency) |
| NFR-02 | security | HMAC rejection before business logic |
| NFR-03 | security | sanitization on every inbound message |
| NFR-04 | security | PII recall ≥ 95%, precision ≥ 99% |
| NFR-05 | security | rate limiter independent per-user buckets |
| NFR-06 | reliability | health check < 500ms |
| NFR-07 | maintainability | single-line JSON logs |
| NFR-08 | maintainability | ruff zero violations, CC ≤ 10 |
| NFR-09 | deployability | docker compose healthy within 60s |
| NFR-10 | security | IP whitelist blocks before HMAC |

## Gate Status
| Gate | Trigger | Score | Status |
|------|---------|-------|--------|
| Gate 1 | P3 per-FR | varies | IN PROGRESS (8/22 PASS) |
| Gate 2 | P3 exit | — | PENDING |
| Gate 3 | P4 exit | — | PENDING |
| Gate 4 | P6 full | — | PENDING |

## Agent Interaction Model
```
Johnny: "執行 Phase N"
  → Agent: plan-phase N       (generates Plan_Phase_N.md)
  → Johnny: reviews plan
  → Agent: run-phase N        (executes plan)
  → POST-FLIGHT: gate check + Hermes reviewer
```

## Project Layout
```
03-development/src/omnibot/   ← main package (tests import from omnibot.*)
03-development/src/app/       ← future package (migration in progress, see TODO.md)
tests/test_frXX.py            ← per-FR test files
02-architecture/TEST_SPEC.md  ← required test function names per FR
harness/                      ← harness-methodology submodule
```

## IMPORTANT for Gate 1 evaluation
Gate 1 evaluates 3 dimensions: linting, type_safety, test_coverage.
Commands (use exactly as printed by run-gate FR-SCOPED TOOL OVERRIDES):
- linting: `ruff check 03-development/src/ 2>&1 | head -200`
- type_safety: `pyright 03-development/src/ --outputjson 2>&1 | head -200`
- test_coverage: see run-gate output for FR-specific coverage command

gate1_result.json MUST include `tool_evidence` in every breakdown entry or finalize-gate will BLOCK with S3 error.
