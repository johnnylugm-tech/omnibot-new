# SAD — OmniBot Phase 1

> Software Architecture Document
> Source SRS: `01-requirements/SRS.md` v1.0 (2026-05-23)
> Phase: 2 — Architecture Design
> Target: 18 modules, 22 FRs traced, 6-layer architecture

---

## 1. Architecture Overview

OmniBot Phase 1 implements a **six-layer pipeline architecture** for multi-platform chatbot processing. Each inbound message flows through a fixed sequence of security checks, transformation, and knowledge resolution before a response is returned.

### 1.1 Layered Architecture

```
+------------------------------------------------------------------+
|                    OmniBot Phase 1 Architecture                    |
+------------------------------------------------------------------+

  +--------------+  +--------------+
  |  Telegram    |  |    LINE      |
  +------+-------+  +------+-------+
         |                  |
  +------+------------------+--------------------------------------+
  |              Transport Layer                                    |
  |   app.api.webhooks                                              |
  |   - POST /api/v1/webhook/telegram  (FR-02)                      |
  |   - POST /api/v1/webhook/line      (FR-03)                      |
  |   - GET  /api/v1/health            (FR-14)                      |
  +------+---------------------------------------------------------+
         |
  +------+---------------------------------------------------------+
  |           Security Interceptor Chain                             |
  |   Executed in fixed order per SPEC.md §Interceptor Sequence:     |
  |   1. IP Whitelist (FR-22)         → 403/400 on reject            |
  |   2. Webhook Signature (FR-04,05) → 401 on fail                  |
  |   3. Platform Adapter Parse (FR-02,03) → 422 on malformed        |
  |   4. Rate Limiter (FR-10)         → 429 on exceed                |
  +------+---------------------------------------------------------+
         |
  +------+---------------------------------------------------------+
  |              Processing Pipeline                                 |
  |   app.processing.pipeline (FR-19): 11-stage PipelineOrchestrator |
  |   Stages 5-8 (post-rate-limit):                                  |
  |   5. Input Sanitization L2  (FR-08)                              |
  |   6. PII Masking L4          (FR-09)                             |
  |   7. Knowledge Match Layer 1 (FR-11)                             |
  |   8. Basic Escalation        (FR-12) if no match                 |
  |   Stages 9-11 (response + observe):                              |
  |   9. Construct UnifiedResponse   (FR-20)                         |
  |   10. Send reply via platform adapter                            |
  |   11. Structured log completion  (FR-13)                         |
  +------+---------------------------------------------------------+
         |
  +------+---------------------------------------------------------+
  |              Knowledge Layer                                     |
  |   app.knowledge.matcher (FR-11)                                  |
  |   - Rule-based matching via ILIKE + keywords array               |
  |   - Returns KnowledgeResult(source="rule", confidence 0.7-0.95)  |
  |   app.knowledge.escalation (FR-12)                               |
  |   - Fallback when no rule match: creates escalation_queue row    |
  |   - Returns KnowledgeResult(source="escalate", id=-1)            |
  +------+---------------------------------------------------------+
         |
  +------+---------------------------------------------------------+
  |              Data Layer                                          |
  |   app.models (FR-01): PostgreSQL 16 schema                       |
  |   - 8 tables: users, conversations, messages, knowledge_base,    |
  |     platform_configs, escalation_queue, user_feedback,           |
  |     security_logs                                                |
  |   - 11 indexes + Phase 2/3 columns with defaults                 |
  |   - Redis 7: Token Bucket state (FR-10), no persistence          |
  +------+---------------------------------------------------------+
         |
  +------+---------------------------------------------------------+
  |              Infrastructure Layer                                |
  |   app.infrastructure.config (FR-21): Env-var config, fail-fast   |
  |   app.infrastructure.logger (FR-13): Structured JSON logging     |
  |   app.infrastructure.errors (FR-17): Standard error codes        |
  |   app.infrastructure.health (FR-14): Health check endpoint       |
  |   docker-compose.yml (FR-15): 3-service dev environment          |
  |   queries/ (FR-16): ODD SQL scripts                              |
  +------+---------------------------------------------------------+
```

### 1.2 Design Principles

1. **Unidirectional data flow**: Messages flow top-down through layers; no upward dependencies. Each layer depends only on layers below it.
2. **Fail-fast at boundaries**: Invalid input is rejected at the earliest possible stage (IP whitelist before HMAC, HMAC before parse, rate limit before processing).
3. **Immutable core types**: `UnifiedMessage` and `UnifiedResponse` are frozen dataclasses — no mutation after construction.
4. **Schema-forward design**: All core tables created in Phase 1. Phase 2/3 columns (`embeddings vector(384)`, `satisfaction_score`, `dst_state JSONB`) included with defaults to avoid ALTER TABLE later.
5. **Platform abstraction**: Telegram and LINE specifics are encapsulated in adapters. All downstream code operates on `UnifiedMessage` / `UnifiedResponse`.

### 1.3 Interceptor Chain Sequence (Phase 1)

Per SPEC.md §Interceptor Sequence, the security interceptor pipeline is:

```
TLS (reverse proxy)
  → IP Whitelist (FR-22)           [app.security.ip_whitelist]
    → Webhook Signature (FR-04/05) [app.security.signature]
      → Platform Adapter Parse     [app.adapters.telegram_adapter / line_adapter]
        → Rate Limiter (FR-10)     [app.security.rate_limiter]
          → Processing Pipeline    [app.processing.pipeline]
```

