# Software Requirements Specification (SRS) — OmniBot

> Phase: 1 — Requirements | Last Gate: Gate None | Updated: 2026-09-04
> Canonical source: SPEC.md (341375 bytes, 7464 lines, 28 in-scope FRs + 6 deferred FRs + 8 NFRs).

## 1. Requirements Overview

OmniBot is a multi-platform (Telegram / LINE / Messenger / WhatsApp / Web / A2A) customer-service conversational agent with PALADIN five-layer defense, four-tier knowledge retrieval, deterministic A/B testing, and LLM-as-a-Judge evaluation. This SRS transcribes 100% of the FRs (FR-01..FR-28 in scope; FR-29..FR-34 explicitly deferred per SPEC.md:7036-7055) and the eight NFRs (NFR-01..NFR-08 per SPEC.md:7064-7126) from `SPEC.md`. Canonical citations accompany every AC; deferred items are recorded with `FR-NN-deferred` markers per the harness P1 ingestion contract.

## 2. Functional Requirements

| ID | Requirement Description (canonical) | Implementation Module | Verification Method |
|----|--------------------------------------|------------------------|---------------------|
| FR-01 | 多通路訊息接入與正規化 (Multi-Platform Ingress & Normalization) — SPEC.md:1172 | adapters.ingress | 4-boundary path suite (Happy/Auth/Throttle/Degradation) per FR-01.AC1..AC4 |
| FR-02 | Webhook 簽名驗證與認證 (Webhook Signature Verification & M2M Authentication) — SPEC.md:1407 | security.auth | HMAC-SHA256 verifier unit tests + 4-boundary path suite per FR-02.AC1..AC4 |
| FR-03 | PALADIN L1 輸入清理與字元正規化 (Input Sanitization & Homoglyph Normalization) — SPEC.md:1580 | security.paladin.l1 | NFKC + homoglyph translation unit tests per FR-03.AC1..AC4 |
| FR-04 | PALADIN L2 規則過濾與特徵比對 (Pattern Detection & Anti-Prompt Injection) — SPEC.md:1690 | security.paladin.l2 | Pattern rule unit tests + injection corpus per FR-04.AC1..AC4 |
| FR-05 | PALADIN L3 指令層次與三明治防護 (Instruction Hierarchy & Sandwich Defense) — SPEC.md:1765 | security.paladin.l3 | Sandwich defense + hierarchy test suite per FR-05.AC1..AC4 |
| FR-06 | PALADIN L4 語義注入分類器與平行化管線 (Semantic Injection Classifier & Async Pipeline) — SPEC.md:1922 | security.paladin.l4 | Async classifier + pipeline test suite per FR-06.AC1..AC4 |
| FR-07 | PALADIN L5 Grounding 知識對齊檢驗 (Grounding Check & Hallucination Mitigation) — SPEC.md:2899 | grounding.check | Grounding alignment suite + knowledge alignment 100% per FR-07.AC1..AC4 |
| FR-08 | PII 偵測、去識別化與 Luhn 校驗 (PII Masking & Luhn Credit Card Validation) — SPEC.md:2169 | security.pii | PII detector + Luhn check unit tests per FR-08.AC1..AC4 |
| FR-09 | 分散式速率限制 (Distributed Rate Limiting with Redis & Lua) — SPEC.md:2435 | ratelimit.redis | Redis Lua atomic counter + sliding window suite per FR-09.AC1..AC4 |
| FR-10 | CIDR 格式 IP 白名單檢查 (CIDR-based IP Whitelist Enforcement) — SPEC.md:2617 | security.ip_whitelist | CIDR match unit tests per FR-10.AC1..AC4 |
| FR-11 | 多輪情緒分析與時間衰減模型 (Multi-turn Emotion Analyzer & Half-Life Decay) — SPEC.md:4099 | emotion.analyzer | Multi-turn emotion + half-life decay unit tests per FR-11.AC1..AC4 |
| FR-12 | 對話狀態追蹤 DST 與意圖路由 (Dialogue State Tracking & Intent Router FSM) — SPEC.md:3604 | dialog.dst | FSM transition + intent routing suite per FR-12.AC1..AC4 |
| FR-13 | 知識檢索 Tier 1 (PostgreSQL 精確與關鍵字匹配) — SPEC.md:3070 | knowledge.tier1 | Exact/keyword match integration suite per FR-13.AC1..AC4 |
| FR-14 | 知識檢索 Tier 2 (pgvector HNSW + RRF k=60 & Parent-Child) — SPEC.md:3146 | knowledge.tier2 | pgvector HNSW + RRF benchmark suite per FR-14.AC1..AC4 |
| FR-15 | 知識檢索 Tier 3 (LLM 生成與多模型備援) — SPEC.md:3222 | knowledge.tier3 | LLM fallback switch + multi-model suite per FR-15.AC1..AC4 |
| FR-16 | 動作執行引擎 (Agentic Action Execution via MCP / A2A / Function Calling) — SPEC.md:3754 | actions.engine | Tool adapter + AEE suite per FR-16.AC1..AC4 |
| FR-17 | 回覆生成與語氣調適 (Response Generator & Dynamic Tone Adjustment) — SPEC.md:4736 | response.generator | Template + tone adapter suite per FR-17.AC1..AC4 |
| FR-18 | 7 大角色 RBAC 權限管理 (Role-Based Access Control & Decorator Middleware) — SPEC.md:4389 | rbac.middleware | RBAC decorator + 7-role matrix suite per FR-18.AC1..AC4 |
| FR-19 | 人工轉接與 SLA 優先佇列 (Human Escalation & Priority Queuing via WebSocket) — SPEC.md:4236 | escalation.queue | Priority queue + WebSocket escalation suite per FR-19.AC1..AC4 |
| FR-20 | LLM-as-a-Judge 自動評測框架 (LLM-as-a-Judge Evaluation Framework) — SPEC.md:263 | eval.judge | Judge + rubric + calibration suite per FR-20.AC1..AC4 |
| FR-21 | 結構化可觀測性與分散式追蹤 (Structured Logging, Prometheus Metrics & OpenTelemetry) — SPEC.md:4938 | observability.core | OTel + Prometheus metric suite per FR-21.AC1..AC4 |
| FR-22 | 異步背景任務系統 (Background Job System with SAQ Worker & Embedding Pipeline) — SPEC.md:5194 | jobs.saq | SAQ worker + embedding pipeline suite per FR-22.AC1..AC4 |
| FR-23 | GDPR 資料生命週期與合規管理 (GDPR Data Lifecycle, Export & Deletion) — SPEC.md:2319 | compliance.gdpr | Export + deletion lifecycle suite per FR-23.AC1..AC4 |
| FR-24 | A/B Testing 實驗框架 (Deterministic SHA-256 Hash Experimentation Framework) — SPEC.md:4567 | experiment.ab | Deterministic hash + assignment suite per FR-24.AC1..AC4 |
| FR-25 | 多媒體訊息處理與處置策略 (Multimedia Message Handling & Escalation Path) — SPEC.md:1291 | adapters.media | Multimedia escalate-to-human suite per FR-25.AC1..AC4 |
| FR-26 | 使用者與 M2M Token 管理 API (User Management & M2M Token Lifecycle API) — SPEC.md:986 | api.users + api.m2m | User CRUD + token rotation suite per FR-26.AC1..AC4 |
| FR-27 | 對話上下文視窗管理 (Conversation Context Window Management) — SPEC.md:3962 | dialog.context | Sliding window + token budget suite per FR-27.AC1..AC4 |
| FR-28 | 高可用性、Redis 異步流與故障隔離 (High Availability, Redis Streams & Circuit Breaker) — SPEC.md:5521 | ha.redis + ha.circuit_breaker | Circuit breaker + Redis Streams suite per FR-28.AC1..AC4 |
| FR-29-deferred | 原生多模態視覺理解 — SPEC.md:7036 | (deferred to v9.0) | NFR-99 — decision pending GPT-4V / Claude Vision cost-benefit |
| FR-30-deferred | 檔案與文件 OCR/AI 解析 — SPEC.md:7039 | (deferred to v9.1) | NFR-99 — decision pending Document AI module |
| FR-31-deferred | 即時語音與音訊串流處理 — SPEC.md:7042 | (deferred to voice-specific track) | NFR-99 — STT/TTS latency risk vs p95<1.0s |
| FR-32-deferred | 繁中與英文以外之多語系支援 — SPEC.md:7045 | (deferred to i18n phase) | NFR-99 — scope limited to zh-TW + en |
| FR-33-deferred | 自建 In-house LLM 微調管線 — SPEC.md:7048 | (deferred pending cost-benefit) | NFR-99 — current 4-Tier + RAG already 90% FCR |
| FR-34-deferred | 原生行動端 App — SPEC.md:7051 | (deferred; web-channel sufficient) | NFR-99 — Telegram/LINE/WA/Messenger/Web widgets cover mobile |

