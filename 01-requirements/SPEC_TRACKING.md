# Specification Tracking Matrix — OmniBot

> Human-readable tracking view across the 28 in-scope FRs + 6 deferred FRs + 8 NFRs transcribed from `SPEC.md`. This matrix is **NOT** the SSOT for status or gate score — `advance-phase` refreshes each FR's Status cell from `build_traceability`'s live code/test scan (IN_PROGRESS once code/module exists, VERIFIED once code+test exist), and the authoritative gate score lives in `quality_manifest.json`. Hand-fill the semantic columns (Spec Description / Intent Class / Decision Framework / Notes); leave Status to refresh itself.

## Project Info
- Project Name: OmniBot
- Version: v1.0.0
- Created: 2026-08-25
- Updated: 2026-09-04
- Phase: 1 — Requirements
- Canonical spec source: `SPEC.md` (repo root, 7464 lines, 28 in-scope FRs + 6 deferred FRs + 8 NFRs)

## Specification Status

| FR ID | Spec Description (canonical) | Intent Class | Decision Framework | Status | Notes |
|-------|------------------------------|--------------|---------------------|--------|-------|
| FR-01 | 多通路訊息接入與正規化 (Multi-Platform Ingress & Normalization) — `SPEC.md:1172` | Integration Adapter | Adapter-pattern; per-platform normalizer | DRAFT | adapters.ingress; 4-boundary path suite per FR-01.AC1..AC4 |
| FR-02 | Webhook 簽名驗證與認證 (Webhook Signature Verification & M2M Authentication) — `SPEC.md:1407` | Security Auth | HMAC-SHA256 verifier + constant-time compare | DRAFT | security.auth; HMAC unit + 4-boundary path suite per FR-02.AC1..AC4 |
| FR-03 | PALADIN L1 輸入清理與字元正規化 (Input Sanitization & Homoglyph Normalization) — `SPEC.md:1580` | Security Pre-processing | NFKC + homoglyph translation table | DRAFT | security.paladin.l1; NFKC + homoglyph unit tests per FR-03.AC1..AC4 |
| FR-04 | PALADIN L2 規則過濾與特徵比對 (Pattern Detection & Anti-Prompt Injection) — `SPEC.md:1690` | Security Pattern Matching | Rule-engine + injection corpus | DRAFT | security.paladin.l2; pattern rule unit tests + injection corpus per FR-04.AC1..AC4 |
| FR-05 | PALADIN L3 指令層次與三明治防護 (Instruction Hierarchy & Sandwich Defense) — `SPEC.md:1765` | Security Prompt Engineering | Sandwich-defense template + hierarchy enforcement | DRAFT | security.paladin.l3; sandwich + hierarchy test suite per FR-05.AC1..AC4 |
| FR-06 | PALADIN L4 語義注入分類器與平行化管線 (Semantic Injection Classifier & Async Pipeline) — `SPEC.md:1922` | Security ML Classifier | Async classifier + parallel pipeline | DRAFT | security.paladin.l4; async classifier + pipeline suite per FR-06.AC1..AC4 |
| FR-07 | PALADIN L5 Grounding 知識對齊檢驗 (Grounding Check & Hallucination Mitigation) — `SPEC.md:2899` | Knowledge Alignment | Citation-required response gate | DRAFT | grounding.check; grounding alignment suite + 100% knowledge alignment per FR-07.AC1..AC4 |
| FR-08 | PII 偵測、去識別化與 Luhn 校驗 (PII Masking & Luhn Credit Card Validation) — `SPEC.md:2169` | Security PII | Regex + Luhn checksum | DRAFT | security.pii; PII detector + Luhn unit tests per FR-08.AC1..AC4 |
| FR-09 | 分散式速率限制 (Distributed Rate Limiting with Redis & Lua) — `SPEC.md:2435` | Infrastructure Rate Limit | Redis Lua atomic counter + sliding window | DRAFT | ratelimit.redis; Redis Lua atomic + sliding window suite per FR-09.AC1..AC4 |
| FR-10 | CIDR 格式 IP 白名單檢查 (CIDR-based IP Whitelist Enforcement) — `SPEC.md:2617` | Security Network | ipaddress CIDR membership | DRAFT | security.ip_whitelist; CIDR match unit tests per FR-10.AC1..AC4 |
| FR-11 | 多輪情緒分析與時間衰減模型 (Multi-turn Emotion Analyzer & Half-Life Decay) — `SPEC.md:4099` | Dialogue Emotion | Multi-turn buffer + half-life decay model | DRAFT | emotion.analyzer; multi-turn + half-life unit tests per FR-11.AC1..AC4 |
| FR-12 | 對話狀態追蹤 DST 與意圖路由 (Dialogue State Tracking & Intent Router FSM) — `SPEC.md:3604` | Dialogue State | FSM transitions + intent routing | DRAFT | dialog.dst; FSM transition + intent routing suite per FR-12.AC1..AC4 |
| FR-13 | 知識檢索 Tier 1 (PostgreSQL 精確與關鍵字匹配) — `SPEC.md:3070` | Knowledge Retrieval | PostgreSQL exact + keyword match | DRAFT | knowledge.tier1; exact/keyword match integration suite per FR-13.AC1..AC4 |
| FR-14 | 知識檢索 Tier 2 (pgvector HNSW + RRF k=60 & Parent-Child) — `SPEC.md:3146` | Knowledge Retrieval | pgvector HNSW + RRF fusion k=60 + parent-child chunking | DRAFT | knowledge.tier2; pgvector HNSW + RRF benchmark suite per FR-14.AC1..AC4 |
| FR-15 | 知識檢索 Tier 3 (LLM 生成與多模型備援) — `SPEC.md:3222` | Knowledge Retrieval | LLM generation + multi-model fallback | DRAFT | knowledge.tier3; LLM fallback switch + multi-model suite per FR-15.AC1..AC4 |
| FR-16 | 動作執行引擎 (Agentic Action Execution via MCP / A2A / Function Calling) — `SPEC.md:3754` | Action Execution | Tool adapter (MCP / A2A / function-calling) | DRAFT | actions.engine; tool adapter + AEE suite per FR-16.AC1..AC4 |
| FR-17 | 回覆生成與語氣調適 (Response Generator & Dynamic Tone Adjustment) — `SPEC.md:4736` | Response Generation | Template + tone adapter | DRAFT | response.generator; template + tone adapter suite per FR-17.AC1..AC4 |
| FR-18 | 7 大角色 RBAC 權限管理 (Role-Based Access Control & Decorator Middleware) — `SPEC.md:4389` | Security Authorization | Decorator middleware + 7-role matrix | DRAFT | rbac.middleware; RBAC decorator + 7-role matrix suite per FR-18.AC1..AC4 |
| FR-19 | 人工轉接與 SLA 優先佇列 (Human Escalation & Priority Queuing via WebSocket) — `SPEC.md:4236` | Operational Escalation | Priority queue + WebSocket | DRAFT | escalation.queue; priority queue + WebSocket escalation suite per FR-19.AC1..AC4 |
| FR-20 | LLM-as-a-Judge 自動評測框架 (LLM-as-a-Judge Evaluation Framework) — `SPEC.md:263` | Evaluation | LLM-as-judge + rubric + calibration | DRAFT | eval.judge; judge + rubric + calibration suite per FR-20.AC1..AC4 |
| FR-21 | 結構化可觀測性與分散式追蹤 (Structured Logging, Prometheus Metrics & OpenTelemetry) — `SPEC.md:4938` | Observability | OTel SDK + Prometheus exporters | DRAFT | observability.core; OTel + Prometheus metric suite per FR-21.AC1..AC4 |
| FR-22 | 異步背景任務系統 (Background Job System with SAQ Worker & Embedding Pipeline) — `SPEC.md:5194` | Infrastructure Async | SAQ worker + embedding pipeline | DRAFT | jobs.saq; SAQ worker + embedding pipeline suite per FR-22.AC1..AC4 |
| FR-23 | GDPR 資料生命週期與合規管理 (GDPR Data Lifecycle, Export & Deletion) — `SPEC.md:2319` | Compliance | Export + deletion lifecycle | DRAFT | compliance.gdpr; export + deletion lifecycle suite per FR-23.AC1..AC4 |
| FR-24 | A/B Testing 實驗框架 (Deterministic SHA-256 Hash Experimentation Framework) — `SPEC.md:4567` | Evaluation Experimentation | Deterministic SHA-256 hash + assignment | DRAFT | experiment.ab; deterministic hash + assignment suite per FR-24.AC1..AC4 |
| FR-25 | 多媒體訊息處理與處置策略 (Multimedia Message Handling & Escalation Path) — `SPEC.md:1291` | Integration Multimedia | Media handler + escalate-to-human policy | DRAFT | adapters.media; multimedia escalate-to-human suite per FR-25.AC1..AC4 |
| FR-26 | 使用者與 M2M Token 管理 API (User Management & M2M Token Lifecycle API) — `SPEC.md:986` | API Management | User CRUD + token rotation lifecycle | DRAFT | api.users + api.m2m; user CRUD + token rotation suite per FR-26.AC1..AC4 |
| FR-27 | 對話上下文視窗管理 (Conversation Context Window Management) — `SPEC.md:3962` | Dialogue Context | Sliding window + token budget | DRAFT | dialog.context; sliding window + token budget suite per FR-27.AC1..AC4 |
| FR-28 | 高可用性、Redis 異步流與故障隔離 (High Availability, Redis Streams & Circuit Breaker) — `SPEC.md:5521` | Reliability HA | Redis Streams + Circuit Breaker | DRAFT | ha.redis + ha.circuit_breaker; circuit breaker + Redis Streams suite per FR-28.AC1..AC4 |
| FR-29-deferred | 原生多模態視覺理解 — `SPEC.md:7036` | Deferred Capability | NFR-99 — pending GPT-4V / Claude Vision cost-benefit | DEFERRED | (deferred to v9.0) |
| FR-30-deferred | 檔案與文件 OCR/AI 解析 — `SPEC.md:7039` | Deferred Capability | NFR-99 — pending Document AI module | DEFERRED | (deferred to v9.1) |
| FR-31-deferred | 即時語音與音訊串流處理 — `SPEC.md:7042` | Deferred Capability | NFR-99 — STT/TTS latency risk vs p95<1.0s | DEFERRED | (deferred to voice-specific track) |
| FR-32-deferred | 繁中與英文以外之多語系支援 — `SPEC.md:7045` | Deferred Capability | NFR-99 — scope limited to zh-TW + en | DEFERRED | (deferred to i18n phase) |
| FR-33-deferred | 自建 In-house LLM 微調管線 — `SPEC.md:7048` | Deferred Capability | NFR-99 — current 4-Tier + RAG already 90% FCR | DEFERRED | (deferred pending cost-benefit) |
| FR-34-deferred | 原生行動端 App — `SPEC.md:7051` | Deferred Capability | NFR-99 — Telegram/LINE/WA/Messenger/Web widgets cover mobile | DEFERRED | (deferred; web-channel sufficient) |

