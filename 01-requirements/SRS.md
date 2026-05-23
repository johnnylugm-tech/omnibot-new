# SRS — OmniBot Phase 1

> Source SPEC: `SPEC.md` v7.0 (2026-05-21)
> Phase: 1 (MVP Foundation)
> Target: FCR >= 50%, p95 < 3.0s, 2 platforms (Telegram + LINE)

## 1. Requirements Overview

OmniBot Phase 1 (MVP Foundation) establishes the core multi-platform chatbot infrastructure. It delivers rule-based knowledge matching (Layer 1), basic PII de-identification, token-bucket rate limiting, structured JSON logging, and a Docker Compose development environment. The system supports Telegram and LINE platforms with webhook signature verification, unified message/responses formats, and a PostgreSQL schema that accommodates all future-phase columns to avoid ALTER TABLE later.

**Scope**: 14 dev modules + 2 cross-cutting concerns + 3 integration/operational FRs → 21 functional requirements.

---

## 2. Functional Requirements

| ID | Requirement Description | Implementation Function (est.) | Verification Method |
|----|------------------------|-------------------------------|--------------------|
| FR-01 | Create complete PostgreSQL schema with all core tables (`users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`) plus indexes (`idx_users_platform_uid`, `idx_conversations_started`, `idx_conversations_user`, `idx_conversations_platform`, `idx_messages_conversation`, `idx_messages_created`, `idx_kb_category`, `idx_kb_keywords`, `idx_kb_embeddings`, `idx_escalation_pending`, `idx_security_logs_date`) as defined in SPEC.md §Database Schema. Phase 2/3 columns (e.g. `embeddings`, `embedding_model`, `satisfaction_score`, `dst_state`) are included with defaults to avoid ALTER TABLE later. | `create_schema()` in migration `001_phase1_core.py` | `psql` schema inspection: all 8 tables + 11 indexes exist; `information_schema.columns` confirms Phase2/3 columns present with defaults |
| FR-02 | Accept Telegram Bot API webhook POST requests, parse the platform-specific payload, and produce an immutable `UnifiedMessage` dataclass instance per SPEC.md §Unified Message Format. Must extract `platform_user_id`, `message_type`, `content`, and populate `raw_payload` with the original request body. | `TelegramAdapter.parse_message(payload: dict) -> UnifiedMessage` | Unit test: valid Telegram JSON payload → correct `UnifiedMessage.platform == Platform.TELEGRAM` with all fields populated; invalid/missing fields → raises descriptive error |
| FR-03 | Accept LINE Messaging API webhook POST requests, parse the platform-specific payload, and produce an immutable `UnifiedMessage` dataclass instance. Must extract `reply_token` from LINE events. | `LineAdapter.parse_message(payload: dict) -> UnifiedMessage` | Unit test: valid LINE JSON payload → correct `UnifiedMessage` with `reply_token` populated; empty events array → handled gracefully |
| FR-04 | Verify Telegram webhook request authenticity using HMAC-SHA256 over the secret key derived from `bot_token`. Reject with `AUTH_INVALID_SIGNATURE` (401) if verification fails. Per SPEC.md §Webhook Signature Verification. | `TelegramWebhookVerifier.verify(body: bytes, signature: str) -> bool` | Unit test: valid (body, signature) pair → `True`; tampered body → `False`; missing signature header → `False`; uses `hmac.compare_digest` for timing safety |
| FR-05 | Verify LINE webhook request authenticity using HMAC-SHA256 over `channel_secret` with Base64-encoded digest comparison. Reject with `AUTH_INVALID_SIGNATURE` (401) if verification fails. Per SPEC.md §Webhook Signature Verification. | `LineWebhookVerifier.verify(body: bytes, signature: str) -> bool` | Unit test: valid (body, signature) pair → `True`; wrong secret → `False`; uses `hmac.compare_digest` for timing safety |
| FR-06 | Define and enforce the immutable `UnifiedMessage` dataclass with all required fields (`platform`, `platform_user_id`, `unified_user_id`, `message_type`, `content`, `raw_payload`, `received_at`, `reply_token`) supporting all `Platform` and `MessageType` enum values defined in SPEC.md §Unified Message Format. | `UnifiedMessage` dataclass, `Platform` enum, `MessageType` enum | Unit test: instantiation with valid args succeeds; mutation attempt raises `FrozenInstanceError`; `received_at` defaults to current UTC; all enum members present |
| FR-07 | Define the generic `ApiResponse[T]` and `PaginatedResponse[T]` dataclasses per SPEC.md §API Design — Unified Response Format. `ApiResponse` must carry `success`, `data`, `error`, `error_code`. `PaginatedResponse` must extend with `total`, `page`, `limit`, `has_next`. | `ApiResponse`, `PaginatedResponse` dataclasses | Unit test: `ApiResponse(success=True, data=obj)` serializes correctly; `PaginatedResponse` includes pagination fields; JSON round-trip preserves `has_next` boolean |
| FR-08 | Normalize all inbound message text using Unicode NFKC normalization, strip non-printable characters (except `\n` and `\t`), and trim whitespace. Per SPEC.md §Security Layer — Input Sanitizer L2. Must NOT perform pattern matching (reserved for Phase 2 L3). | `InputSanitizer.sanitize(text: str) -> str` | Unit test: fullwidth "ＴＥＳＴ" → "TEST"; control chars removed; newlines preserved; empty string → empty string; no regex pattern matching in implementation |
| FR-09 | Detect and mask PII patterns in message text: phone numbers (Taiwan formats `\d{4}-\d{3,4}-\d{3,4}` and `\d{10,11}`), email addresses, and Taiwan-formatted addresses (city/county + road/street/lane/alley/number). Replace matched text with `[<type>_masked]` placeholder. Return `PIIMaskResult` with `masked_text`, `mask_count`, and `pii_types`. Per SPEC.md §PII Masking L4 (Phase 1 subset, no credit card). | `PIIMasking.mask(text: str) -> PIIMaskResult` | Unit test: "call 0912-345-678" → "call [phone_masked]"; "email me at a@b.com" → "email me at [email_masked]"; "台北市信義路五段5號" → contains `[address_masked]`; clean text → `mask_count=0` |
| FR-10 | Enforce per-platform per-user rate limiting using the Token Bucket algorithm. Default capacity and refill rate of 100 tokens/second. Requests exceeding the limit receive HTTP 429 with `RATE_LIMIT_EXCEEDED` error code. Per SPEC.md §Rate Limiter. | `RateLimiter.check(platform: str, user_id: str) -> bool`, `TokenBucket.consume(tokens: int) -> bool` | Unit test: bucket with capacity=2, refill=1/s: 2 fast consumes → True, 3rd → False; wait 1s → True again; separate platform:user keys are independent |
| FR-11 | Query `knowledge_base` table for matching answers using SQL `ILIKE` on question text and `= ANY(keywords)` array match. Return a `KnowledgeResult` with `source="rule"`, confidence 0.95 for exact substring match or 0.7 for ILIKE match. Only active entries (`is_active=TRUE`), ordered by `version DESC`, limited to top 5. Per SPEC.md §Knowledge Layer — `_rule_match` / `_rule_match_list`. | `HybridKnowledgeV7._rule_match(query: str) -> Optional[KnowledgeResult]`, `_rule_match_list(query: str) -> list[KnowledgeResult]` | Unit test: exact keyword match → confidence >= 0.7; inactive entry → excluded; empty result → returns None or empty list; multi-keyword entry matches any keyword |
| FR-12 | When no rule match is found (Layer 1 returns None), create an escalation record in `escalation_queue` with `reason="no_rule_match"` or `"out_of_scope"`, priority=0 (normal), and return a `KnowledgeResult` with `source="escalate"`, `id=-1`, hardcoded handoff message. Phase 1 does NOT implement SLA tracking, priority levels, or agent assignment. Per SPEC.md §Escalation (Phase 1 basic). | `BasicEscalationManager.create(conversation_id: int, reason: str) -> int` | Unit test: escalation creates DB row with `priority=0`, `sla_deadline IS NULL`; returns `KnowledgeResult(id=-1, source="escalate")`; `conversations.scope_type` updated to `'out_of_scope'` when context has `conversation_id` |
| FR-13 | Emit all log entries as single-line JSON objects with fields: `timestamp` (ISO 8601 UTC), `level` (DEBUG/INFO/WARN/ERROR/CRITICAL), `service` (configurable, default "omnibot"), `message`, and arbitrary `**kwargs`. Use Python stdlib `logging` module as transport. Per SPEC.md §Observability — Structured Logger. | `StructuredLogger.log(level: str, message: str, **kwargs)`, `.info()`, `.error()`, `.warn()` | Unit test: captured log output is valid JSON; contains required fields; extra kwargs appear as top-level keys; level mapping correct (INFO→20, ERROR→40) |
| FR-14 | Expose `GET /api/v1/health` returning JSON `{"status": "healthy|degraded|unhealthy", "postgres": bool, "redis": bool, "uptime_seconds": float}`. Status is `"healthy"` when both postgres and redis are reachable, `"degraded"` when one is down, `"unhealthy"` when both are down. Per SPEC.md §API Design — Health Check Endpoint. | `health_check() -> dict` | Integration test: with live DB+Redis → `status=healthy`, both flags true; with DB down → `postgres=false`, `status=degraded`; uptime_seconds increases between calls; returns 200 even when degraded |
| FR-15 | Provide a `docker-compose.yml` with services: `omnibot-api` (build from ., port 8000, healthcheck via `/api/v1/health`, depends on postgres+redis with `condition: service_healthy`), `postgres` (pgvector/pgvector:pg16, healthcheck via `pg_isready`), and `redis` (redis:7-alpine, healthcheck via `redis-cli ping`). Per SPEC.md §Deployment — Docker Compose (Phase 1 subset: no otel/prometheus/grafana). | `docker-compose.yml` | `docker compose up -d && docker compose ps` — all 3 services show `healthy` within 60s; `curl localhost:8000/api/v1/health` returns 200 |
| FR-16 | Provide SQL query scripts for Phase 1 ODD metrics: (a) FCR rate calculation over 30-day window for `scope_type='in_scope'` conversations with non-null `first_contact_resolution`, (b) average and p95 response latency per platform over 30-day window, (c) knowledge source hit distribution (`rule` / `escalate`) for assistant messages over 7-day window. Per SPEC.md §ODD SQL — Phase 1. | ODD SQL script files (e.g. `queries/fcr.sql`, `queries/latency.sql`, `queries/knowledge_hits.sql`) | Manual execution: each query parses and runs without syntax error against schema; FCR query returns `fcr_rate_pct` between 0-100; latency query uses `PERCENTILE_CONT(0.95)` |
| FR-17 | Define and use standardized error codes for Phase 1: `AUTH_INVALID_SIGNATURE` (401), `RATE_LIMIT_EXCEEDED` (429), `KNOWLEDGE_NOT_FOUND` (404), `VALIDATION_ERROR` (422), `INTERNAL_ERROR` (500). Each error response must use the `ApiResponse` format with `success=False`, `error=<human message>`, `error_code=<code>`. Per SPEC.md §API Design — Error Codes. | Error code constants module, error response helper in `ApiResponse` | Unit test: each error code maps to correct HTTP status; `ApiResponse(success=False, error="...", error_code="AUTH_INVALID_SIGNATURE")` serializes with all fields; webhook endpoints return correct error codes on failure |
| FR-18 | All Phase 1 Python code must follow constitution §4 naming conventions: `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE` for constants; all public functions must have docstrings; function length ≤ 50 lines; cyclomatic complexity ≤ 10. Per SPEC.md §Code Conventions and constitution/CONSTITUTION.md §1.2, §4.1. | n/a (code convention, enforced by linter) | `ruff check` passes with zero violations; `radon cc -a` reports max CC ≤ 10; manual review: all `def` in `__init__.py` / public modules have docstrings |
| FR-19 | Implement the core message processing pipeline that orchestrates each inbound request end-to-end: (1) IP Whitelist interception → (2) webhook signature verification → (3) platform adapter parse → (4) rate limiter check → (5) input sanitization L2 → (6) PII masking L4 → (7) knowledge matching Layer 1 → (8) if no match, basic escalation → (9) construct `UnifiedResponse` → (10) send reply via platform adapter → (11) log completion via structured logger. Must handle errors at each stage without crashing the pipeline. | `PipelineOrchestrator.process(platform: Platform, raw_body: bytes, signature: str) -> UnifiedResponse` | Integration test: valid FAQ query flows through all 11 stages → correct UnifiedResponse returned; PII in request is masked in logs; invalid signature → 401 before any processing; rate limit exceeded → 429; no-rule-match → escalation created |
| FR-20 | Define the immutable `UnifiedResponse` dataclass representing the system reply with fields: `platform`, `user_id`, `content` (the text to send back), `source` (KnowledgeSource enum: `rule`/`escalate`), `confidence` (float 0-1), `metadata` (dict for backend-specific fields e.g. Telegram `parse_mode`). Per SPEC.md §Unified Message Format and Glossary. | `UnifiedResponse` dataclass, `KnowledgeSource` enum | Unit test: `UnifiedResponse(source=KnowledgeSource.RULE, confidence=0.95, content="answer")` serializes correctly; immutable (FrozenInstanceError on mutation); `metadata` defaults to empty dict |
| FR-21 | Load and manage configuration from environment variables and/or a `config.yaml` file: bot tokens (`TELEGRAM_BOT_TOKEN`, `LINE_CHANNEL_ACCESS_TOKEN`), channel secrets (`TELEGRAM_WEBHOOK_SECRET`, `LINE_CHANNEL_SECRET`), database connection (`DATABASE_URL`), Redis connection (`REDIS_URL`), rate limiter settings (`RATE_LIMIT_CAPACITY`, `RATE_LIMIT_REFILL_RATE`), and service name (`SERVICE_NAME`). Validate required config at startup; fail fast with a clear error message listing missing keys. | `Settings` pydantic model or dataclass with `ConfigLoader.from_env()` | Unit test: all env vars set → Settings created with correct values; missing `DATABASE_URL` → raises `ConfigError("Missing required config keys: DATABASE_URL")`; optional keys use defaults; config validation runs at import time |
| FR-22 | Implement IP Whitelist interception to filter out requests from unofficial IPs before computing HMAC signature. Unofficial IPs must be rejected with HTTP 403. | `IPWhitelist.is_allowed(ip: str) -> bool` | Unit test: allowed IP → proceeds; unlisted IP → 403 Forbidden; empty IP → 403 |