- IP Whitelist runs **before** HMAC to prevent DDoS via expensive cryptographic operations.
- Rate Limiter runs **after** platform adapter parse because it requires `platform` and `user_id` from the parsed `UnifiedMessage`.
- RBAC (Phase 3) would be inserted after Rate Limiter.

---

## 2. Module Design

### 2.1 app.api.webhooks

| Attribute | Value |
|-----------|-------|
| Responsibility | Accept inbound HTTP POST requests from Telegram and LINE platforms; route to security chain and pipeline; expose health check endpoint |
| External Interface | `POST /api/v1/webhook/telegram` → 200/401/403/429/422, `POST /api/v1/webhook/line` → 200/401/403/429/422, `GET /api/v1/health` → 200 with status JSON |
| Dependencies | `app.security.ip_whitelist`, `app.security.signature`, `app.adapters`, `app.security.rate_limiter`, `app.processing.pipeline`, `app.infrastructure.health` |
| FRs Mapped | FR-02 (Telegram webhook entry), FR-03 (LINE webhook entry), FR-14 (health endpoint), FR-07 (ApiResponse format in responses) |

#### Logical Constraints
- Webhook routes must accept raw `body: bytes` and `signature: str` from headers before any parsing
- All webhook responses use `ApiResponse` format (FR-07): `{"success": bool, "data": T|null, "error": str|null, "error_code": str|null}`
- Health endpoint must return HTTP 200 even in degraded state (NFR-06)
- No business logic in route handlers — delegate to `PipelineOrchestrator.process()`

### 2.2 app.security.ip_whitelist

| Attribute | Value |
|-----------|-------|
| Responsibility | Filter inbound requests by source IP against a configured CIDR whitelist; reject unauthorized IPs before HMAC computation |
| External Interface | `IPWhitelist(cidrs: list[str])`, `IPWhitelist.is_allowed(ip: str) -> bool` |
| Dependencies | `app.infrastructure.config` (reads `IP_WHITELIST_CIDRS`) |
| FRs Mapped | FR-22 |

#### Logical Constraints
- Must execute **before** webhook signature verification (prevents DDoS via HMAC exhaustion) per SPEC.md §Interceptor Sequence
- Whitelist format: comma-separated CIDR strings from `IP_WHITELIST_CIDRS` env var
- Source IP extraction: `X-Forwarded-For` leftmost IP first, fallback `request.client.host`
- Unlisted IP → HTTP 403 (NFR-10)
- Empty/missing IP → HTTP 400 with warning log (NFR-10)
- Invalid CIDR format in config → fail-fast at startup with `IPWhitelistError`
- `is_allowed()` must be fail-secure: invalid IP format returns `False`

### 2.3 app.security.signature

| Attribute | Value |
|-----------|-------|
| Responsibility | Verify webhook request authenticity via platform-specific HMAC-SHA256 signatures; reject invalid signatures with 401 before any message processing |
| External Interface | `WebhookVerifier.verify(body: bytes, signature: str) -> bool`, `TelegramWebhookVerifier`, `LineWebhookVerifier` |
| Dependencies | `app.infrastructure.config` (reads `TELEGRAM_BOT_TOKEN`, `LINE_CHANNEL_SECRET`) |
| FRs Mapped | FR-04 (Telegram HMAC-SHA256 over `bot_token`-derived key), FR-05 (LINE HMAC-SHA256 over `channel_secret` with Base64 digest) |

#### Logical Constraints
- Both verifiers must use `hmac.compare_digest()` for timing-attack resistance (NFR-02)
- Telegram: secret key = `SHA256(bot_token)`, compare hexdigest
- LINE: digest = `HMAC-SHA256(body, channel_secret)`, encode Base64, compare to signature header
- Invalid signature → HTTP 401 with `AUTH_INVALID_SIGNATURE` error code (FR-17, NFR-02)
- Abstract base class `WebhookVerifier` with single `verify()` method for future platform extensibility
- Signature verification must reject before any message body parsing (zero-trust boundary)

### 2.4 app.security.rate_limiter

| Attribute | Value |
|-----------|-------|
| Responsibility | Enforce per-platform per-user rate limiting via Token Bucket algorithm; reject excess requests with HTTP 429 |
| External Interface | `RateLimiter(default_rps: int = 100)`, `RateLimiter.check(platform: str, user_id: str) -> bool` |
| Dependencies | Redis 7 (bucket state storage), `app.infrastructure.config` (reads `RATE_LIMIT_CAPACITY`, `RATE_LIMIT_REFILL_RATE`) |
| FRs Mapped | FR-10 |

#### Logical Constraints
- Key format: `{platform}:{user_id}` — independent buckets per platform-user pair (NFR-05)
- Default: capacity=100 tokens, refill=100 tokens/second
- Token consumption is atomic per `check()` call — no partial credit
- Must execute **after** platform adapter parse (requires `UnifiedMessage.platform` and `.platform_user_id`), per SPEC.md §Interceptor Sequence
- Redis-backed for stateless horizontal scaling; in-memory fallback acceptable for single-node dev
- Exceeded limit → HTTP 429 with `RATE_LIMIT_EXCEEDED` error code

### 2.5 app.adapters.telegram_adapter

| Attribute | Value |
|-----------|-------|
| Responsibility | Parse Telegram Bot API webhook JSON payload into immutable `UnifiedMessage` dataclass |
| External Interface | `TelegramAdapter.parse_message(payload: dict) -> UnifiedMessage`, `TelegramAdapter.send_reply(response: UnifiedResponse) -> bool` (Stage 10) |
| Dependencies | `app.adapters.unified` (UnifiedMessage, Platform enum, MessageType enum) |
| FRs Mapped | FR-02 |

