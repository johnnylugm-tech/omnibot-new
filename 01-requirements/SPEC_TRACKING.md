# SPEC_TRACKING — OmniBot Phase 1

## Project Info
- Project Name: OmniBot
- Version: v7.0
- Created: 2026-05-23
- Source SPEC: `SPEC.md` v7.0 (2026-05-21)
- Phase: 1 (MVP Foundation)

## Specification Status

| FR ID | Spec Description | Intent Class | Decision Framework | Status | Notes |
|-------|-----------------|-------------|-------------------|--------|-------|
| FR-01 | Create complete PostgreSQL schema with all 8 core tables + 11 indexes; Phase 2/3 columns included with defaults to avoid ALTER TABLE later | DATA_MODEL | SPEC.md §Database Schema (lines 1772–2035) | DRAFT | Migration `001_phase1_core.py`; must support pgvector extension; future-proof schema design |
| FR-02 | Accept Telegram Bot API webhook POST, parse payload into immutable UnifiedMessage dataclass | INTEGRATION | SPEC.md §Platform Adapter Layer, §Unified Message Format (lines 412–451) | DRAFT | Adapter pattern; must extract platform_user_id, message_type, content, raw_payload |
| FR-03 | Accept LINE Messaging API webhook POST, parse payload into immutable UnifiedMessage with reply_token | INTEGRATION | SPEC.md §Platform Adapter Layer, §Unified Message Format (lines 412–451) | DRAFT | LINE events array handling; reply_token required for response |
| FR-04 | Verify Telegram webhook signature via HMAC-SHA256 over bot_token-derived secret; reject invalid with 401 AUTH_INVALID_SIGNATURE | SECURITY | SPEC.md §Webhook Signature Verification (lines 457–515, TelegramVerifier) | DRAFT | Must use hmac.compare_digest for timing-safe comparison |
| FR-05 | Verify LINE webhook signature via HMAC-SHA256 over channel_secret with Base64 digest; reject invalid with 401 AUTH_INVALID_SIGNATURE | SECURITY | SPEC.md §Webhook Signature Verification (lines 457–515, LineVerifier) | DRAFT | Must use hmac.compare_digest for timing-safe comparison |
| FR-06 | Define immutable UnifiedMessage dataclass with Platform and MessageType enums; all required fields with defaults | API_DESIGN | SPEC.md §Unified Message Format (lines 412–451) | DRAFT | Frozen dataclass; received_at defaults to UTC now; all enum members defined |
| FR-07 | Define generic ApiResponse[T] and PaginatedResponse[T] dataclasses with success/data/error/error_code fields | API_DESIGN | SPEC.md §API Design — Unified Response Format (lines 374–393) | DRAFT | Generic typing; PaginatedResponse extends with total/page/limit/has_next |
| FR-08 | Normalize inbound text via NFKC; strip non-printable chars (except \n, \t); trim whitespace; no pattern matching | SECURITY | SPEC.md §Security Layer — Input Sanitizer L2 (lines 521–536) | DRAFT | Character-level only; L3 prompt injection defense deferred to Phase 2 |
| FR-09 | Detect and mask PII: Taiwan phone formats, email addresses, Taiwan addresses; return PIIMaskResult with masked_text, mask_count, pii_types | SECURITY | SPEC.md §PII Masking L4 Phase 1 subset (lines 608–684) | DRAFT | Phase 1 subset only (no credit card); recall >= 95%, precision >= 99% |
| FR-10 | Enforce per-platform per-user rate limiting via Token Bucket (default 100 rps); reject excess with 429 RATE_LIMIT_EXCEEDED | PROCESSING | SPEC.md §Rate Limiter Token Bucket (lines 688–730) | DRAFT | Capacity and refill rate configurable; independent per-platform:user keys |
| FR-11 | Query knowledge_base via SQL ILIKE and keyword array match; return KnowledgeResult with source="rule", confidence 0.7-0.95 | KNOWLEDGE | SPEC.md §Knowledge Layer 1 — _rule_match (lines 935–959) | DRAFT | Layer 1 only (rule matching); ILIKE for substring, = ANY(keywords) for keyword match |
| FR-12 | Create escalation record with reason="no_rule_match"/"out_of_scope", priority=0; return handoff KnowledgeResult (no SLA, no agent assignment) | ESCALATION | SPEC.md §Escalation — Basic Handoff Phase 1 (lines 1195–1262) | DRAFT | Phase 1 basic only; SLA tracking, priority levels, agent assignment deferred to Phase 2+ |
| FR-13 | Emit single-line JSON log entries with timestamp (ISO 8601), level, service, message, and arbitrary kwargs via Python stdlib logging | OBSERVABILITY | SPEC.md §Observability — Structured Logger (lines 1441–1490) | DRAFT | Uses stdlib logging as transport; Prometheus/OTel/Grafana deferred to Phase 2/3 |
| FR-14 | Expose GET /api/v1/health returning JSON with postgres status, redis status, uptime_seconds; degrade gracefully (200 even when degraded) | API_DESIGN | SPEC.md §API Design — Health Check Endpoint (lines 356–370) | DRAFT | Returns 200 in all states; status: healthy/degraded/unhealthy; each dependency checked independently |
| FR-15 | Provide docker-compose.yml with omnibot-api (port 8000, healthcheck), postgres (pgvector:pg16), redis (7-alpine); all with healthchecks | DEPLOYMENT | SPEC.md §Deployment — Docker Compose Phase 1 subset (lines 2273–2334) | DRAFT | Phase 1: 3 services only; no otel/prometheus/grafana; all healthy within 60s |
| FR-16 | Provide ODD SQL scripts: FCR rate (30-day), p95 latency per platform (30-day), knowledge source hit distribution (7-day) | OBSERVABILITY | SPEC.md §ODD SQL Phase 1 (lines 2069–2103) | DRAFT | Three query files: fcr.sql, latency.sql, knowledge_hits.sql; PERCENTILE_CONT(0.95) for p95 |
| FR-17 | Define and use standardized error codes: AUTH_INVALID_SIGNATURE (401), RATE_LIMIT_EXCEEDED (429), KNOWLEDGE_NOT_FOUND (404), VALIDATION_ERROR (422), INTERNAL_ERROR (500) | API_DESIGN | SPEC.md §API Design — Error Codes (lines 397–407, Phase 1 subset) | DRAFT | All error responses use ApiResponse format with success=False + error_code |
| FR-18 | Follow Python naming conventions: snake_case, PascalCase, UPPER_SNAKE; docstrings on all public functions; max function length 50; CC <= 10 | CONVENTION | SPEC.md §Code Conventions, constitution/CONSTITUTION.md §1.2, §4.1 | DRAFT | Enforced by ruff + radon; zero lint violations required |
| FR-19 | Implement core message processing pipeline: IP Whitelist → verify → parse → rate limit → sanitize → PII mask → knowledge match → escalate/construct UnifiedResponse → send reply → log | PROCESSING | SPEC.md §System Architecture (lines 87–189), Pipeline flow | DRAFT | Orchestrates all 11 stages end-to-end; errors at any stage must not crash pipeline |
| FR-20 | Define immutable UnifiedResponse dataclass with platform, user_id, content, source (KnowledgeSource enum), confidence, metadata | API_DESIGN | SPEC.md §Unified Message Format (lines 412–451), Glossary | DRAFT | Frozen dataclass; metadata defaults to empty dict; used by all platform adapters |
| FR-21 | Load and validate configuration from env vars (bot tokens, secrets, DB/Redis URLs, rate limiter settings); fail fast on missing required keys | DEPLOYMENT | SPEC.md §Configuration (bot tokens, DB/Redis URLs, rate limiter settings) | DRAFT | Pydantic/dataclass Settings; ConfigError with missing key list on startup |
| FR-22 | Implement IP Whitelist interception to block unofficial IPs | SECURITY | SPEC.md §Security Layer — IP Whitelist (lines 740–766) | DRAFT | Return 400 for empty/missing, 403 for unlisted IP |