### FR Cross-Reference to SPEC.md

| FR | SPEC.md Source Section(s) | NFR Association |
|----|---------------------------|-----------------|
| FR-01 | Database Schema (lines 1772–2035) | NFR-08 (Maintainability) |
| FR-02 | Platform Adapter Layer (lines 104–108), Unified Message Format (lines 412–451) | NFR-01 (Performance) |
| FR-03 | Platform Adapter Layer (lines 104–108), Unified Message Format (lines 412–451) | NFR-01 (Performance) |
| FR-04 | Webhook Signature Verification (lines 457–515, TelegramVerifier) | NFR-02 (Security) |
| FR-05 | Webhook Signature Verification (lines 457–515, LineVerifier) | NFR-02 (Security) |
| FR-06 | Unified Message Format (lines 412–451) | NFR-08 (Maintainability) |
| FR-07 | API Design — Unified Response Format (lines 374–393) | NFR-08 (Maintainability) |
| FR-08 | Input Sanitizer L2 (lines 521–536) | NFR-03 (Security) |
| FR-09 | PII Masking L4 Phase 1 subset (lines 608–684) | NFR-04 (Security) |
| FR-10 | Rate Limiter Token Bucket (lines 688–730) | NFR-01 (Performance), NFR-05 (Security) |
| FR-11 | Knowledge Layer 1 — `_rule_match` (lines 935–959) | NFR-01 (Performance) |
| FR-12 | Escalation — Basic Handoff Phase 1 (lines 1195–1262, basic subset) | NFR-06 (Reliability) |
| FR-13 | Structured Logger (lines 1441–1490) | NFR-07 (Maintainability) |
| FR-14 | API Design — Health Check (lines 356–370) | NFR-06 (Reliability) |
| FR-15 | Deployment — Docker Compose (lines 2273–2334, Phase 1 subset) | NFR-09 (Deployability) |
| FR-16 | ODD SQL Phase 1 (lines 2069–2103) | NFR-08 (Maintainability) |
| FR-17 | API Design — Error Codes (lines 397–407, Phase 1 subset) | NFR-08 (Maintainability) |
| FR-18 | Code Conventions (lines 193–197), Constitution §1.2, §4.1 | NFR-07 (Maintainability) |
| FR-19 | System Architecture (lines 87–189), Pipeline flow | NFR-01 (Performance), NFR-06 (Reliability) |
| FR-20 | Unified Message Format (lines 412–451), Glossary | NFR-08 (Maintainability) |
| FR-21 | SPEC.md §Configuration (various: bot tokens, DB/Redis URLs, rate limiter settings) | NFR-07 (Maintainability), NFR-06 (Reliability) |

