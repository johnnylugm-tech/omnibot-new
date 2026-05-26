# TEST_PLAN — OmniBot Phase 4

> **Version**: v1.0.0
> **Phase**: 4 - Testing
> **Specification Reference**: `SRS.md` v1.0 / `SPEC.md` v7.0
> **Target passing criteria**: 100% tests passed (441 total)

This document maps all Functional Requirements (`FR-01` through `FR-22`) to concrete test cases defined and executed in the `tests/` suite.

---

## 1. Test Suite Mapping

### FR-01: PostgreSQL Schema
- **TC-101 (TC-FR01-01) (Positive):** Verify PostgreSQL schema has all 8 core tables (`users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`).
  - **Input:** Live Database connection.
  - **Expected:** Tables exist in `information_schema.tables`.
  - **Priority:** CRITICAL.
- **TC-102 (TC-FR01-02) (Positive):** Verify all 11 defined indexes are present in the database.
  - **Expected:** Indexes are active and accelerate queries.
  - **Priority:** HIGH.
- **TC-103 (TC-FR01-03) (Boundary):** Ensure Phase 2/3 columns (`embeddings`, `dst_state`) have null defaults.
  - **Expected:** No ALTER TABLE required in future phases.
  - **Priority:** HIGH.

### FR-02: Telegram Webhook Adapter
- **TC-201 (TC-FR02-01) (Positive):** Parse valid Telegram JSON request payload into `UnifiedMessage`.
  - **Input:** JSON payload with `message` block.
  - **Expected:** Dataclass instance with `Platform.TELEGRAM` and correct content.
  - **Priority:** CRITICAL.
- **TC-202 (TC-FR02-02) (Negative):** Parse Telegram payload missing critical fields (`from.id`, `chat.id`).
  - **Expected:** Raises descriptive `ValidationError` (exit 422).
  - **Priority:** HIGH.

### FR-03: LINE Webhook Adapter
- **TC-301 (TC-FR03-01) (Positive):** Parse valid LINE JSON request containing `replyToken`.
  - **Input:** Standard LINE message webhook body.
  - **Expected:** `UnifiedMessage` with `reply_token` correctly populated.
  - **Priority:** CRITICAL.

### FR-04: Telegram Webhook Signature Verifier
- **TC-401 (TC-FR04-01) (Positive):** HMAC-SHA256 verification of authentic body.
  - **Input:** Valid request body and header signature.
  - **Expected:** Verifier returns `True`.
  - **Priority:** CRITICAL.
- **TC-402 (TC-FR04-02) (Negative):** Rejection of tampered body or invalid signature.
  - **Expected:** Verifier returns `False` / Webhook returns `401 AUTH_INVALID_SIGNATURE`.
  - **Priority:** CRITICAL.

### FR-05: LINE Webhook Signature Verifier
- **TC-501 (TC-FR05-01) (Positive):** HMAC-SHA256 Base64-encoded verification of LINE body.
  - **Expected:** Returns `True` for authentic webhook headers.
  - **Priority:** CRITICAL.

### FR-06: Unified Message Dataclass
- **TC-601 (TC-FR06-01) (Positive):** Create `UnifiedMessage` and verify immutability.
  - **Input:** UnifiedMessage constructor args.
  - **Expected:** Object fields are populated; mutation attempt raises `FrozenInstanceError`.
  - **Priority:** HIGH.

### FR-07: Standardized API Responses
- **TC-701 (TC-FR07-01) (Positive):** Serialization of success and paginated responses.
  - **Expected:** JSON format contains `success`, `data`, `error`, `error_code`, `total`, `page`, `limit`, `has_next`.
  - **Priority:** HIGH.

### FR-08: Input Sanitizer (L2)
- **TC-801 (TC-FR08-01) (Boundary):** Unicode normalization of full-width characters and control characters.
  - **Input:** `\uFF34\uFF25\uFF33\uFF34` + control chars.
  - **Expected:** Normalized to `TEST`, control chars trimmed except newlines/tabs.
  - **Priority:** HIGH.

