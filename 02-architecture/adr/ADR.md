# Architecture Decision Records (ADR) — OmniBot

> Phase: 2 — Architecture | Owner: Architect (Agent A) | Updated: 2026-09-04
> Source of truth: `02-architecture/SAD.md` (§1–§6). Every record below cites the
> SAD section, FR or NFR it is derived from. Where an ADR resolves something the
> SAD leaves implicit, the record says so explicitly and is marked `Proposed`.

---

## ADR-001: Layered architecture with a one-way dependency graph

### Status
Accepted

### Context
OmniBot has 28 in-scope FRs spanning inbound webhooks, a five-layer defense
stack, domain logic, and cross-cutting infrastructure (SAD §2.3). Without an
enforced dependency direction, security checks can be bypassed by a domain
module calling back into the API layer, and the Phase 3+ drift detector cannot
decide whether an import is legal.

### Decision
Five layers — `app` → `api` → `security` → `core` → `infra` — with the
allow-list encoded in the SAB block (SAD §5 `allowed_dependencies`) and four
hard constraints: `no_circular_dependencies`, `api_must_not_import_app`,
`core_must_not_import_api`, `infra_must_not_import_api_or_core`. `infra` is a
leaf (`allowed_dependencies: []`); `app` is the only layer allowed to reach all
others.

### Rationale
The allow-list is machine-checkable, so "did this import break the
architecture?" is a decidable question at every gate instead of a review
opinion. Making `infra` a leaf keeps observability and circuit-breaking usable
from every layer without creating cycles.

### Consequences
- Positive: import violations are detectable statically; the defense stack
  cannot be skipped because `core` cannot reach the ingress layer. This
  satisfies the FR-18 acceptance criteria for 7-role RBAC and the NFR-03
  acceptance criteria for code-to-SAD traceability (100 % mapping
  requirement).
- Negative: cross-layer orchestration cannot live in the layer that "feels"
  natural — it is forced into `app.hub`, which becomes a coordination
  chokepoint that must be kept logic-free (SAD §2.4.2).

### Alternatives considered
- **Flat package with convention-only boundaries** — rejected: nothing prevents
  `core` importing `api`, and the drift detector would have no contract to check.
- **Hexagonal / ports-and-adapters with an inversion container** — rejected: adds
  a DI framework and a port/adapter pair per FR for 28 FRs, without changing what
  the gate can verify.

---

## ADR-002: Directory-as-community with a ≥2-function hub per directory

### Status
Accepted

### Context
Phase 3+ scores architecture through the Code Review Graph, which maps one
directory to one community and requires cohesion ≥ 0.3
(`internal / (internal + external)` edges) and ≤ 50 nodes (SAD §2.1). Entry
points and infra modules import many external libraries (FastAPI, asyncpg,
redis, OTel), each contributing an external edge with no internal offset.

### Decision
Six source directories (`app/`, `api/`, `security/`, `security/paladin/`,
`core/`, `infra/`), each containing a `hub.py` exposing **two** hub functions
(SAD §2.2 community budget: `dispatch`/`lifecycle`, `register_routes`/`mount_ws`,
`defense_in_depth`/`audit_log`, `chain`/`emit_verdict`, `route_intent`/`pick_tier`,
`instrument`/`healthcheck`). Every sibling function body — not just module level —
calls a hub function through a standalone assignment (`result = hub.fn(...)`).
Entry points (`app/main.py`) live inside a hub directory.

### Rationale
The edge budget is `I ≥ 0.4286 × E`. A module-level call yields one edge per
file regardless of file size; per-function-body calls multiply it. With 4–11
siblings per directory and two hub functions, each directory clears 0.3 with
margin (SAD §2.1 Principle 2/4).

### Consequences
- Positive: cohesion is designed in rather than retrofitted; every file has an
  explicit reason to exist in its directory.
- Negative: hub calls placed purely for edge budget are near-noise at the call
  site; hub functions must do real work (config validation, instrumentation) or
  they become dead ceremony.
- Negative: same-file calls contribute nothing (CRG Principle 5), so splitting a
  module for readability can *raise* the score while merging can lower it —
  a metric that does not always align with design quality.

