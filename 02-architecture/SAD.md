# Software Architecture Document (SAD) — OmniBot

> Phase: 2 — Architecture | Owner: Architect (Agent A) | Updated: 2026-09-04
> Canonical sources: SPEC.md (7464 lines, 28 in-scope FRs + 6 deferred FRs + 8 NFRs)
> and 01-requirements/SRS.md (canonical FR→module traceability).

---

## 1. Architecture Overview

OmniBot is a multi-platform customer-service conversational agent. It ingests
messages from Telegram / LINE / Messenger / WhatsApp / Web / external A2A agents,
normalizes them to a `UnifiedMessage` schema, runs them through a five-layer
PALADIN defense stack (Input Sanitization → Pattern Detection → Instruction
Hierarchy → Semantic Injection Classifier → Grounding Check), routes them via a
Dialogue State Tracking FSM to either a four-tier Hybrid Knowledge Layer
(PostgreSQL rule → pgvector HNSW + RRF → LLM generation → human escalation) or
an Agentic Action Execution engine (MCP / A2A / CLI), generates a response
through a Tone-adapted Response Generator, applies 7-role RBAC enforcement, and
ships the answer back over the originating channel — all under
structured-logging + Prometheus + OpenTelemetry observability, with an
LLM-as-a-Judge framework calibrating quality against a ≥ 500-sample golden
dataset.

The architecture is **layered** (api → security → core → infra → data), with
strict dependency direction (downstream layers never call upstream). Each layer
exposes a hub module so cross-cutting orchestration stays inside the same
directory (CRG Principle 2/3) and so the `make verify-system` target can reach
real acceptance criteria against real dependencies (Redis, PostgreSQL+pgvector,
LLM provider).

### 1.1 System Verification Target

> **Every exit gate (2, 3 and 4)**: the harness executes `make verify-system`. A
> non-zero exit fails the gate. The target name is fixed — the harness always calls
> `make verify-system`.
>
> This is the only check in the whole framework that runs the delivered system.
> Everything else reads your source text or runs your test suite, both of which
> your test doubles configure. Two rules follow, and the gate enforces both:
>
> 1. **At least one step must invoke the delivered entry point** — the program a
>    user would run (`python -m omnibot …`, your console script, your
>    service). A target that chains `test lint coverage` re-runs dimensions the
>    gate has already scored and verifies nothing further.
> 2. **The step that does so must be able to fail.** `|| true`, a leading `-`,
>    and tool flags like `ruff --exit-zero` all keep a failure out of make's exit
>    code, which is the only thing the gate reads.
>
> Aim for a step that exercises a real acceptance criterion against real
> dependencies — a temporary database, a real file, the actual process — because
> the gate also measures which of your high-risk modules this target executed.
> Any module your test suite replaces with an `autouse` stand-in has to run for
> real here.

**Makefile target**: `verify-system`
**Exercises**:
- `app.main` (entry point — boots FastAPI + SAQ worker against real Redis +
  PostgreSQL containers from `docker-compose.dev.yml`)
- `api.webhooks` (issues a Telegram-shaped POST, asserts HMAC verification,
  assert-rate-limit, assert-422 paths — three of the four FR-01.AC boundaries)
- `security.paladin.l4_semantic` (runs the L4 async classifier end-to-end
  against a real LLM call to validate the ≤ 200 ms async-pipeline budget)
- `core.knowledge_tier2` (issues a pgvector HNSW query against the real
  dev-cluster to validate FR-14.AC1)
- `infra.ha_circuit_breaker` (trips a real Redis breaker and asserts
  fail-open semantics — FR-28.AC3)

This guarantees the target exercises the highest-risk modules named in the
SAB §5 block (`high_risk_modules`) without resorting to `autouse` doubles.

---

## 2. Module Design

### 2.1 Directory Structure Design Principles

> **CRG Architecture Scoring**: Phase 3+ judges your code's community cohesion via
> the Code Review Graph (CRG).  CRG groups files by **directory** — each directory
> is one community.  The architecture score is the fraction of communities that are
> "healthy" (internal edge density ≥ 0.3 AND size ≤ 50 nodes).
>
> **CRG scoring formula**: Each community's cohesion = internal_edges / (internal_edges + external_edges).
> External edges = calls to libraries (stdlib, frameworks) + calls to other communities.
> Internal edge dilution is the primary risk — entry points (CLI, main.py) import many libraries,
> producing external edges with no offsetting internal edges unless they also call sibling modules.
> The fix is **not** to reduce library imports — it is to ensure every function body also calls at least one
> sibling within the same directory.
>
> **Required edge budget**: To reach cohesion ≥ 0.3 with E external edges, you need
> I ≥ ceil(0.4286 × E) internal edges. Each function-body call to a hub function = 1 internal edge.
> Module-level calls create 1 edge per file, but per-function-body calls multiply the count.
> Example: 48 external edges → need ≥21 internal edges. With 5 sibling files each having
> 4 function bodies calling 2 hub functions → 40 internal edges — safely above threshold.

**Design for high cohesion from the start — 6 Universal CRG Design Principles:**

**Principle 1 — Use subdirectories to control CRG community boundaries.** CRG assigns one community per directory. If you dump 10+ files into a flat `src/`, CRG's Leiden algorithm freely splits them into unpredictable communities — some will likely fall below the 0.3 cohesion threshold. Explicit subdirectories (`src/api/`, `src/core/`, `src/infrastructure/`) each become one predictable community. Aim for 3-6 source directories total (excluding tests). Fewer than 3 → oversized single community; more than 6 → too many communities to keep all above 0.3.

**Principle 2 — Every directory needs a hub module (≥2 functions for 4+ siblings).** Each directory with ≥2 files must have a shared module (`utils.py`, `common.py`, `helpers.py`) that ≥70% of sibling files import and call via standalone function calls: `result = hub.fn(...)`. This creates cross-file internal edges. Pure library-utility files that no sibling calls produce zero internal edges — they only dilute the community.

For directories with ≥4 sibling files, **one hub function is rarely enough** — a single function called from 5 files produces ~5 edges, which may not offset ~40+ external edges. Use **≥2 hub functions** so each sibling can call both from multiple function bodies, multiplying internal edge count. The tts-new infrastructure directory (5 siblings, 48 external edges) required 2 hub functions (`validate_config` + `get_config_snapshot`) called from every function body to reach ~32 internal edges and pass 0.3.