#### Logical Constraints
- Input: raw JSON dict from Telegram webhook body (after signature verification)
- Output: `UnifiedMessage(platform=Platform.TELEGRAM, ...)` with all fields populated
- Must extract `platform_user_id`, `message_type`, `content` from Telegram-specific payload structure
- `raw_payload` must contain the original unmodified request body
- Invalid/missing fields → raise descriptive error (caught by pipeline → 422)
- `reply_token` will be `None` for Telegram (LINE-specific field)

### 2.6 app.adapters.line_adapter

| Attribute | Value |
|-----------|-------|
| Responsibility | Parse LINE Messaging API webhook JSON payload into immutable `UnifiedMessage` dataclass |
| External Interface | `LineAdapter.parse_message(payload: dict) -> UnifiedMessage`, `LineAdapter.send_reply(response: UnifiedResponse) -> bool` (Stage 10) |
| Dependencies | `app.adapters.unified` (UnifiedMessage, Platform enum, MessageType enum) |
| FRs Mapped | FR-03 |

#### Logical Constraints
- Input: raw JSON dict from LINE webhook body (after signature verification)
- Must extract `reply_token` from LINE event object and populate `UnifiedMessage.reply_token`
- Empty events array → handled gracefully (no exception, return sentinel or skip)
- LINE text message content extracted from `events[0].message.text`
- Invalid/missing fields → raise descriptive error (caught by pipeline → 422)

### 2.7 app.adapters.unified

| Attribute | Value |
|-----------|-------|
| Responsibility | Define cross-platform immutable dataclasses (`UnifiedMessage`, `UnifiedResponse`), enums (`Platform`, `MessageType`, `KnowledgeSource`), and API response wrappers (`ApiResponse`, `PaginatedResponse`) |
| External Interface | `UnifiedMessage(frozen=True)`, `UnifiedResponse(frozen=True)`, `Platform(Enum)`, `MessageType(Enum)`, `KnowledgeSource(Enum)`, `ApiResponse[T]`, `PaginatedResponse[T]` |
| Dependencies | None (leaf module, zero dependencies) |
| FRs Mapped | FR-06 (UnifiedMessage + Platform + MessageType), FR-07 (ApiResponse + PaginatedResponse), FR-20 (UnifiedResponse + KnowledgeSource) |

#### Logical Constraints
- `UnifiedMessage` and `UnifiedResponse` must be `@dataclass(frozen=True)` — no mutation after construction (FR-06, FR-20)
- `UnifiedMessage.received_at` defaults to `datetime.utcnow()` at construction time
- `UnifiedMessage.reply_token` is `Optional[str]`, populated only for LINE (FR-03)
- `UnifiedMessage.raw_payload` defaults to empty `dict`
- `UnifiedResponse.metadata` defaults to empty `dict` (FR-20)
- `ApiResponse` carries `success: bool`, `data: Optional[T]`, `error: Optional[str]`, `error_code: Optional[str]`
- `PaginatedResponse` extends `ApiResponse[List[T]]` with `total`, `page`, `limit`, `has_next`
- `MessageType` enum: TEXT, IMAGE, STICKER, LOCATION, FILE
- `KnowledgeSource` enum: RULE, ESCALATE (Phase 1); RAG, WIKI added in Phase 2

### 2.8 app.processing.sanitizer

| Attribute | Value |
|-----------|-------|
| Responsibility | Normalize inbound message text: NFKC normalization, strip non-printable characters (except `\n`, `\t`), trim whitespace; no pattern matching |
| External Interface | `InputSanitizer.sanitize(text: str) -> str` |
| Dependencies | None (stdlib `unicodedata` only) |
| FRs Mapped | FR-08 |

#### Logical Constraints
- L2 only: character-level normalization. No regex, no pattern matching (pattern matching is L3, Phase 2)
- NFKC must not alter ASCII alphanumerics (NFR-03)
- Control characters removed except `\n` (U+000A) and `\t` (U+0009)
- Empty string → empty string (idempotent)
- Must be applied to every inbound message before knowledge matching, PII masking, or logging (NFR-03)

### 2.9 app.processing.pii_masker

| Attribute | Value |
|-----------|-------|
| Responsibility | Detect and mask PII patterns in message text; replace with typed placeholders; return mask statistics |
| External Interface | `PIIMasking.mask(text: str) -> PIIMaskResult` (frozen dataclass: `masked_text`, `mask_count`, `pii_types`) |
| Dependencies | None (stdlib `re` only) |
| FRs Mapped | FR-09 |

#### Logical Constraints
- Phase 1 PII types: Taiwan phone (`\d{4}-\d{3,4}-\d{3,4}` and `\d{10,11}`), email, Taiwan address (city/county + road/street/lane/alley/number)
- Credit card + Luhn check is Phase 2 (defined but disabled in Phase 1)
- Matched text replaced with `[{type}_masked]` placeholder (e.g., `[phone_masked]`)
- Pattern application order: phone → email → address (longest-match-first via reversed iteration)
- Recall ≥ 95%, precision ≥ 99% on labeled Taiwan PII corpus (NFR-04)
- `should_escalate(text)` returns True if sensitive keywords detected (密碼, 銀行帳戶, 信用卡號, 提款卡)
- Must run after sanitization (sanitized text may alter PII pattern boundaries)