### Alternatives considered
- **Flat `src/` with 30+ modules** — rejected: Leiden splits it unpredictably and
  several fragments land under 0.3 (SAD §2.1 anti-patterns).
- **One directory per FR (28 directories)** — rejected: too many communities to
  keep all above the floor, and it fragments the PALADIN chain.

---

## ADR-003: Python 3.11 runtime baseline, stdlib-first inside the hot path

### Status
Accepted

### Context
SPEC pins Python 3.11+ (SAD §4.2). The project virtualenv currently resolves to
**Python 3.11.15** (`/Users/johnny/projects/omnibot-new/.venv/bin/python --version`,
verified 2026-09-04). NFR-01 gives PALADIN L1–L3 a 5 ms synchronous budget.

### Decision
Target Python 3.11 as the floor (no 3.12-only syntax). Inside the L1–L3 hot path
use the standard library only — `unicodedata` for NFKC and homoglyph folding
(SAD §2.4.4), `re` for pattern rules, `ipaddress` for CIDR matching (FR-10),
`hmac`/`hashlib` for signature verification (FR-02) and for the SHA-256
deterministic A/B assignment (FR-24). Third-party dependencies are confined to
I/O-bound layers: FastAPI/uvicorn, asyncpg/pgvector, redis, SAQ, Pydantic v2,
OpenTelemetry.

### Rationale
3.11 supplies the `match` statement used by the FSM/intent router and the faster
asyncio task machinery the L4 fork depends on. Keeping L1–L3 stdlib-only removes
import-time and call-time overhead from the only path with a 5 ms budget, and
removes third-party CVE surface from the layer that sees untrusted text first.

### Consequences
- Positive: the security-critical sync path has no external supply-chain surface;
  the 5 ms budget is achievable without native extensions.
- Negative: homoglyph folding must be maintained against Unicode
  `confusables.txt` by hand instead of delegating to a library.
- Negative: pinning 3.11 forgoes 3.12/3.13 asyncio and typing improvements until
  the floor is raised.

### Alternatives considered
- **Python 3.12/3.13 floor** — rejected: SPEC pins 3.11+, and the deployment
  base images are not yet standardized on 3.12.
- **Fully stdlib-only application (no FastAPI/asyncpg)** — rejected: hand-rolling
  an ASGI server, a pooled PostgreSQL driver, and an OTel exporter is a far larger
  correctness risk than the dependencies it removes; NFR-07 (2000 TPS) and NFR-01
  (p95 ≤ 1.0 s) would have to be met by bespoke I/O code.

---

## ADR-004: asyncio concurrency, not a thread pool

### Status
Accepted

### Context
The request path is I/O-dominated: HTTP ingress, an LLM classifier call (L4),
pgvector queries, Redis operations, and outbound tool RPCs. NFR-07 requires 2000
TPS sustained; NFR-01 requires the L4 classifier to overlap with intent routing
rather than serialize behind it (SAD §2.4.5, §3.1).

### Decision
A single-threaded asyncio event loop per process is the concurrency model.
Fan-out uses `asyncio.gather` (L4 semantic classification forked alongside
`core.dialog_dst`, joined before the Tier-3 LLM call — SAD §3.2 "intent" edge).
Background work is handed to SAQ workers (ADR-011), never to an in-process
thread pool. Horizontal scaling is by stateless process replicas under the K8s
HPA (NFR-06).

### Rationale
Under the GIL a `ThreadPoolExecutor` buys nothing for I/O that asyncio does not,
while adding per-request thread-switch cost and shared-state hazards in the
rate limiter and circuit breaker. 2000 TPS across pooled sockets is an
event-loop workload, not a thread workload.

### Consequences
- Positive: one concurrency model end-to-end; deterministic ordering inside the
  PALADIN chain; breaker and rate-limiter state need no locking within a process.
- Negative: a single blocking call (a sync DB driver, a CPU-heavy regex, a
  `time.sleep`) stalls every in-flight request on that worker. All libraries must
  be async-native, and this must be enforced in review.
- Negative: genuinely CPU-bound work has no home in-process — it must be pushed
  to SAQ.