Exception: directories that form a linear processing pipeline (A→B→C) where each file calls the next in chain.

**Principle 3 — Entry points must live inside a hub directory.** Entry-point modules (CLI, `main.py`, `app.py`, daemon) unavoidably import many external libraries — httpx, FastAPI, argparse, asyncio, etc. Each external import adds an external edge. If the entry point sits alone at the project root (e.g. `src/cli.py`), those external edges dominate and cohesion drops below 0.3. Place entry points inside a directory that also contains a hub module — the entry point calls the hub (internal edges) to compensate for its external edges.

**Principle 4 — Every function body must call a hub function (not just module-level).** A file that is never imported or called by any other file in its directory contributes only external edges (its own imports) and zero internal edges — pure dilution. For each file in your design, verify it is either: (a) the hub module itself, (b) called by the hub, or (c) calls the hub. Files that fail this check should be merged into another file or directory.

Critically, **module-level calls alone are insufficient**. A module-level `_ = validate_config()` creates 1 internal edge per file regardless of how many functions it has. CRG counts edges per (caller_node, callee_node) pair — each function body that calls the hub creates a separate edge. To accumulate enough internal edges (see edge budget above), the hub function must be called **from every accessible function body** in each sibling file, not just at module level. Example: a 5-sibling directory needs ~21 internal edges; 5 module-level calls + 5×4 function-body calls = 25 edges.

**Principle 5 — Respect CRG edge-detection limits.** CRG uses Tree-sitter AST parsing and detects cross-file function calls resolved through imports. These limitations are cross-language:
- Calls between functions in the **same** file — NOT detected (zero cohesion contribution)
- `self.method()` calls inside a class — DETECTED (class hierarchy contributes edges)
- `import sibling` → `sibling.fn()` — DETECTED (cross-file import resolved)
- `result = hub.fn(...)` then `log.info(..., extra=result)` — DETECTED (standalone assignment)
- `log.info(..., extra=hub.fn(...))` — INCONSISTENTLY detected (nested arg position)
- Calls through imports at runtime (lazy imports in `__getattr__`, `__init__.py` re-exports) — may be missed if not statically resolvable

**Principle 6 — Size cap: communities stay under 50 nodes.** CRG marks any community with >50 nodes as unhealthy regardless of cohesion. A node ≈ one function or class in a file. If your directory design would produce >50 nodes (roughly 4-6 modules with 8-12 functions each), split into subdirectories. Unlike Principles 1-5, this can be relaxed slightly — the cap is 50, not 30 — so this is rarely the binding constraint unless you have large god-modules.

| Quick reference | check |
|----------------|-------|
| Source directories count? | 3-6 |
| Each dir has a hub file? | Yes |
| Hub has ≥2 functions if ≥4 sibling files? | Yes |
| Entry points inside a hub dir? | Yes |
| Each function body calls a hub function? | Yes (not just module-level) |
| Cross-file calls use standalone assignment? | Yes |
| Community size ≤ 50 nodes? | Yes |
| Edge budget: I ≥ 0.4286 × E? | Yes |

**Anti-patterns that produce low scores:**

```
❌ src/__init__.py, src/main.py, src/models.py, src/cli.py, src/audio.py
   → 5 isolated files in flat src/, zero cross-imports → cohesion=0.0

❌ src/cli.py  (imports httpx, argparse, asyncio — all external, no internal sibling calls)
   → pure external edges, no compensation → cohesion near 0

❌ tests/test_fr01.py, tests/test_fr02.py, ... tests/test_fr08.py
   → 80 nodes in one dir, no internal edges → oversized + zero cohesion

✅ src/api/{cli,main,speech,utils}.py with utils imported by all siblings → hub-and-spoke
✅ src/engines/{synthesis,splitter,parser}.py with synthesis calling both → pipeline chain
✅ src/infrastructure/{circuit,health,config,models}.py → shared domain layer
```

### 2.2 Project Module Tree (derived from SRS.md §2 + SPEC.md architecture)

> The FR→module mapping below is canonical — it is reproduced verbatim from
> `01-requirements/SRS.md` §2 (Implementation Module column), which itself is
> derived from the SPEC.md architecture diagram (§7) and per-FR module clauses
> (e.g. SPEC.md:2726 `app/security/ip_whitelist.py`). Where a single FR owns
> multiple modules (FR-26, FR-28), the SAB `fr_module_traceability` uses the
> YAML-list form.

```
src/
├── app/                              # Entry-point hub (CRG Principle 3)
│   ├── main.py                       # FastAPI/SAQ entry point — boots app.hub
│   ├── config.py                     # pydantic-settings loader — called by app.hub
│   └── hub.py                        # Orchestrator (≥2 hub fns: dispatch, lifecycle)
│
├── api/                              # Inbound/outbound HTTP layer (FR-01,02,18,19,25,26)
│   ├── webhooks.py                   # FR-01 ingress + FR-02 HMAC verify
│   ├── media.py                      # FR-25 multimedia escalation
│   ├── users.py                      # FR-26 user CRUD
│   ├── m2m.py                        # FR-26 M2M token rotation
│   ├── rbac.py                       # FR-18 7-role decorator middleware
│   ├── escalation.py                 # FR-19 priority queue + WebSocket
│   └── hub.py                        # api-level hub (register_routes, mount_ws)
│
├── security/                         # Defense layer (FR-02,03,04,05,06,07,08,09,10,23)
│   ├── auth.py                       # FR-02 HMAC + M2M JWT
│   ├── ratelimit.py                  # FR-09 Redis Lua atomic counter
│   ├── pii.py                        # FR-08 PII + Luhn
│   ├── ip_whitelist.py               # FR-10 CIDR matcher
│   ├── gdpr.py                       # FR-23 export/deletion lifecycle
│   ├── paladin/                      # 5-layer defense (one file per layer)
│   │   ├── l1_sanitize.py            # FR-03 NFKC + homoglyph
│   │   ├── l2_pattern.py             # FR-04 pattern rules
│   │   ├── l3_hierarchy.py           # FR-05 sandwich + hierarchy
│   │   ├── l4_semantic.py            # FR-06 async classifier
│   │   ├── l5_grounding.py           # FR-07 grounding check
│   │   └── hub.py                    # paladin chain orchestrator
│   └── hub.py                        # security-level hub (defense_in_depth)
│
├── core/                             # Domain logic (FR-11,12,13,14,15,16,17,24,27)
│   ├── emotion.py                    # FR-11 multi-turn + half-life decay
│   ├── dialog_dst.py                 # FR-12 FSM + intent router
│   ├── dialog_context.py             # FR-27 sliding window
│   ├── knowledge_tier1.py            # FR-13 PostgreSQL exact/keyword
│   ├── knowledge_tier2.py            # FR-14 pgvector HNSW + RRF
│   ├── knowledge_tier3.py            # FR-15 LLM generation + fallback
│   ├── actions.py                    # FR-16 AEE (MCP/A2A/CLI)
│   ├── response.py                   # FR-17 tone-adapted generator
│   ├── experiment.py                 # FR-24 SHA-256 A/B framework
│   ├── eval.py                       # FR-20 LLM-as-a-Judge
│   └── hub.py                        # core-level hub (route_intent, pick_tier)
│
└── infra/                            # Cross-cutting infra (FR-21,22,28)
    ├── observability.py              # FR-21 OTel + Prometheus
    ├── jobs.py                       # FR-22 SAQ worker + embedding pipeline
    ├── ha_redis.py                   # FR-28 Redis Streams
    ├── ha_circuit_breaker.py         # FR-28 circuit breaker
    └── hub.py                        # infra-level hub (instrument, healthcheck)
```