---

## 3. Non-Functional Requirements (NFR)

| ID | Type | Requirement | Test Method |
|----|------|-------------|-------------|
| NFR-01 | Performance | p95 end-to-end response latency (webhook receipt → reply sent) must be < 3.0 seconds under normal load for rule-matched (Layer 1) queries. Measured via `conversations.response_time_ms`. | k6 load test: 200 VUs, 10 min, FAQ query payload; `PERCENTILE_CONT(0.95)` on `response_time_ms` from ODD SQL |
| NFR-02 | Security | All webhook endpoints (`/api/v1/webhook/telegram`, `/api/v1/webhook/line`) must reject requests with invalid or missing signatures with HTTP 401 and `AUTH_INVALID_SIGNATURE` error code before any business logic executes. | Red team test: replay valid payload with tampered signature → 401; missing signature header → 401; timing-safe comparison verified via unit test |
| NFR-03 | Security | Input sanitization L2 must be applied to every inbound message before it reaches any downstream processing (knowledge matching, PII masking, logging). NFKC normalization must not alter ASCII alphanumerics. | Unit test: verify sanitizer is called in the message pipeline before `_rule_match`; NFKC produces expected output for fullwidth, combining chars |
| NFR-04 | Security | PII masking must detect and replace >= 95% of Taiwan phone numbers, email addresses, and Taiwan addresses in test corpus. False positive rate (masking non-PII text) must be < 1%. | Unit test with labeled PII corpus: recall ≥ 95%, precision ≥ 99% for Phase 1 PII types; `should_escalate` returns True for sensitive keyword matches |
| NFR-05 | Security | Rate limiter must reject excess requests with HTTP 429 within one token consumption window (1s at default 100 rps). Separate platform:user buckets must not interfere. | Unit test: burst of 101 requests → 100 pass, 1 gets 429; different users on same platform have independent limits |
| NFR-06 | Reliability | Health check endpoint must return within 500ms and accurately reflect live PostgreSQL and Redis connectivity. Must return HTTP 200 even in degraded state (one dependency down). | Integration test: healthy → 200 OK, `status=healthy`; kill postgres container → 200 OK, `postgres=false`, `status=degraded`; both down → `status=unhealthy` |
| NFR-07 | Maintainability | All log output must be valid single-line JSON objects parseable by `jq` and log aggregation tools. Log level filtering must work via standard Python logging configuration. | Log inspection test: capture stdout → each line is valid JSON with required fields; `logging.getLogger("omnibot").setLevel(WARNING)` suppresses INFO lines |
| NFR-08 | Maintainability | All Phase 1 Python source files must pass `ruff check` with zero violations, function cyclomatic complexity ≤ 10 (`radon cc`), and all public functions/classes must have docstrings. | CI lint gate: `ruff check .` → exit 0; `radon cc -a app/` → max ≤ 10 |
| NFR-09 | Deployability | `docker compose up -d` must bring all 3 services (api, postgres, redis) to `healthy` state within 60 seconds on a clean checkout. `docker compose down -v` must remove all volumes and networks. | Deployment smoke test: fresh clone → `docker compose up -d` → `docker compose ps` shows healthy within 60s → `curl /api/v1/health` returns 200 → `docker compose down -v` leaves no dangling resources |
| NFR-10 | Security | IP Whitelist must block unauthorized traffic (HTTP 403) before reaching the webhook signature validation layer to prevent DDoS via expensive HMAC calculations. | Red team test: Unlisted IP -> 403; Listed IP -> 401 (if signature missing/wrong) or 200 |

