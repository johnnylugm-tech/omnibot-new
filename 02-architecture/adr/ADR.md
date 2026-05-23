# Architecture Decision Records — OmniBot Phase 1

> Source SAD: `02-architecture/SAD.md` v1.0 (2026-05-23)
> Source SRS: `01-requirements/SRS.md` v1.0 (2026-05-23)
> Phase: 2 — Architecture Design
> Total ADRs: 7

---

## ADR-1: FastAPI as Web Framework

**Status**: Accepted

**Context**: OmniBot must expose asynchronous HTTP webhook endpoints for Telegram Bot API and LINE Messaging API (`POST /api/v1/webhook/telegram`, `POST /api/v1/webhook/line`) plus a health check endpoint (`GET /api/v1/health`). The framework must support raw byte-body access (needed for HMAC signature verification before any parsing), Pydantic validation, and automatic OpenAPI documentation generation. The system must handle concurrent webhook requests from multiple platforms.

**Decision**: Use **FastAPI 0.115+** with **uvicorn** as the ASGI server.

**Rationale**:
- **Native async support**: FastAPI is built on Starlette and `asyncio`, enabling non-blocking I/O for database queries, Redis operations, and outbound HTTP calls to platform APIs — critical for meeting NFR-01 (p95 < 3.0s).
- **Raw body access**: FastAPI supports `body: bytes` as a direct parameter type, allowing HMAC verification on the raw request body before JSON parsing (FR-04, FR-05).
- **Pydantic v2 integration**: Built-in request/response validation aligns with FR-06 (`UnifiedMessage`), FR-07 (`ApiResponse`), and FR-21 (Settings validation).
- **OpenAPI auto-generation**: Zero-effort API docs support testing and integration.
- **Dependency injection**: Enables clean wiring of `PipelineOrchestrator`, security interceptors, and platform adapters into route handlers.
- **Ecosystem**: Strong community, active maintenance, mature async database driver support (`asyncpg`, `redis.asyncio`).

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Flask | Synchronous WSGI framework; no native async support; requires `quart` fork for async; no built-in Pydantic validation |
| Django + DRF | Overly heavy for a webhook-only service; ORM-first design conflicts with async-first architecture; unnecessary admin, sessions, middleware overhead |
| aiohttp | Lacks built-in validation and OpenAPI support; requires more boilerplate for schema enforcement |

**Consequences**:
- + Async-first architecture matches the end-to-end request flow (webhook → processing pipeline → reply).
- + Automatic OpenAPI schema simplifies integration testing and platform partner onboarding.
- + Pydantic validation catches malformed payloads before they reach the pipeline (Stage 3 → 422).
- - Team members unfamiliar with ASGI/Starlette may face a learning curve around middleware ordering, lifespan events, and async context propagation.
- - Requires `pytest-asyncio` for all handler tests.

---

## ADR-2: PostgreSQL 16 for Persistent Storage

**Status**: Accepted

**Context**: OmniBot needs a relational database for 8 core tables (FR-01): `users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`. The schema includes JSONB columns for flexible metadata, GIN indexes for keyword array matching, and CTE queries for ODD analytics (FR-16). Phase 2 will require `pgvector` for embedding-based RAG. Phase 1 must include Phase 2/3 columns with defaults to avoid `ALTER TABLE` later.

**Decision**: Use **PostgreSQL 16** with the **pgvector/pgvector** Docker image and **asyncpg 0.30+** as the async driver, managed via **Alembic 1.14+** migrations.

