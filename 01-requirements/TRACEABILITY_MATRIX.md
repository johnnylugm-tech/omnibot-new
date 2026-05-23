# TRACEABILITY MATRIX — OmniBot Phase 1

> Source SRS: `01-requirements/SRS.md` (v1.0, 2026-05-23)
> Source SPEC: `SPEC.md` v7.0 (2026-05-21)
> Phase: 1 (MVP Foundation)
> Total FRs: 21 | Total NFRs: 9

---

## FR <-> SRS Mapping

| FR ID | Functional Requirement | SRS Section (§2) | Intent Class | Priority | Status |
|-------|-----------------------|-------------------|-------------|----------|--------|
| FR-01 | PostgreSQL schema: 8 tables + 11 indexes; Phase 2/3 columns with defaults | Database Schema (SPEC lines 1772–2035) | DATA_MODEL | P0 | DRAFT |
| FR-02 | Telegram webhook POST → `UnifiedMessage` parsing | Platform Adapter Layer, Unified Message Format (SPEC lines 412–451) | INTEGRATION | P0 | DRAFT |
| FR-03 | LINE webhook POST → `UnifiedMessage` parsing with `reply_token` | Platform Adapter Layer, Unified Message Format (SPEC lines 412–451) | INTEGRATION | P0 | DRAFT |
| FR-04 | Telegram webhook HMAC-SHA256 signature verification → 401 on failure | Webhook Signature Verification (SPEC lines 457–515) | SECURITY | P0 | DRAFT |
| FR-05 | LINE webhook HMAC-SHA256 Base64 signature verification → 401 on failure | Webhook Signature Verification (SPEC lines 457–515) | SECURITY | P0 | DRAFT |
| FR-06 | `UnifiedMessage` dataclass with `Platform`/`MessageType` enums | Unified Message Format (SPEC lines 412–451) | API_DESIGN | P0 | DRAFT |
| FR-07 | Generic `ApiResponse[T]` and `PaginatedResponse[T]` dataclasses | API Design — Unified Response Format (SPEC lines 374–393) | API_DESIGN | P0 | DRAFT |
| FR-08 | Input sanitization L2: NFKC + strip non-printable + trim | Security Layer — Input Sanitizer L2 (SPEC lines 521–536) | SECURITY | P0 | DRAFT |
| FR-09 | PII masking: Taiwan phone, email, address; `PIIMaskResult` return | PII Masking L4 Phase 1 subset (SPEC lines 608–684) | SECURITY | P0 | DRAFT |
| FR-10 | Token Bucket rate limiter; reject excess with 429 | Rate Limiter (SPEC lines 688–730) | PROCESSING | P0 | DRAFT |
| FR-11 | Knowledge base ILIKE + keyword array match; `KnowledgeResult` with source="rule" | Knowledge Layer 1 — `_rule_match` (SPEC lines 935–959) | KNOWLEDGE | P0 | DRAFT |
| FR-12 | Basic escalation: create record when no rule match; no SLA/priority/assignment | Escalation — Basic Handoff Phase 1 (SPEC lines 1195–1262) | ESCALATION | P1 | DRAFT |
| FR-13 | Structured JSON logging: timestamp, level, service, message, kwargs | Structured Logger (SPEC lines 1441–1490) | OBSERVABILITY | P1 | DRAFT |
| FR-14 | `GET /api/v1/health` with postgres/redis/uptime; three-state health | API Design — Health Check (SPEC lines 356–370) | API_DESIGN | P0 | DRAFT |
| FR-15 | `docker-compose.yml`: 3 services with healthchecks | Deployment — Docker Compose Phase 1 (SPEC lines 2273–2334) | DEPLOYMENT | P1 | DRAFT |
| FR-16 | ODD SQL scripts: FCR (30d), p95 latency (30d), knowledge hits (7d) | ODD SQL Phase 1 (SPEC lines 2069–2103) | OBSERVABILITY | P1 | DRAFT |
| FR-17 | Standardized error codes: `AUTH_INVALID_SIGNATURE` (401), `RATE_LIMIT_EXCEEDED` (429), `KNOWLEDGE_NOT_FOUND` (404), `VALIDATION_ERROR` (422), `INTERNAL_ERROR` (500) | API Design — Error Codes (SPEC lines 397–407) | API_DESIGN | P0 | DRAFT |
| FR-18 | Python conventions: snake_case, PascalCase, UPPER_SNAKE; docstrings; max CC ≤ 10 | Code Conventions (SPEC lines 193–197), Constitution §1.2, §4.1 | CONVENTION | P1 | DRAFT |
| FR-19 | Core pipeline: verify → rate limit → parse → sanitize → PII mask → knowledge → escalate → respond → log | System Architecture (SPEC lines 87–189) | PROCESSING | P0 | DRAFT |
| FR-20 | `UnifiedResponse` dataclass with platform, user_id, content, source, confidence, metadata | Unified Message Format (SPEC lines 412–451), Glossary | API_DESIGN | P0 | DRAFT |
| FR-21 | Config loader from env vars; fail fast on missing required keys | Configuration (bot tokens, DB/Redis URLs, rate limiter) | DEPLOYMENT | P0 | DRAFT |