### Intent Class Summary

| Intent Class | FR Count | FR IDs |
|-------------|----------|--------|
| API_DESIGN | 5 | FR-06, FR-07, FR-14, FR-17, FR-20 |
| PROCESSING | 2 | FR-10, FR-19 |
| SECURITY | 5 | FR-04, FR-05, FR-08, FR-09, FR-22 |
| INTEGRATION | 2 | FR-02, FR-03 |
| DATA_MODEL | 1 | FR-01 |
| KNOWLEDGE | 1 | FR-11 |
| ESCALATION | 1 | FR-12 |
| OBSERVABILITY | 2 | FR-13, FR-16 |
| DEPLOYMENT | 2 | FR-15, FR-21 |
| CONVENTION | 1 | FR-18 |

## NFR Tracking

| NFR ID | Type | Requirement Summary | Status | Notes |
|--------|------|--------------------|--------|-------|
| NFR-01 | Performance | p95 end-to-end response latency < 3.0s for Layer 1 (rule-matched) queries under normal load | DRAFT | Measured via conversations.response_time_ms; k6 load test 200 VUs 10 min |
| NFR-02 | Security | All webhook endpoints reject invalid/missing signatures with 401 AUTH_INVALID_SIGNATURE before any business logic executes | DRAFT | Red team validation; timing-safe hmac.compare_digest required |
| NFR-03 | Security | Input sanitization L2 (NFKC normalization) applied to every inbound message before any downstream processing | DRAFT | NFKC must not alter ASCII alphanumerics; verified in pipeline order |
| NFR-04 | Security | PII masking: recall >= 95%, precision >= 99% for Taiwan phone/email/address in Phase 1 | DRAFT | Labeled PII test corpus; credit card + Luhn check deferred to Phase 2 |
| NFR-05 | Security | Rate limiter rejects excess requests with 429 within one token window; per-user buckets independent | DRAFT | Burst test: capacity + 1 requests → last gets 429; cross-user isolation verified |
| NFR-06 | Reliability | Health check returns within 500ms; accurately reports postgres+redis status; returns HTTP 200 even in degraded state | DRAFT | Three-state health: healthy/degraded/unhealthy; container kill tests |
| NFR-07 | Maintainability | All logs are single-line valid JSON parseable by jq; level filtering works via stdlib logging configuration | DRAFT | Required fields: timestamp, level, service, message; setLevel(WARNING) suppresses INFO |
| NFR-08 | Maintainability | ruff check zero violations; max cyclomatic complexity <= 10; all public functions have docstrings | DRAFT | CI lint gate; radon cc check; manual docstring review for public API surface |
| NFR-09 | Deployability | docker compose up brings all 3 services to healthy within 60s; docker compose down -v removes all volumes/networks | DRAFT | Fresh clone smoke test; no dangling resources after teardown |
| NFR-10 | Security | IP Whitelist must block unauthorized traffic (HTTP 403/400) before reaching the webhook signature validation layer | DRAFT | Unlisted IP -> 403; empty/missing IP -> 400 |

