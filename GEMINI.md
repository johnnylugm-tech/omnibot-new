<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.

---

## 🛡️ 防禦性系統工程審計協議 (Defensive System Audit Protocol, DSAP)

當你被要求進行「代碼審查 (Code Review)」、「系統審計 (System Audit)」、「程式碼重構」或「生成執行計劃」時，必須無條件遵守以下四重防禦性協議：

### §1. 憲章至上與反向測試防護 (Grounding First & Test-Mock Defense)
*   **核心原則**：`CONSTITUTION.md`（團隊憲章）具備最高法效優先級（憲章 > SAD > 代碼與測試）。
*   **執行協議**：
    1. 禁盲目信任現有的單元測試（即便測試全數綠燈）。
    2. 必須以憲章定義的門檻、維度、與角色分配表作為唯一的權威真理來源。
    3. 若發現現有代碼或測試的斷言（例如 `assert gate1_dims == 4`）與憲章規定衝突，**必須**判定該測試本身為 Bug 並予以重構，絕不允許為了順應既有測試綠燈而妥協規格。

### §2. 深度指令語意審計 (Deep Semantic Command Audit)
*   **核心原則**：嚴禁僅做表層 Checkbox 存在性或 Markdown 標題的「結構性視覺驗證」。
*   **執行協議**：
    1. 當審計任務計畫或代碼時，必須深入至底層具體執行的 Shell 指令（例如 `run-fr-step --step TDD-RED` vs `GATE1-DELTA`）進行逐字校對。
    2. 必須進行語意與定位的雙向驗證：確保該指令的執行行為（如：開發 vs 驗證），與當前 Phase 的核心定位（如：Phase 4 Testing）100% 吻合。

### §3. 自癒路徑閉環化 (Corrective Path Completeness)
*   **核心原則**：不允許任何「懸空狀態門檻（Dangling Thresholds）」。
*   **執行協議**：
    1. 在設計或審查 any 帶有閾值的檢測步驟（如 `Phase Truth ≥ 90%` 或 `Gate score ≥ 80`）時，必須強制在其下方配對設計出完整的 `FAIL` 降級、診斷、自癒與人手介入路徑。
    2. 統一採用以下防禦性自癒範式：
       > **[門檻條件]** ...
       > `FAIL` → 檢查日誌檔或輸出定位失敗維度 → 修復相關 artifacts → 重新執行檢測
       > 連續 3 次失敗 → 強制觸發 `PAUSE` 並將錯誤日誌彙整，escalate 至人類（Johnny）。

### §4. 全局一致性交叉矩陣 (Global Consistency Matrix Check)
*   **核心原則**：禁止孤立單點審查。
*   **執行協議**：
    1. 當產出物為多個關聯 Markdown 計劃或配置文件時，禁止單個檔案孤立審核。
    2. 必須建立全局一致性矩陣，橫向交叉比對：跨階段過渡邊界、命名空間、版本編號、以及 Checkpoint 的命名語意（如：統一使用 `CHECKPOINT-GATE-{gate_num}` 與 `CHECKPOINT-PEER-REVIEW`，禁止出現混淆的硬編碼）。
