# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Testing
```bash
# Run all tests
PYTHONPATH=03-development/src python3 -m pytest tests/ -v --tb=short

# Run a single test file
PYTHONPATH=03-development/src python3 -m pytest tests/test_fr02.py -v

# Run with coverage (required: 100% on src)
/opt/homebrew/bin/python3.12 -m pytest tests/ --tb=short -q \
  --cov=03-development/src --cov-fail-under=100

# Run a single test by name
PYTHONPATH=03-development/src python3 -m pytest tests/ -k "test_fr02_telegram_valid_payload"
```

### Linting & Type Checking
```bash
# Linting (zero violations required)
ruff check 03-development/src/ 2>&1 | head -200

# Type checking
pyright 03-development/src/ --outputjson 2>&1 | head -200

# Spec-coverage check (≥90% required)
python3 harness/harness_cli.py spec-coverage-check --project . --threshold 90.0
```

### Harness (Quality Gate Framework)
```bash
# Check current phase / gate status
python3 harness/harness_cli.py status --project .

# Run phase preflight (FSM, Constitution, Kill-Switch, CI readiness)
python3 harness/harness_cli.py run-phase --phase N --project .

# Run Gate 1 evaluation for a single FR
python3 harness/harness_cli.py run-gate --gate 1 --phase N --fr-id FR-XX --project .
python3 harness/harness_cli.py finalize-gate --gate 1 --phase N --fr-id FR-XX --project .

# Advance FSM to next phase (runs TDD-PRECHECK internally)
python3 harness/harness_cli.py advance-phase --completed N --project .

# Crash recovery
python3 harness/harness_cli.py resume-fr-phase --phase N --project .
python3 harness/harness_cli.py generate-next-plan --project .

# Submodule update
git submodule update --remote harness
```

### Docker
```bash
docker compose up -d          # Start postgres + redis + omnibot-api
docker compose logs -f        # Tail logs
docker compose down -v        # Tear down (including volumes)
```

## Architecture

### Package Layout
```
03-development/src/omnibot/   ← main Python package (import as omnibot.*)
  adapters/                   ← platform-specific webhook parsers (telegram.py, line.py)
  security/                   ← verifiers.py (HMAC), rate_limiter.py, whitelist.py
  processing/                 ← pipeline.py (orchestrator), pii.py, sanitizer.py
  knowledge/                  ← matcher.py (Layer 1 rule-based KB lookup)
  escalation/                 ← queue.py (human handoff)
  db/                         ← SQLAlchemy async engine + schema DDL
  models/                     ← UnifiedMessage, Platform, MessageType (frozen dataclasses)
  infrastructure/             ← health.py (/api/v1/health endpoint)
  logging/                    ← logger.py (structured JSON logger)
  config.py                   ← Settings dataclass, loads env vars, fail-fast
  errors.py                   ← ValidationError, ConfigError

tests/test_frXX.py            ← per-FR test files (one file per FR)
02-architecture/TEST_SPEC.md  ← canonical test function names per FR
harness/                      ← harness-methodology git submodule
.methodology/                 ← FSM state, quality manifest, phase plans
```

### Message Flow (PipelineOrchestrator, 11 stages)
All inbound messages follow a fixed stage order enforced in `processing/pipeline.py`:

1. **IP whitelist check** (`security/whitelist.py`) — blocks before any auth
2. **HMAC signature verification** (`security/verifiers.py`) — platform-specific, constant-time
3. **Platform adapter parse** (`adapters/telegram.py` or `adapters/line.py`) → `UnifiedMessage`
4. **Rate limiter** (`security/rate_limiter.py`) — per-user token bucket
5. **Input sanitization** (`processing/sanitizer.py`) — fullwidth→ASCII, script injection strip
6. **PII masking** (`processing/pii.py`) — Taiwan phone/ID/email, must run before any AI call
7. **Knowledge matching** (`knowledge/matcher.py`) — Layer 1 rule-based
8. **Escalation** (`escalation/queue.py`) — triggered when no knowledge match
9. **Response construction** → `UnifiedResponse`
10. **Platform reply** (platform adapter)
11. **Structured log** (`logging/logger.py`)

**The stage order is a security invariant**: IP whitelist → HMAC → sanitize → PII → process. Never reorder.

### Key Data Types (`models/__init__.py`)
- `UnifiedMessage` — frozen dataclass; cross-platform normalized inbound message
- `Platform` — enum: `TELEGRAM`, `LINE` (+ future MESSENGER, WHATSAPP)
- `UnifiedResponse` — outbound response structure

### Security Constraints
- `security/verifiers.py`: `hmac.compare_digest` used exclusively (constant-time). Never use `==` for signature comparison.
- `processing/pii.py`: PII masking recall ≥ 95% / precision ≥ 99%. Must execute before any LLM call.
- All secrets via environment variables (`Settings` dataclass in `config.py`). Required vars: `TELEGRAM_BOT_TOKEN`, `LINE_CHANNEL_SECRET`, `DATABASE_URL`, `REDIS_URL`.

### Database (`db/`)
- SQLAlchemy async engine (`create_async_engine`) — no sync I/O in main thread
- Schema: `users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`
- pgvector extension (pg16) for future RAG/semantic search

### Testing Conventions
- `PYTHONPATH=03-development/src` must be set for all test runs
- Each `tests/test_frXX.py` covers exactly one FR; test function names must match `02-architecture/TEST_SPEC.md`
- Infrastructure stubs (DB, Redis) use dependency injection — tests inject mock callables, not monkeypatching
- `# pragma: no cover` only for genuinely unreachable infrastructure stubs

## Harness-Methodology Framework

This project uses a structured quality gate framework (`harness/` submodule, v2.7.0). Current state: **Phase 7 (Risk Management)**, Gate 4 PASS (score 96.5).

### Phase FSM
State tracked in `.methodology/state.json`. Do not edit manually; use `advance-phase`.

### Gate 4 (14 dimensions, score ≥ 85)
Completed. Results in `.sessi-work/gate4_result.json`.

### Working in Phase 7+
- Per-FR work uses `GATE1-DELTA` (delta check — skips full TDD when code unchanged)
- Deliverables in `07-risk/`: `RISK_REGISTER.md`, `RISK_STATUS_REPORT.md`, `RISK_ASSESSMENT.md`
- All Phase 7 artifacts must contain keyword `QUALITY_REPORT` (ASPICE traceability)

## MCP Tools: code-review-graph

Use CRG tools **before** Grep/Glob/Read for codebase exploration. The graph is pre-built and auto-updates on file changes.

| Tool | Use when |
|------|----------|
| `semantic_search_nodes` | Finding functions/classes by name or concept |
| `query_graph` | Tracing callers, callees, imports (`callers_of`/`tests_for`) |
| `get_impact_radius` | Understanding blast radius before editing |
| `detect_changes` | Risk-scored review of recent edits |
| `get_architecture_overview` | High-level structural overview |
| `generate_wiki` | Refresh wiki pages before DA challenge or architecture review |

Fall back to `grep`/`Read` only when the graph doesn't cover what you need.