### Priority Legend
- **P0**: Must-have for MVP — foundational infrastructure, security, core pipeline, platform I/O
- **P1**: Important but verifiable after core — escalation handoff, deployment, ODD, code conventions

---

## SRS <-> Code Mapping

| SRS Section (FR) | Expected Code File | Expected Function/Class | Target Lines (est.) | Status |
|------------------|--------------------|------------------------|---------------------|--------|
| FR-01 | `db/migrations/001_phase1_core.py` | `create_schema()` | ~120 | Not Started |
| FR-02 | `app/adapters/telegram_adapter.py` | `TelegramAdapter.parse_message(payload: dict) -> UnifiedMessage` | ~60 | Not Started |
| FR-03 | `app/adapters/line_adapter.py` | `LineAdapter.parse_message(payload: dict) -> UnifiedMessage` | ~60 | Not Started |
| FR-04 | `app/security/telegram_webhook_verifier.py` | `TelegramWebhookVerifier.verify(body: bytes, signature: str) -> bool` | ~30 | Not Started |
| FR-05 | `app/security/line_webhook_verifier.py` | `LineWebhookVerifier.verify(body: bytes, signature: str) -> bool` | ~30 | Not Started |
| FR-06 | `app/models/unified_message.py` | `UnifiedMessage` dataclass, `Platform` enum, `MessageType` enum | ~50 | Not Started |
| FR-07 | `app/models/api_response.py` | `ApiResponse[T]` dataclass, `PaginatedResponse[T]` dataclass | ~40 | Not Started |
| FR-08 | `app/security/input_sanitizer.py` | `InputSanitizer.sanitize(text: str) -> str` | ~25 | Not Started |
| FR-09 | `app/security/pii_masking.py` | `PIIMasking.mask(text: str) -> PIIMaskResult`, `PIIMaskResult` dataclass | ~80 | Not Started |
| FR-10 | `app/security/rate_limiter.py` | `RateLimiter.check(platform: str, user_id: str) -> bool`, `TokenBucket.consume(tokens: int) -> bool` | ~50 | Not Started |
| FR-11 | `app/knowledge/hybrid_knowledge_v7.py` | `HybridKnowledgeV7._rule_match(query: str) -> Optional[KnowledgeResult]`, `_rule_match_list(query: str) -> list[KnowledgeResult]` | ~60 | Not Started |
| FR-12 | `app/escalation/basic_escalation_manager.py` | `BasicEscalationManager.create(conversation_id: int, reason: str) -> int` | ~40 | Not Started |
| FR-13 | `app/observability/structured_logger.py` | `StructuredLogger.log(level: str, message: str, **kwargs)`, `.info()`, `.error()`, `.warn()` | ~50 | Not Started |
| FR-14 | `app/api/health.py` | `health_check() -> dict` | ~35 | Not Started |
| FR-15 | `docker-compose.yml` | (infrastructure file — 3 services: api, postgres, redis) | ~80 | Not Started |
| FR-16 | `queries/fcr.sql`, `queries/latency.sql`, `queries/knowledge_hits.sql` | (SQL scripts — no Python function) | ~60 | Not Started |
| FR-17 | `app/models/error_codes.py` | Error code constants, `ApiResponse` error constructor helper | ~30 | Not Started |
| FR-18 | (lint-enforced — no dedicated code file) | n/a (enforced via `ruff check` + `radon cc`) | n/a | Not Started |
| FR-19 | `app/pipeline/orchestrator.py` | `PipelineOrchestrator.process(platform: Platform, raw_body: bytes, signature: str) -> UnifiedResponse` | ~80 | Not Started |
| FR-20 | `app/models/unified_response.py` | `UnifiedResponse` dataclass, `KnowledgeSource` enum | ~30 | Not Started |
| FR-21 | `app/config/settings.py` | `Settings` model, `ConfigLoader.from_env()` | ~40 | Not Started |