### FR-09: PII Masking (L4)
- **TC-901 (TC-FR09-01) (Boundary):** Detect and mask Taiwan phone numbers, email addresses, and physical addresses.
  - **Input:** "My email is a@b.com, call 0912-345-678, at 台北市信義路五段5號"
  - **Expected:** "My email is [email_masked], call [phone_masked], at [address_masked]".
  - **Priority:** HIGH.

### FR-10: Token Bucket Rate Limiter
- **TC-1001 (TC-FR10-01) (Boundary):** Rate limiter blocks excess requests under burst load, separate per user.
  - **Input:** Burst of 100+ requests.
  - **Expected:** Tokens consumed correctly; excess requests return `False` / HTTP 429.
  - **Priority:** HIGH.

### FR-11: Rule-Based Knowledge Matcher
- **TC-1101 (TC-FR11-01) (Positive):** Match questions using SQL ILIKE or keywords array matching.
  - **Expected:** Confidence 0.95 on exact match, 0.7 on array match; inactive entries ignored.
  - **Priority:** CRITICAL.

### FR-12: Basic Escalation Queue
- **TC-1201 (TC-FR12-01) (Positive):** Handoff out-of-scope or unmatched messages to the escalation queue.
  - **Expected:** Database entry created with `priority=0`, returning `id=-1` handoff indicator.
  - **Priority:** CRITICAL.

### FR-13: Structured JSON Logger
- **TC-1301 (TC-FR13-01) (Positive):** Log output format.
  - **Expected:** Single-line JSON strings parsed successfully, containing standard ISO timestamp and custom keys.
  - **Priority:** HIGH.

### FR-14: Health Check Endpoint
- **TC-1401 (TC-FR14-01) (Boundary):** Health check returns Degraded or Healthy depending on Postgres/Redis availability.
  - **Expected:** Always returns HTTP 200; degraded states report down status properly.
  - **Priority:** HIGH.

### FR-15: Docker Compose Environment
- **TC-1501 (TC-FR15-01) (Positive):** Service startup and dependencies.
  - **Expected:** PostgreSQL, Redis, and API containers start up successfully and report healthy status in 60s.
  - **Priority:** HIGH.

### FR-16: ODD Metrics SQL
- **TC-1601 (TC-FR16-01) (Positive):** Execution of SQL scripts for FCR, latency, and knowledge hits.
  - **Expected:** SQL runs without syntax error; returns numeric stats within limits.
  - **Priority:** HIGH.

### FR-17: Standardized Error Codes
- **TC-1701 (TC-FR17-01) (Positive):** Map exceptions to correct standardized HTTP codes.
  - **Expected:** Matches standard status: 401 for Auth, 429 for Rate, 404 for KB, 422 for Validation.
  - **Priority:** HIGH.

### FR-18: Code Conventions
- **TC-1801 (TC-FR18-01) (Positive):** Naming conventions, function length, CC metrics.
  - **Expected:** Zero ruff violations, radon CC <= 10.
  - **Priority:** HIGH.

### FR-19: Core Message Pipeline
- **TC-1901 (TC-FR19-01) (Positive):** Flow message end-to-end through 11 distinct pipeline stages.
  - **Expected:** Full transactional verification across all components.
  - **Priority:** CRITICAL.

### FR-20: Unified Response format
- **TC-2001 (TC-FR20-01) (Positive):** Immutability of UnifiedResponse.
  - **Expected:** Dataclass object frozen, metadata defaults to empty dict.
  - **Priority:** HIGH.

### FR-21: Config Loader
- **TC-2101 (TC-FR21-01) (Boundary):** Validates required environment settings at startup.
  - **Expected:** Fails fast with clear listing of missing keys.
  - **Priority:** HIGH.

### FR-22: IP Whitelist Interceptor
- **TC-2201 (TC-FR22-01) (Boundary):** Block unauthorized client IPs before computing signature.
  - **Input:** Request from unofficial IP.
  - **Expected:** Aborted with HTTP 403 Forbidden.
  - **Priority:** CRITICAL.