---

## 4. Constraints

- **Runtime**: Python 3.9+, PostgreSQL 16 (pgvector), Redis 7
- **Platform scope Phase 1**: Telegram + LINE only (Messenger + WhatsApp deferred to Phase 2)
- **Schema completeness**: All core tables created in Phase 1; Phase 2/3 columns (e.g. `embeddings vector(384)`, `satisfaction_score`, `dst_state JSONB`) included with defaults — no ALTER TABLE in later phases per SPEC.md design principle
- **Knowledge Layer**: Phase 1 implements Layer 1 (rule matching) only; Layer 2 (RAG), Layer 3 (LLM), Layer 4 (SLA escalation) are Phase 2+
- **PII scope**: Phase 1 masks phone/email/address (Taiwan formats); credit card + Luhn check is Phase 2
- **Security**: No Phase 2 L3 Prompt Injection Defense in Phase 1; input sanitization is character-level only (L2)
- **Escalation**: No SLA tracking, priority levels, or agent assignment in Phase 1
- **Observability**: Structured logging only; Prometheus metrics, OpenTelemetry tracing, Grafana are Phase 2/3
- **Deployment**: Docker Compose single-node development environment; Kubernetes, load balancing, backup are Phase 3
- **i18n**: zh-TW only in Phase 1; multi-language PII patterns are Phase 3

