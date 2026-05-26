# Phase 4 Full Execution Plan -- omnibot-new

> **Version**: v2.4.0 (project plan)
> **Project**: omnibot-new
> **Date**: 2026-05-26
> **Framework**: harness-methodology v2.4.0
> **Phase**: 4 - Testing
> **Status**: Full version (including Phase 4 detailed tasks)

---

## Phase 4 Tasks: Test Planning & Execution

### Phase 4 Overview
Phase 4 formulates and executes a complete test plan based on Phase 3 code.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). Phase exits via Gate 3 (14 dims).

> **Crash Recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step. Each `run-fr-step` auto-pushes to GitHub on completion.
> Per-FR TDD-RED/GREEN/IMPROVE/GATE1 each push immediately (idempotent on re-run).
> At milestones, `HANDOVER.md` is written with phase/FR/status summary.

> **Checkpoint Index**:
> - CHECKPOINT-1: Gate 1 / FR-01 *(auto-push via run-fr-step)*
> - CHECKPOINT-2: Gate 1 / FR-02 *(auto-push via run-fr-step)*
> - CHECKPOINT-3: Gate 1 / FR-03 *(auto-push via run-fr-step)*
> - CHECKPOINT-4: Gate 1 / FR-04 *(auto-push via run-fr-step)*
> - CHECKPOINT-5: Gate 1 / FR-05 *(auto-push via run-fr-step)*
> - CHECKPOINT-6: Gate 1 / FR-06 *(auto-push via run-fr-step)*
> - CHECKPOINT-7: Gate 1 / FR-07 *(auto-push via run-fr-step)*
> - CHECKPOINT-8: Gate 1 / FR-08 *(auto-push via run-fr-step)*
> - CHECKPOINT-9: Gate 1 / FR-09 *(auto-push via run-fr-step)*
> - CHECKPOINT-10: Gate 1 / FR-10 *(auto-push via run-fr-step)*
> - CHECKPOINT-11: Gate 1 / FR-11 *(auto-push via run-fr-step)*
> - CHECKPOINT-12: Gate 1 / FR-12 *(auto-push via run-fr-step)*
> - CHECKPOINT-13: Gate 1 / FR-13 *(auto-push via run-fr-step)*
> - CHECKPOINT-14: Gate 1 / FR-14 *(auto-push via run-fr-step)*
> - CHECKPOINT-15: Gate 1 / FR-15 *(auto-push via run-fr-step)*
> - CHECKPOINT-16: Gate 1 / FR-16 *(auto-push via run-fr-step)*
> - CHECKPOINT-17: Gate 1 / FR-17 *(auto-push via run-fr-step)*
> - CHECKPOINT-18: Gate 1 / FR-18 *(auto-push via run-fr-step)*
> - CHECKPOINT-19: Gate 1 / FR-19 *(auto-push via run-fr-step)*
> - CHECKPOINT-20: Gate 1 / FR-20 *(auto-push via run-fr-step)*
> - CHECKPOINT-21: Gate 1 / FR-21 *(auto-push via run-fr-step)*
> - CHECKPOINT-22: Gate 1 / FR-22 *(auto-push via run-fr-step)*
> - CHECKPOINT-23: Gate 3 (Phase 4 Exit) → **push + HANDOVER.md**

### Entry Gate Verification

- [x] **[ENTRY-CHECK]** Gate 2 PASS:
  Proof: .methodology/quality_manifest.json records Gate 2 PASS from P3.
  If NOT confirmed: return to Phase 3 and complete exit gate first.

### Pre-Phase Preflight