### 2.10 app.processing.pipeline

| Attribute | Value |
|-----------|-------|
| Responsibility | Orchestrate the 11-stage end-to-end message processing flow; handle errors at each stage without crashing the pipeline; produce structured log on completion |
| External Interface | `PipelineOrchestrator.process(platform: Platform, raw_body: bytes, signature: str, client_ip: str) -> UnifiedResponse` |
| Dependencies | `app.security.ip_whitelist`, `app.security.signature`, `app.adapters`, `app.security.rate_limiter`, `app.processing.sanitizer`, `app.processing.pii_masker`, `app.knowledge.matcher`, `app.knowledge.escalation`, `app.adapters.unified`, `app.infrastructure.logger` |
| FRs Mapped | FR-19 |

#### Logical Constraints
- 11-stage fixed sequence (FR-19):
  1. IP Whitelist interception → reject early (403/400)
  2. Webhook signature verification → reject early (401)
  3. Platform adapter parse → UnifiedMessage (422 on failure)
  4. Rate limiter check → block if exceeded (429)
  5. Input sanitization L2 (NFKC)
  6. PII masking L4
  7. Knowledge matching Layer 1
  8. Basic escalation (if Layer 1 returns None)
  9. Construct UnifiedResponse
  10. Send reply via platform adapter
  11. Log completion via structured logger with `timestamp`
- Each stage emits a typed result; the next stage receives the previous stage's output
- Any stage failure → appropriate error response (ApiResponse format) + structured log
- Pipeline must not crash; all exceptions caught and translated to error codes (FR-17)
- Must create DB transaction boundaries: new conversation + message rows within a single transaction

### 2.11 app.knowledge.matcher

| Attribute | Value |
|-----------|-------|
| Responsibility | Query `knowledge_base` table for matching answers using SQL `ILIKE` on question text and `= ANY(keywords)` array match; return ranked `KnowledgeResult` list |
| External Interface | `HybridKnowledgeV7._rule_match(query: str) -> Optional[KnowledgeResult]`, `HybridKnowledgeV7._rule_match_list(query: str) -> list[KnowledgeResult]` |
| Dependencies | PostgreSQL (`knowledge_base` table), `app.adapters.unified` (KnowledgeResult dataclass) |
| FRs Mapped | FR-11 |

#### Logical Constraints
- Only active entries (`is_active = TRUE`)
- Ordered by `version DESC`, limited to top 5
- Confidence: 0.95 for exact substring match (`query.lower() in question.lower()`), 0.7 for ILIKE match
- Multi-keyword entries: match if any keyword in the array matches
- Returns `KnowledgeResult(id, content, confidence, source="rule", knowledge_id)` on match
- Returns `None` when no match found → triggers escalation (FR-12)
- `KnowledgeResult.id = -1` reserved for non-knowledge-base sources (escalation)
- Phase 1 only: `source` is always `"rule"` or `"escalate"`; `"rag"` and `"wiki"` added in Phase 2

### 2.12 app.knowledge.escalation

| Attribute | Value |
|-----------|-------|
| Responsibility | Create escalation record in `escalation_queue` when no rule match is found; return handoff response to user |
| External Interface | `BasicEscalationManager.create(conversation_id: int, reason: str) -> int` |
| Dependencies | PostgreSQL (`escalation_queue`, `conversations` tables), `app.adapters.unified` (KnowledgeResult) |
| FRs Mapped | FR-12 |

#### Logical Constraints
- Called only when `_rule_match()` returns `None` (Layer 1 exhausted)
- Creates row in `escalation_queue` with `priority=0` (normal), `sla_deadline IS NULL` (no SLA in Phase 1)
- Updates `conversations.scope_type` to `'out_of_scope'` when `conversation_id` is available in context
- Returns `KnowledgeResult(id=-1, content="正在為您轉接人工客服，請稍候...", source="escalate", confidence=0.0)`
- No SLA tracking, priority levels, or agent assignment in Phase 1 (FR-12, §4 Constraints)
- Escalation reasons: `"no_rule_match"`, `"out_of_scope"`

### 2.13 app.infrastructure.config

| Attribute | Value |
|-----------|-------|
| Responsibility | Load and validate all configuration from environment variables; fail fast at startup with clear error listing missing keys |
| External Interface | `Settings` pydantic/dataclass, `ConfigLoader.from_env() -> Settings` |
| Dependencies | None (stdlib `os` only; optionally `pydantic-settings`) |
| FRs Mapped | FR-21 |

#### Logical Constraints
- Required env vars: `TELEGRAM_BOT_TOKEN`, `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET`, `DATABASE_URL`, `REDIS_URL`
- Optional with defaults: `TELEGRAM_WEBHOOK_SECRET` (default: derived from bot_token), `RATE_LIMIT_CAPACITY` (100), `RATE_LIMIT_REFILL_RATE` (100.0), `SERVICE_NAME` ("omnibot"), `IP_WHITELIST_CIDRS` ("" — empty = reject all)
- Missing required key → `ConfigError(f"Missing required config keys: {missing_keys}")` raised at startup
- Invalid CIDR format in `IP_WHITELIST_CIDRS` → `IPWhitelistError` at startup
- All values are strings from env; type coercion happens in Settings model

### 2.14 app.infrastructure.logger