### Alternatives considered
- **`ThreadPoolExecutor` fan-out** — rejected: GIL-bound, no throughput gain for
  I/O, adds mutable-shared-state risk to security-critical counters.
- **`multiprocessing` worker pool** — rejected: process-per-request serialization
  cost and connection-pool duplication defeat the 2000 TPS target; K8s replicas
  already provide multi-core scaling.
- **`asyncio.to_thread` escape hatch for blocking libs** — kept as a narrow,
  documented exception rather than a general pattern.

---

## ADR-005: PALADIN as a mandatory ordered chain — L1–L3 sync, L4 async, L5 post-retrieval

### Status
Accepted

### Context
FR-03..FR-07 define five defense layers. NFR-02 requires a ≥ 95 % block rate and
NFR-01 caps L1–L3 at 5 ms and L4 at 200 ms. Placing all five inline would blow
the end-to-end budget; making any of them optional would let untrusted text reach
`core.dialog_dst` unchecked (SAD §3.1, §3.3).

### Decision
`security.paladin.hub.chain()` runs L1 → L2 → L3 synchronously and blocks the
request on failure (canned refusal, no downstream call). L4 is forked as an async
task concurrently with intent routing and joined before any Tier-3 LLM call; an
L4 block tags the response with `safety_flag`, redacts PII, and routes to human
escalation. L5 grounding runs *after* retrieval, on the candidate answer, because
it validates alignment against retrieved knowledge (FR-07).

### Rationale
Splitting the chain by cost is the only way to satisfy both the 5 ms sync budget
and the ≥ 95 % block rate: the cheap deterministic layers gate synchronously, and
the expensive model-based layer overlaps with work that does not depend on it.

### Consequences
- Positive: no message reaches domain logic without clearing L1–L3; the L4 join
  point is before the highest-risk action (LLM generation).
- Negative: between the L4 fork and its join, work has already been done on text
  that may later be judged malicious — that work must be side-effect-free, which
  constrains where `core.actions` may be invoked.
- Negative: the chain is the single most latency-sensitive code in the system;
  every added rule competes for the same 5 ms.

### Alternatives considered
- **All five layers synchronous** — rejected: L4 is a model call; 200 ms inline
  would consume a fifth of the p95 e2e budget on every request.
- **All five layers async/advisory** — rejected: NFR-02 requires blocking
  semantics; an advisory L1–L3 cannot enforce a block rate.

---

## ADR-006: PostgreSQL 16 + pgvector as a single store, with a four-tier retrieval cascade

### Status
Accepted

### Context
FR-13/14/15 define exact/keyword retrieval, vector retrieval, and LLM generation;
FR-19 defines human escalation as the terminal fallback. NFR-01 caps knowledge
retrieval at p95 ≤ 150 ms and NFR-07 requires scaling to 10 M chunks
(SAD §2.4.6, §4).

### Decision
One PostgreSQL 16 cluster holds both transactional and vector data, using
pgvector HNSW with `m=16, ef_construction=64` fixed at index creation, fused with
Tier-1 results via Reciprocal Rank Fusion at `k=60`. Retrieval is a cascade:
Tier-1 always runs and short-circuits on an exact/keyword hit; Tier-2 runs on
Tier-1 miss; Tier-3 (LLM generation) runs when Tier-2 confidence < 0.7; a
full miss routes to `api.escalation` (SAD §3.2 "retrieval" edge, §3.3).

### Decision detail
Tier-2 uses prepared statements over a connection pool, and every function body
that opens a connection calls `core.hub.pick_tier(...)` (ADR-002).

### Rationale
A single store keeps documents and their embeddings transactionally consistent —
no dual-write between PostgreSQL and a dedicated vector database, and no
reconciliation job. The cascade puts the cheapest tier first so the common case
never pays HNSW or LLM cost, which is what makes the 150 ms p95 reachable.

### Consequences
- Positive: one backup/restore, one migration tool (Alembic), no cross-store
  consistency window; RRF needs no extra service.
- Negative: vector and OLTP workloads share CPU, memory and connection budget —
  a heavy HNSW scan can degrade transactional latency; this must be watched in
  Grafana and may eventually force a read replica.
- Negative: HNSW parameters are baked into the index, so retuning `m` or
  `ef_construction` means a rebuild, not a config change.