**Community (directory) budget:**

| Directory | File count | Hub fn count | Layer |
|-----------|-----------:|-------------:|-------|
| `app/` | 3 | 2 (`dispatch`, `lifecycle`) | entry-point |
| `api/` | 7 | 2 (`register_routes`, `mount_ws`) | inbound/outbound |
| `security/` (root) | 6 | 2 (`defense_in_depth`, `audit_log`) | defense |
| `security/paladin/` | 6 | 2 (`chain`, `emit_verdict`) | defense sub |
| `core/` | 11 | 2 (`route_intent`, `pick_tier`) | domain |
| `infra/` | 5 | 2 (`instrument`, `healthcheck`) | infra |

All communities are ≤ 50 nodes (size cap, Principle 6) and have ≥ 2 hub
functions, which gives each ≥ 4 sibling files the edge budget they need to
clear the 0.3 cohesion floor.

### 2.3 FR → Module Mapping (canonical, traceable to SRS.md §2)

| FR | Title | Module(s) | Verification Method |
|----|-------|-----------|---------------------|
| FR-01 | Multi-Platform Ingress & Normalization | `api.webhooks` | 4-boundary path suite (FR-01.AC1..AC4) |
| FR-02 | Webhook Signature Verification & M2M Authentication | `security.auth`, `api.webhooks` | HMAC-SHA256 verifier unit + 4-boundary path suite |
| FR-03 | PALADIN L1 Input Sanitization & Homoglyph Normalization | `security.paladin.l1_sanitize` | NFKC + homoglyph translation unit tests |
| FR-04 | PALADIN L2 Pattern Detection & Anti-Prompt Injection | `security.paladin.l2_pattern` | Pattern rule unit tests + injection corpus |
| FR-05 | PALADIN L3 Instruction Hierarchy & Sandwich Defense | `security.paladin.l3_hierarchy` | Sandwich defense + hierarchy test suite |
| FR-06 | PALADIN L4 Semantic Injection Classifier & Async Pipeline | `security.paladin.l4_semantic` | Async classifier + pipeline test suite |
| FR-07 | PALADIN L5 Grounding Knowledge Alignment | `security.paladin.l5_grounding` | Grounding alignment suite + knowledge alignment 100% |
| FR-08 | PII Detection, Masking & Luhn Validation | `security.pii` | PII detector + Luhn check unit tests |
| FR-09 | Distributed Rate Limiting (Redis & Lua) | `security.ratelimit` | Redis Lua atomic counter + sliding window suite |
| FR-10 | CIDR-based IP Whitelist Enforcement | `security.ip_whitelist` | CIDR match unit tests |
| FR-11 | Multi-turn Emotion Analyzer & Half-Life Decay | `core.emotion` | Multi-turn emotion + half-life decay unit tests |
| FR-12 | Dialogue State Tracking & Intent Router FSM | `core.dialog_dst` | FSM transition + intent routing suite |
| FR-13 | Knowledge Retrieval Tier 1 (PostgreSQL exact/keyword) | `core.knowledge_tier1` | Exact/keyword match integration suite |
| FR-14 | Knowledge Retrieval Tier 2 (pgvector HNSW + RRF) | `core.knowledge_tier2` | pgvector HNSW + RRF benchmark suite |
| FR-15 | Knowledge Retrieval Tier 3 (LLM generation + multi-model) | `core.knowledge_tier3` | LLM fallback switch + multi-model suite |
| FR-16 | Action Execution Engine (MCP / A2A / CLI) | `core.actions` | Tool adapter + AEE suite |
| FR-17 | Response Generator & Dynamic Tone Adjustment | `core.response` | Template + tone adapter suite |
| FR-18 | 7-Role RBAC & Decorator Middleware | `api.rbac` | RBAC decorator + 7-role matrix suite |
| FR-19 | Human Escalation & SLA Priority Queue | `api.escalation` | Priority queue + WebSocket escalation suite |
| FR-20 | LLM-as-a-Judge Evaluation Framework | `core.eval` | Judge + rubric + calibration suite |
| FR-21 | Structured Logging, Prometheus & OpenTelemetry | `infra.observability` | OTel + Prometheus metric suite |
| FR-22 | Async Background Job System (SAQ + Embedding) | `infra.jobs` | SAQ worker + embedding pipeline suite |
| FR-23 | GDPR Data Lifecycle, Export & Deletion | `security.gdpr` | Export + deletion lifecycle suite |
| FR-24 | A/B Testing Framework (SHA-256 deterministic) | `core.experiment` | Deterministic hash + assignment suite |
| FR-25 | Multimedia Message Handling & Escalation | `api.media` | Multimedia escalate-to-human suite |
| FR-26 | User & M2M Token Management API | `api.users`, `api.m2m` | User CRUD + token rotation suite |
| FR-27 | Conversation Context Window Management | `core.dialog_context` | Sliding window + token budget suite |
| FR-28 | High Availability, Redis Streams & Circuit Breaker | `infra.ha_redis`, `infra.ha_circuit_breaker` | Circuit breaker + Redis Streams suite |
| FR-29..34 | deferred | (out of scope this phase) | NFR-99 |

### 2.4 Per-Module Specification

#### 2.4.1 `app.main`

