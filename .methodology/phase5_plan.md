# Phase 5 Full Execution Plan -- omnibot-new

> **Version**: v2.4.0 (project plan)
> **Project**: omnibot-new
> **Date**: 2026-05-30
> **Framework**: harness-methodology v2.4.0
> **Phase**: 5 - Verification & Delivery
> **Status**: Full version (including Phase 5 detailed tasks)
> **Mode**: Dynamic (load-context at execution time)


---

## Phase 5 Tasks: Verification & Delivery

### Phase 5 Overview
Phase 5 verifies the system against test results, ensuring all FRs meet acceptance criteria.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). No harness run-gate — P5 was cleared by Gate 3 at P4 exit. However, advance-phase still enforces TDD-PRECHECK (pytest 100% + D4 spec-coverage ≥80%) before FSM transition.

> If code changes are needed for any FR (e.g., bug fixes found during verification), run full TDD: `run-fr-step --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1. Crash recovery (`resume-fr-phase`) auto-detects code changes and switches from GATE1-DELTA to full TDD when needed.

> **Crash Recovery**: `python3 harness_cli.py resume-fr-phase --phase 5 --project .`
> prints the next pending step. Each `run-fr-step` auto-pushes to GitHub on completion.
> Per-FR TDD-RED/GREEN/IMPROVE/GATE1 each push immediately (idempotent on re-run).
> At milestones, `HANDOVER.md` is written with phase/FR/status summary.

> **Checkpoint Index**:
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

### 🔄 [PHASE-CONTEXT] — Load Before Starting

```bash
python3 harness_cli.py load-context --phase 5 --project . --json \
  > .sessi-work/phase5_ctx.json
```
> Outputs `fr_ids`, `fr_details`, `modules` from current project state.
> All `{FR-ID}` references in tasks below come from this file.

### FR Tasks — Expanded at Execution Time

> Read `fr_ids` from `.sessi-work/phase5_ctx.json`.
> For each `{FR-ID}` in the list, execute the template below:

---
**{FR-ID} — {FR-TITLE from fr_details}**

- [ ] **[ORCH-GATE1-DELTA]** `run-fr-step --phase 5 --fr-id {FR-ID} --step GATE1-DELTA --project .`
> Crash recovery: `resume-fr-phase` auto-detects code changes → switches to full TDD if needed.
>
> **GATE1-DELTA outcomes:**
> - CASE 1 PASS:    Gate 1 PASS → continue to next {FR-ID}
> - CASE 2 FAIL:    Gate 1 FAIL → full TDD auto-triggered by crash recovery:
>   `run-fr-step --phase 5 --fr-id {FR-ID} --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1
> - CASE 3 BLOCKED: 3 TDD rounds still failing → escalate to human.
>   Provide: last Gate 1 output + pytest failure log.

---

### P5 System Verification

- [ ] **[BASELINE]** Generate `05-verification/BASELINE.md` (system state snapshot):
  - Document: current version, test results summary, coverage %, Gate 3 composite score
  - Reference: `04-testing/TEST_RESULTS.md` and `03-development/src/` module list
- [ ] **[VERIFY-REPORT]** Generate `05-verification/VERIFICATION_REPORT.md`:
  - For each FR: verification status, acceptance criteria result (PASS/FAIL), evidence
  - Include: test coverage %, mutation score, deferred issues from Gate 3
  - Certify: all Gate 3 open issues addressed or deferred with justification
- [ ] Re-run integration tests: `pytest tests/integration/ -q` (or equivalent per NFRs)
- [ ] Confirm performance NFRs met: review benchmark entries in `04-testing/TEST_RESULTS.md`
- [ ] Re-run security scan clean: `bandit -r 03-development/src/ -ll` + `gitleaks detect`

### P5 Milestone Push (10-Push Strategy ⑦)

- [ ] **PUSH ⑦ — P5-baseline** (after BASELINE.md is generated):
  ```bash
  python3 harness_cli.py push-milestone --type p5-baseline --project .
  ```
  > Writes HANDOVER.md + commits + pushes.

### Phase 5 Deliverables
- [ ] `05-verification/BASELINE.md` - System baseline
- [ ] `05-verification/VERIFICATION_REPORT.md` - Verification report
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_PLAN.md` by filename keyword `TEST_PLAN` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_RESULTS.md` by filename keyword `TEST_RESULTS` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 5 → Phase 6: Quality Assurance

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

- [ ] **[D4-GAP WARNING]** Gate 4 (next phase) requires spec-coverage ≥ 90% but current advance threshold is 80%.
  > Close this gap NOW to avoid a surprise Gate 4 D4 block.
  > Check: `python3 harness_cli.py spec-coverage-check --project . --threshold 90.0`
  > If below 90%: add missing test implementations before advancing to Phase 6.

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
