# Phase 7 Full Execution Plan -- omnibot-new

> **Version**: v2.4.0 (project plan)
> **Project**: omnibot-new
> **Date**: 2026-05-30
> **Framework**: harness-methodology v2.4.0
> **Phase**: 7 - Risk Management
> **Status**: Full version (including Phase 7 detailed tasks)
> **Mode**: Dynamic (load-context at execution time)


---

## Phase 7 Tasks: Risk Management

### Phase 7 Overview
Phase 7 identifies, tracks, and mitigates all risks introduced during development.
Each FR gets a Gate 1 risk-aware re-evaluation (CHECKPOINT). No harness run-gate — P7 cleared by Gate 4. However, advance-phase still enforces TDD-PRECHECK (pytest 100% + D4 spec-coverage ≥90%) before FSM transition.

> If risk mitigation requires code changes to any FR, run full TDD: `run-fr-step --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1. Crash recovery (`resume-fr-phase`) auto-detects code changes and switches from GATE1-DELTA to full TDD when needed.

> **Crash Recovery**: `python3 harness_cli.py resume-fr-phase --phase 7 --project .`
> prints the next pending step. Each `run-fr-step` auto-pushes to GitHub on completion.
> Per-FR TDD-RED/GREEN/IMPROVE/GATE1 each push immediately (idempotent on re-run).
> At milestones, `HANDOVER.md` is written with phase/FR/status summary.

> **Checkpoint Index**:
> - MILESTONE: P7 exit push (risk register complete) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Gate 4 PASS:
  Proof: .methodology/quality_manifest.json records Gate 4 PASS from P6.
  If NOT confirmed: return to Phase 6 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 7 --project .
  ```
  If FAILED: fix FSM/Constitution/Drift issues. There is no gate bypass flag.
  Re-run `run-phase` after each fix. Max 3 attempts.
  After 3 FAIL: escalate to human — provide last `run-phase --phase 7` full output.
  Human fix → re-run `run-phase --phase 7 --project .` → PASS required before continuing.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. Phase 7 confirmed in `.methodology/state.json` (`advance-phase` already run)
  > If stale: run `python3 harness_cli.py init-project --phase 7 --project . --overwrite`

### 🔄 [PHASE-CONTEXT] — Load Before Starting

```bash
python3 harness_cli.py load-context --phase 7 --project . --json \
  > .sessi-work/phase7_ctx.json
```
> Outputs `fr_ids`, `fr_details`, `modules` from current project state.
> All `{FR-ID}` references in tasks below come from this file.

### FR Tasks — Expanded at Execution Time

> Read `fr_ids` from `.sessi-work/phase7_ctx.json`.
> For each `{FR-ID}` in the list, execute the template below:

---
**{FR-ID} — {FR-TITLE from fr_details}**

- [ ] **[ORCH-GATE1-DELTA]** `run-fr-step --phase 7 --fr-id {FR-ID} --step GATE1-DELTA --project .`
> Crash recovery: `resume-fr-phase` auto-detects code changes → switches to full TDD if needed.
>
> **GATE1-DELTA outcomes:**
> - CASE 1 PASS:    Gate 1 PASS → continue to next {FR-ID}
> - CASE 2 FAIL:    Gate 1 FAIL → full TDD auto-triggered by crash recovery:
>   `run-fr-step --phase 7 --fr-id {FR-ID} --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1
> - CASE 3 BLOCKED: 3 TDD rounds still failing → escalate to human.
>   Provide: last Gate 1 output + pytest failure log.

---

### P7 Risk Register Generation

> Generate risk deliverables ONCE before per-FR evaluation (orchestrator runs directly).

- [ ] **[RISK-REGISTER]** Generate `07-risk/RISK_REGISTER.md`:
  - Review open issues from Gate 3/4, `deferred_fixes.md`, and `.sessi-work/issue_registry.json`
  - For each risk: ID, name, likelihood (1–5), impact (1–5), category, mitigation approach
- [ ] **[RISK-MITIGATION]** Generate `07-risk/RISK_MITIGATION_PLANS.md`:
  - For HIGH risks (likelihood × impact ≥ 9): write formal mitigation plan with owner + deadline
- [ ] **[RISK-STATUS]** Generate `07-risk/RISK_STATUS_REPORT.md`:
  - Summary of all risks, current status, mitigation owner, target date

### P7 Milestone Push (10-Push Strategy ⑨)

- [ ] **PUSH ⑨ — P7 exit** (after risk register is complete):
  ```bash
  python3 harness_cli.py push-milestone --type p7 --project .
  ```
  > Writes HANDOVER.md + commits + pushes.

### Phase 7 Deliverables
- [ ] `07-risk/RISK_REGISTER.md` - Risk register
- [ ] `07-risk/RISK_MITIGATION_PLANS.md` - Mitigation plans
- [ ] `07-risk/RISK_STATUS_REPORT.md` - Risk status report
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 7 MUST reference `06-quality/QUALITY_REPORT.md` by filename keyword `QUALITY_REPORT` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 7 → Phase 8: Configuration Management

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

- [ ] **[TDD-PRECHECK]** Verify TDD checks pass — advance-phase enforces both:
  - `pytest --tb=short -q --cov=03-development/src --cov-fail-under=100` (exit 9)
  - `python3 harness_cli.py spec-coverage-check --project . --threshold 90.0` (exit 10, D4 unified v2.6)
  > For genuinely untestable lines add: `# pragma: no cover` (requires justification comment).

- [ ] Advance FSM to Phase 8 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 7 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 8 entry (`P8-entry` checkpoint, correct plan path)
- [ ] Open `phase8_plan.md` and follow from the top.
- [ ] If session crashes during Phase 8: read `HANDOVER.md` or run `generate-next-plan`