| Attribute | Value |
|-----------|-------|
| Responsibility | Boot FastAPI app, start SAQ worker, wire `app.hub.dispatch()` to webhook routes |
| External Interface | `python -m omnibot` (console entry), `omnibot serve` (CLI subcommand) |
| Dependencies | `app.hub`, `api.hub`, `infra.hub`, FastAPI, uvicorn, SAQ |

#### Logical Constraints
- Must not import `core.*` or `security.*` directly — only via `api.hub` / `security.hub`.
- Must call `app.hub.lifecycle()` once at startup AND once at shutdown (satisfies
  CRG Principle 4 — function-body call, not module-level).

#### 2.4.2 `app.hub`

| Attribute | Value |
|-----------|-------|
| Responsibility | Cross-layer orchestration: order PALADIN chain → DST → knowledge tier pick → RBAC enforce → log + emit metrics |
| External Interface | `dispatch(unified_message) -> UnifiedResponse`, `lifecycle() -> None` |
| Dependencies | `api.hub`, `security.hub`, `core.hub`, `infra.hub`, `app.config` |

#### Logical Constraints
- Must be called from at least 2 sibling files (`app.main`, `api.hub`) via
  standalone assignment (`result = hub.dispatch(msg)`) — guarantees internal
  edge budget.
- No business logic in this module — pure orchestration only.

#### 2.4.3 `api.webhooks` (FR-01, FR-02)

| Attribute | Value |
|-----------|-------|
| Responsibility | Accept platform webhooks (Telegram / LINE / Messenger / WhatsApp / Web), verify HMAC via `security.auth`, normalize to `UnifiedMessage`, hand to `app.hub.dispatch` |
| External Interface | HTTP POST `/api/v1/webhook/{telegram,line,messenger,whatsapp,web}`, GET `/api/v1/webhook/{messenger,whatsapp}` (hub.challenge) |
| Dependencies | `api.hub`, `security.auth`, `security.ratelimit`, `security.ip_whitelist` |

#### Logical Constraints
- Returns HTTP 200 within ≤ 5 ms of receiving a verified payload so the
  upstream channel does not retry.
- Each platform adapter MUST call `api.hub.register_routes(...)` from its own
  function body (not just import) to satisfy CRG Principle 4.

#### 2.4.4 `security.paladin.l1_sanitize` (FR-03)

| Attribute | Value |
|-----------|-------|
| Responsibility | NFKC normalize, strip control chars, fold homoglyphs (per Unicode confusables.txt) before any downstream layer sees the text |
| External Interface | `sanitize(text: str) -> SanitizedText` |
| Dependencies | `unicodedata`, `security.paladin.hub` |

#### Logical Constraints
- MUST run synchronously and complete in ≤ 5 ms (NFR-01 PALADIN L1~L3 budget).
- Side-effect: emits `paladin_l1_latency_seconds` Prometheus histogram.

#### 2.4.5 `security.paladin.l4_semantic` (FR-06)

| Attribute | Value |
|-----------|-------|
| Responsibility | Async semantic-injection classifier using a fine-tuned small model (or external API), parallelized via `asyncio.gather` over multi-modal channels |
| External Interface | `classify_async(text: str) -> Verdict`, `pipeline(text, channel) -> Verdict` |
| Dependencies | `security.paladin.hub`, `infra.observability`, `infra.jobs` (SAQ for non-blocking dispatch) |

#### Logical Constraints
- Async budget: ≤ 200 ms end-to-end (NFR-01).
- MUST run in parallel with `core.dialog_dst` (independent of intent routing)
  to honor the SPEC.md pipeline timing budget.

#### 2.4.6 `core.knowledge_tier2` (FR-14)

| Attribute | Value |
|-----------|-------|
| Responsibility | pgvector HNSW (m=16, ef_construction=64) top-k retrieval with RRF k=60 fusion against Tier-1 results; parent-child document expansion |
| External Interface | `retrieve(query: str, k: int = 10) -> list[KnowledgeHit]` |
| Dependencies | `asyncpg`, `pgvector`, `core.hub`, `infra.observability` |

#### Logical Constraints
- p95 ≤ 150 ms (NFR-01). Must use prepared statements + connection pool.
- Must call `core.hub.pick_tier(...)` from every function body that opens a
  connection (CRG Principle 4).

#### 2.4.7 `core.dialog_dst` (FR-12) and `core.dialog_context` (FR-27)

| Attribute | Value |
|-----------|-------|
| Responsibility | `dialog_dst`: FSM-based dialogue state tracking with slot filling + intent routing (qa vs task). `dialog_context`: sliding-window + token-budget management (≤ 4096 tokens, FR-27) |
| External Interface | `transition(state, event) -> State`, `route(state) -> Intent`, `window(messages, budget) -> Trimmed` |
| Dependencies | `core.hub`, `core.dialog_context` (cross-talk) |

#### Logical Constraints
- FSM transitions guarded by `core.hub.route_intent(...)` from every function
  body (CRG Principle 4).
- Context window must never exceed the budget — emit `context_overflow_total`
  counter and downgrade to summary on overflow.

#### 2.4.8 `infra.ha_circuit_breaker` (FR-28)

| Attribute | Value |
|-----------|-------|
| Responsibility | Track per-dependency (Redis / LLM / MCP / A2A) failure rate; open at > 50 % over a 60-second window; half-open after cool-down |
| External Interface | `call(name, fn, *a, **kw) -> T`, `state(name) -> State` |
| Dependencies | `infra.observability`, `infra.hub` |

#### Logical Constraints
- Fail-open on Redis itself (per NFR-04 "Redis fail-open").
- All call sites MUST go through `infra.hub.instrument(...)` so circuit state is
  visible in Grafana (CRG Principle 4).

---

## 3. Interfaces & Data Flows

### 3.1 Inbound Message Flow (happy path)