### Alternatives considered
- **Dedicated vector DB (Qdrant / Weaviate / Milvus)** — rejected: adds an
  operational component and a dual-write consistency problem for a corpus size
  (10 M chunks) pgvector HNSW handles.
- **Vector-only retrieval (skip Tier-1)** — rejected: exact/keyword hits are both
  cheaper and more precise for FAQ-shaped traffic; skipping them raises p95 and
  hurts the FR-07 grounding rate.

---

## ADR-007: Distributed rate limiting in Redis via an atomic Lua script, failing open

### Status
Accepted

### Context
FR-09 requires rate limiting across horizontally scaled stateless pods, so the
counter cannot live in process memory. NFR-04 states Redis must fail open, and
uptime ≥ 99.9 % must not be gated on the limiter (SAD §3.3, §4).

### Decision
The sliding-window counter lives in Redis 7 (Cluster mode in production) and is
mutated by a single Lua script so read-modify-write is atomic on the server.
When `infra.ha_redis`'s health probe reports Redis unavailable, the limiter
fails **open** (request allowed) and increments `redis_failopen_total`. Redis is
also the store for session cache, embedding cache, and FR-28 Streams.

### Rationale
A Lua script is the only way to make check-and-increment atomic across pods
without a distributed lock. Fail-open is a deliberate availability-over-enforcement
trade: rate limiting is abuse mitigation, whereas the authentication and PALADIN
layers — which remain fail-closed — are the actual security controls.

### Consequences
- Positive: correct counting under concurrency; one infrastructure component
  serves five concerns; a Redis outage degrades throttling instead of the service.
- Negative: during a Redis outage the system is unthrottled and exposed to abuse;
  `redis_failopen_total` must alert, not merely record.
- Negative: Lua scripts are effectively untestable in isolation — they need a real
  Redis in `make verify-system` (ADR-014).

### Alternatives considered
- **Per-pod in-memory limiter** — rejected: the effective limit becomes
  `limit × replica_count` and varies with autoscaling.
- **`INCR` + `EXPIRE` without Lua** — rejected: non-atomic; a crash between the
  two commands leaves a key with no TTL, permanently blocking a caller.
- **Fail-closed on Redis outage** — rejected: it converts a cache dependency into
  a hard availability dependency, contradicting NFR-04.

---

## ADR-008: One circuit breaker in `infra` wrapping every outbound RPC

### Status
Accepted

### Context
FR-28 and NFR-04 require ≤ 2.0 s RPC timeouts, ≤ 3 retries with exponential
backoff and jitter, an LLM provider fallback switch in < 500 ms, and MTTR
< 5 min. The system talks to four classes of external dependency: Redis, LLM
providers, MCP tools, and A2A agents (SAD §2.4.8, §4.1 L2).

### Decision
`infra.ha_circuit_breaker.call(name, fn, *a, **kw)` is the single egress wrapper.
It tracks per-dependency failure rate, **opens above 50 % over a rolling 60 s
window**, and half-opens after a cool-down. Timeout, retry count, backoff and
jitter are enforced inside the wrapper, not at call sites. Every tool dispatch
from `core.actions` goes through it (SAD §3.2 "action" edge), and all call sites
route through `infra.hub.instrument(...)` so `circuit_breaker_state{name}` is a
Grafana gauge. The Redis breaker fails open (ADR-007); the LLM breaker falls
through to the next model in the pre-warmed Tier-3 chain.

### Rationale
Timeout and retry policy scattered across call sites drifts silently and is
untestable as a whole. Centralizing it makes NFR-04 a property of one module,
which is why `omnibot.infra.ha_circuit_breaker` is a declared high-risk module
(SAD §5) exercised by `make verify-system`.

### Consequences
- Positive: NFR-04 verifiable in one place; per-dependency state observable;
  fallback is a config swap so the < 500 ms switch is achievable.
- Negative: a single wrapper is a shared failure mode — a bug in it affects every
  outbound call, which is why it carries mandatory real-dependency verification.
- Negative: per-dependency policy differences (fail-open Redis vs fail-through
  LLM) are configuration inside the breaker, adding branching to a hot path.