- [x] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 4 --project .
  ```
  If FAILED: fix FSM/Constitution/Drift issues. There is no gate bypass flag.
  Re-run `run-phase` after each fix. Max 3 attempts.
  After 3 FAIL: escalate to human — provide last `run-phase --phase 4` full output.
  Human fix → re-run `run-phase --phase 4 --project .` → PASS required before continuing.

- [x] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. Phase 4 confirmed in `.methodology/state.json` (`advance-phase` already run)
  > If stale: run `python3 harness_cli.py init-project --phase 4 --project . --overwrite`

### CHECKPOINT-0: Generate TEST_PLAN.md

> Generate `04-testing/TEST_PLAN.md` from SRS.md FR acceptance criteria.
> This step runs once before per-FR test execution.

**Generate TEST_PLAN.md** (orchestrator runs directly — not a sub-agent dispatch):
- [x] Read SRS.md FR acceptance criteria → write TEST_PLAN.md with per-FR test cases
  - For each FR: test case ID, description, input, expected output, priority
  - Include positive, negative, boundary, and edge case categories
  - Output: `04-testing/TEST_PLAN.md`
- [x] Verify TEST_PLAN.md covers all FRs from manifest/quality_manifest.json
- [x] **[TP-DONE]** TEST_PLAN.md written: all FRs have ≥1 test case, NFRs addressed

### FR Test Coverage

#### FR-01: Create complete PostgreSQL schema with all core tables (`users`, `conversations`
**Test Target**: Verify Create complete PostgreSQL schema with all core tables (`users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`) plus indexe...

**TDD — FR-01** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-01:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-01 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-01`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-01:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-01 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr01.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-01:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-01 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr01.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-01:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-01 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-01): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-01` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-01
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-02: Accept Telegram Bot API webhook POST requests, parse the platform-specific paylo
**Test Target**: Verify Accept Telegram Bot API webhook POST requests, parse the platform-specific payload, and produce an immutable `UnifiedMessage` dataclass instance per SPEC.md §Unified Message Format. Must extract `p...

**TDD — FR-02** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-02:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-02 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-02`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-02:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-02 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr02.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-02:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-02 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr02.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-02:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-02 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-02): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-02` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-02
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-03: Accept LINE Messaging API webhook POST requests, parse the platform-specific pay
**Test Target**: Verify Accept LINE Messaging API webhook POST requests, parse the platform-specific payload, and produce an immutable `UnifiedMessage` dataclass instance. Must extract `reply_token` from LINE events.

**TDD — FR-03** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-03:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-03 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-03`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-03:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-03 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr03.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-03:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-03 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr03.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-03:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-03 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-03): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-03` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-03
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-04: Verify Telegram webhook request authenticity using HMAC-SHA256 over the secret k
**Test Target**: Verify Verify Telegram webhook request authenticity using HMAC-SHA256 over the secret key derived from `bot_token`. Reject with `AUTH_INVALID_SIGNATURE` (401) if verification fails. Per SPEC.md §Webhook S...

**TDD — FR-04** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-04:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-04 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-04`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-04:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-04 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr04.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-04:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-04 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr04.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-04:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-04 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-04): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-04` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-04
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-05: Verify LINE webhook request authenticity using HMAC-SHA256 over `channel_secret`
**Test Target**: Verify Verify LINE webhook request authenticity using HMAC-SHA256 over `channel_secret` with Base64-encoded digest comparison. Reject with `AUTH_INVALID_SIGNATURE` (401) if verification fails. Per SPEC.md...

**TDD — FR-05** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-05:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-05 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-05`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-05:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-05 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr05.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-05:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-05 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr05.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-05:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-05 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-05): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-05` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-05
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-06: Define and enforce the immutable `UnifiedMessage` dataclass with all required fi
**Test Target**: Verify Define and enforce the immutable `UnifiedMessage` dataclass with all required fields (`platform`, `platform_user_id`, `unified_user_id`, `message_type`, `content`, `raw_payload`, `received_at`, `re...

**TDD — FR-06** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-06:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-06 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-06`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-06:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-06 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr06.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-06:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-06 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr06.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-06:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-06 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-06): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-06` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-06
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-07: Define the generic `ApiResponse[T]` and `PaginatedResponse[T]` dataclasses per S
**Test Target**: Verify Define the generic `ApiResponse[T]` and `PaginatedResponse[T]` dataclasses per SPEC.md §API Design — Unified Response Format. `ApiResponse` must carry `success`, `data`, `error`, `error_code`. `Pag...

**TDD — FR-07** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-07:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-07 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-07`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-07:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-07 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr07.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-07:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-07 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr07.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-07:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-07 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-07): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-07` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-07
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-08: Normalize all inbound message text using Unicode NFKC normalization, strip non-p
**Test Target**: Verify Normalize all inbound message text using Unicode NFKC normalization, strip non-printable characters (except `\n` and `\t`), and trim whitespace. Per SPEC.md §Security Layer — Input Sanitizer L2. Mu...