**Rationale**:
- **CTE support**: ODD queries (FR-16: FCR rate, p95 latency, knowledge source distribution) use `WITH` clauses and `PERCENTILE_CONT(0.95)` — PostgreSQL's CTE and window function support is mature.
- **JSONB**: Flexible storage for `platform_configs.config`, `messages.raw_payload`, and Phase 3 `conversations.dst_state` without schema churn.
- **GIN indexes**: `idx_kb_keywords` uses GIN on `knowledge_base.keywords TEXT[]` for efficient `= ANY(keywords)` array matching (FR-11).
- **pgvector readiness**: The `pgvector/pgvector:pg16` image includes the `vector(384)` type pre-installed, matching the `paraphrase-multilingual-MiniLM-L12-v2` embedding dimension for Phase 2 RAG. Phase 1 creates the `embeddings` column with `NULL` default.
- **ACID guarantees**: Single-transaction writes for user/conversation/message inserts (SAD §5.2) ensure atomicity.
- **Strong ecosystem**: `asyncpg` is the fastest Python PostgreSQL driver with first-class async support.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| SQLite | No concurrent write support; no GIN index; no JSONB; unsuitable for multi-worker deployment |
| MySQL 8 | Weaker JSON support (no JSONB binary storage); no pgvector equivalent; CTE performance inferior for analytical queries |
| MongoDB | Document model mismatches the relational nature of users→conversations→messages→escalations; no CTE for ODD analytics |

**Consequences**:
- + Powerful analytical queries via CTE + window functions directly against operational tables (no ETL needed for ODD).
- + Phase 2 RAG is a column activation (`SET NOT NULL` + populate embeddings), not a migration — no `ALTER TABLE` downtime.
- + JSONB columns allow per-platform metadata and Phase 3 DST state without schema changes.
- - Requires a separate PostgreSQL container in the Docker Compose deployment (3-service minimum: api + postgres + redis).
- - `asyncpg` connection pool tuning needed for production load (pool size, timeout, keepalive).

---

## ADR-3: Redis 7 for Rate Limiting

**Status**: Accepted

**Context**: OmniBot must enforce per-platform per-user rate limiting via the Token Bucket algorithm (FR-10, NFR-05). Default capacity is 100 tokens with 100 tokens/second refill. The rate limiter must work across multiple API worker processes (horizontal scaling). Bucket state must be keyed as `{platform}:{user_id}` for independent per-user buckets.

**Decision**: Use **Redis 7** (`redis:7-alpine`) with **redis-py 5.x** (`redis.asyncio`) as the token bucket state store. Token consumption is atomic per `check()` call.

**Rationale**:
- **Atomic operations**: Redis `INCR`/`DECR` and `EXPIRE` (TTL) map directly to token bucket semantics — check token count, decrement if available, auto-reset via key TTL. No distributed locking needed.
- **Shared state**: Redis provides a single source of truth for rate limit state accessible from all API worker processes, enabling stateless horizontal scaling.
- **Sub-millisecond latency**: In-memory operations add negligible overhead to the per-request rate check (Stage 4 of the pipeline), critical for NFR-01 (p95 < 3.0s).
- **TTL-based bucket reset**: `EXPIRE bucket_key refill_interval` auto-resets buckets without a separate cleanup process.
- **Phase 2+ extensibility**: Redis Streams can be used for async processing in Phase 2 without changing infrastructure.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| In-memory dict | State lost on process restart; cannot share across multiple API workers; no TTL-based auto-cleanup |
| PostgreSQL advisory locks | Per-request rate check would contend on locks; pg_advisory_lock latency (~0.5ms) adds up under load; not designed for high-frequency atomic counters |
| PostgreSQL `pg_bouncer` + counter table | `UPDATE ... SET count = count - 1 WHERE ... RETURNING count` requires row-level locking; significantly slower than Redis INCR for 100+ req/s |

**Consequences**:
- + Fast, atomic token bucket operations with ~0.2ms latency.
- + Rate limit state shared across all API workers — stateless horizontal scaling.
- + Fail-open behavior when Redis is unreachable (log warning, allow request through) per SAD §3 L3 degradation.
- - Additional infrastructure dependency (3-service minimum: api + postgres + redis).
- - Redis data is ephemeral — token bucket state lost on restart (acceptable: rate limit resets are non-critical).

---

## ADR-4: Docker Compose for Local Dev and Deployment

**Status**: Accepted