---

## Code <-> Test Mapping

### Unit Test Mapping

| Source Code File | Expected Test File | Coverage Target | Status |
|-----------------|--------------------|-----------------|--------|
| `db/migrations/001_phase1_core.py` | `tests/db/test_migrations.py` | Schema validation: 8 tables + 11 indexes + Phase 2/3 columns | Not Started |
| `app/adapters/telegram_adapter.py` | `tests/adapters/test_telegram_adapter.py` | Telegram payload parsing (valid + invalid) | Not Started |
| `app/adapters/line_adapter.py` | `tests/adapters/test_line_adapter.py` | LINE payload parsing (valid + invalid + empty events) | Not Started |
| `app/security/telegram_webhook_verifier.py` | `tests/security/test_telegram_webhook_verifier.py` | Signature verification (valid, tampered, missing, timing-safe) | Not Started |
| `app/security/line_webhook_verifier.py` | `tests/security/test_line_webhook_verifier.py` | Signature verification (valid, wrong secret, timing-safe) | Not Started |
| `app/models/unified_message.py` | `tests/models/test_unified_message.py` | Dataclass: instantiation, immutability, defaults, enum members | Not Started |
| `app/models/api_response.py` | `tests/models/test_api_response.py` | Serialization, pagination fields, JSON round-trip | Not Started |
| `app/security/input_sanitizer.py` | `tests/security/test_input_sanitizer.py` | NFKC, control char removal, whitespace trim, newline/tab preservation | Not Started |
| `app/security/pii_masking.py` | `tests/security/test_pii_masking.py` | Labeled PII corpus: recall ≥ 95%, precision ≥ 99%; `should_escalate` | Not Started |
| `app/security/rate_limiter.py` | `tests/security/test_rate_limiter.py` | Token bucket burst/refill; per-user isolation; capacity limits | Not Started |
| `app/knowledge/hybrid_knowledge_v7.py` | `tests/knowledge/test_hybrid_knowledge_v7.py` | Keyword match, ILIKE match, inactive exclusion, empty results | Not Started |
| `app/escalation/basic_escalation_manager.py` | `tests/escalation/test_basic_escalation_manager.py` | Escalation row creation, priority=0, no SLA deadline, id=-1 | Not Started |
| `app/observability/structured_logger.py` | `tests/observability/test_structured_logger.py` | JSON validity, required fields, extra kwargs, level filtering | Not Started |
| `app/api/health.py` | `tests/api/test_health.py` | Healthy/degraded/unhealthy; 200 in all states; uptime increases | Not Started |
| `docker-compose.yml` | `tests/deployment/test_docker_compose.py` | `docker compose up` healthy within 60s; `down -v` cleanup | Not Started |
| `queries/fcr.sql`, `queries/latency.sql`, `queries/knowledge_hits.sql` | `tests/queries/test_odd_queries.py` | SQL parseable; FCR returns percentage; PERCENTILE_CONT for p95 | Not Started |
| `app/models/error_codes.py` | `tests/models/test_error_codes.py` | Error code → HTTP status mapping; `ApiResponse` error serialization | Not Started |
| (lint-enforced — FR-18) | CI lint gate | `ruff check` exit 0; `radon cc` max ≤ 10; docstring coverage | Not Started |
| `app/pipeline/orchestrator.py` | `tests/pipeline/test_pipeline_orchestrator.py` | Full 10-stage pipeline flow; error handling per stage; PII masked in logs | Not Started |
| `app/models/unified_response.py` | `tests/models/test_unified_response.py` | Dataclass: serialization, immutability, metadata defaults | Not Started |
| `app/config/settings.py` | `tests/config/test_settings.py` | Env var loading, missing key → ConfigError, optional key defaults | Not Started |