```
Platform (HTTPS POST)
   │
   ▼
api.webhooks.verify_hmac()  ── calls ──▶ security.auth
   │
   ▼
security.ip_whitelist.check()  ── reject (403) if CIDR miss
   │
   ▼
security.ratelimit.consume()  ── reject (429) if bucket empty
   │
   ▼
security.paladin.l1_sanitize → l2_pattern → l3_hierarchy   (sync, ≤ 5 ms)
   │
   ├── async fork ──▶ security.paladin.l4_semantic (≤ 200 ms, gather at join)
   │
   ▼
security.pii.mask()
   │
   ▼
core.emotion.analyze()  (bypass if platform==AGENT)
   │
   ▼
core.dialog_dst.route()  ── qa branch | task branch
   │
   ├── qa ──▶ core.knowledge_tier1 → tier2 (HNSW+RRF) → tier3 (LLM fallback)
   │                                          │
   │                                          ▼
   │                              security.paladin.l5_grounding
   │
   ├── task ──▶ core.actions.execute()  ── MCP | A2A | CLI adapters
   │
   ▼
core.response.generate(tone=...)  ── core.experiment.pick_variant()
   │
   ▼
api.rbac.enforce(actor, role)
   │
   ▼
infra.observability.emit(metrics, trace, log)
   │
   ▼
api.webhooks.reply(platform, channel, response)
```

### 3.2 Module-to-Module Data Contracts

| Edge | From → To | Contract Type | Notes |
|------|-----------|---------------|-------|
| ingress | `api.webhooks` → `app.hub` | `UnifiedMessage` (Pydantic v2 model) | Normalized across all platforms |
| defense | `app.hub` → `security.paladin.hub` | `UnifiedMessage` + `SanitizedText` | L1..L3 synchronous, L4 forked async |
| intent | `security.paladin.hub` → `core.dialog_dst` | `Verdict` + `SanitizedText` | Blocks L1..L3 failures; awaits L4 verdict before Tier-3 LLM call |
| retrieval | `core.dialog_dst` → `core.knowledge_tier1/2/3` | `RetrievalQuery` → `list[KnowledgeHit]` | Tier-1 always runs; Tier-2 on miss; Tier-3 on Tier-2 confidence < 0.7 |
| action | `core.dialog_dst` → `core.actions` | `ActionRequest` (Pydantic, validated against MCP/A2A/CLI schemas) | `infra.ha_circuit_breaker.call(...)` wraps every tool dispatch |
| response | `core.response` → `api.webhooks` | `UnifiedResponse` | Tone + variant already baked in |
| observability | every module → `infra.observability` | OTel spans + Prometheus counters | Inherited via `infra.hub.instrument(...)` decorator |

### 3.3 Failure & Degradation Flows

| Failure | Detection | Mitigation | Visible Side |
|---------|-----------|-----------|-------------|
| HMAC verify fail | `security.auth.verify_hmac()` | Return HTTP 401; log `auth_failure_total{platform}` | OTel span tag + auth audit |
| Rate limit hit | `security.ratelimit.consume()` | Return HTTP 429; emit `Retry-After` header | Counter `rate_limited_total{platform}` |
| L1..L3 detection | `security.paladin.hub` | Reject message; return canned refusal; do NOT call downstream | Verdict log `paladin_block_total{layer}` |
| L4 detection (async) | `security.paladin.l4_semantic` | Tag response with `safety_flag`; redact PII; route to human | Counter `paladin_l4_block_total` |
| LLM provider 5xx | `infra.ha_circuit_breaker` | Open breaker; fallback to next model in Tier-3 chain | `circuit_breaker_state{name}` gauge |
| Redis down | `infra.ha_redis` health probe | Fail-open rate limiter (NFR-04) | `redis_failopen_total` counter |
| Tool timeout (> 2s) | `infra.ha_circuit_breaker` | Retry ≤ 3 times with exponential backoff + jitter (NFR-04) | `tool_timeout_total{tool}` |
| All retrieval tiers miss | `core.hub.pick_tier()` | Route to `api.escalation` (FR-19) | `knowledge_miss_total` |

---

## 4. NFR Handling