| Attribute | Value |
|-----------|-------|
| Responsibility | Emit single-line JSON log entries with required fields; wrap Python stdlib `logging` as transport |
| External Interface | `StructuredLogger(service: str = "omnibot")`, `.log(level, message, **kwargs)`, `.info()`, `.error()`, `.warn()` |
| Dependencies | Python stdlib `logging`, `json`, `datetime` |
| FRs Mapped | FR-13 |

#### Logical Constraints
- Every log entry is a single-line JSON object (NFR-07)
- Required fields: `timestamp` (ISO 8601 UTC), `level` (DEBUG/INFO/WARN/ERROR/CRITICAL), `service` (configurable), `message`
- Extra `**kwargs` appear as top-level keys in the JSON object
- Uses Python stdlib `logging` module as transport — compatible with all log aggregation tools
- Level filtering works via standard `logging.getLogger("omnibot").setLevel()` (NFR-07)
- Log level usage: DEBUG (SQL params, match scores), INFO (business events), WARN (low confidence, PII detected), ERROR (DB failures), CRITICAL (security events)

### 2.15 app.infrastructure.errors

| Attribute | Value |
|-----------|-------|
| Responsibility | Define standardized error code constants and HTTP status mappings; provide helper to construct error `ApiResponse` |
| External Interface | Error code constants: `AUTH_INVALID_SIGNATURE`, `RATE_LIMIT_EXCEEDED`, `KNOWLEDGE_NOT_FOUND`, `VALIDATION_ERROR`, `INTERNAL_ERROR`; `error_response(code: str, message: str) -> ApiResponse` |
| Dependencies | `app.adapters.unified` (ApiResponse) |
| FRs Mapped | FR-17 |

#### Logical Constraints
- Phase 1 error codes and HTTP statuses:
  - `AUTH_INVALID_SIGNATURE` → 401
  - `RATE_LIMIT_EXCEEDED` → 429
  - `KNOWLEDGE_NOT_FOUND` → 404
  - `VALIDATION_ERROR` → 422
  - `INTERNAL_ERROR` → 500
- All error responses use `ApiResponse(success=False, error=<human_message>, error_code=<code>)` format
- Error code constants are `UPPER_SNAKE_CASE` (FR-18 naming convention)
- `VALIDATION_ERROR` also covers `IPWhitelistError` (400) and adapter parse failures (422)

### 2.16 app.infrastructure.health

| Attribute | Value |
|-----------|-------|
| Responsibility | Expose `GET /api/v1/health` endpoint; probe PostgreSQL and Redis connectivity; return composite health status |
| External Interface | `health_check() -> dict` with keys `status`, `postgres`, `redis`, `uptime_seconds` |
| Dependencies | PostgreSQL connection pool, Redis client, `app.infrastructure.config` |
| FRs Mapped | FR-14 |

#### Logical Constraints
- Response format: `{"status": "healthy|degraded|unhealthy", "postgres": bool, "redis": bool, "uptime_seconds": float}`
- `"healthy"` when both postgres and redis are reachable
- `"degraded"` when one dependency is unreachable
- `"unhealthy"` when both are unreachable
- Must return HTTP 200 even in degraded/unhealthy state (NFR-06)
- Response time must be < 500ms (NFR-06)
- `uptime_seconds` must increase monotonically between calls
- Each probe must have its own timeout (e.g., 2 seconds) to prevent cascading delays

### 2.17 app.models

| Attribute | Value |
|-----------|-------|
| Responsibility | Define PostgreSQL schema via Alembic migration; create all 8 core tables + 11 indexes; include Phase 2/3 columns with defaults |
| External Interface | Migration `001_phase1_core.py` with `create_schema()`, SQLAlchemy ORM models |
| Dependencies | PostgreSQL 16 (pgvector extension), Alembic |
| FRs Mapped | FR-01 |

#### Logical Constraints
- 8 tables: `users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`
- 11 indexes: `idx_users_platform_uid`, `idx_conversations_started`, `idx_conversations_user`, `idx_conversations_platform`, `idx_messages_conversation`, `idx_messages_created`, `idx_kb_category`, `idx_kb_keywords` (GIN), `idx_kb_embeddings` (ivfflat), `idx_escalation_pending` (partial), `idx_security_logs_date`
- Phase 2/3 columns included with NULL defaults: `knowledge_base.embeddings vector(384)`, `knowledge_base.embedding_model`, `conversations.satisfaction_score`, `conversations.dst_state JSONB`, `messages.sentiment_category`, `messages.sentiment_intensity`, etc.
- `knowledge_base.embeddings` uses `vector(384)` type matching `paraphrase-multilingual-MiniLM-L12-v2` embedding dimension
- `users` table: `UNIQUE(platform, platform_user_id)` constraint
- `conversations` table: `unified_user_id UUID REFERENCES users(unified_user_id)`
- No ALTER TABLE needed in Phase 2/3 per SPEC.md design principle

### 2.18 queries/

| Attribute | Value |
|-----------|-------|
| Responsibility | Provide executable SQL scripts for Phase 1 ODD (Operational Data Dashboard) metrics |
| External Interface | `queries/fcr.sql`, `queries/latency.sql`, `queries/knowledge_hits.sql` |
| Dependencies | PostgreSQL `conversations`, `messages` tables |
| FRs Mapped | FR-16 |

#### Logical Constraints
- `queries/fcr.sql`: FCR rate over 30-day window for `scope_type='in_scope'` conversations where `first_contact_resolution IS NOT NULL`; result column `fcr_rate_pct` between 0-100
- `queries/latency.sql`: `AVG(response_time_ms)` and `PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms)` per platform over 30-day window
- `queries/knowledge_hits.sql`: knowledge source distribution (`rule`/`escalate`) for `role='assistant'` messages over 7-day window
- All queries must use parameterized values (no string concatenation)
- Each `.sql` file must be self-contained and executable against the Phase 1 schema