---

## 5. Glossary

| Term | Definition |
|------|------------|
| **FCR** | First Contact Resolution — percentage of user queries resolved in the first interaction without escalation or follow-up |
| **DST** | Dialogue State Tracking — conversation state machine tracking intents, slots, and dialog turns (Phase 2) |
| **RAG** | Retrieval-Augmented Generation — semantic search over vector embeddings to find relevant knowledge (Phase 2) |
| **RRF** | Reciprocal Rank Fusion — algorithm that merges ranked result lists from multiple retrieval methods; k=60 (Phase 2) |
| **PII** | Personally Identifiable Information — data that can identify an individual (phone, email, address, credit card) |
| **RBAC** | Role-Based Access Control — permission system mapping roles to resource:action pairs (Phase 3) |
| **SLA** | Service Level Agreement — contracted response time targets for escalation handling (Phase 2 primary, Phase 3 full) |
| **ODD** | Operational Data Dashboard — SQL queries for KPI monitoring (FCR, latency, cost, etc.) |
| **CSAT** | Customer Satisfaction Score — aggregated user satisfaction metric (Phase 2+ measurement, Phase 3 target) |
| **NFKC** | Unicode Normalization Form KC — compatibility decomposition + canonical composition; normalizes fullwidth to ASCII |
| **Token Bucket** | Rate limiting algorithm: fixed-capacity bucket refilled at constant rate; tokens consumed per request |
| **L2/L3/L4/L5** | Security layer numbering: L2=Input Sanitization, L3=Prompt Injection Defense, L4=PII Masking, L5=Grounding Checks |
| **UnifiedMessage** | Immutable dataclass representing a cross-platform normalized inbound message |
| **UnifiedResponse** | Immutable dataclass representing a system reply with knowledge source and confidence metadata |
| **ApiResponse** | Generic API response wrapper with `success`, `data`, `error`, `error_code` fields |