| NFR | Type | Module(s) | Design Strategy | Verification |
|-----|------|-----------|-----------------|--------------|
| **NFR-01** Performance — p95 e2e ≤ 1.0 s @ 2000 TPS; PALADIN L1–L3 ≤ 5 ms; L4 async ≤ 200 ms; knowledge p95 ≤ 150 ms; embedding p95 ≤ 100 ms; Admin UI ≤ 1.5 s | performance | All PALADIN layers (`security.paladin.l1..l4`), `core.knowledge_tier1/2/3`, `infra.jobs` | (1) L1–L3 are pure-Python sync (no I/O); (2) L4 runs as `asyncio.gather` alongside `core.dialog_dst`; (3) Tier-1 always runs first to short-circuit before Tier-2 HNSW; (4) Embedding is batched + cached in `infra.jobs`; (5) Admin UI is pre-rendered SPA with cached fragments. Budgets enforced via `infra.observability` histograms (gate-checked). | k6 (Functional/Stress/Spike/Soak) + Prometheus p95 histogram in `infra.observability`; Gate 3 / Gate 4 |
| **NFR-02** Security — OWASP LLM Top-10 100 %; Gitleaks = 100; Bandit ≥ 80 (0 High/Critical); PALADIN Block ≥ 95 %; RBAC 7-role enforcement; PG TDE + TLS 1.3 + Redis TLS/AUTH/ACL | security | `security.paladin.l1..l5`, `security.auth`, `security.pii`, `security.ip_whitelist`, `security.ratelimit`, `api.rbac`, `security.gdpr` | (1) Five-layer defense is mandatory — message cannot reach `core.dialog_dst` without clearing all five; (2) `security.paladin.hub` chain enforces 95 % block-rate KPI via weekly red-team corpus replay; (3) `api.rbac` decorator applied at route registration, not inside handlers (impossible to forget); (4) TLS 1.3 only (no TLS 1.2 fallback); Redis ACL scopes commands; PG `pgaudit` enabled; Bandit/Gitleaks run in `make verify-system`. | bandit + gitleaks + semgrep + red-team prompt injection suite; Gate 1–4 |
| **NFR-03** Maintainability — fn ≤ 50 lines, CC ≤ 10; Ruff ≥ 90; Pyright ≥ 85; Alembic bidirectional 100 % roundtrip; Code-to-SAD mapping = 100 % | maintainability | Every module | (1) 50-line cap enforced by `radon mi -s -n B src/`; (2) Pyright strict mode in `pyproject.toml`; (3) Every `alembic upgrade head` script must have a paired `downgrade` that re-runs without diff; (4) `FR → Module` table in §2.3 is canonical and `make verify-system` cross-checks every imported module against it. | radon-mi + ruff + pyright + alembic upgrade/downgrade/upgrade + SAD mapping; Gate 1–4 |
| **NFR-04** Reliability — monthly uptime ≥ 99.9 %; tool/A2A RPC timeout ≤ 2.0 s; retry ≤ 3 with exponential backoff + jitter; LLM fallback switch < 500 ms; Redis fail-open; MTTR < 5 min | reliability | `infra.ha_circuit_breaker`, `infra.ha_redis`, `infra.jobs`, `core.knowledge_tier3` | (1) `infra.ha_circuit_breaker` enforces all RPC timeouts (2.0 s) + retry (3x) + jitter; (2) LLM fallback is a pre-warmed chain — switching providers is a config swap, not a code change, so < 500 ms; (3) `infra.ha_redis` health probe → fail-open rate limiter; (4) K8s `RollingUpdate maxUnavailable=0` guarantees zero-downtime deploy. | Prometheus SLO + Chaos Mesh DR drill + circuit breaker unit tests; Gate 3/4 |
| **NFR-05** Testability — Line coverage Gate-1 owned 100 %; Gate-2/4 ≥ 90 %; Mutation Killed ≥ 80 %; D4 Spec cov Gate 1 ≥ 40 / Gate 2 ≥ 60 / Gate 3 ≥ 80 / Gate 4 ≥ 90 %; golden ≥ 500 samples, Kappa ≥ 0.7 | testability | All modules; golden set in `core.eval` | (1) Per-FR test naming `test_fr{NN}_{scenario}` so D4 spec-coverage tool matches; (2) `mutmut` runs against every owned module in `make verify-system`; (3) Golden dataset lives in `tests/golden/` (≥ 500 samples); (4) Cohen's Kappa monthly calibration with n ≥ 100 reviewers. | pytest-cov + mutmut + golden calibration; Gate 1–4 |
| **NFR-06** Deployability — Docker Compose + K8s Deployment/Service/HPA; HPA CPU > 70 % / Mem > 80 %; RollingUpdate maxSurge=25 %, maxUnavailable=0; rollback < 5 min | deployability | `app.main`, `infra.observability`, `infra.jobs` | (1) `Dockerfile` builds once; dev uses `docker-compose.dev.yml`, prod uses `infra/k8s/*.yaml`; (2) HPA pinned in manifests; (3) `kubectl rollout undo` is the rollback lever, surfaced as a runbook. | kubectl rollout undo + Helm chart lint + GitOps (P8) |
| **NFR-07** Scalability — 2000 TPS sustained; pgvector HNSW (m=16, ef_construction=64) to 10 M chunks; Redis Cluster ready | scalability | `core.knowledge_tier2`, `infra.ha_redis`, `infra.jobs` | (1) pgvector HNSW parameters set at index creation (not configurable per query); (2) Redis Cluster mode is the prod default — `infra.ha_redis` is connection-pool aware; (3) Stateless app pods scale horizontally; (4) `infra.jobs` (SAQ) workers scale independently on embedding backlog. | k6 ≥ 30 min soak + pgvector benchmark + redis-cli cluster create; Gate 3/4 |
| **NFR-08** Usability — CSAT ≥ 4.8/5.0; LLM-Judge Politeness ≥ 4.5/5.0 with zh-TW empathy; Accuracy 100 % knowledge alignment; Admin/Agent portal WebSocket live-sync | usability | `core.response`, `core.eval`, `api.escalation` | (1) `core.response` selects tone based on `core.emotion` (empathy for negative sentiment); (2) `core.eval` (FR-20) runs LLM-as-a-Judge on a rolling 5 % sample of production traffic; (3) `api.escalation` WebSocket pushes ticket state changes to Agent portal in < 1 s; (4) Knowledge alignment is 100 % enforced by `security.paladin.l5_grounding` (FR-07). | FR-20 LLM-as-a-Judge + monthly human calibration (n ≥ 100, Kappa ≥ 0.7); Gate 3/4 |

### 4.1 Error Handling Tiers (cross-cutting)

| Level | Handling Strategy | Where |
|-------|-------------------|-------|
| L1 — Immediate return | Validation / auth / rate-limit failures return synchronously to the caller with the proper HTTP status code (`api.webhooks`) | `api.webhooks`, `security.auth`, `security.ratelimit` |
| L2 — Retry 3 times | Tool / A2A / LLM provider transient failures (timeout, 5xx) → exponential backoff + jitter via `infra.ha_circuit_breaker` | `infra.ha_circuit_breaker` |
| L3 — Graceful degradation | Tier-2 miss → Tier-3 LLM fallback; Tier-3 miss → `api.escalation`; LLM provider down → next model in chain | `core.knowledge_tier3`, `core.hub`, `api.escalation` |

### 4.2 Technology Choices

| Technology | Rationale |
|------------|-----------|
| Python 3.11+ | SPEC.md pinned; `match` statement + faster asyncio for PALADIN L4 pipeline |
| FastAPI + uvicorn | Async-native webhook handlers; OpenAPI auto-gen for FR-26 admin API |
| PostgreSQL 16 + pgvector | Single store for transactional + vector data; HNSW index for FR-14 |
| Redis 7 (Cluster) | Distributed rate limiting (FR-09), streams (FR-28), session cache, embeddings cache |
| SAQ (asyncio queue) | Async background jobs (FR-22); embeds naturally with FastAPI |
| Pydantic v2 | Strict validation for every cross-module data contract (UnifiedMessage, ActionRequest, etc.) |
| OpenTelemetry + Prometheus + Grafana | FR-21 observability stack; p95 histograms are gate-checked |
| Alembic | Bidirectional migrations (NFR-03); roundtrip is gate-checked |
| Ruff + Pyright + radon-mi + bandit + gitleaks | Static analysis stack covering NFR-03 + NFR-02 |

---

## 5. SAB Block (machine-readable — BINDING CONTRACT)

> **CONTRACT**: Field names, types, `sab:` root key, and `phase` as int must
> match `core/quality_gate/sab_parser.py:render_canonical_sab_template()`.
> Do NOT hand-write the YAML — paste from the canonical template and replace
> EXAMPLE values with your project's real values.
> Validate before committing: `python3 scripts/generate_sab.py --validate --project .`