**Context**: OmniBot Phase 1 requires a reproducible 3-service development environment (FR-15): `omnibot-api`, `postgres` (pgvector), and `redis`. Services must start in dependency order (postgres + redis healthy before api). The environment must reach `healthy` state within 60 seconds (NFR-09). Phase 3 will introduce Kubernetes for production, but Phase 1-2 use single-node deployment.

**Decision**: Use **Docker Compose v3.8** with per-service health checks (`pg_isready`, `redis-cli ping`, `/api/v1/health`) and `depends_on` with `condition: service_healthy`.

**Rationale**:
- **Single-command startup**: `docker compose up -d` brings up the entire stack. No manual dependency orchestration.
- **Health check gating**: `depends_on: condition: service_healthy` ensures the API only starts after PostgreSQL and Redis pass their health probes, preventing race-condition startup errors.
- **Volume management**: Named volumes for PostgreSQL data ensure data persistence across container restarts. `docker compose down -v` cleanly removes all volumes for a fresh start.
- **CI parity**: The same `docker-compose.yml` can be used in GitHub Actions / CI pipelines, ensuring dev-CI-prod parity.
- **Image pinning**: Explicit image tags (`pgvector/pgvector:pg16`, `redis:7-alpine`) guarantee reproducibility.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Kubernetes (k3s/minikube) | Overkill for 3-service setup; adds YAML complexity, ingress configuration, and node management with no Phase 1 benefit |
| Bare metal / venv | No reproducibility across developer machines; manual PostgreSQL + Redis installation; OS-specific setup drift |
| Docker Swarm | Declining ecosystem support; less community adoption than Compose for dev environments |

**Consequences**:
- + Identical environment on every developer machine (`docker compose up`).
- + Health-check-based startup ordering prevents "API started before DB ready" race conditions.
- + CI can run integration tests against the same Compose file.
- - Docker daemon required on all developer machines (resource overhead on lower-spec hardware).
- - Single-node design — no built-in load balancing or auto-scaling (deferred to Phase 3 Kubernetes).

---

## ADR-5: Pipeline Orchestrator Pattern

**Status**: Accepted

**Context**: OmniBot's core message processing flow consists of 11 sequential stages (FR-19): IP Whitelist → Webhook Signature → Platform Adapter Parse → Rate Limiter → Input Sanitization → PII Masking → Knowledge Matching → Escalation → Construct Response → Send Reply → Structured Logging. Each stage can fail independently, and a failure at any stage must not crash the pipeline. Errors must be mapped to standardized error codes (FR-17).

**Decision**: Implement a **sequential pipeline** with per-stage error isolation via `PipelineOrchestrator.process()`. Each stage returns an `Either[Error, Success]`-style result; the orchestrator catches exceptions, maps them to error codes, logs them, and short-circuits the pipeline with the appropriate `ApiResponse`.

**Rationale**:
- **Independent testability**: Each stage is a standalone callable with explicit input/output types. Unit tests can verify each stage in isolation (e.g., `InputSanitizer.sanitize("ＴＥＳＴ") == "TEST"`) without standing up the full pipeline.
- **Explicit data flow**: The pipeline composition is linear and explicit — stage N+1 receives stage N's output as input. No hidden side effects or event bus magic.
- **Error isolation**: A `try/except` wrapper at each stage boundary ensures a failure in stage N (e.g., PII masking regex explosion) does not cascade to stage N+1. The orchestrator catches, maps to an error code, logs, and returns.
- **Short-circuit semantics**: Security rejections (IP 403, HMAC 401, rate limit 429) stop the pipeline immediately — no wasted processing after a security gate rejects.
- **Observability**: Each stage can be timed independently, and the structured log at Stage 11 captures per-stage timing for latency analysis.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Event-driven (Pub/Sub) | Linear message processing doesn't benefit from event choreography; adds broker dependency (Redis Streams / RabbitMQ) with no Phase 1 value; harder to trace end-to-end request flow |
| Middleware chain (ASGI middleware) | Harder to test stages in isolation; middleware ordering is implicit and error-prone; cannot easily short-circuit between security and processing stages |
| Actor model | Concurrency model adds complexity for a strictly sequential flow; each message is processed independently — no shared state between concurrent requests |