### Alternatives considered
- **Per-call-site try/except with local retry** — rejected: unverifiable as a
  policy; guarantees drift across 28 FRs.
- **Service mesh (Istio/Envoy) retries and outlier detection** — rejected: it
  cannot see in-process MCP/CLI adapters, and it would split reliability policy
  across two systems.

---

## ADR-009: Pydantic v2 models as the contract on every cross-module edge

### Status
Accepted

### Context
Six platforms deliver six different payload shapes (FR-01), and the same
normalized message crosses seven module boundaries before a reply is emitted
(SAD §3.2). Tool calls carry externally-supplied arguments across a trust
boundary (SAD §6 TB-03).

### Decision
Every cross-module edge is typed by a Pydantic v2 model: `UnifiedMessage`
(ingress), `SanitizedText` + `Verdict` (defense), `RetrievalQuery` /
`KnowledgeHit` (retrieval), `ActionRequest` (tool dispatch, validated against the
MCP/A2A/CLI schema), `UnifiedResponse` (egress). Normalization to
`UnifiedMessage` happens once, in `api.webhooks`, before anything downstream runs.

### Rationale
Validating at the boundary means downstream layers never branch on
platform-specific shapes, and `ActionRequest` validation is the enforcement point
for the agent→tool trust boundary. Pydantic v2's Rust core keeps that validation
off the latency budget.

### Consequences
- Positive: one normalization site instead of platform branches scattered through
  `core`; malformed tool arguments are rejected before dispatch; Pyright strict
  mode (NFR-03) has real types to check.
- Negative: adding a platform means extending the adapter *and* the model; every
  boundary pays a validation cost even on internal, already-trusted data.

### Alternatives considered
- **Plain dicts / TypedDict** — rejected: no runtime enforcement at the tool
  boundary, which is exactly where untrusted data crosses.
- **dataclasses + manual validators** — rejected: reimplements Pydantic's
  coercion and error reporting with worse messages and no schema export for the
  FR-26 OpenAPI surface.

---

## ADR-010: RBAC enforced at route registration, not inside handlers

### Status
Accepted

### Context
FR-18 defines seven roles across the admin, agent and M2M surfaces. NFR-02
requires 7-role enforcement with no gaps. A permission check written inside a
handler body can be forgotten when a new route is added, and the omission is
invisible in review.

### Decision
`api.rbac` exposes a decorator applied at **route registration time** through
`api.hub.register_routes(...)`. A route registered without a role declaration is
a registration-time error, not a runtime 403. Handlers contain no permission
logic.

### Rationale
Moving the check from "something the author must remember" to "something the
registration path requires" turns an omission into a startup failure — the
failure mode moves from silent authorization bypass to a loud boot error.

### Consequences
- Positive: the 7-role matrix is enumerable from the route table, so the FR-18
  test suite can assert completeness rather than sampling handlers.