<!-- SAB:START -->
```yaml
sab:
  version: "1.0"
  created_at: "2026-09-04"
  phase: 2  # MUST be int, NOT a string — parser raises on 'phase: "2"'
  project: "omnibot"

  layers:
    - name: api
      modules:
        - name: "omnibot.api.webhooks"
        - name: "omnibot.api.media"
        - name: "omnibot.api.users"
        - name: "omnibot.api.m2m"
        - name: "omnibot.api.rbac"
        - name: "omnibot.api.escalation"
        - name: "omnibot.api.hub"
      allowed_dependencies: ["security", "core", "infra"]
    - name: security
      modules:
        - name: "omnibot.security.auth"
        - name: "omnibot.security.ratelimit"
        - name: "omnibot.security.pii"
        - name: "omnibot.security.ip_whitelist"
        - name: "omnibot.security.gdpr"
        - name: "omnibot.security.paladin.l1_sanitize"
        - name: "omnibot.security.paladin.l2_pattern"
        - name: "omnibot.security.paladin.l3_hierarchy"
        - name: "omnibot.security.paladin.l4_semantic"
        - name: "omnibot.security.paladin.l5_grounding"
        - name: "omnibot.security.paladin.hub"
        - name: "omnibot.security.hub"
      allowed_dependencies: ["core", "infra"]
    - name: core
      modules:
        - name: "omnibot.core.emotion"
        - name: "omnibot.core.dialog_dst"
        - name: "omnibot.core.dialog_context"
        - name: "omnibot.core.knowledge_tier1"
        - name: "omnibot.core.knowledge_tier2"
        - name: "omnibot.core.knowledge_tier3"
        - name: "omnibot.core.actions"
        - name: "omnibot.core.response"
        - name: "omnibot.core.experiment"
        - name: "omnibot.core.eval"
        - name: "omnibot.core.hub"
      allowed_dependencies: ["infra"]
    - name: infra
      modules:
        - name: "omnibot.infra.observability"
        - name: "omnibot.infra.jobs"
        - name: "omnibot.infra.ha_redis"
        - name: "omnibot.infra.ha_circuit_breaker"
        - name: "omnibot.infra.hub"
      allowed_dependencies: []
    - name: app
      modules:
        - name: "omnibot.app.main"
        - name: "omnibot.app.config"
        - name: "omnibot.app.hub"
      allowed_dependencies: ["api", "security", "core", "infra"]

  allowed_dependencies:
    - { from: app,    to: api }
    - { from: app,    to: security }
    - { from: app,    to: core }
    - { from: app,    to: infra }
    - { from: api,    to: security }
    - { from: api,    to: core }
    - { from: api,    to: infra }
    - { from: security, to: core }
    - { from: security, to: infra }
    - { from: core,   to: infra }

  quality_targets:
    max_complexity: 10     # SPEC NFR-03 cap (CC ≤ 10)
    min_coverage: 90       # SPEC NFR-05 Gate 2/4 floor
    max_coupling: 0.3      # CRG community cohesion floor

  nfr_dimension_mapping: {}  # auto-derived from nfr_traceability.type

  nfr_traceability:
    NFR-01:
      type: performance
      target: "p95_e2e <= 1.0s @ 2000 TPS"
      module: omnibot.security.paladin.l4_semantic
    NFR-02:
      type: security
      target: "PALADIN_block_rate >= 95"
      module: omnibot.security.paladin.l4_semantic
    NFR-03:
      type: maintainability
      target: "code_to_sad_mapping = 100"
      module: omnibot.app.main
    NFR-04:
      type: reliability
      target: "monthly_uptime >= 99.9"
      module: omnibot.infra.ha_circuit_breaker
    NFR-05:
      type: testability
      target: "mutation_killed >= 80"
      module: omnibot.core.eval
    NFR-06:
      type: deployability
      target: "rollback_time < 5min"
      module: omnibot.infra.observability
    NFR-07:
      type: scalability
      target: "2000_TPS_sustained_under_4k6_scenarios"
      module: omnibot.core.knowledge_tier2
    NFR-08:
      type: usability
      target: "csat >= 4.8"
      module: omnibot.core.eval

  advisory_only: []  # AUTO-FILLED by parser — omit or leave []

  gate_score_overrides: {}  # AUTO-DERIVED by parser — omit or leave {}

  fr_module_traceability:
    FR-01: "omnibot.api.webhooks"
    FR-02: ["omnibot.security.auth", "omnibot.api.webhooks"]
    FR-03: "omnibot.security.paladin.l1_sanitize"
    FR-04: "omnibot.security.paladin.l2_pattern"
    FR-05: "omnibot.security.paladin.l3_hierarchy"
    FR-06: "omnibot.security.paladin.l4_semantic"
    FR-07: "omnibot.security.paladin.l5_grounding"
    FR-08: "omnibot.security.pii"
    FR-09: "omnibot.security.ratelimit"
    FR-10: "omnibot.security.ip_whitelist"
    FR-11: "omnibot.core.emotion"
    FR-12: "omnibot.core.dialog_dst"
    FR-13: "omnibot.core.knowledge_tier1"
    FR-14: "omnibot.core.knowledge_tier2"
    FR-15: "omnibot.core.knowledge_tier3"
    FR-16: "omnibot.core.actions"
    FR-17: "omnibot.core.response"
    FR-18: "omnibot.api.rbac"
    FR-19: "omnibot.api.escalation"
    FR-20: "omnibot.core.eval"
    FR-21: "omnibot.infra.observability"
    FR-22: "omnibot.infra.jobs"
    FR-23: "omnibot.security.gdpr"
    FR-24: "omnibot.core.experiment"
    FR-25: "omnibot.api.media"
    FR-26: ["omnibot.api.users", "omnibot.api.m2m"]
    FR-27: "omnibot.core.dialog_context"
    FR-28: ["omnibot.infra.ha_redis", "omnibot.infra.ha_circuit_breaker"]

  architecture_constraints:
    - "no_circular_dependencies"
    - "api_must_not_import_app"          # inverse — prevents webhooks from bootstrapping the app
    - "core_must_not_import_api"         # domain stays pure
    - "infra_must_not_import_api_or_core" # infra is leaf

  high_risk_modules:
    - "omnibot.app.main"
    - "omnibot.api.webhooks"
    - "omnibot.security.paladin.l4_semantic"
    - "omnibot.core.knowledge_tier2"
    - "omnibot.infra.ha_circuit_breaker"

  required_artifacts:
    - ".env.example"
    - "docker-compose.dev.yml"
    - "infra/k8s/deployment.yaml"
    - "tests/golden/conversations.jsonl"
```
<!-- SAB:END -->

Note: Fill in the YAML above — it is used for Drift Detection and gate scoring.
Generate: `python3 scripts/generate_sab.py --project . [--overwrite]`

---

## 6. Security Design (STRIDE-lite — machine-readable, BINDING CONTRACT)