**Consequences**:
- + Each stage is a standalone, independently testable unit.
- + Explicit, readable data flow — no hidden dependencies between stages.
- + Short-circuit security gates (IP → HMAC → rate limit) block early, saving downstream compute.
- + Per-stage timing and error tracking for observability.
- - Sequential execution is not parallelizable per-request (but each request is I/O-bound, not CPU-bound, so sequential execution is not a bottleneck).
- - Adding a new stage requires modifying the orchestrator's stage list (acceptable: stages change infrequently and are defined by the architecture).

---

## ADR-6: Platform Adapter Pattern

**Status**: Accepted

**Context**: OmniBot must support Telegram Bot API (FR-02) and LINE Messaging API (FR-03) with a unified internal format. Messenger and WhatsApp are deferred to Phase 2. Each platform has a distinct webhook payload structure, authentication mechanism, and reply API. All downstream processing (sanitization, PII masking, knowledge matching, logging) must operate on platform-agnostic types.

**Decision**: Implement the **adapter pattern** with a `Platform` enum (`TELEGRAM`, `LINE`), a common `UnifiedMessage` and `UnifiedResponse` frozen dataclass, and per-platform adapter classes (`TelegramAdapter`, `LineAdapter`) each implementing a standard interface: `parse_message(payload: dict) -> UnifiedMessage` and `send_reply(response: UnifiedResponse) -> bool`.

**Rationale**:
- **Platform extensibility**: Adding a new platform (e.g., Messenger in Phase 2) requires only implementing a new adapter with `parse_message` + `send_reply`. No changes to the pipeline, knowledge layer, security layer, or logging.
- **Isolated complexity**: Platform-specific quirks (Telegram's `message_id` vs LINE's `reply_token`, different signature verification algorithms) are contained within their respective adapter modules.
- **Immutable core types**: `UnifiedMessage` and `UnifiedResponse` are `@dataclass(frozen=True)` — no mutation after construction. This prevents accidental modification of message data as it flows through the pipeline, ensuring thread safety and clear ownership of state.
- **Unified routing**: The webhook layer routes by `POST /api/v1/webhook/{platform}` and selects the adapter by `Platform` enum. The `PipelineOrchestrator` receives a `UnifiedMessage` and never knows which platform originated the request.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Platform-specific endpoints with diverging logic | Code duplication across platforms; knowledge layer would need per-platform branches; adding a platform requires changes in every layer |
| Generic webhook parser with configuration | Cannot handle platform-specific quirks (LINE's reply_token, Telegram's callback_query); configuration-driven parsing becomes a poorly-specified DSL |
| Inheritance hierarchy (BaseMessage → TelegramMessage, LineMessage) | Violates the principle that downstream code should be platform-agnostic; requires `isinstance` checks throughout the pipeline |

**Consequences**:
- + Adding a new platform requires only one new module (adapter) implementing a well-defined interface.
- + Platform-specific complexity is fully contained — pipeline and knowledge layers have zero platform awareness.
- + Immutable dataclasses prevent accidental mutation and enable safe concurrent access.
- - Each adapter must be maintained when its platform API changes (e.g., LINE deprecating a field, Telegram adding a new message type).
- - Adapter interface must remain stable — changes to `UnifiedMessage` or `UnifiedResponse` fields affect all adapters.

---

## ADR-7: Interceptor Chain Order

**Status**: Accepted

**Context**: Per SPEC.md §Interceptor Sequence and SECURITY.md, the security interceptor chain must execute in a fixed order for DDoS protection and correct per-user rate limiting. The four interceptors are: IP Whitelist (FR-22), Webhook Signature Verification (FR-04/FR-05), Platform Adapter Parse (FR-02/FR-03), and Rate Limiter (FR-10). Each interceptor rejects with a specific HTTP status and error code on failure.

**Decision**: Execute interceptors in this fixed order: **IP Whitelist → HMAC Signature Verification → Platform Adapter Parse → Rate Limiter → Processing Pipeline**.