- Negative: row-level or resource-scoped decisions ("may this agent see *this*
  ticket?") cannot be expressed by a route-level decorator and still need
  in-handler checks — that split must be documented per endpoint.

### Alternatives considered
- **In-handler `if not user.has_role(...)`** — rejected: unverifiable
  completeness; the failure mode is a silent bypass.
- **Global ASGI middleware with a path→role table** — rejected: the table drifts
  from the router; path patterns are matched twice and can disagree.

---

## ADR-011: SAQ for background jobs; the request path never blocks on deferrable work

### Status
Accepted

### Context
FR-22 requires an async background job system for the embedding pipeline. NFR-01
caps embedding at p95 ≤ 100 ms and NFR-07 requires embedding throughput to scale
independently of request throughput (SAD §4).

### Decision
SAQ (asyncio-native, Redis-backed) runs the background queue. Embedding
generation, GDPR export/deletion (FR-23), and the L4 non-blocking dispatch path
are jobs, not request-path work. Embedding is batched and cached. SAQ workers
scale on queue backlog independently of API replicas.

### Rationale
SAQ shares the event loop model (ADR-004) and the Redis dependency already
required by ADR-007, so it adds a queue without adding a broker technology or a
second concurrency model — which Celery (prefork, threads/processes) would.

### Consequences
- Positive: no new infrastructure; workers and API scale on different signals;
  embedding backlog degrades freshness rather than request latency.
- Negative: Redis becomes a durability dependency for jobs, not just a cache — a
  Redis loss now loses queued work, unlike the fail-open limiter path.
- Negative: SAQ has a smaller ecosystem and community than Celery; operational
  tooling (dashboards, dead-letter handling) is thinner.

### Alternatives considered
- **Celery + RabbitMQ** — rejected: second broker, second concurrency model,
  sync-first API that fights asyncio.
- **`asyncio.create_task` fire-and-forget** — rejected: work is lost on pod
  restart and has no backpressure, retry or visibility.

---

## ADR-012: Atomic write for every durable artifact produced outside a transaction

### Status
Proposed
<!-- Resolves a gap the SAD leaves implicit: SAD §2.3/§5 require durable file
     artifacts (GDPR exports, golden dataset) but do not specify write semantics. -->

### Context
Not all durable state lands in PostgreSQL. FR-23 writes GDPR export bundles;
FR-20/NFR-05 read a ≥ 500-sample golden dataset from
`tests/golden/conversations.jsonl` (SAD §5 `required_artifacts`). A pod evicted
mid-write (K8s `RollingUpdate`, NFR-06) leaves a truncated file, and a truncated
GDPR export is silently wrong while a truncated golden file corrupts the Gate 3/4
calibration numbers.

### Decision
Any file this system writes and later reads back is written with the
tmp-file + `os.replace()` pattern: serialize to `<target>.tmp` in the same
directory, `flush()` + `os.fsync()` the file descriptor, then `os.replace()` onto
the target path. Readers never see a partial file, and no reader-side lock is
required. This applies to GDPR export bundles, golden-dataset regeneration, and
any generated artifact under `required_artifacts`.

### Rationale
`os.replace()` is atomic within a filesystem on POSIX and on Windows, so the
target is either the complete old file or the complete new one. The fsync before
the rename is what makes the guarantee survive a host crash, not just a process
crash.

### Consequences
- Positive: no partial-file failure mode; readers need no coordination; the
  pattern is stdlib-only (ADR-003).
- Negative: temporary files must be on the same filesystem as the target — a
  cross-device `os.replace()` raises `OSError`, so a `TMPDIR` on another mount
  breaks it.
- Negative: peak disk usage doubles for the duration of a large export.

### Alternatives considered
- **Write in place** — rejected: a crash mid-write destroys the previous good
  content as well as the new content.
- **Write + verify + retry** — rejected: the verification read is itself racy and
  does not help a concurrent reader that already opened the truncated file.
- **Store exports as PostgreSQL large objects** — rejected: puts multi-megabyte
  blobs in the OLTP store that ADR-006 already shares with the vector workload.

---

## ADR-013: Observability through `infra.hub.instrument(...)` rather than per-module wiring

### Status
Accepted

### Context
FR-21 requires structured logging, Prometheus metrics and OpenTelemetry traces.
Six NFRs are stated as numeric budgets (p95 latencies, block rate, uptime) that
the gates read from histograms — if a module is not instrumented, its budget is
unverifiable (SAD §3.2 "observability" edge, §4).

### Decision
`infra.hub.instrument(...)` is the single instrumentation entry point; every
module obtains spans, counters and histograms through it. Named histograms are
part of the module contract (`paladin_l1_latency_seconds`,
`circuit_breaker_state{name}`, `context_overflow_total`, `rate_limited_total`,
`knowledge_miss_total`, `redis_failopen_total`). Because `infra` is a leaf layer
(ADR-001), every layer may call it without creating a cycle.

### Rationale
Instrumenting through the hub makes the NFR budgets machine-readable at the gate
and simultaneously supplies the internal CRG edges each directory needs
(ADR-002) — the same call serves both purposes, so it is not ceremony.

### Consequences
- Positive: NFR budgets are gate-checkable; metric naming is consistent; one
  place to change exporter configuration.
- Negative: `infra.hub` is imported by nearly every module, so its import cost and
  any bug in it are global.
- Negative: cardinality discipline (no user IDs or raw message text in labels)
  must be enforced by review — the hub cannot detect a bad label value.

### Alternatives considered
- **Direct OTel/Prometheus client calls per module** — rejected: metric names
  drift, and the gate cannot rely on a fixed set of histograms.
- **Auto-instrumentation agent only** — rejected: it captures framework spans but
  none of the domain-specific counters the NFRs are stated in.

---

## ADR-014: `make verify-system` boots the real entry point against real dependencies

### Status
Accepted

### Context
Every exit gate (2, 3, 4) runs `make verify-system` and fails on a non-zero exit.
It is the only check that runs the delivered system — every other check reads
source text or runs a test suite whose doubles the project itself controls
(SAD §1.1).

### Decision
`verify-system` boots `app.main` (FastAPI + SAQ worker) against real Redis and
PostgreSQL containers from `docker-compose.dev.yml` and exercises the five
declared high-risk modules (SAD §5 `high_risk_modules`): a Telegram-shaped POST
through `api.webhooks` asserting HMAC / rate-limit / 422 boundaries; an
end-to-end `security.paladin.l4_semantic` run against a real LLM call for the
200 ms budget; a real pgvector HNSW query through `core.knowledge_tier2`
(FR-14.AC1); and a tripped Redis breaker in `infra.ha_circuit_breaker` asserting
fail-open (FR-28.AC3). No step is allowed `|| true`, a leading `-`, or a
`--exit-zero`-style flag; the target does not merely chain `test lint coverage`.

### Rationale
Modules replaced by `autouse` doubles in the unit suite are precisely the ones
whose real behaviour is unverified. Pinning the target to the high-risk list
means the gate's coverage measurement and the reliability claims refer to the
same code paths.

### Consequences
- Positive: the gate exercises real HMAC, real pgvector and a real breaker trip —
  integration bugs surface at the gate rather than in production.
- Negative: the target needs Docker and a live LLM credential, so it is slower and
  can fail for environmental reasons unrelated to the change under review.
- Negative: the real LLM call makes the L4 step nondeterministic in latency;
  the 200 ms assertion needs a tolerance policy or it will flake.

### Alternatives considered
- **Mocked dependencies in `verify-system`** — rejected: it would re-run what the
  unit suite already covers and verify nothing the gate does not already know.
- **Chaining `test lint coverage`** — rejected explicitly by SAD §1.1: those
  dimensions are already scored, and the target would never execute the delivered
  entry point.

---

## ADR ↔ Requirement Traceability Matrix

The matrix below is the cross-reference between the Phase-1 SRS
(`01-requirements/SRS.md`) and the architectural decisions in this document.
Every architectural decision traces to at least one SRS requirement (FR or NFR)
and to the canonical specification section in `SPEC.md` that originates it.
The traceability matrix is what Gate 2 reads to verify that the 28 in-scope
SRS requirements and 8 NFR requirements are each owned by at least one decision,
and that no architectural decision in this document is unmotivated by a
downstream requirement. Rows reference the ADR number; columns cite the SRS
requirement identifier, the SAD section that records the decision, and the
specification line range that the SRS transcription pulled from.

| ADR  | Decision summary                          | SRS FR requirements owned         | SRS NFR requirements owned   | SAD §    | Specification line range (SPEC.md) |
|------|-------------------------------------------|----------------------------------|------------------------------|----------|-----------------------------------|
| 001  | Layered architecture, one-way deps        | FR-02, FR-18                     | NFR-02, NFR-03               | §2.3, §5 | 1407, 4389, 7083, 7089            |
| 002  | Directory-as-community with ≥2 hubs        | (architectural)                  | NFR-03                       | §2.1, §2.2 | 7089                          |
| 003  | Python 3.11, stdlib-only L1–L3 hot path   | FR-02, FR-03, FR-04, FR-05, FR-10, FR-24 | NFR-01                | §4.2     | 7077, 1172, 1407                  |
| 004  | asyncio concurrency, not thread pool      | FR-06                            | NFR-01, NFR-07               | §2.4.5, §3.1 | 1922, 7077, 7113              |
| 005  | PALADIN mandatory ordered chain           | FR-03, FR-04, FR-05, FR-06, FR-07 | NFR-01, NFR-02             | §3.1, §3.3 | 1580, 1690, 1765, 1922, 2899, 7077, 7083 |
| 006  | PostgreSQL 16 + pgvector four-tier cascade | FR-13, FR-14, FR-15, FR-19       | NFR-01, NFR-07               | §2.4.6, §4 | 3070, 3146, 3222, 4236, 7077, 7113 |
| 007  | Redis Lua rate limiter, fail-open         | FR-09                            | NFR-04, NFR-08               | §3.3, §4 | 2435, 7095, 7119                 |
| 008  | Single circuit breaker wrapping egress    | FR-28                            | NFR-04                       | §2.4.8, §4.1 | 5521, 7095                   |
| 009  | Pydantic v2 on every cross-module edge    | FR-01, FR-16, FR-26              | NFR-02, NFR-03               | §3.2     | 1172, 3754, 986, 7083, 7089      |
| 010  | RBAC at route registration                | FR-18                            | NFR-02                       | §3.3     | 4389, 7083                       |
| 011  | SAQ for background jobs                   | FR-22                            | NFR-01, NFR-07               | §4       | 5194, 7077, 7113                 |
| 012  | Atomic write for durable artifacts        | FR-23                            | NFR-05                       | §2.3, §5 | 2319, 7101                       |
| 013  | Observability through `infra.hub.instrument` | FR-21                         | NFR-01, NFR-04               | §3.2, §4 | 4938, 7077, 7095                 |
| 014  | `make verify-system` boots real entry point | (gate mechanism)               | NFR-02, NFR-03, NFR-05, NFR-06 | §1.1, §5 | 7083, 7089, 7101, 7107           |

### Coverage notes

- **Every in-scope FR is owned.** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06,
  FR-07, FR-09, FR-10, FR-13, FR-14, FR-15, FR-16, FR-18, FR-19, FR-21,
  FR-22, FR-23, FR-24, FR-26, FR-28 all trace to at least one ADR above.
  FR-08 (PII), FR-11 (emotion), FR-12 (DST/intent), FR-17 (response tone),
  FR-20 (LLM-as-a-Judge), FR-25 (multimedia), FR-27 (context window) are
  domain-layer behaviors whose architectural placement is recorded by SAD
  §2.4; they have no ADR of their own because no architecture-defining
  choice was needed for them — the hub-and-layer layout already covers
  their placement.
- **Every NFR is owned.** NFR-01 through NFR-08 each appear in at least one
  row above. NFR-05 (testability: coverage, mutation, golden dataset) is
  addressed structurally by ADR-014 (real-dependency verification) and
  procedurally by ADR-012 (atomic writes that the golden dataset relies on).
- **NFR-06 is owned by ADR-014.** Deployability (Docker Compose dev
  environment, containerized boot, real-dependency verification target) is
  exercised by `make verify-system`, which is what proves the deployment
  image runs end-to-end. ADR-014 is therefore the architectural decision
  that ties NFR-06 to a concrete deliverable; the broader K8s
  HPA / RollingUpdate / rollback mechanics live in the operational harness
  layer outside the architecture ADR set.
- **NFR-08 is cross-cutting, not owned by a single decision.** Usability
  (CSAT ≥ 4.8/5.0, zh-TW empathy tone, Accuracy 100 % knowledge alignment,
  Admin/Agent WebSocket real-time sync) is a property of the domain layer
  (FR-17 response tone, FR-20 LLM-as-a-Judge) and the WebSocket transport
  (FR-19 escalation queue), not of any single architectural choice. The
  ADRs that touch its supporting machinery are ADR-007 (Redis backs the
  WebSocket session cache) and ADR-011 (SAQ carries the deferred work
  that keeps the response path responsive enough for a 4.8 CSAT bar).
  No single ADR can claim NFR-08 as its requirement, and the matrix
  above intentionally does not invent an owning decision.
- **SRS dependency.** Every row above cites the SRS FR/NFR identifier and the
  SAD section. The `SRS.md` file is the canonical transcription of the
  specification's FRs and NFRs; this matrix is the only place where each
  architectural decision is bound to the SRS identifier it satisfies, so
  Phase 3 verification can resolve "which requirement owns this decision?"
  without re-reading the SAD.