> **CONTRACT**: Field names and the `security_design:` root key are parsed
> by `core/quality_gate/security_design.py:extract_security_block()`.
> Do NOT hand-write the YAML — paste from the canonical template and
> replace EXAMPLE values with your project's real values.
> Validate: `python3 harness_cli.py check-artifact-consistency --project .`
>
> `applicability: none` is a fully valid, honest declaration for a project
> with no real attack surface (e.g. a pure CLI formatting tool) — it
> requires a `justification` (>=20 chars) and skips the rest of this
> block. This is a decidable structural check, not a keyword scorer: an
> honest `none` always passes.

<!-- SEC:START -->
```yaml
security_design:
  version: "1.0"
  applicability: full   # OmniBot accepts untrusted inbound webhooks — full STRIDE-lite required
  justification: ""     # n/a — applicability: full
  trust_boundaries:
    - id: TB-01
      name: "external webhook ingress"
      description: "unauthenticated HTTPS requests from Telegram / LINE / Messenger / WhatsApp / Web / A2A crossing into the API layer"
    - id: TB-02
      name: "user → agent trust"
      description: "messages flowing from end users (any channel) into PALADIN L1..L5 and the knowledge layer — must be treated as adversarial"
    - id: TB-03
      name: "agent → external tool"
      description: "agent dispatching tool calls to MCP / A2A / CLI adapters — crosses from trusted in-process code to a remote/foreign trust domain"
    - id: TB-04
      name: "agent → data store"
      description: "PostgreSQL (with TDE) and Redis (with TLS + ACL) accessed from the application — must enforce least privilege"
    - id: TB-05
      name: "admin/agent portal"
      description: "WebSocket + REST traffic from authenticated humans managing knowledge and tickets — bypasses PALADIN but is gated by RBAC"
  threats:
    - id: T-01
      boundary: TB-01
      category: spoofing
      description: "attacker forges a webhook from a known platform (e.g. Telegram) using a leaked bot token"
      mitigation: "HMAC-SHA256 signature verification on every inbound webhook (FR-02); constant-time comparison; token rotation enforced by security.auth"
      owner_module: "omnibot.security.auth"
      nfr: NFR-02
      verified_by: "test_sec_t01_hmac_spoofing_rejected"
    - id: T-02
      boundary: TB-01
      category: tampering
      description: "malformed or oversized payload mutates task state without validation"
      mitigation: "Pydantic v2 schema validation in api.webhooks + reject-on-unknown-fields; 422 Unprocessable Entity on schema failure"
      owner_module: "omnibot.api.webhooks"
      nfr: NFR-02
      verified_by: "test_sec_t02_malformed_payload_rejected"
    - id: T-03
      boundary: TB-02
      category: tampering
      description: "prompt-injection payload bypasses PALADIN L1..L3 and reaches the LLM"
      mitigation: "PALADIN 5-layer mandatory chain (FR-03..FR-07) — L1 NFKC sanitize, L2 pattern rules, L3 sandwich/hierarchy, L4 async semantic classifier, L5 grounding; rejection at any layer blocks downstream"
      owner_module: "omnibot.security.paladin.l4_semantic"
      nfr: NFR-02
      verified_by: "test_sec_t03_paladin_chain_blocks_injection"
    - id: T-04
      boundary: TB-02
      category: information_disclosure
      description: "PII (credit card, ID, address, phone) leaks into LLM context or logs"
      mitigation: "FR-08 PII detection + Luhn validation runs after PALADIN L3 and masks before any LLM call; FR-23 GDPR export/deletion lifecycle for retention"
      owner_module: "omnibot.security.pii"
      nfr: NFR-02
      verified_by: "test_sec_t04_pii_masked_before_llm"
    - id: T-05
      boundary: TB-02
      category: denial_of_service
      description: "attacker floods a single channel, exhausting rate-limit budget and starving legitimate users"
      mitigation: "FR-09 Redis Lua atomic counter + sliding window — distributed across all app pods; 429 with Retry-After; emit rate_limited_total{platform}"
      owner_module: "omnibot.security.ratelimit"
      nfr: NFR-02
      verified_by: "test_sec_t05_rate_limit_burst_blocks"
    - id: T-06
      boundary: TB-03
      category: elevation_of_privilege
      description: "tool adapter (MCP/A2A/CLI) prompt-injects the agent into escalating privileges"
      mitigation: "Pydantic-validated ActionRequest schema; tool adapters sandboxed; omnibot.core.actions validates every arg against the tool's declared schema; circuit breaker on repeat timeout"
      owner_module: "omnibot.core.actions"
      nfr: NFR-02
      verified_by: "test_sec_t06_action_request_schema_enforced"
    - id: T-07
      boundary: TB-04
      category: information_disclosure
      description: "compromised app pod reads data it should not (e.g. other tenants' conversations)"
      mitigation: "PostgreSQL row-level security (RLS) on multi-tenant tables; Redis ACL scopes commands per service account; TLS 1.3 only; PG TDE at rest"
      owner_module: "omnibot.infra.ha_redis"
      nfr: NFR-02
      verified_by: "test_sec_t07_redis_acl_enforced"
    - id: T-08
      boundary: TB-05
      category: elevation_of_privilege
      description: "agent (low role) accesses admin (high role) endpoints"
      mitigation: "FR-18 7-role RBAC decorator applied at route registration (not inside handlers — impossible to forget); denied requests emit rbac_deny_total{role}"
      owner_module: "omnibot.api.rbac"
      nfr: NFR-02
      verified_by: "test_sec_t08_rbac_role_enforced"
    - id: T-09
      boundary: TB-02
      category: repudiation
      description: "user denies sending a message that triggered an escalation or action"
      mitigation: "structured audit log (FR-21) captures user_id, channel, content hash, IP, trace_id; tamper-evident append-only sink; tied to WebSocket escalation event"
      owner_module: "omnibot.infra.observability"
      nfr: NFR-02
      verified_by: "test_sec_t09_audit_log_captures_user_action"
```
<!-- SEC:END -->

Note: `owner_module` must name a module declared in the §5 SAB block;
`nfr` (optional) must exist in SRS.md; `verified_by` names the test that
proves the mitigation — from Phase 5 onward, `check-artifact-consistency`
blocks if that test doesn't exist yet. Threats also seed
`bug-hunt-targets`' adversarial-review targeting and force NFR-pattern
test cases in `derive_test_cases.md` Step 1c regardless of SRS keywords.