---

## 3. Error Handling

| Level | Strategy | Triggers | Behavior |
|-------|----------|----------|----------|
| **L1 — Immediate Return** | Reject request at boundary; no retry | Invalid IP (403), empty IP (400), invalid webhook signature (401), rate limit exceeded (429), malformed payload (422) | Return `ApiResponse(success=False, error_code=<code>)` immediately; log warning; no downstream processing |
| **L2 — Retry with Backoff** | Retry 3x with exponential backoff + jitter | DB write failure (connection lost, deadlock), Redis connection timeout | Exponential backoff: 1s → 2s → 4s with ±50% jitter; max total wait ~7s; if all retries fail → escalate to L3 |
| **L3 — Graceful Degradation** | Continue with reduced functionality | Knowledge match timeout (>2s), DB completely unreachable after L2 retries, Redis unavailable for rate limiter | Knowledge timeout → escalate to human handoff; Redis unavailable → allow request through (fail-open for rate limiter) with warning log; DB unreachable → return `INTERNAL_ERROR` (500) |

### 3.1 Error Code Mapping

| Error Code | HTTP Status | Level | Retry? |
|------------|-------------|-------|--------|
| `AUTH_INVALID_SIGNATURE` | 401 | L1 | No |
| `RATE_LIMIT_EXCEEDED` | 429 | L1 | No |
| `VALIDATION_ERROR` | 422 | L1 | No |
| `KNOWLEDGE_NOT_FOUND` | 404 | L3 | No — escalate |
| `INTERNAL_ERROR` | 500 | L3 | Yes (L2 first) |

### 3.2 Pipeline Error Isolation

Each pipeline stage has its own try/except. A failure in stage N does not cascade to stage N+1 — the orchestrator catches the exception, maps it to an error code, logs it, and returns the appropriate error response. The pipeline never crashes.

---

## 4. Technology Choices

| Technology | Version | Role | Rationale |
|------------|---------|------|-----------|
| **Python** | 3.12+ | Runtime | Modern async support (`asyncio`), native type hints, frozen dataclasses; large ecosystem for webhooks and NLP |
| **FastAPI** | 0.115+ | Web framework | Native async, automatic OpenAPI docs, Pydantic v2 validation, dependency injection, first-class `bytes` body support for raw webhook verification |
| **Pydantic** | 2.x | Settings + validation | Built into FastAPI; `BaseSettings` for env-var config with fail-fast validation (FR-21); model serialization |
| **PostgreSQL** | 16 (pgvector/pgvector image) | Primary database | JSONB for flexible metadata, GIN indexes for keyword arrays, CTE support for ODD queries, pgvector extension pre-installed for Phase 2; `PERCENTILE_CONT` for p95 latency ODD |
| **Redis** | 7 (redis:7-alpine) | Rate limiter state | In-memory atomic operations ideal for Token Bucket; sub-millisecond latency; Phase 2/3 will use Redis Streams for async processing |
| **Docker Compose** | v3.8 | Dev environment | Reproducible local environment; healthcheck-based service dependency ordering; single-node dev (Kubernetes is Phase 3) |
| **Alembic** | 1.14+ | Schema migrations | Standard Python migration tool; each migration has upgrade/downgrade; Phase 3 requires migration management |
| **ruff** | 0.8+ | Linter + formatter | Fast Rust-based linter; enforces FR-18 naming conventions; integrates with CI pipeline (NFR-08) |
| **radon** | 6.x | Complexity analysis | Cyclomatic complexity enforcement (max ≤ 10 per FR-18); CI gate (NFR-08) |
| **pytest** | 8.x | Test framework | Standard Python testing; `pytest-asyncio` for async handler tests; fixture-based setup for DB/Redis integration tests |
| **pytest-asyncio** | 0.24+ | Async test support | Required for FastAPI async endpoint testing and pipeline integration tests |
| **asyncpg** | 0.30+ | PostgreSQL driver | High-performance async PostgreSQL driver; connection pooling; compatible with FastAPI async handlers |
| **redis-py** | 5.x | Redis client | Official Redis client with async support via `redis.asyncio`; used for rate limiter state management |
| **httpx** | 0.28+ | HTTP client (testing) | Async HTTP client for integration tests; `ASGITransport` for FastAPI test client |
| **k6** | latest | Load testing | OSS load testing tool; used for NFR-01 latency validation (200 VUs, 10 min) |

---

## 5. Data Flow

### 5.1 End-to-End Request Flow