## 3. Non-Functional Requirements (NFR)

| ID | Type | Requirement (canonical) | Test Method |
|----|------|--------------------------|-------------|
| NFR-01 | performance | 端到端延遲與吞吐量門檻 — p95 e2e ≤ 1.0s @ 2000 TPS sustained; PALADIN L1~L3 ≤ 5ms; PALADIN L4 async ≤ 200ms; 知識搜尋 p95 ≤ 150ms; Embedding API p95 ≤ 100ms; Admin UI page load ≤ 1.5s — SPEC.md:7077 | k6 (4 scenarios: Functional/Stress/Spike/Soak) + Prometheus p95 histogram (Gate 3 / Gate 4) |
| NFR-02 | security | 縱深防禦與合規 — OWASP LLM Top 10 (2025) 100% 條款覆蓋; Gitleaks = 100; Bandit ≥ 80 (0 High/Critical); PALADIN 五層 Block rate ≥ 95%; RBAC 7 角色強制執行; PostgreSQL TDE + TLS 1.3 + Redis TLS/AUTH/ACL — SPEC.md:7083 | bandit + gitleaks + semgrep + red-team prompt injection suite (Gate 1~4) |
| NFR-03 | maintainability | 程式碼品質與文件耦合 — 函式 ≤ 50 行、CC ≤ 10; Ruff ≥ 90; Pyright ≥ 85; Alembic 版本化 migration 雙向 100% roundtrip; Code-to-SAD 對映率 = 100% — SPEC.md:7089 | radon-mi + ruff + pyright + alembic upgrade/downgrade/upgrade + SAD mapping (Gate 1~4) |
| NFR-04 | reliability | 可用性、降級與災難復原 — 月可用性 ≥ 99.9%; 外部 tool / A2A RPC timeout ≤ 2.0s; 重試 ≤ 3 次 with exponential backoff + jitter; LLM fallback switch time < 500ms; Redis fail-open; MTTR < 5 分鐘 — SPEC.md:7095 | Prometheus uptime SLO + Chaos Mesh DR drill + Circuit Breaker unit tests (Gate 3 / Gate 4) |
| NFR-05 | testability | 覆蓋率、突變測試與黃金數據 — Line coverage Gate 1 owned 100%; Gate 2/Gate 4 全庫 ≥ 90%; Mutation Killed Score ≥ 80%; D4 Spec coverage Gate 1 ≥ 40% / Gate 2 ≥ 60% / Gate 3 ≥ 80% / Gate 4 ≥ 90%; 黃金數據 ≥ 500 samples、Cohen's Kappa ≥ 0.7 — SPEC.md:7101 | pytest-cov + mutmut + tests/golden/ calibration (Gate 1~4) |
| NFR-06 | deployability | 容器化與零停機部署 — Docker Compose (dev) + Kubernetes Deployment/Service/HPA (prod); HPA CPU > 70% 或 Memory > 80%; RollingUpdate maxSurge=25%, maxUnavailable=0; Rollback < 5 分鐘 — SPEC.md:7107 | kubectl rollout undo + Helm chart lint + GitOps (P8) |
| NFR-07 | scalability | 持續吞吐量與向量規模 — 2000 TPS sustained under 4 k6 load scenarios; pgvector HNSW (m=16, ef_construction=64) 支援至 10M chunks; Redis Cluster ready + connection pooling — SPEC.md:7113 | k6 sustained ≥ 30 min soak + pgvector benchmark + redis-cli cluster create (Gate 3 / Gate 4) |
| NFR-08 | usability | 客戶滿意度與回覆品質 — CSAT ≥ 4.8/5.0; LLM-Judge Politeness ≥ 4.5/5.0 with zh-TW empathy; Accuracy 100% 知識對齊; Admin/Agent portal WebSocket 即時同步 — SPEC.md:7119 | FR-20 LLM-as-a-Judge 自動評測 + 月度真人抽樣校準 (n ≥ 100, Cohen's Kappa ≥ 0.7) (Gate 3 / Gate 4) |

## 4. Constraints
- {constraint 1}
- {constraint 2}

## 5. Glossary
| Term | Definition |
|------|------------|
| {term} | {definition} |

## 6. Cross-Cutting Test Requirements

> 此章節由 harness P1 模板自動注入，開發者必須填入具體測試名稱後才可進入 P2。
> `verify-spec` 檢查的是 FR→module 追溯完整性（實作是否存在），並非本節
> 的 placeholder 是否已填——填寫本節由人工 review + Agent B P2 審查把關。

### API Completeness（每個端點必須有以下四類測試）
- 正常流程 (2xx)
- 認證失敗 (401)
- 速率限制 (429)
- 驗證錯誤 (400/422)

**待填清單**（開發者補充）：
- [ ] `test_<endpoint>_<scenario>_returns_<status>`
- [ ] ...

### Security Red Team
- [ ] `test_redteam_prompt_injection_direct_<entrypoint>_payload`
- [ ] `test_redteam_rate_limit_burst_attack_blocked`
- [ ] `test_redteam_pii_mixed_<type>_leak_detected`

> These are examples, not an enforced list — the enforced mechanism is
> `02-architecture/SAD.md` §6's STRIDE-lite threat model: every declared
> `threats[]` entry names a `verified_by` test that `check-artifact-
> consistency` requires to exist on disk from Phase 5 onward, and each
> threat forces its matching NFR test pattern in `derive_test_cases.md`
> Step 1c regardless of SRS keywords. Use this section for narrative
> intent; SAD.md §6 is where red-team coverage becomes binding.

### KPI Gates（對應 ODD SQL + k6）
- [ ] `test_kpi_p95_latency_phase<N>_under_<X>s`
- [ ] `test_kpi_fcr_phase<N>_target_<X>_percent`

### Deployment Smoke
- [ ] `test_deploy_docker_compose_all_services_healthy`
- [ ] `test_deploy_health_endpoint_returns_200_after_startup`
- [ ] `test_backup_pg_basebackup_and_restore` (Phase 3+)

### Version Consistency（Phase 2+ 必填）
- [ ] `test_backward_compat_phase<N-1>_tests_pass_in_phase<N>_env`

---

## 7. FR Block (machine-readable)

<!-- FR:START -->
```json
{
  "version": "1.0",
  "created_at": "2026-09-04",
  "phase": 1,
  "project": "omnibot",
  "functional_requirements": [
    {"id": "FR-01", "description": "多通路訊息接入與正規化 (Multi-Platform Ingress & Normalization)", "implementation_functions": ["adapters.ingress"], "verification_method": "4-boundary path suite (FR-01.AC1..AC4)"},
    {"id": "FR-02", "description": "Webhook 簽名驗證與認證 (Webhook Signature Verification & M2M Authentication)", "implementation_functions": ["security.auth"], "verification_method": "HMAC-SHA256 verifier unit + 4-boundary path suite (FR-02.AC1..AC4)"},
    {"id": "FR-03", "description": "PALADIN L1 輸入清理與字元正規化 (Input Sanitization & Homoglyph Normalization)", "implementation_functions": ["security.paladin.l1"], "verification_method": "NFKC + homoglyph translation unit tests (FR-03.AC1..AC4)"},
    {"id": "FR-04", "description": "PALADIN L2 規則過濾與特徵比對 (Pattern Detection & Anti-Prompt Injection)", "implementation_functions": ["security.paladin.l2"], "verification_method": "Pattern rule unit tests + injection corpus (FR-04.AC1..AC4)"},
    {"id": "FR-05", "description": "PALADIN L3 指令層次與三明治防護 (Instruction Hierarchy & Sandwich Defense)", "implementation_functions": ["security.paladin.l3"], "verification_method": "Sandwich defense + hierarchy test suite (FR-05.AC1..AC4)"},
    {"id": "FR-06", "description": "PALADIN L4 語義注入分類器與平行化管線 (Semantic Injection Classifier & Async Pipeline)", "implementation_functions": ["security.paladin.l4"], "verification_method": "Async classifier + pipeline test suite (FR-06.AC1..AC4)"},
    {"id": "FR-07", "description": "PALADIN L5 Grounding 知識對齊檢驗 (Grounding Check & Hallucination Mitigation)", "implementation_functions": ["grounding.check"], "verification_method": "Grounding alignment suite + knowledge alignment 100% (FR-07.AC1..AC4)"},
    {"id": "FR-08", "description": "PII 偵測、去識別化與 Luhn 校驗 (PII Masking & Luhn Credit Card Validation)", "implementation_functions": ["security.pii"], "verification_method": "PII detector + Luhn check unit tests (FR-08.AC1..AC4)"},
    {"id": "FR-09", "description": "分散式速率限制 (Distributed Rate Limiting with Redis & Lua)", "implementation_functions": ["ratelimit.redis"], "verification_method": "Redis Lua atomic counter + sliding window suite (FR-09.AC1..AC4)"},
    {"id": "FR-10", "description": "CIDR 格式 IP 白名單檢查 (CIDR-based IP Whitelist Enforcement)", "implementation_functions": ["security.ip_whitelist"], "verification_method": "CIDR match unit tests (FR-10.AC1..AC4)"},
    {"id": "FR-11", "description": "多輪情緒分析與時間衰減模型 (Multi-turn Emotion Analyzer & Half-Life Decay)", "implementation_functions": ["emotion.analyzer"], "verification_method": "Multi-turn emotion + half-life decay unit tests (FR-11.AC1..AC4)"},
    {"id": "FR-12", "description": "對話狀態追蹤 DST 與意圖路由 (Dialogue State Tracking & Intent Router FSM)", "implementation_functions": ["dialog.dst"], "verification_method": "FSM transition + intent routing suite (FR-12.AC1..AC4)"},
    {"id": "FR-13", "description": "知識檢索 Tier 1 (PostgreSQL 精確與關鍵字匹配)", "implementation_functions": ["knowledge.tier1"], "verification_method": "Exact/keyword match integration suite (FR-13.AC1..AC4)"},
    {"id": "FR-14", "description": "知識檢索 Tier 2 (pgvector HNSW + RRF k=60 & Parent-Child)", "implementation_functions": ["knowledge.tier2"], "verification_method": "pgvector HNSW + RRF benchmark suite (FR-14.AC1..AC4)"},
    {"id": "FR-15", "description": "知識檢索 Tier 3 (LLM 生成與多模型備援)", "implementation_functions": ["knowledge.tier3"], "verification_method": "LLM fallback switch + multi-model suite (FR-15.AC1..AC4)"},
    {"id": "FR-16", "description": "動作執行引擎 (Agentic Action Execution via MCP / A2A / Function Calling)", "implementation_functions": ["actions.engine"], "verification_method": "Tool adapter + AEE suite (FR-16.AC1..AC4)"},
    {"id": "FR-17", "description": "回覆生成與語氣調適 (Response Generator & Dynamic Tone Adjustment)", "implementation_functions": ["response.generator"], "verification_method": "Template + tone adapter suite (FR-17.AC1..AC4)"},
    {"id": "FR-18", "description": "7 大角色 RBAC 權限管理 (Role-Based Access Control & Decorator Middleware)", "implementation_functions": ["rbac.middleware"], "verification_method": "RBAC decorator + 7-role matrix suite (FR-18.AC1..AC4)"},
    {"id": "FR-19", "description": "人工轉接與 SLA 優先佇列 (Human Escalation & Priority Queuing via WebSocket)", "implementation_functions": ["escalation.queue"], "verification_method": "Priority queue + WebSocket escalation suite (FR-19.AC1..AC4)"},
    {"id": "FR-20", "description": "LLM-as-a-Judge 自動評測框架 (LLM-as-a-Judge Evaluation Framework)", "implementation_functions": ["eval.judge"], "verification_method": "Judge + rubric + calibration suite (FR-20.AC1..AC4)"},
    {"id": "FR-21", "description": "結構化可觀測性與分散式追蹤 (Structured Logging, Prometheus Metrics & OpenTelemetry)", "implementation_functions": ["observability.core"], "verification_method": "OTel + Prometheus metric suite (FR-21.AC1..AC4)"},
    {"id": "FR-22", "description": "異步背景任務系統 (Background Job System with SAQ Worker & Embedding Pipeline)", "implementation_functions": ["jobs.saq"], "verification_method": "SAQ worker + embedding pipeline suite (FR-22.AC1..AC4)"},
    {"id": "FR-23", "description": "GDPR 資料生命週期與合規管理 (GDPR Data Lifecycle, Export & Deletion)", "implementation_functions": ["compliance.gdpr"], "verification_method": "Export + deletion lifecycle suite (FR-23.AC1..AC4)"},
    {"id": "FR-24", "description": "A/B Testing 實驗框架 (Deterministic SHA-256 Hash Experimentation Framework)", "implementation_functions": ["experiment.ab"], "verification_method": "Deterministic hash + assignment suite (FR-24.AC1..AC4)"},
    {"id": "FR-25", "description": "多媒體訊息處理與處置策略 (Multimedia Message Handling & Escalation Path)", "implementation_functions": ["adapters.media"], "verification_method": "Multimedia escalate-to-human suite (FR-25.AC1..AC4)"},
    {"id": "FR-26", "description": "使用者與 M2M Token 管理 API (User Management & M2M Token Lifecycle API)", "implementation_functions": ["api.users", "api.m2m"], "verification_method": "User CRUD + token rotation suite (FR-26.AC1..AC4)"},
    {"id": "FR-27", "description": "對話上下文視窗管理 (Conversation Context Window Management)", "implementation_functions": ["dialog.context"], "verification_method": "Sliding window + token budget suite (FR-27.AC1..AC4)"},
    {"id": "FR-28", "description": "高可用性、Redis 異步流與故障隔離 (High Availability, Redis Streams & Circuit Breaker)", "implementation_functions": ["ha.redis", "ha.circuit_breaker"], "verification_method": "Circuit breaker + Redis Streams suite (FR-28.AC1..AC4)"},
    {"id": "FR-29-deferred", "description": "原生多模態視覺理解 — deferred to v9.0", "implementation_functions": [], "verification_method": "NFR-99 — pending GPT-4V / Claude Vision cost-benefit"},
    {"id": "FR-30-deferred", "description": "檔案與文件 OCR/AI 解析 — deferred to v9.1", "implementation_functions": [], "verification_method": "NFR-99 — pending Document AI module"},
    {"id": "FR-31-deferred", "description": "即時語音與音訊串流處理 — deferred to voice track", "implementation_functions": [], "verification_method": "NFR-99 — STT/TTS latency risk vs p95<1.0s"},
    {"id": "FR-32-deferred", "description": "繁中與英文以外之多語系支援 — deferred to i18n phase", "implementation_functions": [], "verification_method": "NFR-99 — scope limited to zh-TW + en"},
    {"id": "FR-33-deferred", "description": "自建 In-house LLM 微調管線 — deferred pending cost-benefit", "implementation_functions": [], "verification_method": "NFR-99 — current 4-Tier + RAG already 90% FCR"},
    {"id": "FR-34-deferred", "description": "原生行動端 App — deferred; web-channel sufficient", "implementation_functions": [], "verification_method": "NFR-99 — Telegram/LINE/WA/Messenger/Web widgets cover mobile"}
  ],
  "non_functional_requirements": [
    {"id": "NFR-01", "type": "performance", "description": "p95 e2e ≤ 1.0s @ 2000 TPS sustained; PALADIN L1~L3 ≤ 5ms; L4 async ≤ 200ms; 知識搜尋 p95 ≤ 150ms; Embedding p95 ≤ 100ms; Admin UI ≤ 1.5s", "test_method": "k6 (Functional/Stress/Spike/Soak) + Prometheus p95 histogram (Gate 3/4)"},
    {"id": "NFR-02", "type": "security", "description": "OWASP LLM Top 10 (2025) 100% 覆蓋; Gitleaks = 100; Bandit ≥ 80 (0 High/Critical); PALADIN Block rate ≥ 95%; RBAC 7 角色強制; PG TDE + TLS 1.3 + Redis TLS/AUTH/ACL", "test_method": "bandit + gitleaks + semgrep + red-team prompt injection suite (Gate 1~4)"},
    {"id": "NFR-03", "type": "maintainability", "description": "函式 ≤ 50 行、CC ≤ 10; Ruff ≥ 90; Pyright ≥ 85; Alembic 雙向 100% roundtrip; Code-to-SAD 對映率 = 100%", "test_method": "radon-mi + ruff + pyright + alembic upgrade/downgrade + SAD mapping (Gate 1~4)"},
    {"id": "NFR-04", "type": "reliability", "description": "月可用性 ≥ 99.9%; tool/A2A RPC timeout ≤ 2.0s; 重試 ≤ 3 次 with exponential backoff + jitter; LLM fallback switch < 500ms; Redis fail-open; MTTR < 5min", "test_method": "Prometheus SLO + Chaos Mesh DR drill + Circuit Breaker unit tests (Gate 3/4)"},
    {"id": "NFR-05", "type": "testability", "description": "Line coverage Gate 1 owned 100%; Gate 2/4 全庫 ≥ 90%; Mutation Killed ≥ 80%; D4 Spec cov Gate 1 ≥ 40% / Gate 2 ≥ 60% / Gate 3 ≥ 80% / Gate 4 ≥ 90%; 黃金數據 ≥ 500 samples, Kappa ≥ 0.7", "test_method": "pytest-cov + mutmut + tests/golden/ calibration (Gate 1~4)"},
    {"id": "NFR-06", "type": "deployability", "description": "Docker Compose + K8s Deployment/Service/HPA; HPA CPU > 70% / Memory > 80%; RollingUpdate maxSurge=25%, maxUnavailable=0; Rollback < 5min", "test_method": "kubectl rollout undo + Helm chart lint + GitOps (P8)"},
    {"id": "NFR-07", "type": "scalability", "description": "2000 TPS sustained under 4 k6 scenarios; pgvector HNSW (m=16, ef_construction=64) 至 10M chunks; Redis Cluster ready + connection pooling", "test_method": "k6 ≥ 30 min soak + pgvector benchmark + redis-cli cluster create (Gate 3/4)"},
    {"id": "NFR-08", "type": "usability", "description": "CSAT ≥ 4.8/5.0; LLM-Judge Politeness ≥ 4.5/5.0 with zh-TW empathy; Accuracy 100% 知識對齊; Admin/Agent portal WebSocket 即時同步", "test_method": "FR-20 LLM-as-a-Judge + 月度真人抽樣校準 (n ≥ 100, Kappa ≥ 0.7) (Gate 3/4)"}
  ]
}
```
<!-- FR:END -->

Note: `type:` must be one of the values above — this list mirrors
`harness/core/quality_gate/sab_parser.ALL_NFR_TYPES` (the vocabulary Phase 2's
`generate_sab.py --validate` enforces) and is pinned by
`tests/test_sab_parser.py::TestCanonicalTemplate::test_srs_template_nfr_type_example_matches_vocabulary`;
if it ever falls out of sync that test fails.

Note: Fill in the JSON above - used for downstream requirements traceability.
Ingestion mode (PROJECT_BRIEF.md declares a `canonical_spec`): every `### FR-NN`
in the canonical source MUST appear here, and every FR here MUST trace back to a
canonical clause — `harness_cli.py check-spec-alignment` blocks on a dropped or
invented requirement. Defer a canonical FR you cannot yet transcribe as
`FR-NN-deferred` / NFR-99 rather than omitting it.