---

## 6. Cross-Cutting Test Requirements

### API Completeness

Each webhook endpoint must have these four test categories:

- [ ] `test_webhook_telegram_valid_payload_returns_200` — valid signed payload → 200 OK
- [ ] `test_webhook_telegram_invalid_signature_returns_401` — tampered signature → 401
- [ ] `test_webhook_telegram_rate_limit_exceeded_returns_429` — burst > 100 → 429
- [ ] `test_webhook_telegram_malformed_body_returns_422` — invalid JSON → 422
- [ ] `test_webhook_line_valid_payload_returns_200` — valid signed payload → 200 OK
- [ ] `test_webhook_line_invalid_signature_returns_401` — tampered signature → 401
- [ ] `test_webhook_line_rate_limit_exceeded_returns_429` — burst > 100 → 429
- [ ] `test_webhook_line_malformed_body_returns_422` — invalid JSON → 422
- [ ] `test_health_endpoint_all_services_up_returns_200` — DB+Redis healthy → 200, status=healthy
- [ ] `test_health_endpoint_db_down_returns_200_degraded` — DB unreachable → 200, status=degraded
- [ ] `test_health_endpoint_redis_down_returns_200_degraded` — Redis unreachable → 200, status=degraded

### Security Red Team

- [ ] `test_redteam_ip_whitelist_blocks_unknown_ip` — request from non-whitelisted IP → 403 Forbidden before signature check
- [ ] `test_redteam_webhook_signature_replay_attack_blocked` — replayed valid signature with modified body → 401
- [ ] `test_redteam_webhook_timing_attack_signature_enumeration_resistant` — timing difference between valid/invalid signature < 5ms (hmac.compare_digest)
- [ ] `test_redteam_rate_limit_burst_attack_blocked` — 1000 requests in 1s → at least 900 get 429
- [ ] `test_redteam_pii_phone_leak_masked` — message with embedded 0912-345-678 → response/DB contains `[phone_masked]` not raw number
- [ ] `test_redteam_pii_email_leak_masked` — message with user@example.com → masked
- [ ] `test_redteam_pii_address_leak_masked` — message with 台北市信義路五段5號 → masked
- [ ] `test_redteam_input_sanitization_null_byte_removed` — `\x00` in input → stripped
- [ ] `test_redteam_input_sanitization_unicode_confusion_normalized` — fullwidth payload → NFKC normalized

### KPI Gates

- [ ] `test_kpi_p95_latency_phase1_under_3s` — k6 load test: 200 VUs, FAQ queries only, p95 < 3000ms
- [ ] `test_kpi_fcr_phase1_target_50_percent` — ODD FCR SQL returns >= 50% for in_scope conversations (post 100+ test conversations)

### Deployment Smoke

- [ ] `test_deploy_docker_compose_all_services_healthy` — `docker compose up -d` → all 3 services healthy within 60s
- [ ] `test_deploy_health_endpoint_returns_200_after_startup` — `curl -f http://localhost:8000/api/v1/health` → 200, JSON with expected schema
- [ ] `test_deploy_docker_compose_down_cleans_up` — `docker compose down -v` → no containers, networks, or volumes remain

---

## 7. FR Block (machine-readable)