**TDD — FR-08** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-08:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-08 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-08`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-08:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-08 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr08.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-08:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-08 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr08.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-08:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-08 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-08): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-08` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-08
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-09: Detect and mask PII patterns in message text: phone numbers (Taiwan formats `\d{
**Test Target**: Verify Detect and mask PII patterns in message text: phone numbers (Taiwan formats `\d{4}-\d{3,4}-\d{3,4}` and `\d{10,11}`), email addresses, and Taiwan-formatted addresses (city/county + road/street/lane...

**TDD — FR-09** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-09:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-09 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-09`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-09:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-09 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr09.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-09:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-09 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr09.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-09:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-09 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-09): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-09` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-09
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-10: Enforce per-platform per-user rate limiting using the Token Bucket algorithm. De
**Test Target**: Verify Enforce per-platform per-user rate limiting using the Token Bucket algorithm. Default capacity and refill rate of 100 tokens/second. Requests exceeding the limit receive HTTP 429 with `RATE_LIMIT_E...

**TDD — FR-10** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-10:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-10 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-10`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-10:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-10 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr10.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-10:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-10 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr10.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-10:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-10 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-10): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-10` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-10
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-11: Query `knowledge_base` table for matching answers using SQL `ILIKE` on question 
**Test Target**: Verify Query `knowledge_base` table for matching answers using SQL `ILIKE` on question text and `= ANY(keywords)` array match. Return a `KnowledgeResult` with `source="rule"`, confidence 0.95 for exact su...

**TDD — FR-11** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-11:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-11 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-11`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-11:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-11 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr11.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-11:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-11 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr11.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-11:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-11 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-11): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-11` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-11
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-12: When no rule match is found (Layer 1 returns None), create an escalation record 
**Test Target**: Verify When no rule match is found (Layer 1 returns None), create an escalation record in `escalation_queue` with `reason="no_rule_match"` or `"out_of_scope"`, priority=0 (normal), and return a `Knowledge...

**TDD — FR-12** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-12:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-12 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-12`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-12:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-12 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr12.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-12:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-12 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr12.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-12:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-12 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-12): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-12` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-12
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-13: Emit all log entries as single-line JSON objects with fields: `timestamp` (ISO 8
**Test Target**: Verify Emit all log entries as single-line JSON objects with fields: `timestamp` (ISO 8601 UTC), `level` (DEBUG/INFO/WARN/ERROR/CRITICAL), `service` (configurable, default "omnibot"), `message`, and arbit...

**TDD — FR-13** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-13:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-13 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-13`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-13:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-13 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr13.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-13:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-13 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr13.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-13:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-13 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-13): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-13` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-13
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-14: Expose `GET /api/v1/health` returning JSON `{"status": "healthy
**Test Target**: Verify Expose `GET /api/v1/health` returning JSON `{"status": "healthy

**TDD — FR-14** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-14:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-14 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-14`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-14:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-14 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr14.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-14:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-14 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr14.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-14:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-14 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-14): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-14` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-14
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-15: Provide a `docker-compose.yml` with services: `omnibot-api` (build from ., port 
**Test Target**: Verify Provide a `docker-compose.yml` with services: `omnibot-api` (build from ., port 8000, healthcheck via `/api/v1/health`, depends on postgres+redis with `condition: service_healthy`), `postgres` (pgv...

**TDD — FR-15** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-15:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-15 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-15`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-15:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-15 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr15.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-15:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-15 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr15.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-15:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-15 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-15): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-15` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-15
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-16: Provide SQL query scripts for Phase 1 ODD metrics: (a) FCR rate calculation over
**Test Target**: Verify Provide SQL query scripts for Phase 1 ODD metrics: (a) FCR rate calculation over 30-day window for `scope_type='in_scope'` conversations with non-null `first_contact_resolution`, (b) average and p9...

**TDD — FR-16** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-16:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-16 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-16`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-16:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-16 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr16.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-16:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-16 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr16.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-16:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-16 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-16): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-16` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-16
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-17: Define and use standardized error codes for Phase 1: `AUTH_INVALID_SIGNATURE` (4
**Test Target**: Verify Define and use standardized error codes for Phase 1: `AUTH_INVALID_SIGNATURE` (401), `RATE_LIMIT_EXCEEDED` (429), `KNOWLEDGE_NOT_FOUND` (404), `VALIDATION_ERROR` (422), `INTERNAL_ERROR` (500). Each...

**TDD — FR-17** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-17:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-17 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-17`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-17:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-17 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr17.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-17:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-17 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr17.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-17:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-17 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-17): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-17` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-17
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-18: All Phase 1 Python code must follow constitution §4 naming conventions: `snake_c
**Test Target**: Verify All Phase 1 Python code must follow constitution §4 naming conventions: `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE` for constants; all public functions must have d...