### Cross-Cutting Test Requirements (SRS §6)

| Test Category | Test Cases | Mapped Source Files | Target Coverage | Status |
|--------------|------------|---------------------|-----------------|--------|
| **API Completeness** | `test_webhook_telegram_valid_payload_returns_200` | FR-02, FR-04, FR-19 | `app/adapters/`, `app/security/`, `app/pipeline/` | Not Started |
| | `test_webhook_telegram_invalid_signature_returns_401` | FR-04 | `app/security/telegram_webhook_verifier.py` | Not Started |
| | `test_webhook_telegram_rate_limit_exceeded_returns_429` | FR-10 | `app/security/rate_limiter.py` | Not Started |
| | `test_webhook_telegram_malformed_body_returns_422` | FR-02, FR-17 | `app/adapters/telegram_adapter.py`, `app/models/error_codes.py` | Not Started |
| | `test_webhook_line_valid_payload_returns_200` | FR-03, FR-05, FR-19 | `app/adapters/`, `app/security/`, `app/pipeline/` | Not Started |
| | `test_webhook_line_invalid_signature_returns_401` | FR-05 | `app/security/line_webhook_verifier.py` | Not Started |
| | `test_webhook_line_rate_limit_exceeded_returns_429` | FR-10 | `app/security/rate_limiter.py` | Not Started |
| | `test_webhook_line_malformed_body_returns_422` | FR-03, FR-17 | `app/adapters/line_adapter.py`, `app/models/error_codes.py` | Not Started |
| | `test_health_endpoint_all_services_up_returns_200` | FR-14 | `app/api/health.py` | Not Started |
| | `test_health_endpoint_db_down_returns_200_degraded` | FR-14 | `app/api/health.py` | Not Started |
| | `test_health_endpoint_redis_down_returns_200_degraded` | FR-14 | `app/api/health.py` | Not Started |
| **Security Red Team** | `test_redteam_webhook_signature_replay_attack_blocked` | FR-04, FR-05 | `app/security/telegram_webhook_verifier.py`, `app/security/line_webhook_verifier.py` | Not Started |
| | `test_redteam_webhook_timing_attack_signature_enumeration_resistant` | FR-04, FR-05 | `app/security/telegram_webhook_verifier.py`, `app/security/line_webhook_verifier.py` | Not Started |
| | `test_redteam_rate_limit_burst_attack_blocked` | FR-10 | `app/security/rate_limiter.py` | Not Started |
| | `test_redteam_pii_phone_leak_masked` | FR-09 | `app/security/pii_masking.py` | Not Started |
| | `test_redteam_pii_email_leak_masked` | FR-09 | `app/security/pii_masking.py` | Not Started |
| | `test_redteam_pii_address_leak_masked` | FR-09 | `app/security/pii_masking.py` | Not Started |
| | `test_redteam_input_sanitization_null_byte_removed` | FR-08 | `app/security/input_sanitizer.py` | Not Started |
| | `test_redteam_input_sanitization_unicode_confusion_normalized` | FR-08 | `app/security/input_sanitizer.py` | Not Started |
| **KPI Gates** | `test_kpi_p95_latency_phase1_under_3s` | FR-19, NFR-01 | `app/pipeline/orchestrator.py` | Not Started |
| | `test_kpi_fcr_phase1_target_50_percent` | FR-16, FR-11, FR-12 | `app/knowledge/`, `app/escalation/`, `queries/fcr.sql` | Not Started |
| **Deployment Smoke** | `test_deploy_docker_compose_all_services_healthy` | FR-15 | `docker-compose.yml` | Not Started |
| | `test_deploy_health_endpoint_returns_200_after_startup` | FR-14, FR-15 | `app/api/health.py`, `docker-compose.yml` | Not Started |
| | `test_deploy_docker_compose_down_cleans_up` | FR-15 | `docker-compose.yml` | Not Started |

---

## Completeness Verification

### Coverage Metrics

| Trace Link | Actual | Target | Status |
|-----------|--------|--------|--------|
| FR → SRS | 21/21 = **100%** | 100% | MET |
| SRS → Code | 21/21 = **100%** (FR-18 lint-enforced, no code file) | 100% | MET |
| Code → Test | 21/21 = **100%** (FR-18 covered by CI lint gate) | 100% | MET |
| NFR Association | 24 NFR associations / 21 FRs = **114%** | ≥ 50% | MET |