<!-- FR:START -->
```json
{
  "version": "1.0",
  "created_at": "2026-05-23",
  "phase": 1,
  "project": "omnibot",
  "functional_requirements": [
    {
      "id": "FR-01",
      "description": "Create complete PostgreSQL schema with all core tables and indexes; Phase 2/3 columns included with defaults",
      "implementation_functions": ["create_schema"],
      "verification_method": "psql schema inspection: 8 tables + 11 indexes; Phase 2/3 columns present with defaults"
    },
    {
      "id": "FR-02",
      "description": "Accept Telegram webhook POST, parse into UnifiedMessage",
      "implementation_functions": ["TelegramAdapter.parse_message"],
      "verification_method": "Unit test: valid Telegram JSON -> correct UnifiedMessage; invalid -> raises error"
    },
    {
      "id": "FR-03",
      "description": "Accept LINE webhook POST, parse into UnifiedMessage with reply_token",
      "implementation_functions": ["LineAdapter.parse_message"],
      "verification_method": "Unit test: valid LINE JSON -> UnifiedMessage with reply_token; empty events -> handled"
    },
    {
      "id": "FR-04",
      "description": "Verify Telegram webhook signature via HMAC-SHA256; reject invalid with 401",
      "implementation_functions": ["TelegramWebhookVerifier.verify"],
      "verification_method": "Unit test: valid pair -> True; tampered body -> False; uses hmac.compare_digest"
    },
    {
      "id": "FR-05",
      "description": "Verify LINE webhook signature via HMAC-SHA256 with Base64 digest; reject invalid with 401",
      "implementation_functions": ["LineWebhookVerifier.verify"],
      "verification_method": "Unit test: valid pair -> True; wrong secret -> False; uses hmac.compare_digest"
    },
    {
      "id": "FR-06",
      "description": "Define immutable UnifiedMessage dataclass with Platform/MessageType enums",
      "implementation_functions": ["UnifiedMessage", "Platform", "MessageType"],
      "verification_method": "Unit test: instantiation succeeds; mutation raises FrozenInstanceError; all enum members present"
    },
    {
      "id": "FR-07",
      "description": "Define generic ApiResponse[T] and PaginatedResponse[T] dataclasses",
      "implementation_functions": ["ApiResponse", "PaginatedResponse"],
      "verification_method": "Unit test: serialization, pagination fields, JSON round-trip"
    },
    {
      "id": "FR-08",
      "description": "Normalize input text via NFKC; remove non-printable chars except newline/tab; trim",
      "implementation_functions": ["InputSanitizer.sanitize"],
      "verification_method": "Unit test: fullwidth -> ASCII; control chars removed; newlines preserved; no pattern matching"
    },
    {
      "id": "FR-09",
      "description": "Detect and mask PII: Taiwan phone, email, Taiwan address; return PIIMaskResult",
      "implementation_functions": ["PIIMasking.mask"],
      "verification_method": "Unit test: labeled PII corpus -> recall >= 95%; clean text -> mask_count=0"
    },
    {
      "id": "FR-10",
      "description": "Enforce per-platform per-user rate limiting via Token Bucket (100 rps default); reject excess with 429",
      "implementation_functions": ["RateLimiter.check", "TokenBucket.consume"],
      "verification_method": "Unit test: burst test with capacity=2; separate keys independent; refill over time"
    },
    {
      "id": "FR-11",
      "description": "Query knowledge_base via ILIKE + keywords array match; return KnowledgeResult with source=rule",
      "implementation_functions": ["HybridKnowledgeV7._rule_match", "HybridKnowledgeV7._rule_match_list"],
      "verification_method": "Unit test: keyword match -> confidence >= 0.7; inactive excluded; empty -> None"
    },
    {
      "id": "FR-12",
      "description": "Create escalation record when no rule match; return handoff KnowledgeResult (no SLA)",
      "implementation_functions": ["BasicEscalationManager.create"],
      "verification_method": "Unit test: escalation row created with priority=0, no SLA deadline; id=-1, source=escalate"
    },
    {
      "id": "FR-13",
      "description": "Emit single-line JSON log entries with timestamp, level, service, message, and extra kwargs",
      "implementation_functions": ["StructuredLogger.log", "StructuredLogger.info", "StructuredLogger.error", "StructuredLogger.warn"],
      "verification_method": "Unit test: captured output is valid JSON; required fields present; extra kwargs as top-level keys"
    },
    {
      "id": "FR-14",
      "description": "Expose GET /api/v1/health returning postgres + redis status + uptime; degrade gracefully",
      "implementation_functions": ["health_check"],
      "verification_method": "Integration test: healthy/degraded/unhealthy statuses; 200 even when degraded; uptime increases"
    },
    {
      "id": "FR-15",
      "description": "Provide docker-compose.yml with omnibot-api, postgres (pgvector), redis; all with healthchecks",
      "implementation_functions": ["docker-compose.yml"],
      "verification_method": "Smoke test: docker compose up -> 3 services healthy within 60s; health endpoint returns 200"
    },
    {
      "id": "FR-16",
      "description": "Provide Phase 1 ODD SQL queries: FCR rate, p95 latency per platform, knowledge source distribution",
      "implementation_functions": ["queries/fcr.sql", "queries/latency.sql", "queries/knowledge_hits.sql"],
      "verification_method": "Manual execution: SQL parses without error; FCR returns percentage; latency uses PERCENTILE_CONT"
    },
    {
      "id": "FR-17",
      "description": "Use standardized error codes (AUTH_INVALID_SIGNATURE 401, RATE_LIMIT_EXCEEDED 429, etc.) in ApiResponse format",
      "implementation_functions": ["error_codes module", "ApiResponse error constructor"],
      "verification_method": "Unit test: code->status mapping correct; error responses include success=False + error_code"
    },
    {
      "id": "FR-18",
      "description": "Follow Python naming conventions (snake_case, PascalCase, UPPER_SNAKE) with docstrings; max function length 50; CC <= 10",
      "implementation_functions": ["n/a (lint-enforced)"],
      "verification_method": "ruff check -> 0 violations; radon cc -> max <= 10; manual review for docstrings"
    },
    {
      "id": "FR-19",
      "description": "Implement core message processing pipeline orchestrating IP Whitelist → webhook verify → parse → rate limit → sanitize → PII mask → knowledge match → escalate → respond → log",
      "implementation_functions": ["PipelineOrchestrator.process"],
      "verification_method": "Integration test: full pipeline flow; PII masked in logs; invalid signature -> 401"
    },
    {
      "id": "FR-20",
      "description": "Define immutable UnifiedResponse dataclass with platform, user_id, content, source, confidence, metadata",
      "implementation_functions": ["UnifiedResponse", "KnowledgeSource"],
      "verification_method": "Unit test: serialization; immutability; metadata defaults to empty dict"
    },
    {
      "id": "FR-21",
      "description": "Load and validate configuration from env vars: bot tokens, channel secrets, DB/Redis URLs, rate limiter settings; fail fast on missing keys",
      "implementation_functions": ["Settings", "ConfigLoader.from_env"],
      "verification_method": "Unit test: all vars set -> correct Settings; missing critical key -> ConfigError"
    },
    {
      "id": "FR-22",
      "description": "Implement IP Whitelist interception to filter out requests from unofficial IPs before computing HMAC signature. Unofficial IPs must be rejected with HTTP 403.",
      "implementation_functions": ["IPWhitelist.is_allowed"],
      "verification_method": "Unit test: allowed IP -> proceeds; unlisted IP -> 403 Forbidden; empty IP -> 403"
    }
  ],
  "non_functional_requirements": [
    {
      "id": "NFR-01",
      "type": "performance",
      "description": "p95 end-to-end response latency < 3.0s for Layer 1 (rule-matched) queries under normal load",
      "test_method": "k6 load test 200 VUs 10 min; PERCENTILE_CONT(0.95) on response_time_ms"
    },
    {
      "id": "NFR-02",
      "type": "security",
      "description": "All webhook endpoints reject invalid/missing signatures with 401 before business logic",
      "test_method": "Red team: tampered signature -> 401; missing signature -> 401; hmac.compare_digest verified"
    },
    {
      "id": "NFR-03",
      "type": "security",
      "description": "Input sanitization L2 (NFKC) applied to every inbound message before downstream processing",
      "test_method": "Unit test: sanitizer called in pipeline; NFKC fullwidth/combining chars produce expected output"
    },
    {
      "id": "NFR-04",
      "type": "security",
      "description": "PII masking: recall >= 95%, precision >= 99% for Taiwan phone/email/address in Phase 1",
      "test_method": "Unit test with labeled PII corpus"
    },
    {
      "id": "NFR-05",
      "type": "security",
      "description": "Rate limiter: excess requests get 429 within one token window; independent per-user buckets",
      "test_method": "Unit test: burst 101 -> 100 pass 1 fail; different users have independent limits"
    },
    {
      "id": "NFR-06",
      "type": "reliability",
      "description": "Health check returns within 500ms; accurately reports postgres+redis status; 200 even when degraded",
      "test_method": "Integration test: healthy/degraded/unhealthy verification; kill containers -> status changes"
    },
    {
      "id": "NFR-07",
      "type": "maintainability",
      "description": "All logs are single-line valid JSON with required fields; level filtering works via stdlib logging config",
      "test_method": "Log inspection: each line parseable by jq; setLevel(WARNING) suppresses INFO"
    },
    {
      "id": "NFR-08",
      "type": "maintainability",
      "description": "ruff check zero violations; max cyclomatic complexity <= 10; all public functions have docstrings",
      "test_method": "CI lint gate: ruff exit 0; radon cc max <= 10"
    },
    {
      "id": "NFR-09",
      "type": "deployability",
      "description": "docker compose up brings all 3 services to healthy within 60s; docker compose down -v cleans up fully",
      "test_method": "Deployment smoke: fresh clone -> up -> healthy in 60s -> curl health 200 -> down -v clean"
    },
    {
      "id": "NFR-10",
      "type": "security",
      "description": "IP Whitelist must block unauthorized traffic (HTTP 403) before reaching the webhook signature validation layer to prevent DDoS via expensive HMAC calculations",
      "test_method": "Red team test: Unlisted IP -> 403; Listed IP -> 401 (if signature missing/wrong) or 200"
    }
  ]
}
```
<!-- FR:END -->