**TDD — FR-18** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-18:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-18 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-18`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-18:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-18 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr18.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-18:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-18 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr18.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-18:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-18 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-18): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-18` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-18
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-19: Implement the core message processing pipeline that orchestrates each inbound re
**Test Target**: Verify Implement the core message processing pipeline that orchestrates each inbound request end-to-end: (1) IP Whitelist interception → (2) webhook signature verification → (3) platform adapter parse → (...

**TDD — FR-19** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-19:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-19 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-19`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-19:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-19 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr19.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-19:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-19 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr19.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-19:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-19 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-19): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-19` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-19
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-20: Define the immutable `UnifiedResponse` dataclass representing the system reply w
**Test Target**: Verify Define the immutable `UnifiedResponse` dataclass representing the system reply with fields: `platform`, `user_id`, `content` (the text to send back), `source` (KnowledgeSource enum: `rule`/`escalat...

**TDD — FR-20** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-20:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-20 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-20`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-20:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-20 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr20.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-20:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-20 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr20.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-20:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-20 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-20): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-20` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-20
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-21: Load and manage configuration from environment variables and/or a `config.yaml` 
**Test Target**: Verify Load and manage configuration from environment variables and/or a `config.yaml` file: bot tokens (`TELEGRAM_BOT_TOKEN`, `LINE_CHANNEL_ACCESS_TOKEN`), channel secrets (`TELEGRAM_WEBHOOK_SECRET`, `LI...

**TDD — FR-21** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-21:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-21 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-21`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-21:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-21 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr21.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-21:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-21 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr21.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-21:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-21 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-21): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-21` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-21
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

#### FR-22: Implement IP Whitelist interception to filter out requests from unofficial IPs b
**Test Target**: Verify Implement IP Whitelist interception to filter out requests from unofficial IPs before computing HMAC signature. Unofficial IPs must be rejected with HTTP 403. Missing or empty IPs must be rejected ...

**TDD — FR-22** (Orchestrator dispatches sub-agents · push after each step):

- [x] **[ORCH-RED]** Dispatch TDD-RED sub-agent for FR-22:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-22 --step TDD-RED \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `git log --oneline -1` shows `test(RED): failing test for FR-22`
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GREEN]** Dispatch TDD-GREEN sub-agent for FR-22:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-22 --step TDD-GREEN \
    --project . --srs 01-requirements/SRS.md
  ```
  → Verify: `pytest tests/test_fr22.py -q` all pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-IMPROVE]** Dispatch TDD-IMPROVE sub-agent for FR-22:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-22 --step TDD-IMPROVE \
    --project .
  ```
  → Verify: `pytest tests/test_fr22.py -q` still pass
  → GitHub push: ✅ auto-done by run-fr-step

- [x] **[ORCH-GATE1]** Dispatch GATE1 evaluator sub-agent for FR-22:
  ```bash
  python3 harness_cli.py run-fr-step --phase 4 --fr-id FR-22 --step GATE1 \
    --project .
  ```
  → Verify: `git log --oneline -1` shows `feat(FR-22): Gate1 PASS`
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1 --fr-id FR-22` → exit 0 required before continuing.

- [x] **[ORCH-POST]** After GATE1 PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-22
  python3 scripts/generate_sab.py --project .
  ```

> 💡 **Crash recovery**: `python3 harness_cli.py resume-fr-phase --phase 4 --project .`
> prints the next pending step (idempotent on re-run).

### TEST_RESULTS.md Summary (required for C5 P4 audit)

- [x] **[TEST-RESULTS-SUMMARY]** Finalize `04-testing/TEST_RESULTS.md` before milestone push:
  - Add execution summary line: `N passed, M failed` or `Pass Rate: N%` (required — C5 P4 audit checks for pass rate pattern)
  - Ensure ≥3 TC-XX or TR-XX references appear across the document (C5 P4 audit requires tc_refs + tr_refs ≥ 3)

### P4 Milestone Pushes

> Per-FR steps push automatically via `run-fr-step`. The two **milestone pushes** below
> also write `HANDOVER.md` with phase/FR/status summary and push to origin.
> All FR IDs in this project: FR-01,FR-02,FR-03,FR-04,FR-05,…+17

- [x] **P4-mid** (trigger when ≥11/22 FRs have Gate 1 PASS):
  ```bash
  python3 harness_cli.py push-milestone --type p4-mid --project . \
    --fr-done 11 --fr-total 22 --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11
  ```
  > `--fr-ids` lists the FRs with Gate 1 PASS so far. Replace `FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11` with actual.
  > Writes HANDOVER.md + commits + pushes. Next session reads HANDOVER.md to resume.

