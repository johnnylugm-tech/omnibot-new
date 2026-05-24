### CRITICAL

**C-1: 缺少 `run-phase --phase 3` 官方 CLI 鉤子觸發命令**

| | |
|---|---|
| **phase3 位置** | L58-66，`### Pre-Phase Preflight` |
| **內容** | `python3 harness_cli.py run-phase --phase 3 --project .` |
| **purrfect 狀態** | **確實缺少** — purrfect 只有手動 bash 指令（L30-37），無官方 CLI 鉤子觸發 |
| **功能差異** | `run-phase` 會觸發 FSM/Constitution/Kill-Switch/Drift/CI Readiness 五項鉤子；手動 ls/grep 不會觸發框架鉤子系统 |
| **影響** | 跳過此步 → Constitution/Drift 驗證永不觸發，CI 狀態 drift 無法被攔截 |

### IMPORTANT

**I-1: 缺少 NFR Coverage Table（10 項 NFR + Gate 2 維度說明）**

| | |
|---|---|
| **phase3 位置** | L1308-1324 |
| **內容** | 10 項 NFR 表格 + bandit/gitleaks/mutmut 等 Gate 2 安全維度說明 |
| **purrfect 狀態** | 確實缺少 — 無等價內容 |

**I-2: 缺少 Phase 3 Deliverables 獨立章節**

| | |
|---|---|
| **phase3 位置** | L1395-1401 |
| **內容** | `03-development/src/`、`tests/`、`.methodology/sessions_spawn.log`、Gate1/2 PASS 清單 |
| **purrfect 狀態** | 確實缺少 — 無等價章節 |

**I-3: 缺少 [PHASE-TRUTH] HR-11 ≥90% 驗證標記**

| | |
|---|---|
| **phase3 位置** | L1393 |
| **內容** | `Phase Truth ≥ 90% — verified by advance-phase` |
| **purrfect 狀態** | 確實缺少 — 無此標記 |

**I-4: 缺少 Phase 3 → Phase 4 transition 結尾動作**

| | |
|---|---|
| **phase3 位置** | L1422 |
| **內容** | 「Open phase4_plan.md and follow from the top.」 |
| **purrfect 狀態** | 確實缺少 — purrfect L189-190 有 advance-phase 指令，但結尾無此句 |

---