```
TLS (reverse proxy)
  → IP Whitelist (FR-22)           → 403/400 on reject
    → HMAC Signature (FR-04/05)    → 401 on reject
      → Platform Adapter Parse     → 422 on reject
        → Rate Limiter (FR-10)     → 429 on reject
          → Processing Pipeline
```

**Rationale**:
- **IP Whitelist first**: IP check is the cheapest operation (string comparison against CIDR list). It blocks unauthorized traffic before any cryptographic computation (HMAC), preventing DDoS via HMAC exhaustion. If an attacker's IP is not in the whitelist, they never reach the costly `hmac.compare_digest()` call.
- **HMAC second**: Signature verification authenticates the request origin. Invalid signatures are rejected before any message body parsing (zero-trust boundary). This prevents processing of spoofed or tampered payloads.
- **Adapter parse third**: The rate limiter needs `platform` and `user_id` from the parsed `UnifiedMessage` to construct the bucket key `{platform}:{user_id}`. Parsing must happen before rate limiting because the rate limiter cannot identify the user without parsing the message.
- **Rate limiter fourth (last interceptor)**: Rate limiting is the final security gate before the processing pipeline. Once through, the request enters the computationally heavier stages (sanitization, PII masking, knowledge matching, escalation).
- **Coherent with error model**: Each interceptor maps to a specific HTTP status (403/400 → 401 → 422 → 429) in a progression from network-level to application-level rejection.

**Alternatives considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Rate limit before parse | Cannot identify the user without parsing; would require rate limiting by IP alone, which is easily bypassed via shared IPs (corporate NAT, VPN) |
| HMAC before IP check | Attackers with invalid signatures can trigger expensive cryptographic operations; DDoS vector — thousands of invalid HMAC requests exhaust CPU |
| Parse before HMAC | Violates zero-trust: parsing untrusted input before authentication is a security risk; malformed payloads could exploit parser vulnerabilities |

**Consequences**:
- + DDoS-resistant: unauthorized IPs never reach HMAC computation, preventing CPU exhaustion attacks.
- + Correct per-user rate limiting: user identity is available from the parsed message before the rate limiter check.
- + Clear separation of concerns: network security → authentication → parsing → application-level rate limiting.
- + Aligned with defense-in-depth: each layer provides an independent security control.
- - Parse happens before rate limit, so a small amount of CPU is spent on JSON parsing even for rate-limited users. This is a minor cost — JSON parsing of a short text message is sub-millisecond and does not meaningfully reduce DDoS protection.
- - Adding a new interceptor (e.g., Phase 3 RBAC) requires understanding its position in the sequence relative to existing interceptors.

---

## Decision Traceability Matrix

| ADR | Decision | SAD § Reference | FR Coverage | NFR Coverage |
|-----|----------|-----------------|-------------|--------------|
| ADR-1 | FastAPI + uvicorn | §4 Technology Choices | FR-02, FR-03, FR-07, FR-14, FR-21 | NFR-01 |
| ADR-2 | PostgreSQL 16 + asyncpg | §4 Technology Choices | FR-01, FR-11, FR-12, FR-16 | NFR-08 |
| ADR-3 | Redis 7 for rate limiting | §4 Technology Choices | FR-10 | NFR-01, NFR-05 |
| ADR-4 | Docker Compose v3.8 | §4 Technology Choices, §2.18 | FR-15 | NFR-09 |
| ADR-5 | Pipeline Orchestrator | §2.10, §5.1 | FR-19 | NFR-01, NFR-06 |
| ADR-6 | Platform Adapter Pattern | §2.5-2.7, §1.2 Design Principle 5 | FR-02, FR-03, FR-06, FR-20 | NFR-08 |
| ADR-7 | Interceptor Chain Order | §1.3, §5.1 | FR-04, FR-05, FR-10, FR-22 | NFR-02, NFR-05, NFR-10 |

---

*ADR Version: 1.0*
*Generated: 2026-05-23*
*Phase: 2 — Architecture Design*
*Next: quality_manifest.json generation → Agent B (TECH_LEAD) review → P3 handoff*