- [x] **P4-pre-gate3** (trigger when all 22 FRs Gate 1 PASS, before Gate 3):
  ```bash
  python3 harness_cli.py push-milestone --type p4-pre-gate3 --project . \
    --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12,FR-13,FR-14,FR-15,FR-16,FR-17,FR-18,FR-19,FR-20,FR-21,FR-22
  ```
  > Last stable snapshot before Gate 3 evaluation. HANDOVER.md + push.


### 🔒 CHECKPOINT-23: Gate 3 — Phase 4 Exit
> linting(90) · type_safety(85) · test_coverage(80) · security(80) · secrets_scanning(100) · license_compliance(100) · mutation_testing(70) · integration_coverage(60) · architecture(80) · readability(80) · error_handling(80) · documentation(75) · test_assertion_quality(60) · performance(75)  [CRG recon inside run-gate · D4 spec-coverage unified ≥80%]

- [x] **G3a** Prepare Gate 3:
  ```bash
  python3 harness_cli.py run-gate --gate 3 --phase 4 --project .
  ```
  Read the evaluation prompt printed above.
  (CRG recon triggered inside run-gate automatically — no separate action needed)

- [x] **G3b** Evaluate all Gate 3 dimensions inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate3_result.json`
  - Failing dim: fix code → re-evaluate → re-score

- [x] **G3c** Finalize Gate 3:
  ```bash
  python3 harness_cli.py finalize-gate --gate 3 --phase 4 --project .
  ```
- [x] **[D4]** D4 spec-coverage-check — unified v2.6 (Gate 3 threshold 80%):
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 80.0
  ```
  FAIL → fix missing test implementations → re-run until coverage meets threshold

  **Early-stop cases after G3c:**
  - CASE 1 PASS:     score ≥ score_gate AND critical==0 → `quality_complete=True` → G3d
  - CASE 2 CONTINUE: score ≥ score_gate BUT issues remain → fix → repeat G3a
  - CASE 3 PLATEAU:  3 consecutive rounds, no new issues → `deferred_fixes.md` → proceed to push
  - CASE 4 BLOCKED:  max_rounds exhausted, not PASS → `GateBlockedError` → escalate to human
    > Human fix → re-run `run-gate --gate 3 → finalize-gate --gate 3` → CASE 1 PASS required before continuing.

- [x] **G3d** ✅ Verify checkpoint saved (finalize-gate above already pushed + wrote HANDOVER.md):
  ```bash
  # Confirm HANDOVER.md exists at project root (written by finalize-gate → commit_and_push_gate)
  ls -la HANDOVER.md
  git log --oneline -1
  ```
  > `finalize-gate --gate 3` (G3c) calls `commit_and_push_gate()` which writes
  > `HANDOVER.md` **before** committing + pushing. No separate push needed here.
  > If HANDOVER.md is missing, re-run `finalize-gate` (do **not** raw-push).

- [x] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

### Phase 4 Deliverables
- [x] `TEST_PLAN.md` - Test plan
- [x] `TEST_RESULTS.md` - Test results (pass rate summary + ≥3 TC/TR refs required)
- [x] `COVERAGE_REPORT.md` - Coverage report
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner
- [x] Gate 1 PASS for every FR
- [x] Gate 3 PASS (phase exit, composite ≥ 80, 14 dims)

#### ASPICE Traceability Requirements (enforced by postflight)

- [x] **[ASPICE]** Artifact for Phase 4 MUST reference `03-development/src` by filename keyword `src` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [x] **[ASPICE]** Artifact for Phase 4 MUST reference `03-development/tests/` by filename keyword `tests` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 4 → Phase 5: Verification & Delivery

- [x] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [x] Generate Phase 5 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 5 --project . \
    --output .methodology/phase5_plan.md
  ```
- [x] **[TDD-PRECHECK]** Verify TDD checks pass — advance-phase enforces both:
  - `pytest --tb=short -q --cov=03-development/src --cov-fail-under=100` (exit 9)
  - `python3 harness_cli.py spec-coverage-check --project . --threshold 80.0` (exit 10, D4 unified v2.6)
  > For genuinely untestable lines add: `# pragma: no cover` (requires justification comment).

- [x] Advance FSM to Phase 5 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 4 --project .
  ```
- [x] Confirm `HANDOVER.md` reflects Phase 5 entry (`P5-entry` checkpoint, correct plan path)
- [x] Open `phase5_plan.md` and follow from the top.
- [x] If session crashes during Phase 5: read `HANDOVER.md` or run `generate-next-plan`
