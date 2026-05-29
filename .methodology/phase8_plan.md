# Phase 8 Full Execution Plan -- omnibot-new

> **Version**: v2.4.0 (project plan)
> **Project**: omnibot-new
> **Date**: 2026-05-30
> **Framework**: harness-methodology v2.4.0
> **Phase**: 8 - Configuration Management
> **Status**: Full version (including Phase 8 detailed tasks)
> **Mode**: Dynamic (load-context at execution time)


---

## Phase 8 Tasks: Configuration Management

### Phase 8 Overview
Phase 8 establishes a complete configuration management system ensuring traceability.
Each FR gets a Gate 1 config-aware re-evaluation (CHECKPOINT). No harness run-gate — P8 cleared by Gate 4. However, advance-phase still enforces TDD-PRECHECK (pytest 100% + D4 spec-coverage ≥90%) before FSM transition.

> If configuration changes require code modifications to any FR, run full TDD: `run-fr-step --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1. Crash recovery (`resume-fr-phase`) auto-detects code changes and switches from GATE1-DELTA to full TDD when needed.

> **Crash Recovery**: `python3 harness_cli.py resume-fr-phase --phase 8 --project .`
> prints the next pending step. Each `run-fr-step` auto-pushes to GitHub on completion.
> Per-FR TDD-RED/GREEN/IMPROVE/GATE1 each push immediately (idempotent on re-run).
> At milestones, `HANDOVER.md` is written with phase/FR/status summary.

> **Checkpoint Index**:
> - MILESTONE: P8 exit push (config records complete) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Gate 4 PASS (P6 exit — P7 has no exit gate, P7 completed stands between):
  Proof: .methodology/quality_manifest.json records Gate 4 PASS from P6.
  If NOT confirmed: return to Phase 6 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 8 --project .
  ```
  If FAILED: fix FSM/Constitution/Drift issues. There is no gate bypass flag.
  Re-run `run-phase` after each fix. Max 3 attempts.
  After 3 FAIL: escalate to human — provide last `run-phase --phase 8` full output.
  Human fix → re-run `run-phase --phase 8 --project .` → PASS required before continuing.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. Phase 8 confirmed in `.methodology/state.json` (`advance-phase` already run)
  > If stale: run `python3 harness_cli.py init-project --phase 8 --project . --overwrite`

### 🔄 [PHASE-CONTEXT] — Load Before Starting

```bash
python3 harness_cli.py load-context --phase 8 --project . --json \
  > .sessi-work/phase8_ctx.json
```
> Outputs `fr_ids`, `fr_details`, `modules` from current project state.
> All `{FR-ID}` references in tasks below come from this file.

### FR Tasks — Expanded at Execution Time

> Read `fr_ids` from `.sessi-work/phase8_ctx.json`.
> For each `{FR-ID}` in the list, execute the template below:

---
**{FR-ID} — {FR-TITLE from fr_details}**

- [ ] **[ORCH-GATE1-DELTA]** `run-fr-step --phase 8 --fr-id {FR-ID} --step GATE1-DELTA --project .`
> Crash recovery: `resume-fr-phase` auto-detects code changes → switches to full TDD if needed.
>
> **GATE1-DELTA outcomes:**
> - CASE 1 PASS:    Gate 1 PASS → continue to next {FR-ID}
> - CASE 2 FAIL:    Gate 1 FAIL → full TDD auto-triggered by crash recovery:
>   `run-fr-step --phase 8 --fr-id {FR-ID} --step TDD-RED` → TDD-GREEN → TDD-IMPROVE → GATE1
> - CASE 3 BLOCKED: 3 TDD rounds still failing → escalate to human.
>   Provide: last Gate 1 output + pytest failure log.

---

### P8 Archive — REQUIRED before push-milestone (CI p8-archive-check)

- [ ] **[P8-ARCHIVE]** Create `.methodology-archive/` directory (required for CI `p8-archive-check`):
  ```bash
  mkdir -p .methodology-archive
  cp -r .sessi-work/ .methodology-archive/
  ```
  > Must run BEFORE `push-milestone --type p8`; `_validate_p8_completion()` in push-milestone auto-verifies.
  > CI job `p8-archive-check` also validates this directory on push to main.

- [ ] **[P8-HANDOVER-CHECK]** Verify `HANDOVER.md` has no Phase 9 references (validated by CI `p8-archive-check`):
  ```bash
  grep -qi "phase 9\|phase9\|phase9_plan" HANDOVER.md \
    && echo "ERROR: Phase 9 refs found — remove them" \
    || echo "OK: no Phase 9 refs"
  ```
  Phase 8 is the final phase. Any Phase 9 references must be removed.

### P8 Milestone Push (10-Push Strategy ⑩)

- [ ] **PUSH ⑩ — P8 exit** (after config records are complete):
  ```bash
  python3 harness_cli.py push-milestone --type p8 --project .
  ```
  > Writes HANDOVER.md + commits + pushes. Pipeline complete.

### Phase 8 Deliverables
- [ ] `CONFIG_RECORDS.md` - Configuration records
- [ ] `RELEASE_CHECKLIST.md` - Release checklist
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_STATUS_REPORT.md` by filename keyword `RISK_STATUS_REPORT` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_REGISTER.md` by filename keyword `RISK_REGISTER` (ASPICE traceability — `postflight_artifact_links()` enforces this)


- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

### 🎉 Pipeline Complete

- [ ] All 8 phases complete. Archive `.methodology/` for the audit trail.