## Non-Functional Requirements Tracking

| NFR ID | Type | Spec Description (canonical) | Decision Framework | Status | Notes |
|--------|------|------------------------------|---------------------|--------|-------|
| NFR-01 | performance | p95 e2e ≤ 1.0s @ 2000 TPS sustained; PALADIN L1~L3 ≤ 5ms; L4 async ≤ 200ms; 知識搜尋 p95 ≤ 150ms; Embedding p95 ≤ 100ms; Admin UI ≤ 1.5s — `SPEC.md:7077` | k6 + Prometheus p95 histogram (4 scenarios: Functional/Stress/Spike/Soak) | DRAFT | Gate 3 / Gate 4 enforcement |
| NFR-02 | security | OWASP LLM Top 10 (2025) 100% 覆蓋; Gitleaks = 100; Bandit ≥ 80 (0 High/Critical); PALADIN Block rate ≥ 95%; RBAC 7 角色強制; PG TDE + TLS 1.3 + Redis TLS/AUTH/ACL — `SPEC.md:7083` | bandit + gitleaks + semgrep + red-team prompt injection suite | DRAFT | Gate 1~4 enforcement |
| NFR-03 | maintainability | 函式 ≤ 50 行、CC ≤ 10; Ruff ≥ 90; Pyright ≥ 85; Alembic 雙向 100% roundtrip; Code-to-SAD 對映率 = 100% — `SPEC.md:7089` | radon-mi + ruff + pyright + alembic upgrade/downgrade + SAD mapping | DRAFT | Gate 1~4 enforcement |
| NFR-04 | reliability | 月可用性 ≥ 99.9%; tool/A2A RPC timeout ≤ 2.0s; 重試 ≤ 3 次 with exponential backoff + jitter; LLM fallback switch < 500ms; Redis fail-open; MTTR < 5min — `SPEC.md:7095` | Prometheus SLO + Chaos Mesh DR drill + Circuit Breaker unit tests | DRAFT | Gate 3 / Gate 4 enforcement |
| NFR-05 | testability | Line coverage Gate 1 owned 100%; Gate 2/Gate 4 全庫 ≥ 90%; Mutation Killed ≥ 80%; D4 Spec cov Gate 1 ≥ 40% / Gate 2 ≥ 60% / Gate 3 ≥ 80% / Gate 4 ≥ 90%; 黃金數據 ≥ 500 samples, Kappa ≥ 0.7 — `SPEC.md:7101` | pytest-cov + mutmut + tests/golden/ calibration | DRAFT | Gate 1~4 enforcement |
| NFR-06 | deployability | Docker Compose + K8s Deployment/Service/HPA; HPA CPU > 70% / Memory > 80%; RollingUpdate maxSurge=25%, maxUnavailable=0; Rollback < 5min — `SPEC.md:7107` | kubectl rollout undo + Helm chart lint + GitOps | DRAFT | P8 enforcement |
| NFR-07 | scalability | 2000 TPS sustained under 4 k6 scenarios; pgvector HNSW (m=16, ef_construction=64) 至 10M chunks; Redis Cluster ready + connection pooling — `SPEC.md:7113` | k6 ≥ 30 min soak + pgvector benchmark + redis-cli cluster create | DRAFT | Gate 3 / Gate 4 enforcement |
| NFR-08 | usability | CSAT ≥ 4.8/5.0; LLM-Judge Politeness ≥ 4.5/5.0 with zh-TW empathy; Accuracy 100% 知識對齊; Admin/Agent portal WebSocket 即時同步 — `SPEC.md:7119` | FR-20 LLM-as-a-Judge + 月度真人抽樣校準 (n ≥ 100, Kappa ≥ 0.7) | DRAFT | Gate 3 / Gate 4 enforcement |

## Completeness Verification

| Check | Target | Actual | Status |
|-------|--------|--------|--------|
| FR transcription coverage (in-scope FR-01..FR-28) | 28/28 | 28/28 | OK |
| Deferred FR markers (FR-29..FR-34) | 6/6 marked `-deferred` | 6/6 | OK |
| NFR transcription coverage (NFR-01..NFR-08) | 8/8 | 8/8 | OK |
| Canonical spec source path | bare `SPEC.md` (root) | bare `SPEC.md` (root) | OK |
| Canonical citation per FR/NFR | 100% | 100% | OK |
| Status cell authority | `build_traceability` / `quality_manifest.json` (machine-refreshed) | hand-fill left blank for refresh | OK |

## Update log

| Date | Change | By |
|------|--------|----|
| 2026-08-25 | Initial template creation | Agent A |
| 2026-09-04 | Round 1: populated all 28 in-scope FRs + 6 deferred FRs + 8 NFRs from SRS.md; canonical spec source path normalized to bare `SPEC.md` (root) per harness `check_forward_refs` guard; Status cells intentionally left for `advance-phase` to machine-refresh from `build_traceability`. | Agent A |