### FR Status Summary

| Status | Count | FR IDs |
|--------|-------|--------|
| DRAFT | 21 | FR-01 through FR-21 |
| IN_REVIEW | 0 | — |
| APPROVED | 0 | — |
| IMPLEMENTED | 0 | — |

### NFR Type Coverage

| NFR Type | NFR IDs | FRs Covered | Coverage % |
|----------|---------|------------|------------|
| Performance | NFR-01 | FR-02, FR-03, FR-10, FR-11, FR-19 | 5/21 = 24% |
| Security | NFR-02, NFR-03, NFR-04, NFR-05 | FR-04, FR-05, FR-08, FR-09, FR-10 | 5/21 = 24% |
| Reliability | NFR-06 | FR-12, FR-14, FR-19, FR-21 | 4/21 = 19% |
| Maintainability | NFR-07, NFR-08 | FR-01, FR-06, FR-07, FR-13, FR-16, FR-17, FR-18, FR-20, FR-21 | 9/21 = 43% |
| Deployability | NFR-09 | FR-15 | 1/21 = 5% |

### Gap Analysis

- **No FR without NFR association** — all 21 FRs have ≥ 1 NFR linked (see SRS §2 Cross-Reference table)
- **Top NFR coverage**: Maintainability (43%), Performance + Security (24% each)
- **Lowest NFR coverage**: Deployability (5%) — expected for Phase 1 with single-node Docker Compose
- **No coverage gaps** — all 5 NFR types from constitution quality dimensions are represented

---

## ASPICE Compliance

### SWE.3 Software Detailed Design and Unit Construction

| Process Attribute | SWE.3.B.SP1: Develop Detailed Design | SWE.3.B.SP2: Develop and Execute Unit Tests | SWE.3.B.SP3: Ensure Consistency and Traceability |
|------------------|--------------------------------------|---------------------------------------------|--------------------------------------------------|
| **Requirement** | Each FR documented with implementation function, expected code file, and SRS section reference | Each FR has ≥ 1 test case defined (unit + cross-cutting); test files mapped to source files | Bidirectional traceability established: FR ↔ SRS ↔ Code ↔ Test |
| **Phase 1 Status** | COMPLIANT — all 21 FRs have implementation functions and code files in SRS.md | COMPLIANT — all 21 FRs mapped to test files; 23 cross-cutting test cases defined in SRS §6 | COMPLIANT — TRACEABILITY_MATRIX.md provides FR→SRS→Code→Test links for all 21 FRs |
| **Evidence** | SRS.md §2 (Functional Requirements table, FR Cross-Reference) and §7 (FR Block JSON) | SRS.md §6 (Cross-Cutting Test Requirements); Code ↔ Test Mapping table above | This TRACEABILITY_MATRIX.md; SPEC_TRACKING.md FR-to-NFR Trace Matrix |
| **Gap** | FR-18 is lint-enforced (no dedicated code file) — acceptable per SRS | FR-18 is CI lint gate (not unit test) — acceptable per SRS §6 intent | None — all trace paths are complete |

### ASPICE Compliance Summary

| Criterion | Status | Notes |
|-----------|--------|-------|
| SWE.3.B.SP1 — Detailed Design | PASS | All 21 FRs have design-level documentation: function signatures, data structures, file layout |
| SWE.3.B.SP2 — Unit Tests | PASS | Test file + coverage target defined per FR; 23 cross-cutting test cases cover API completeness, security, KPI gates, and deployment smoke |
| SWE.3.B.SP3 — Traceability | PASS | Bidirectional trace: FR ↔ SRS (this matrix §FR↔SRS), SRS ↔ Code (§SRS↔Code), Code ↔ Test (§Code↔Test), FR ↔ NFR (SPEC_TRACKING.md matrix) |
| Overall | PASS | All three SWE.3.B process attributes are satisfied for Phase 1 requirements baseline |

---

## Change History

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-05-23 | 1.0 | Requirements Engineer (Agent A) | Initial creation — 21 FRs, 9 NFRs, full traceability mapping |