### NFR Type Coverage

| NFR Type | Count | NFR IDs |
|----------|-------|---------|
| Performance | 1 | NFR-01 |
| Security | 5 | NFR-02, NFR-03, NFR-04, NFR-05, NFR-10 |
| Reliability | 1 | NFR-06 |
| Maintainability | 2 | NFR-07, NFR-08 |
| Deployability | 1 | NFR-09 |

### FR-to-NFR Trace Matrix

| FR ID | NFR-01 (Perf) | NFR-02 (Sec) | NFR-03 (Sec) | NFR-04 (Sec) | NFR-05 (Sec) | NFR-06 (Rel) | NFR-07 (Maint) | NFR-08 (Maint) | NFR-09 (Deploy) | NFR-10 (Sec) |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| FR-01 | | | | | | | | X | | |
| FR-02 | X | | | | | | | | | |
| FR-03 | X | | | | | | | | | |
| FR-04 | | X | | | | | | | | |
| FR-05 | | X | | | | | | | | |
| FR-06 | | | | | | | | X | | |
| FR-07 | | | | | | | | X | | |
| FR-08 | | | X | | | | | | | |
| FR-09 | | | | X | | | | | | |
| FR-10 | X | | | | X | | | | | |
| FR-11 | X | | | | | | | | | |
| FR-12 | | | | | | X | | | | |
| FR-13 | | | | | | | X | | | |
| FR-14 | | | | | | X | | | | |
| FR-15 | | | | | | | | | X | |
| FR-16 | | | | | | | | X | | |
| FR-17 | | | | | | | | X | | |
| FR-18 | | | | | | | X | | | |
| FR-19 | X | | | | | X | | | | |
| FR-20 | | | | | | | | X | | |
| FR-21 | | | | | | X | X | | | |
| FR-22 | | | | | | | | | | X |

**NFR Coverage Rate**: 25 NFR associations / 22 FRs = 113% (≥ 50% threshold met)