```
  1. External Platform (Telegram/LINE) sends webhook POST
          │
          ▼
  2. FastAPI route handler receives raw body + headers
          │
          ▼
  3. PipelineOrchestrator.process(platform, body, signature, client_ip)
          │
          ▼  [Stage 1] IP Whitelist
     Extract source IP (X-Forwarded-For → request.client.host)
     IPWhitelist.is_allowed(ip)
       ├─ False → HTTP 403/400, log warning, STOP
       └─ True → continue
          │
          ▼  [Stage 2] Webhook Signature Verification
     Select verifier by platform:
       Telegram: sha256(bot_token) → HMAC-SHA256 → hexdigest compare
       LINE:     HMAC-SHA256(channel_secret, body) → Base64 compare
       ├─ Invalid → HTTP 401, AUTH_INVALID_SIGNATURE, STOP
       └─ Valid → continue
          │
          ▼  [Stage 3] Platform Adapter Parse
     Parse JSON body → extract platform_user_id, content, message_type, reply_token
     Construct UnifiedMessage(frozen=True)
       ├─ Parse error → HTTP 422, VALIDATION_ERROR, STOP
       └─ Success → continue
          │
          ▼  [Stage 4] Rate Limiter Check
     RateLimiter.check(platform=msg.platform, user_id=msg.platform_user_id)
       ├─ Token exhausted → HTTP 429, RATE_LIMIT_EXCEEDED, STOP
       └─ Token consumed → continue
          │
          ▼  [Stage 5] Input Sanitization L2
     InputSanitizer.sanitize(msg.content)
       → NFKC normalize, strip control chars, trim
       → sanitized_text: str
          │
          ▼  [Stage 6] PII Masking L4
     PIIMasking.mask(sanitized_text)
       → PIIMaskResult(masked_text, mask_count, pii_types)
       → log warning if PII detected
          │
          ▼  [Stage 7] Knowledge Matching Layer 1
     HybridKnowledgeV7._rule_match(masked_text)
       ├─ Match found → KnowledgeResult(source="rule", confidence)
       │     → skip to Stage 9
       └─ None → continue to Stage 8
          │
          ▼  [Stage 8] Basic Escalation
     BasicEscalationManager.create(conversation_id, reason)
       → INSERT INTO escalation_queue
       → UPDATE conversations SET scope_type='out_of_scope'
       → KnowledgeResult(source="escalate", id=-1)
          │
          ▼  [Stage 9] Construct UnifiedResponse
     UnifiedResponse(
         platform=msg.platform,
         user_id=msg.unified_user_id,
         content=knowledge_result.content,
         source=knowledge_result.source,
         confidence=knowledge_result.confidence,
         metadata={...}
     )
          │
          ▼  [Stage 10] Send Reply via Platform Adapter
     Platform-specific API call (Telegram sendMessage / LINE reply)
       → External HTTP request to platform API
          │
          ▼  [Stage 11] Structured Log Completion
     StructuredLogger.info("pipeline_complete", **{
         "platform": msg.platform,
         "source": result.source,
         "confidence": result.confidence,
         "pii_masked": mask_count,
         "elapsed_ms": elapsed,
         ...
     })
          │
          ▼
     Return ApiResponse(success=True, data=UnifiedResponse)
```

### 5.2 Database Write Flow

Within the pipeline (between Stage 3 and Stage 11), the orchestrator persists data:

```
  BEGIN TRANSACTION
    INSERT INTO users (...) ON CONFLICT (platform, platform_user_id) DO UPDATE
    INSERT INTO conversations (unified_user_id, platform, scope_type, ...)
    INSERT INTO messages (conversation_id, role='user', content=original, ...)
    INSERT INTO messages (conversation_id, role='assistant', content=response, knowledge_source=..., confidence_score=...)
    [if escalate] INSERT INTO escalation_queue (...)
  COMMIT
```

All inserts happen in a single transaction for atomicity. On any DB error → L2 retry (3x with exponential backoff).

### 5.3 Knowledge Resolution Decision Tree

```
  _rule_match(query)
      │
      ├── exact substring match (query in question)
      │     → confidence=0.95, source="rule"
      │
      ├── ILIKE match
      │     → confidence=0.70, source="rule"
      │
      ├── keywords array match (query = ANY(keywords))
      │     → confidence=0.70, source="rule"
      │
      └── no match
            → _escalate(reason="no_rule_match")
                  → confidence=0.0, source="escalate", id=-1
```

---

## 6. SAB Block (machine-readable)

