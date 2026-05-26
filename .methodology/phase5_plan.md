# Phase 5 Full Execution Plan -- omnibot-new

> **Version**: v2.4.0 (project plan)
> **Project**: omnibot-new
> **Date**: 2026-05-26
> **Framework**: harness-methodology v2.4.0
> **Phase**: 5 - Verification & Delivery
> **Status**: Full version (including Phase 5 detailed tasks)

---

## Phase 5 Tasks: Verification & Delivery

### Phase 5 Overview
Phase 5 verifies the system against test results, ensuring all FRs meet acceptance criteria.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). No phase-exit gate — P5 was cleared by Gate 3 at P4 exit.

> If code changes are needed for any FR (e.g., bug fixes found during verification), run full TDD: `run-fr-step --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1. Crash recovery (`resume-fr-phase`) auto-detects code changes and switches from GATE1-DELTA to full TDD when needed.

> **Crash Recovery**: `python3 harness_cli.py resume-fr-phase --phase 5 --project .`
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
> - MILESTONE: P5-baseline push (BASELINE.md generated) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Gate 3 PASS:
  Proof: .methodology/quality_manifest.json records Gate 3 PASS from P4.
  If NOT confirmed: return to Phase 4 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 5 --project .
  ```
  If FAILED: fix FSM/Constitution/Drift issues. There is no gate bypass flag.
  Re-run `run-phase` after each fix. Max 3 attempts.
  After 3 FAIL: escalate to human — provide last `run-phase --phase 5` full output.
  Human fix → re-run `run-phase --phase 5 --project .` → PASS required before continuing.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. Phase 5 confirmed in `.methodology/state.json` (`advance-phase` already run)
  > If stale: run `python3 harness_cli.py init-project --phase 5 --project . --overwrite`

### FR Verification Tasks (22 total)

#### FR-01: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-01
- [ ] Run integration tests for FR-01
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-01** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-01 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-01 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-01` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-01
  python3 scripts/generate_sab.py --project .
  ```

#### FR-02: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-02
- [ ] Run integration tests for FR-02
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-02** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-02 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-02 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-02` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-02
  python3 scripts/generate_sab.py --project .
  ```

#### FR-03: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-03
- [ ] Run integration tests for FR-03
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-03** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-03 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-03 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-03` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-03
  python3 scripts/generate_sab.py --project .
  ```

#### FR-04: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-04
- [ ] Run integration tests for FR-04
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-04** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-04 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-04 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-04` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-04
  python3 scripts/generate_sab.py --project .
  ```

#### FR-05: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-05
- [ ] Run integration tests for FR-05
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-05** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-05 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-05 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-05` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-05
  python3 scripts/generate_sab.py --project .
  ```

#### FR-06: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-06
- [ ] Run integration tests for FR-06
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-06** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-06 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-06 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-06` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-06
  python3 scripts/generate_sab.py --project .
  ```

#### FR-07: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-07
- [ ] Run integration tests for FR-07
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-07** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-07 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-07 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-07` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-07
  python3 scripts/generate_sab.py --project .
  ```

#### FR-08: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-08
- [ ] Run integration tests for FR-08
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-08** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-08 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-08 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-08` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-08
  python3 scripts/generate_sab.py --project .
  ```

#### FR-09: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-09
- [ ] Run integration tests for FR-09
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-09** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-09 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-09 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-09` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-09
  python3 scripts/generate_sab.py --project .
  ```

#### FR-10: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-10
- [ ] Run integration tests for FR-10
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-10** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-10 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-10 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-10` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-10
  python3 scripts/generate_sab.py --project .
  ```

#### FR-11: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-11
- [ ] Run integration tests for FR-11
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-11** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-11 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-11 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-11` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-11
  python3 scripts/generate_sab.py --project .
  ```

#### FR-12: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-12
- [ ] Run integration tests for FR-12
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-12** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-12 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-12 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-12` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-12
  python3 scripts/generate_sab.py --project .
  ```

#### FR-13: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-13
- [ ] Run integration tests for FR-13
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-13** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-13 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-13 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-13` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-13
  python3 scripts/generate_sab.py --project .
  ```

#### FR-14: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-14
- [ ] Run integration tests for FR-14
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-14** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-14 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-14 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-14` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-14
  python3 scripts/generate_sab.py --project .
  ```