<!-- SAB:START -->
```json
{
  "version": "1.0",
  "created_at": "2026-05-23",
  "phase": 2,
  "project": "omnibot",
  "layers": [
    {
      "name": "transport",
      "description": "HTTP webhook endpoints and health check",
      "modules": ["app.api.webhooks", "app.infrastructure.health"],
      "fr_coverage": ["FR-02", "FR-03", "FR-07", "FR-14"],
      "allowed_dependencies": ["security", "processing", "adapters"]
    },
    {
      "name": "security",
      "description": "Security interceptor chain: IP whitelist, webhook signature verification, rate limiting",
      "modules": ["app.security.ip_whitelist", "app.security.signature", "app.security.rate_limiter"],
      "fr_coverage": ["FR-04", "FR-05", "FR-10", "FR-22"],
      "allowed_dependencies": ["infrastructure"]
    },
    {
      "name": "adapters",
      "description": "Platform-specific message parsing and unified message types",
      "modules": ["app.adapters.telegram_adapter", "app.adapters.line_adapter", "app.adapters.unified"],
      "fr_coverage": ["FR-02", "FR-03", "FR-06", "FR-20"],
      "allowed_dependencies": []
    },
    {
      "name": "processing",
      "description": "Message processing pipeline: sanitization, PII masking, pipeline orchestration",
      "modules": ["app.processing.sanitizer", "app.processing.pii_masker", "app.processing.pipeline"],
      "fr_coverage": ["FR-08", "FR-09", "FR-19"],
      "allowed_dependencies": ["adapters", "knowledge", "security", "infrastructure"]
    },
    {
      "name": "knowledge",
      "description": "Rule-based knowledge matching and basic escalation",
      "modules": ["app.knowledge.matcher", "app.knowledge.escalation"],
      "fr_coverage": ["FR-11", "FR-12"],
      "allowed_dependencies": ["adapters", "data"]
    },
    {
      "name": "data",
      "description": "PostgreSQL schema, ORM models, migration scripts",
      "modules": ["app.models"],
      "fr_coverage": ["FR-01"],
      "allowed_dependencies": []
    },
    {
      "name": "infrastructure",
      "description": "Configuration, structured logging, error codes, deployment",
      "modules": ["app.infrastructure.config", "app.infrastructure.logger", "app.infrastructure.errors"],
      "fr_coverage": ["FR-13", "FR-17", "FR-21"],
      "allowed_dependencies": []
    },
    {
      "name": "operations",
      "description": "ODD SQL queries, Docker Compose, code conventions",
      "modules": ["queries", "docker-compose.yml"],
      "fr_coverage": ["FR-15", "FR-16", "FR-18"],
      "allowed_dependencies": ["data"]
    }
  ],
  "dependencies": {
    "transport": ["security", "adapters", "processing", "infrastructure"],
    "security": ["infrastructure"],
    "adapters": [],
    "processing": ["adapters", "knowledge", "security", "infrastructure"],
    "knowledge": ["adapters", "data"],
    "data": [],
    "infrastructure": ["adapters"],
    "operations": ["data"]
  },
  "quality_targets": {
    "max_complexity": 10,
    "min_coverage": 80,
    "max_coupling": 0.3,
    "p95_latency_ms": 3000,
    "fcr_target_pct": 50,
    "max_function_lines": 50,
    "service_health_timeout_ms": 500,
    "docker_startup_seconds": 60,
    "pii_recall_pct": 95,
    "pii_precision_pct": 99
  },
  "fr_module_traceability": {
    "FR-01": "app.models",
    "FR-02": "app.api.webhooks + app.adapters.telegram_adapter",
    "FR-03": "app.api.webhooks + app.adapters.line_adapter",
    "FR-04": "app.security.signature",
    "FR-05": "app.security.signature",
    "FR-06": "app.adapters.unified",
    "FR-07": "app.adapters.unified",
    "FR-08": "app.processing.sanitizer",
    "FR-09": "app.processing.pii_masker",
    "FR-10": "app.security.rate_limiter",
    "FR-11": "app.knowledge.matcher",
    "FR-12": "app.knowledge.escalation",
    "FR-13": "app.infrastructure.logger",
    "FR-14": "app.infrastructure.health",
    "FR-15": "docker-compose.yml",
    "FR-16": "queries/",
    "FR-17": "app.infrastructure.errors",
    "FR-18": "cross-cutting (ruff + radon enforcement)",
    "FR-19": "app.processing.pipeline",
    "FR-20": "app.adapters.unified",
    "FR-21": "app.infrastructure.config",
    "FR-22": "app.security.ip_whitelist"
  },
  "nfr_traceability": {
    "NFR-01": {"type": "performance", "target": "p95 < 3.0s", "module": "app.processing.pipeline"},
    "NFR-02": {"type": "security", "target": "webhook rejection before business logic", "module": "app.security.signature"},
    "NFR-03": {"type": "security", "target": "sanitization on every inbound message", "module": "app.processing.sanitizer"},
    "NFR-04": {"type": "security", "target": "PII recall >= 95%, precision >= 99%", "module": "app.processing.pii_masker"},
    "NFR-05": {"type": "security", "target": "rate limiter independent per-user buckets", "module": "app.security.rate_limiter"},
    "NFR-06": {"type": "reliability", "target": "health check < 500ms, 200 even when degraded", "module": "app.infrastructure.health"},
    "NFR-07": {"type": "maintainability", "target": "single-line JSON logs, level filtering", "module": "app.infrastructure.logger"},
    "NFR-08": {"type": "maintainability", "target": "ruff zero violations, CC <= 10", "module": "cross-cutting"},
    "NFR-09": {"type": "deployability", "target": "docker compose healthy within 60s", "module": "docker-compose.yml"},
    "NFR-10": {"type": "security", "target": "IP whitelist blocks before HMAC", "module": "app.security.ip_whitelist"}
  }
}
```
<!-- SAB:END -->

---

## 7. Architectural Decisions Summary

Key architectural decisions documented in `docs/adr/ADR-001-technology-stack.md`:

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | Python 3.12+ + FastAPI + PostgreSQL 16 + Redis 7 | Async-first stack; FastAPI provides raw body access for webhook verification; PostgreSQL JSONB + pgvector for Phase 2 RAG; Redis for atomic token bucket operations |
| ADR-002 | Six-layer architecture with unidirectional dependencies | Enforces separation of concerns; each layer testable in isolation; prevents circular imports; matches SPEC.md interceptor chain sequence |
| ADR-003 | Immutable dataclasses for core message types (`frozen=True`) | Prevents accidental mutation in pipeline; thread-safe for potential async concurrency; clear ownership of state transitions |

> See `docs/adr/` for full ADR records.

---

## 8. Dependency Graph (DAG)

```
  operations ──→ data
  transport ──→ security ──→ infrastructure
     │              │              │
     │              └──→ adapters ←┘
     │                      ↑
     └──→ processing ──────┤
              │              │
              └──→ knowledge ──→ data
```

All edges point downward. Zero circular dependencies. Verified DAG property.

---

*SAD Version: 1.0*
*Generated: 2026-05-23*
*Phase: 2 — Architecture Design*
*Next: Agent B (TECH_LEAD) review → quality_manifest.json generation → P3 handoff*