#### FR-15: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-15
- [ ] Run integration tests for FR-15
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-15** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-15 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-15 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-15` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-15
  python3 scripts/generate_sab.py --project .
  ```

#### FR-16: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-16
- [ ] Run integration tests for FR-16
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-16** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-16 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-16 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-16` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-16
  python3 scripts/generate_sab.py --project .
  ```

#### FR-17: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-17
- [ ] Run integration tests for FR-17
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-17** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-17 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-17 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-17` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-17
  python3 scripts/generate_sab.py --project .
  ```

#### FR-18: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-18
- [ ] Run integration tests for FR-18
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-18** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-18 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-18 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-18` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-18
  python3 scripts/generate_sab.py --project .
  ```

#### FR-19: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-19
- [ ] Run integration tests for FR-19
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-19** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-19 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-19 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-19` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-19
  python3 scripts/generate_sab.py --project .
  ```

#### FR-20: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-20
- [ ] Run integration tests for FR-20
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-20** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-20 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-20 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-20` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-20
  python3 scripts/generate_sab.py --project .
  ```

#### FR-21: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-21
- [ ] Run integration tests for FR-21
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-21** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-21 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-21 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-21` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-21
  python3 scripts/generate_sab.py --project .
  ```

#### FR-22: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-22
- [ ] Run integration tests for FR-22
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**Gate 1 Re-evaluation — FR-22** (carry-forward · sub-agent dispatch):
- [x] **[ORCH-GATE1-DELTA]** Dispatch GATE1-DELTA evaluator sub-agent:
  ```bash
  python3 harness_cli.py run-fr-step --phase 5 --fr-id FR-22 \
    --step GATE1-DELTA --project .
  ```
  → Code-change detection: git diff FR-22 files since last Gate 1 PASS
  → No changes → skip (idempotent — safe to re-run)
  → Changes detected → full GATE1 re-evaluation (3 dims: linting/type_safety/test_coverage)
  → GitHub push: ✅ auto-done by run-fr-step
  → GATE1 FAIL: auto-dispatches CODE-FIX sub-agent → retries (max 3 rounds)
  → exit 2 = BLOCKED: human intervention required before continuing
  → Human fix → re-run `run-fr-step --step GATE1-DELTA --fr-id FR-22` → exit 0 required before continuing.

- [ ] **[ORCH-POST]** After GATE1-DELTA PASS — orchestrator runs directly:
  ```bash
  python3 harness_cli.py spec-coverage-check --project . --threshold 40.0 --fr-id FR-22
  python3 scripts/generate_sab.py --project .
  ```

- [ ] Integration tests pass
- [ ] Performance tests meet targets
- [ ] Security scan passes
- [ ] Baseline established

### P5 Milestone Push (10-Push Strategy ⑦)

- [ ] **PUSH ⑦ — P5-baseline** (after BASELINE.md is generated):
  ```bash
  python3 harness_cli.py push-milestone --type p5-baseline --project .
  ```
  > Writes HANDOVER.md + commits + pushes.

### Phase 5 Deliverables
- [ ] `BASELINE.md` - System baseline
- [ ] `VERIFICATION_REPORT.md` - Verification report
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_PLAN.md` by filename keyword `TEST_PLAN` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_RESULTS.md` by filename keyword `TEST_RESULTS` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 5 → Phase 6: Quality Assurance

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Generate Phase 6 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 6 --project . \
    --output .methodology/phase6_plan.md
  ```
- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

- [ ] **[TDD-PRECHECK]** Verify TDD checks pass — advance-phase enforces both:
  - `pytest --tb=short -q --cov=03-development/src --cov-fail-under=100` (exit 9)
  - `python3 harness_cli.py spec-coverage-check --project . --threshold 80.0` (exit 10, D4 unified v2.6)
  > For genuinely untestable lines add: `# pragma: no cover` (requires justification comment).

- [ ] Advance FSM to Phase 6 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 5 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 6 entry (`P6-entry` checkpoint, correct plan path)
- [ ] Open `phase6_plan.md` and follow from the top.
- [ ] If session crashes during Phase 6: read `HANDOVER.md` or run `generate-next-plan`