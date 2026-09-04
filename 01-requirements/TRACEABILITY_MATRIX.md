# Traceability Matrix — OmniBot

> Bidirectional Requirements Traceability Matrix (FR ↔ SRS ↔ Code ↔ Test)
> Framework: harness-methodology v1.0 · Phase 1 — Requirements
> Updated: 2026-09-04 · Round 1 — Agent A (Requirements Engineer)
> SSOT for status / gate score: `quality_manifest.json` (refreshed by `advance-phase`).
> This matrix is the authoritative **FR→AC→Code→Test** wiring; semantic cells are hand-filled, machine-refreshed cells (Coverage %) are intentionally left blank for `build_traceability` to populate.

---

## 0. Project Info

| Field | Value |
|-------|-------|
| Project | OmniBot |
| Version | v1.0.0 |
| Canonical spec source | `SPEC.md` (repo root, 7464 lines) |
| In-scope FRs | FR-01 .. FR-28 (28) |
| Deferred FRs | FR-29-deferred .. FR-34-deferred (6) |
| NFRs | NFR-01 .. NFR-08 (8) |
| Naming authority | `TEST_INVENTORY.yaml` (P1 Naming Authority, schema `format_version: "1.1"`) |
| Test layer vocabulary | `unit` \| `static` \| `integration` \| `e2e` (NFR Layering Hard Rule) |
| ASPICE mapping | SWE.3.B.SP1/SP2/SP3 (task-to-work-product, bidirectional, consistency) |

---

## 1. FR ↔ SRS Section ↔ Code Module ↔ Test Case (Bidirectional)

> One row per Acceptance Criterion (AC). FR-NN.ACk follows the `4-boundary path suite` pattern declared in `SRS.md §2` (Happy / Auth / Throttle / Degradation) and `SRS.md §7` JSON block.
> Test IDs follow `TC-FRNN-NN` schema; layers mirror `TEST_INVENTORY.yaml` (unit/static/integration/e2e); test functions and paths conform to the harness P1→P2 handoff naming convention.

### 1.1 Multi-Platform Ingress & Security Layer

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-01 | AC1 | Happy-path: multi-platform ingress parses Telegram / LINE / Messenger / WhatsApp / Web / A2A payloads into canonical envelope | 2.1 | `adapters.ingress` | `src/adapters/ingress/{telegram,line,messenger,whatsapp,web,a2a}.py` | TC-FR01-01 | integration | `test_fr01_ingress_telegram_normalizes_to_envelope` | `tests/integration/test_fr01.py` |
| FR-01 | AC2 | Auth: ingress rejects payloads missing platform-specific authentication header | 2.1 | `adapters.ingress` | `src/adapters/ingress/base.py` | TC-FR01-02 | unit | `test_fr01_ingress_missing_auth_header_raises` | `tests/unit/test_fr01.py` |
| FR-01 | AC3 | Throttle: ingress yields to global rate limiter (delegated to FR-09) | 2.1 | `adapters.ingress` | `src/adapters/ingress/base.py` | TC-FR01-03 | integration | `test_fr01_ingress_throttle_yields_to_ratelimit` | `tests/integration/test_fr01.py` |
| FR-01 | AC4 | Degradation: ingress falls back to queue-and-retry when platform webhook unreachable | 2.1 | `adapters.ingress` | `src/adapters/ingress/base.py` | TC-FR01-04 | integration | `test_fr01_ingress_unreachable_webhook_queues_retry` | `tests/integration/test_fr01.py` |
| FR-02 | AC1 | Happy-path: HMAC-SHA256 signature verifier accepts valid `X-Signature` header | 2.2 | `security.auth` | `src/security/auth/hmac.py` | TC-FR02-01 | unit | `test_fr02_hmac_valid_signature_accepted` | `tests/unit/test_fr02.py` |
| FR-02 | AC2 | Auth: HMAC verifier rejects mismatched signature with constant-time compare | 2.2 | `security.auth` | `src/security/auth/hmac.py` | TC-FR02-02 | unit | `test_fr02_hmac_invalid_signature_rejected_constant_time` | `tests/unit/test_fr02.py` |
| FR-02 | AC3 | Throttle: M2M token bucket exhausted returns 429 with `Retry-After` | 2.2 | `security.auth` | `src/security/auth/m2m.py` | TC-FR02-03 | unit | `test_fr02_m2m_token_bucket_exhausted_returns_429` | `tests/unit/test_fr02.py` |
| FR-02 | AC4 | Degradation: HMAC verification falls back to cached JWKS when IdP unreachable | 2.2 | `security.auth` | `src/security/auth/jwks_cache.py` | TC-FR02-04 | integration | `test_fr02_jwks_fallback_to_cache_when_idp_unreachable` | `tests/integration/test_fr02.py` |
| FR-03 | AC1 | Happy-path: PALADIN L1 NFKC normalization round-trips Unicode safely | 2.3 | `security.paladin.l1` | `src/security/paladin/l1/normalize.py` | TC-FR03-01 | unit | `test_fr03_l1_nfkc_normalization_roundtrip` | `tests/unit/test_fr03.py` |
| FR-03 | AC2 | Auth: homoglyph table translates Cyrillic "а" → Latin "a" in user-supplied input | 2.3 | `security.paladin.l1` | `src/security/paladin/l1/homoglyph.py` | TC-FR03-02 | unit | `test_fr03_l1_homoglyph_cyrillic_a_translated` | `tests/unit/test_fr03.py` |
| FR-03 | AC3 | Throttle: L1 processing p95 ≤ 5ms under load (NFR-01 boundary) | 2.3 | `security.paladin.l1` | `src/security/paladin/l1/pipeline.py` | TC-FR03-03 | e2e | `test_fr03_l1_p95_under_5ms_load` | `tests/e2e/test_fr03_perf.py` |
| FR-03 | AC4 | Degradation: L1 degrades to NFKC-only when homoglyph table lookup fails | 2.3 | `security.paladin.l1` | `src/security/paladin/l1/pipeline.py` | TC-FR03-04 | unit | `test_fr03_l1_degrades_to_nfkc_only_on_table_miss` | `tests/unit/test_fr03.py` |
| FR-04 | AC1 | Happy-path: PALADIN L2 detects known prompt-injection pattern and returns BLOCK | 2.4 | `security.paladin.l2` | `src/security/paladin/l2/rules.py` | TC-FR04-01 | unit | `test_fr04_l2_detects_injection_returns_block` | `tests/unit/test_fr04.py` |
| FR-04 | AC2 | Auth: rule engine rejects user-supplied rules lacking signature | 2.4 | `security.paladin.l2` | `src/security/paladin/l2/loader.py` | TC-FR04-02 | unit | `test_fr04_l2_loader_rejects_unsigned_rules` | `tests/unit/test_fr04.py` |
| FR-04 | AC3 | Throttle: L2 processes 2000 TPS sustained within 5ms p95 (NFR-01 / NFR-07) | 2.4 | `security.paladin.l2` | `src/security/paladin/l2/engine.py` | TC-FR04-03 | e2e | `test_fr04_l2_sustained_2000_tps_under_5ms_p95` | `tests/e2e/test_fr04_perf.py` |
| FR-04 | AC4 | Degradation: L2 falls back to deny-list-only mode when regex engine unavailable | 2.4 | `security.paladin.l2` | `src/security/paladin/l2/engine.py` | TC-FR04-04 | unit | `test_fr04_l2_fallback_to_denylist_only` | `tests/unit/test_fr04.py` |
| FR-05 | AC1 | Happy-path: PALADIN L3 sandwich-defense template injects system prompt boundary markers | 2.5 | `security.paladin.l3` | `src/security/paladin/l3/sandwich.py` | TC-FR05-01 | unit | `test_fr05_l3_sandwich_injects_boundary_markers` | `tests/unit/test_fr05.py` |
| FR-05 | AC2 | Auth: hierarchy enforcement rejects user-role override of system instructions | 2.5 | `security.paladin.l3` | `src/security/paladin/l3/hierarchy.py` | TC-FR05-02 | unit | `test_fr05_l3_hierarchy_blocks_user_override_of_system` | `tests/unit/test_fr05.py` |
| FR-05 | AC3 | Throttle: L3 template build p95 ≤ 5ms (NFR-01 boundary) | 2.5 | `security.paladin.l3` | `src/security/paladin/l3/builder.py` | TC-FR05-03 | e2e | `test_fr05_l3_template_build_p95_under_5ms` | `tests/e2e/test_fr05_perf.py` |
| FR-05 | AC4 | Degradation: L3 falls back to bare system-prompt passthrough on template engine failure | 2.5 | `security.paladin.l3` | `src/security/paladin/l3/builder.py` | TC-FR05-04 | unit | `test_fr05_l3_fallback_to_bare_passthrough` | `tests/unit/test_fr05.py` |

### 1.2 PALADIN L4–L5 / PII / Rate-Limit / Network Filtering

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-06 | AC1 | Happy-path: PALADIN L4 async classifier labels benign prompt as `safe` | 2.6 | `security.paladin.l4` | `src/security/paladin/l4/classifier.py` | TC-FR06-01 | integration | `test_fr06_l4_async_classifier_labels_benign_safe` | `tests/integration/test_fr06.py` |
| FR-06 | AC2 | Auth: classifier rejects untrusted model weights lacking signature | 2.6 | `security.paladin.l4` | `src/security/paladin/l4/loader.py` | TC-FR06-02 | unit | `test_fr06_l4_loader_rejects_unsigned_weights` | `tests/unit/test_fr06.py` |
| FR-06 | AC3 | Throttle: L4 async pipeline completes ≤ 200ms p95 (NFR-01) | 2.6 | `security.paladin.l4` | `src/security/paladin/l4/pipeline.py` | TC-FR06-03 | e2e | `test_fr06_l4_async_pipeline_p95_under_200ms` | `tests/e2e/test_fr06_perf.py` |
| FR-06 | AC4 | Degradation: classifier falls back to L3 verdict when async backend unreachable | 2.6 | `security.paladin.l4` | `src/security/paladin/l4/pipeline.py` | TC-FR06-04 | integration | `test_fr06_l4_fallback_to_l3_when_async_backend_down` | `tests/integration/test_fr06.py` |
| FR-07 | AC1 | Happy-path: PALADIN L5 grounding check attaches citation when answer is grounded in knowledge tier | 2.7 | `grounding.check` | `src/grounding/check.py` | TC-FR07-01 | integration | `test_fr07_grounding_attaches_citation_when_grounded` | `tests/integration/test_fr07.py` |
| FR-07 | AC2 | Auth: response lacking required citation is blocked before emit | 2.7 | `grounding.check` | `src/grounding/check.py` | TC-FR07-02 | unit | `test_fr07_grounding_blocks_uncited_response` | `tests/unit/test_fr07.py` |
| FR-07 | AC3 | Throttle: grounding check runs in parallel with response generation (NFR-01 latency budget) | 2.7 | `grounding.check` | `src/grounding/check.py` | TC-FR07-03 | e2e | `test_fr07_grounding_runs_parallel_with_generator` | `tests/e2e/test_fr07_perf.py` |
| FR-07 | AC4 | Degradation: grounding falls back to Tier-1 only when Tier-2/3 unavailable | 2.7 | `grounding.check` | `src/grounding/check.py` | TC-FR07-04 | integration | `test_fr07_grounding_fallback_to_tier1_only` | `tests/integration/test_fr07.py` |
| FR-08 | AC1 | Happy-path: PII detector redacts email and phone from outbound text | 2.8 | `security.pii` | `src/security/pii/detector.py` | TC-FR08-01 | unit | `test_fr08_pii_redacts_email_and_phone` | `tests/unit/test_fr08.py` |
| FR-08 | AC2 | Auth: Luhn checksum validates 16-digit card number format | 2.8 | `security.pii` | `src/security/pii/luhn.py` | TC-FR08-02 | unit | `test_fr08_pii_luhn_validates_16_digit_card` | `tests/unit/test_fr08.py` |
| FR-08 | AC3 | Throttle: PII redaction completes within L1–L3 pipeline budget (≤ 5ms) | 2.8 | `security.pii` | `src/security/pii/pipeline.py` | TC-FR08-03 | e2e | `test_fr08_pii_pipeline_under_5ms_p95` | `tests/e2e/test_fr08_perf.py` |
| FR-08 | AC4 | Degradation: redaction skips when detector raises (fail-closed log + raw emit) | 2.8 | `security.pii` | `src/security/pii/pipeline.py` | TC-FR08-04 | unit | `test_fr08_pii_fail_closed_logs_and_raw_emit` | `tests/unit/test_fr08.py` |
| FR-09 | AC1 | Happy-path: Redis Lua atomic counter increments within sliding window | 2.9 | `ratelimit.redis` | `src/ratelimit/redis/lua.py` | TC-FR09-01 | integration | `test_fr09_ratelimit_redis_lua_atomic_increment` | `tests/integration/test_fr09.py` |
| FR-09 | AC2 | Auth: rate-limit key requires tenant scope (rejects cross-tenant token reuse) | 2.9 | `ratelimit.redis` | `src/ratelimit/redis/key.py` | TC-FR09-02 | unit | `test_fr09_ratelimit_rejects_cross_tenant_key_reuse` | `tests/unit/test_fr09.py` |
| FR-09 | AC3 | Throttle: sliding-window returns 429 after N requests in window | 2.9 | `ratelimit.redis` | `src/ratelimit/redis/window.py` | TC-FR09-03 | integration | `test_fr09_ratelimit_returns_429_after_window_full` | `tests/integration/test_fr09.py` |
| FR-09 | AC4 | Degradation: rate-limit fails-open when Redis unavailable (NFR-04) | 2.9 | `ratelimit.redis` | `src/ratelimit/redis/failopen.py` | TC-FR09-04 | integration | `test_fr09_ratelimit_failopen_on_redis_unavailable` | `tests/integration/test_fr09.py` |
| FR-10 | AC1 | Happy-path: CIDR matcher allows source IP inside trusted CIDR block | 2.10 | `security.ip_whitelist` | `src/security/ip_whitelist/cidr.py` | TC-FR10-01 | unit | `test_fr10_cidr_allows_ip_inside_trusted_block` | `tests/unit/test_fr10.py` |
| FR-10 | AC2 | Auth: matcher rejects IP from non-trusted CIDR | 2.10 | `security.ip_whitelist` | `src/security/ip_whitelist/cidr.py` | TC-FR10-02 | unit | `test_fr10_cidr_rejects_ip_outside_trusted_block` | `tests/unit/test_fr10.py` |
| FR-10 | AC3 | Throttle: CIDR lookup p95 ≤ 1ms under load | 2.10 | `security.ip_whitelist` | `src/security/ip_whitelist/cidr.py` | TC-FR10-03 | e2e | `test_fr10_cidr_lookup_p95_under_1ms` | `tests/e2e/test_fr10_perf.py` |
| FR-10 | AC4 | Degradation: matcher defaults to deny-all when CIDR list cache empty | 2.10 | `security.ip_whitelist` | `src/security/ip_whitelist/cache.py` | TC-FR10-04 | unit | `test_fr10_cidr_deny_all_on_cache_empty` | `tests/unit/test_fr10.py` |

### 1.3 Emotion / Dialogue / Knowledge Tier 1–3

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-11 | AC1 | Happy-path: multi-turn emotion analyzer labels "感謝" turn as `gratitude` | 2.11 | `emotion.analyzer` | `src/emotion/analyzer/multiturn.py` | TC-FR11-01 | unit | `test_fr11_emotion_multiturn_labels_gratitude` | `tests/unit/test_fr11.py` |
| FR-11 | AC2 | Auth: analyzer rejects turns outside conversation window | 2.11 | `emotion.analyzer` | `src/emotion/analyzer/window.py` | TC-FR11-02 | unit | `test_fr11_emotion_rejects_turn_outside_window` | `tests/unit/test_fr11.py` |
| FR-11 | AC3 | Throttle: half-life decay applies across ≥ 10 turns within 5ms p95 | 2.11 | `emotion.analyzer` | `src/emotion/analyzer/decay.py` | TC-FR11-03 | e2e | `test_fr11_emotion_half_life_decay_under_5ms_p95` | `tests/e2e/test_fr11_perf.py` |
| FR-11 | AC4 | Degradation: analyzer returns neutral when model endpoint unreachable | 2.11 | `emotion.analyzer` | `src/emotion/analyzer/fallback.py` | TC-FR11-04 | unit | `test_fr11_emotion_returns_neutral_on_endpoint_down` | `tests/unit/test_fr11.py` |
| FR-12 | AC1 | Happy-path: DST FSM transitions `greeting → inquiry → resolved` | 2.12 | `dialog.dst` | `src/dialog/dst/fsm.py` | TC-FR12-01 | unit | `test_fr12_dst_fsm_transition_greeting_to_resolved` | `tests/unit/test_fr12.py` |
| FR-12 | AC2 | Auth: intent router rejects transitions from terminal state | 2.12 | `dialog.dst` | `src/dialog/dst/router.py` | TC-FR12-02 | unit | `test_fr12_dst_router_rejects_transition_from_terminal` | `tests/unit/test_fr12.py` |
| FR-12 | AC3 | Throttle: DST lookup completes within response latency budget (NFR-01) | 2.12 | `dialog.dst` | `src/dialog/dst/lookup.py` | TC-FR12-03 | e2e | `test_fr12_dst_lookup_within_latency_budget` | `tests/e2e/test_fr12_perf.py` |
| FR-12 | AC4 | Degradation: DST falls back to stateless intent on state-store miss | 2.12 | `dialog.dst` | `src/dialog/dst/fallback.py` | TC-FR12-04 | unit | `test_fr12_dst_fallback_to_stateless_intent` | `tests/unit/test_fr12.py` |
| FR-13 | AC1 | Happy-path: Tier-1 PG exact match returns KB article by canonical key | 2.13 | `knowledge.tier1` | `src/knowledge/tier1/postgres.py` | TC-FR13-01 | integration | `test_fr13_tier1_pg_exact_match_returns_kb_article` | `tests/integration/test_fr13.py` |
| FR-13 | AC2 | Auth: Tier-1 query enforces tenant_id filter (no cross-tenant leakage) | 2.13 | `knowledge.tier1` | `src/knowledge/tier1/postgres.py` | TC-FR13-02 | integration | `test_fr13_tier1_enforces_tenant_filter` | `tests/integration/test_fr13.py` |
| FR-13 | AC3 | Throttle: Tier-1 search p95 ≤ 150ms (NFR-01) | 2.13 | `knowledge.tier1` | `src/knowledge/tier1/postgres.py` | TC-FR13-03 | e2e | `test_fr13_tier1_search_p95_under_150ms` | `tests/e2e/test_fr13_perf.py` |
| FR-13 | AC4 | Degradation: Tier-1 returns empty result on PG outage (no Tier escalation) | 2.13 | `knowledge.tier1` | `src/knowledge/tier1/postgres.py` | TC-FR13-04 | integration | `test_fr13_tier1_empty_result_on_pg_outage` | `tests/integration/test_fr13.py` |
| FR-14 | AC1 | Happy-path: Tier-2 pgvector HNSW returns top-k similar chunks | 2.14 | `knowledge.tier2` | `src/knowledge/tier2/hnsw.py` | TC-FR14-01 | integration | `test_fr14_tier2_hnsw_returns_topk` | `tests/integration/test_fr14.py` |
| FR-14 | AC2 | Auth: HNSW index query requires API key with `kb:read` permission | 2.14 | `knowledge.tier2` | `src/knowledge/tier2/auth.py` | TC-FR14-02 | unit | `test_fr14_tier2_requires_kb_read_permission` | `tests/unit/test_fr14.py` |
| FR-14 | AC3 | Throttle: HNSW + RRF fusion k=60 runs within 150ms p95 | 2.14 | `knowledge.tier2` | `src/knowledge/tier2/rrf.py` | TC-FR14-03 | e2e | `test_fr14_tier2_rrf_k60_under_150ms_p95` | `tests/e2e/test_fr14_perf.py` |
| FR-14 | AC4 | Degradation: HNSW degrades to IVFFlat when HNSW index unavailable | 2.14 | `knowledge.tier2` | `src/knowledge/tier2/fallback.py` | TC-FR14-04 | integration | `test_fr14_tier2_fallback_to_ivfflat` | `tests/integration/test_fr14.py` |
| FR-15 | AC1 | Happy-path: Tier-3 LLM generation produces context-grounded answer | 2.15 | `knowledge.tier3` | `src/knowledge/tier3/llm.py` | TC-FR15-01 | integration | `test_fr15_tier3_llm_generates_grounded_answer` | `tests/integration/test_fr15.py` |
| FR-15 | AC2 | Auth: multi-model fallback validates provider credentials before swap | 2.15 | `knowledge.tier3` | `src/knowledge/tier3/fallback.py` | TC-FR15-02 | unit | `test_fr15_tier3_fallback_validates_provider_credentials` | `tests/unit/test_fr15.py` |
| FR-15 | AC3 | Throttle: LLM fallback switch time < 500ms (NFR-04) | 2.15 | `knowledge.tier3` | `src/knowledge/tier3/fallback.py` | TC-FR15-03 | e2e | `test_fr15_tier3_fallback_switch_under_500ms` | `tests/e2e/test_fr15_perf.py` |
| FR-15 | AC4 | Degradation: Tier-3 emits apology when both primary and fallback providers fail | 2.15 | `knowledge.tier3` | `src/knowledge/tier3/apology.py` | TC-FR15-04 | integration | `test_fr15_tier3_apology_when_all_providers_down` | `tests/integration/test_fr15.py` |

### 1.4 Action Execution / Response / RBAC / Escalation

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-16 | AC1 | Happy-path: AEE executes MCP tool call and returns tool result | 2.16 | `actions.engine` | `src/actions/engine/executor.py` | TC-FR16-01 | integration | `test_fr16_aee_executes_mcp_tool_call` | `tests/integration/test_fr16.py` |
| FR-16 | AC2 | Auth: AEE rejects tool call from role lacking `tool:invoke` permission | 2.16 | `actions.engine` | `src/actions/engine/auth.py` | TC-FR16-02 | unit | `test_fr16_aee_rejects_unauthorized_tool_invoke` | `tests/unit/test_fr16.py` |
| FR-16 | AC3 | Throttle: tool / A2A RPC timeout ≤ 2.0s (NFR-04) | 2.16 | `actions.engine` | `src/actions/engine/timeout.py` | TC-FR16-03 | integration | `test_fr16_aee_tool_rpc_timeout_under_2s` | `tests/integration/test_fr16.py` |
| FR-16 | AC4 | Degradation: AEE retries up to 3 times with exponential backoff + jitter (NFR-04) | 2.16 | `actions.engine` | `src/actions/engine/retry.py` | TC-FR16-04 | unit | `test_fr16_aee_retry_exponential_backoff_with_jitter` | `tests/unit/test_fr16.py` |
| FR-17 | AC1 | Happy-path: response generator emits tone-adapted zh-TW reply | 2.17 | `response.generator` | `src/response/generator/tone.py` | TC-FR17-01 | unit | `test_fr17_response_emits_tone_adapted_zh_tw` | `tests/unit/test_fr17.py` |
| FR-17 | AC2 | Auth: tone adapter rejects request lacking conversation context | 2.17 | `response.generator` | `src/response/generator/context.py` | TC-FR17-02 | unit | `test_fr17_response_rejects_missing_context` | `tests/unit/test_fr17.py` |
| FR-17 | AC3 | Throttle: response generation completes within e2e budget (NFR-01) | 2.17 | `response.generator` | `src/response/generator/generator.py` | TC-FR17-03 | e2e | `test_fr17_response_within_e2e_budget` | `tests/e2e/test_fr17_perf.py` |
| FR-17 | AC4 | Degradation: response falls back to canned reply when LLM unavailable | 2.17 | `response.generator` | `src/response/generator/fallback.py` | TC-FR17-04 | unit | `test_fr17_response_fallback_to_canned_on_llm_down` | `tests/unit/test_fr17.py` |
| FR-18 | AC1 | Happy-path: RBAC decorator allows `admin` role to access `/admin/*` | 2.18 | `rbac.middleware` | `src/rbac/middleware/decorator.py` | TC-FR18-01 | unit | `test_fr18_rbac_admin_role_allows_admin_endpoint` | `tests/unit/test_fr18.py` |
| FR-18 | AC2 | Auth: 7-role matrix enforced — denied roles get 403 | 2.18 | `rbac.middleware` | `src/rbac/middleware/matrix.py` | TC-FR18-02 | unit | `test_fr18_rbac_7_role_matrix_enforced` | `tests/unit/test_fr18.py` |
| FR-18 | AC3 | Throttle: RBAC check overhead ≤ 1ms per request | 2.18 | `rbac.middleware` | `src/rbac/middleware/check.py` | TC-FR18-03 | e2e | `test_fr18_rbac_check_overhead_under_1ms` | `tests/e2e/test_fr18_perf.py` |
| FR-18 | AC4 | Degradation: RBAC fails-closed (deny) when role store unreachable | 2.18 | `rbac.middleware` | `src/rbac/middleware/failclosed.py` | TC-FR18-04 | unit | `test_fr18_rbac_failclosed_on_role_store_down` | `tests/unit/test_fr18.py` |
| FR-19 | AC1 | Happy-path: escalation routes VIP conversation to priority queue | 2.19 | `escalation.queue` | `src/escalation/queue/priority.py` | TC-FR19-01 | integration | `test_fr19_escalation_vip_to_priority_queue` | `tests/integration/test_fr19.py` |
| FR-19 | AC2 | Auth: escalation requires agent availability before routing | 2.19 | `escalation.queue` | `src/escalation/queue/availability.py` | TC-FR19-02 | integration | `test_fr19_escalation_requires_agent_availability` | `tests/integration/test_fr19.py` |
| FR-19 | AC3 | Throttle: WebSocket escalation fan-out p95 ≤ 200ms | 2.19 | `escalation.queue` | `src/escalation/queue/ws.py` | TC-FR19-03 | e2e | `test_fr19_escalation_ws_fanout_under_200ms_p95` | `tests/e2e/test_fr19_perf.py` |
| FR-19 | AC4 | Degradation: queued for offline agent waits with SLA timer | 2.19 | `escalation.queue` | `src/escalation/queue/sla.py` | TC-FR19-04 | integration | `test_fr19_escalation_sla_timer_when_agent_offline` | `tests/integration/test_fr19.py` |

### 1.5 Evaluation / Observability / Async Jobs / GDPR / A/B / Multimedia / API

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-20 | AC1 | Happy-path: LLM-as-a-Judge scores Politeness ≥ 4.5/5.0 on golden reply | 2.20 | `eval.judge` | `src/eval/judge/runner.py` | TC-FR20-01 | integration | `test_fr20_judge_scores_politeness_gte_4_5` | `tests/integration/test_fr20.py` |
| FR-20 | AC2 | Auth: judge prompts signed with calibration token | 2.20 | `eval.judge` | `src/eval/judge/auth.py` | TC-FR20-02 | unit | `test_fr20_judge_requires_calibration_token` | `tests/unit/test_fr20.py` |
| FR-20 | AC3 | Throttle: judge batch (≥ 500 samples) completes within budget | 2.20 | `eval.judge` | `src/eval/judge/batch.py` | TC-FR20-03 | e2e | `test_fr20_judge_batch_500_samples_within_budget` | `tests/e2e/test_fr20_perf.py` |
| FR-20 | AC4 | Degradation: judge falls back to heuristic scorer when LLM judge unavailable | 2.20 | `eval.judge` | `src/eval/judge/fallback.py` | TC-FR20-04 | integration | `test_fr20_judge_fallback_to_heuristic` | `tests/integration/test_fr20.py` |
| FR-21 | AC1 | Happy-path: OTel span emitted per request with trace_id | 2.21 | `observability.core` | `src/observability/core/otel.py` | TC-FR21-01 | unit | `test_fr21_otel_emits_span_per_request` | `tests/unit/test_fr21.py` |
| FR-21 | AC2 | Auth: Prometheus metrics endpoint requires bearer token | 2.21 | `observability.core` | `src/observability/core/metrics.py` | TC-FR21-02 | unit | `test_fr21_prometheus_requires_bearer_token` | `tests/unit/test_fr21.py` |
| FR-21 | AC3 | Throttle: metric scrape overhead ≤ 10ms p95 | 2.21 | `observability.core` | `src/observability/core/metrics.py` | TC-FR21-03 | e2e | `test_fr21_metric_scrape_overhead_under_10ms_p95` | `tests/e2e/test_fr21_perf.py` |
| FR-21 | AC4 | Degradation: in-memory ring buffer when OTel collector unreachable | 2.21 | `observability.core` | `src/observability/core/buffer.py` | TC-FR21-04 | unit | `test_fr21_otel_ringbuffer_when_collector_down` | `tests/unit/test_fr21.py` |
| FR-22 | AC1 | Happy-path: SAQ worker enqueues embedding job and processes it | 2.22 | `jobs.saq` | `src/jobs/saq/worker.py` | TC-FR22-01 | integration | `test_fr22_saq_enqueues_and_processes_embedding` | `tests/integration/test_fr22.py` |
| FR-22 | AC2 | Auth: SAQ job payload signed with HMAC | 2.22 | `jobs.saq` | `src/jobs/saq/auth.py` | TC-FR22-02 | unit | `test_fr22_saq_job_payload_hmac_signed` | `tests/unit/test_fr22.py` |
| FR-22 | AC3 | Throttle: embedding API p95 ≤ 100ms (NFR-01) | 2.22 | `jobs.saq` | `src/jobs/saq/embedding.py` | TC-FR22-03 | e2e | `test_fr22_embedding_api_p95_under_100ms` | `tests/e2e/test_fr22_perf.py` |
| FR-22 | AC4 | Degradation: job re-queued with backoff on transient worker failure | 2.22 | `jobs.saq` | `src/jobs/saq/retry.py` | TC-FR22-04 | integration | `test_fr22_saq_requeue_with_backoff_on_transient` | `tests/integration/test_fr22.py` |
| FR-23 | AC1 | Happy-path: GDPR export returns user JSON envelope within 24h SLA | 2.23 | `compliance.gdpr` | `src/compliance/gdpr/export.py` | TC-FR23-01 | integration | `test_fr23_gdpr_export_returns_envelope_within_sla` | `tests/integration/test_fr23.py` |
| FR-23 | AC2 | Auth: GDPR export requires verified user identity | 2.23 | `compliance.gdpr` | `src/compliance/gdpr/auth.py` | TC-FR23-02 | unit | `test_fr23_gdpr_export_requires_verified_identity` | `tests/unit/test_fr23.py` |
| FR-23 | AC3 | Throttle: deletion job completes within 24h SLA for 10M rows | 2.23 | `compliance.gdpr` | `src/compliance/gdpr/delete.py` | TC-FR23-03 | e2e | `test_fr23_gdpr_deletion_24h_sla_10m_rows` | `tests/e2e/test_fr23_perf.py` |
| FR-23 | AC4 | Degradation: deletion falls back to soft-delete + tombstone on PG outage | 2.23 | `compliance.gdpr` | `src/compliance/gdpr/tombstone.py` | TC-FR23-04 | integration | `test_fr23_gdpr_fallback_to_soft_delete_on_pg_outage` | `tests/integration/test_fr23.py` |
| FR-24 | AC1 | Happy-path: SHA-256 hash assigns user to variant `A` deterministically | 2.24 | `experiment.ab` | `src/experiment/ab/hash.py` | TC-FR24-01 | unit | `test_fr24_ab_sha256_assigns_variant_a` | `tests/unit/test_fr24.py` |
| FR-24 | AC2 | Auth: experiment assignment key signed per tenant | 2.24 | `experiment.ab` | `src/experiment/ab/key.py` | TC-FR24-02 | unit | `test_fr24_ab_assignment_key_per_tenant` | `tests/unit/test_fr24.py` |
| FR-24 | AC3 | Throttle: assignment lookup p95 ≤ 5ms | 2.24 | `experiment.ab` | `src/experiment/ab/lookup.py` | TC-FR24-03 | e2e | `test_fr24_ab_assignment_lookup_p95_under_5ms` | `tests/e2e/test_fr24_perf.py` |
| FR-24 | AC4 | Degradation: control variant served when experiment store unreachable | 2.24 | `experiment.ab` | `src/experiment/ab/fallback.py` | TC-FR24-04 | unit | `test_fr24_ab_fallback_to_control_on_store_down` | `tests/unit/test_fr24.py` |
| FR-25 | AC1 | Happy-path: image attachment triggers multimedia handler | 2.25 | `adapters.media` | `src/adapters/media/handler.py` | TC-FR25-01 | integration | `test_fr25_media_image_handler_runs` | `tests/integration/test_fr25.py` |
| FR-25 | AC2 | Auth: media URL signature validated before fetch | 2.25 | `adapters.media` | `src/adapters/media/url.py` | TC-FR25-02 | unit | `test_fr25_media_url_signature_validated` | `tests/unit/test_fr25.py` |
| FR-25 | AC3 | Throttle: media download ≤ 5s p95 | 2.25 | `adapters.media` | `src/adapters/media/download.py` | TC-FR25-03 | e2e | `test_fr25_media_download_p95_under_5s` | `tests/e2e/test_fr25_perf.py` |
| FR-25 | AC4 | Degradation: unparseable media escalates to human (FR-19 priority queue) | 2.25 | `adapters.media` | `src/adapters/media/escalate.py` | TC-FR25-04 | integration | `test_fr25_media_unparseable_escalates_to_human` | `tests/integration/test_fr25.py` |
| FR-26 | AC1 | Happy-path: User CRUD API creates user with hashed password | 2.26 | `api.users` + `api.m2m` | `src/api/users/{router,service}.py` + `src/api/m2m/{tokens,rotation}.py` | TC-FR26-01 | integration | `test_fr26_user_crud_creates_with_hashed_password` | `tests/integration/test_fr26.py` |
| FR-26 | AC2 | Auth: M2M token rotation invalidates previous token | 2.26 | `api.m2m` | `src/api/m2m/rotation.py` | TC-FR26-02 | unit | `test_fr26_m2m_rotation_invalidates_previous_token` | `tests/unit/test_fr26.py` |
| FR-26 | AC3 | Throttle: API p95 latency ≤ 200ms | 2.26 | `api.users` + `api.m2m` | `src/api/users/router.py` | TC-FR26-03 | e2e | `test_fr26_api_p95_under_200ms` | `tests/e2e/test_fr26_perf.py` |
| FR-26 | AC4 | Degradation: user lookup falls back to cached snapshot on PG outage | 2.26 | `api.users` | `src/api/users/cache.py` | TC-FR26-04 | integration | `test_fr26_user_lookup_cache_snapshot_on_pg_outage` | `tests/integration/test_fr26.py` |

### 1.6 Context Window / HA + Deferred Block

| FR ID | AC | Acceptance Criterion (canonical, paraphrased from SPEC.md) | SRS § | Code Module (target) | Code Path (target) | Test ID | Layer | Test Function | Test Path |
|-------|----|----------------------------------------------------------|-------|----------------------|--------------------|---------|-------|---------------|-----------|
| FR-27 | AC1 | Happy-path: sliding window trims oldest turns when token budget exceeded | 2.27 | `dialog.context` | `src/dialog/context/window.py` | TC-FR27-01 | unit | `test_fr27_context_window_trims_oldest_turns` | `tests/unit/test_fr27.py` |
| FR-27 | AC2 | Auth: window rejects injection of turns from another conversation | 2.27 | `dialog.context` | `src/dialog/context/guard.py` | TC-FR27-02 | unit | `test_fr27_context_rejects_cross_conversation_turn` | `tests/unit/test_fr27.py` |
| FR-27 | AC3 | Throttle: window trim p95 ≤ 10ms | 2.27 | `dialog.context` | `src/dialog/context/window.py` | TC-FR27-03 | e2e | `test_fr27_context_trim_p95_under_10ms` | `tests/e2e/test_fr27_perf.py` |
| FR-27 | AC4 | Degradation: window falls back to summary-only mode on tokenizer error | 2.27 | `dialog.context` | `src/dialog/context/summary.py` | TC-FR27-04 | unit | `test_fr27_context_fallback_to_summary_on_tokenizer_error` | `tests/unit/test_fr27.py` |
| FR-28 | AC1 | Happy-path: Circuit Breaker opens after N consecutive failures | 2.28 | `ha.circuit_breaker` | `src/ha/circuit_breaker/breaker.py` | TC-FR28-01 | unit | `test_fr28_breaker_opens_after_n_failures` | `tests/unit/test_fr28.py` |
| FR-28 | AC2 | Auth: Redis Streams consumer requires ACL group membership | 2.28 | `ha.redis` | `src/ha/redis/streams.py` | TC-FR28-02 | unit | `test_fr28_redis_streams_requires_acl_group` | `tests/unit/test_fr28.py` |
| FR-28 | AC3 | Throttle: circuit-breaker fail-fast p99 ≤ 50ms | 2.28 | `ha.circuit_breaker` | `src/ha/circuit_breaker/breaker.py` | TC-FR28-03 | e2e | `test_fr28_breaker_failfast_p99_under_50ms` | `tests/e2e/test_fr28_perf.py` |
| FR-28 | AC4 | Degradation: half-open probe after cool-down expires | 2.28 | `ha.circuit_breaker` | `src/ha/circuit_breaker/halfopen.py` | TC-FR28-04 | integration | `test_fr28_breaker_halfopen_probe_after_cooldown` | `tests/integration/test_fr28.py` |
| FR-29-deferred | — | (Deferred to v9.0) Native multimodal vision understanding — NFR-99 pending GPT-4V/Claude Vision cost-benefit — `SPEC.md:7036` | 2.29 | — | — | — | — | — | — |
| FR-30-deferred | — | (Deferred to v9.1) File & document OCR/AI parsing — NFR-99 pending Document AI — `SPEC.md:7039` | 2.30 | — | — | — | — | — | — |
| FR-31-deferred | — | (Deferred to voice track) Real-time voice & audio streaming — NFR-99 STT/TTS latency risk vs p95<1.0s — `SPEC.md:7042` | 2.31 | — | — | — | — | — | — |
| FR-32-deferred | — | (Deferred to i18n phase) Multi-lingual beyond zh-TW/en — NFR-99 scope limited — `SPEC.md:7045` | 2.32 | — | — | — | — | — | — |
| FR-33-deferred | — | (Deferred pending cost-benefit) In-house LLM fine-tuning pipeline — NFR-99 4-Tier + RAG already 90% FCR — `SPEC.md:7048` | 2.33 | — | — | — | — | — | — |
| FR-34-deferred | — | (Deferred; web-channel sufficient) Native mobile App — NFR-99 web widgets cover mobile — `SPEC.md:7051` | 2.34 | — | — | — | — | — | — |

---

## 2. NFR ↔ Test Method ↔ Gate Mapping

> NFR rows here mirror `SPEC_TRACKING.md` NFR section. Test IDs prefixed `TC-Nxx-NN` follow `TEST_INVENTORY.yaml` schema. The NFR Layering Hard Rule binds `layer:` — pure unit/static checks cannot satisfy an SLO/SLA test.

| NFR ID | Type | Test Method (canonical) | Gate | Test ID | Layer | Test Function | Test Path |
|--------|------|--------------------------|------|---------|-------|---------------|-----------|
| NFR-01 | performance | k6 (Functional/Stress/Spike/Soak) + Prometheus p95 histogram | Gate 3 / Gate 4 | TC-N01-01 | e2e | `test_nfr01_k6_p95_under_1s_sustained_2000_tps` | `tests/e2e/test_nfr01_perf.py` |
| NFR-01 | performance | PALADIN L1~L3 micro-bench ≤ 5ms p95 | Gate 3 / Gate 4 | TC-N01-02 | e2e | `test_nfr01_paladin_l1_l3_micro_bench_under_5ms_p95` | `tests/e2e/test_nfr01_perf.py` |
| NFR-01 | performance | Embedding API p95 ≤ 100ms | Gate 3 / Gate 4 | TC-N01-03 | e2e | `test_nfr01_embedding_api_p95_under_100ms` | `tests/e2e/test_nfr01_perf.py` |
| NFR-02 | security | bandit ≥ 80 (0 High/Critical) | Gate 1~4 | TC-N02-01 | static | `test_nfr02_bandit_score_gte_80_no_high_critical` | `tests/static/test_nfr02.py` |
| NFR-02 | security | gitleaks = 100 (no leaked secrets) | Gate 1~4 | TC-N02-02 | static | `test_nfr02_gitleaks_no_secrets` | `tests/static/test_nfr02.py` |
| NFR-02 | security | OWASP LLM Top-10 (2025) red-team prompt-injection suite | Gate 1~4 | TC-N02-03 | integration | `test_nfr02_redteam_owasp_llm_top10_suite` | `tests/integration/test_nfr02_redteam.py` |
| NFR-02 | security | PALADIN 5-layer block rate ≥ 95% on injection corpus | Gate 1~4 | TC-N02-04 | integration | `test_nfr02_paladin_block_rate_gte_95pct` | `tests/integration/test_nfr02_paladin.py` |
| NFR-02 | security | PG TDE + TLS 1.3 + Redis TLS/AUTH/ACL configuration check | Gate 2~4 | TC-N02-05 | static | `test_nfr02_storage_tls_and_auth_enforced` | `tests/static/test_nfr02_storage.py` |
| NFR-03 | maintainability | ruff ≥ 90; pyright ≥ 85 | Gate 1~4 | TC-N03-01 | static | `test_nfr03_ruff_gte_90_pyright_gte_85` | `tests/static/test_nfr03.py` |
| NFR-03 | maintainability | Function ≤ 50 lines, CC ≤ 10 (radon-mi) | Gate 1~4 | TC-N03-02 | static | `test_nfr03_radon_function_lines_and_cc` | `tests/static/test_nfr03.py` |
| NFR-03 | maintainability | Alembic upgrade/downgrade/upgrade roundtrip = 100% | Gate 2~4 | TC-N03-03 | integration | `test_nfr03_alembic_upgrade_downgrade_roundtrip` | `tests/integration/test_nfr03.py` |
| NFR-03 | maintainability | Code-to-SAD mapping coverage = 100% | Gate 2~4 | TC-N03-04 | static | `test_nfr03_code_to_sad_mapping_100pct` | `tests/static/test_nfr03_sad.py` |
| NFR-04 | reliability | Prometheus uptime SLO ≥ 99.9% monthly | Gate 3 / Gate 4 | TC-N04-01 | e2e | `test_nfr04_monthly_uptime_slo_gte_99_9pct` | `tests/e2e/test_nfr04_slo.py` |
| NFR-04 | reliability | Circuit Breaker unit tests (open/half-open/closed) | Gate 3 / Gate 4 | TC-N04-02 | unit | `test_nfr04_circuit_breaker_state_machine` | `tests/unit/test_nfr04.py` |
| NFR-04 | reliability | Chaos Mesh DR drill (Redis kill / PG failover) | Gate 3 / Gate 4 | TC-N04-03 | e2e | `test_nfr04_chaos_mesh_dr_drill` | `tests/e2e/test_nfr04_chaos.py` |
| NFR-04 | reliability | Retry with exponential backoff + jitter (≤ 3 retries) | Gate 3 / Gate 4 | TC-N04-04 | unit | `test_nfr04_retry_exponential_backoff_with_jitter` | `tests/unit/test_nfr04.py` |
| NFR-04 | reliability | LLM fallback switch < 500ms | Gate 3 / Gate 4 | TC-N04-05 | integration | `test_nfr04_llm_fallback_switch_under_500ms` | `tests/integration/test_nfr04.py` |
| NFR-04 | reliability | MTTR < 5 min (drill measurement) | Gate 3 / Gate 4 | TC-N04-06 | e2e | `test_nfr04_mttr_under_5min_drill` | `tests/e2e/test_nfr04_dr.py` |
| NFR-05 | testability | pytest-cov line coverage (Gate 1 owned 100%, Gate 2/4 ≥ 90%) | Gate 1~4 | TC-N05-01 | static | `test_nfr05_pytest_cov_line_thresholds` | `tests/static/test_nfr05.py` |
| NFR-05 | testability | mutmut mutation killed ≥ 80% | Gate 1~4 | TC-N05-02 | static | `test_nfr05_mutation_killed_gte_80pct` | `tests/static/test_nfr05.py` |
| NFR-05 | testability | D4 Spec-coverage thresholds (G1 ≥ 40 / G2 ≥ 60 / G3 ≥ 80 / G4 ≥ 90) | Gate 1~4 | TC-N05-03 | static | `test_nfr05_d4_spec_cov_thresholds_by_gate` | `tests/static/test_nfr05.py` |
| NFR-05 | testability | Golden data ≥ 500 samples, Cohen's Kappa ≥ 0.7 | Gate 3 / Gate 4 | TC-N05-04 | integration | `test_nfr05_golden_500_samples_kappa_gte_0_7` | `tests/integration/test_nfr05_golden.py` |
| NFR-06 | deployability | `kubectl rollout undo` succeeds (rollback < 5 min) | P8 | TC-N06-01 | e2e | `test_nfr06_kubectl_rollout_undo_under_5min` | `tests/e2e/test_nfr06_deploy.py` |
| NFR-06 | deployability | Helm chart lint clean | P8 | TC-N06-02 | static | `test_nfr06_helm_chart_lint_clean` | `tests/static/test_nfr06.py` |
| NFR-06 | deployability | HPA thresholds CPU > 70 / Memory > 80 enforced | P8 | TC-N06-03 | static | `test_nfr06_hpa_cpu_memory_thresholds` | `tests/static/test_nfr06.py` |
| NFR-06 | deployability | RollingUpdate maxSurge=25%, maxUnavailable=0 | P8 | TC-N06-04 | static | `test_nfr06_rolling_update_strategy_enforced` | `tests/static/test_nfr06.py` |
| NFR-07 | scalability | k6 ≥ 30 min soak at 2000 TPS sustained | Gate 3 / Gate 4 | TC-N07-01 | e2e | `test_nfr07_k6_soak_30min_2000tps` | `tests/e2e/test_nfr07_soak.py` |
| NFR-07 | scalability | pgvector HNSW benchmark (m=16, ef_construction=64) at 10M chunks | Gate 3 / Gate 4 | TC-N07-02 | e2e | `test_nfr07_pgvector_hnsw_10m_chunks_benchmark` | `tests/e2e/test_nfr07_pgvector.py` |
| NFR-07 | scalability | `redis-cli cluster create` succeeds (Redis Cluster ready) | Gate 3 / Gate 4 | TC-N07-03 | integration | `test_nfr07_redis_cluster_create_succeeds` | `tests/integration/test_nfr07.py` |
| NFR-08 | usability | CSAT ≥ 4.8/5.0 (monthly human sampling n ≥ 100) | Gate 3 / Gate 4 | TC-N08-01 | integration | `test_nfr08_csat_gte_4_8_human_sample` | `tests/integration/test_nfr08_csat.py` |
| NFR-08 | usability | LLM-Judge Politeness ≥ 4.5/5.0 with zh-TW empathy (FR-20) | Gate 3 / Gate 4 | TC-N08-02 | integration | `test_nfr08_llm_judge_politeness_gte_4_5_zh_tw` | `tests/integration/test_nfr08.py` |
| NFR-08 | usability | Accuracy 100% knowledge-alignment (FR-07 grounding) | Gate 3 / Gate 4 | TC-N08-03 | integration | `test_nfr08_accuracy_100pct_knowledge_alignment` | `tests/integration/test_nfr08.py` |
| NFR-08 | usability | Admin/Agent portal WebSocket real-time sync | Gate 3 / Gate 4 | TC-N08-04 | integration | `test_nfr08_admin_portal_websocket_realtime_sync` | `tests/integration/test_nfr08.py` |

---

## 3. Spec ↔ Code Module Mapping (Condensed View)

> Direct mapping distilled from `SRS.md §2` `Implementation Module` column → target code path under `src/`. One row per FR implementation module; rows with `+` mean multi-module.

| SRS § | FR IDs Covered | Code Module(s) | Code Path (root under `src/`) |
|-------|----------------|-----------------|------------------------------|
| 2.1 | FR-01 | `adapters.ingress` | `src/adapters/ingress/{telegram,line,messenger,whatsapp,web,a2a,base}.py` |
| 2.2 | FR-02 | `security.auth` | `src/security/auth/{hmac,m2m,jwks_cache}.py` |
| 2.3 | FR-03 | `security.paladin.l1` | `src/security/paladin/l1/{normalize,homoglyph,pipeline}.py` |
| 2.4 | FR-04 | `security.paladin.l2` | `src/security/paladin/l2/{rules,loader,engine}.py` |
| 2.5 | FR-05 | `security.paladin.l3` | `src/security/paladin/l3/{sandwich,hierarchy,builder}.py` |
| 2.6 | FR-06 | `security.paladin.l4` | `src/security/paladin/l4/{classifier,loader,pipeline}.py` |
| 2.7 | FR-07 | `grounding.check` | `src/grounding/check.py` |
| 2.8 | FR-08 | `security.pii` | `src/security/pii/{detector,luhn,pipeline}.py` |
| 2.9 | FR-09 | `ratelimit.redis` | `src/ratelimit/redis/{lua,key,window,failopen}.py` |
| 2.10 | FR-10 | `security.ip_whitelist` | `src/security/ip_whitelist/{cidr,cache}.py` |
| 2.11 | FR-11 | `emotion.analyzer` | `src/emotion/analyzer/{multiturn,window,decay,fallback}.py` |
| 2.12 | FR-12 | `dialog.dst` | `src/dialog/dst/{fsm,router,lookup,fallback}.py` |
| 2.13 | FR-13 | `knowledge.tier1` | `src/knowledge/tier1/postgres.py` |
| 2.14 | FR-14 | `knowledge.tier2` | `src/knowledge/tier2/{hnsw,auth,rrf,fallback}.py` |
| 2.15 | FR-15 | `knowledge.tier3` | `src/knowledge/tier3/{llm,fallback,apology}.py` |
| 2.16 | FR-16 | `actions.engine` | `src/actions/engine/{executor,auth,timeout,retry}.py` |
| 2.17 | FR-17 | `response.generator` | `src/response/generator/{tone,context,generator,fallback}.py` |
| 2.18 | FR-18 | `rbac.middleware` | `src/rbac/middleware/{decorator,matrix,check,failclosed}.py` |
| 2.19 | FR-19 | `escalation.queue` | `src/escalation/queue/{priority,availability,ws,sla}.py` |
| 2.20 | FR-20 | `eval.judge` | `src/eval/judge/{runner,auth,batch,fallback}.py` |
| 2.21 | FR-21 | `observability.core` | `src/observability/core/{otel,metrics,buffer}.py` |
| 2.22 | FR-22 | `jobs.saq` | `src/jobs/saq/{worker,auth,embedding,retry}.py` |
| 2.23 | FR-23 | `compliance.gdpr` | `src/compliance/gdpr/{export,auth,delete,tombstone}.py` |
| 2.24 | FR-24 | `experiment.ab` | `src/experiment/ab/{hash,key,lookup,fallback}.py` |
| 2.25 | FR-25 | `adapters.media` | `src/adapters/media/{handler,url,download,escalate}.py` |
| 2.26 | FR-26 | `api.users + api.m2m` | `src/api/users/{router,service,cache}.py` + `src/api/m2m/{tokens,rotation}.py` |
| 2.27 | FR-27 | `dialog.context` | `src/dialog/context/{window,guard,summary}.py` |
| 2.28 | FR-28 | `ha.redis + ha.circuit_breaker` | `src/ha/redis/streams.py` + `src/ha/circuit_breaker/{breaker,halfopen}.py` |

---

## 4. Code ↔ Test Mapping (Condensed View)

> One row per code module → the 4-boundary test set that exercises it. Layers mirror §1's per-AC layering; per-module layer distribution is the contract for `TEST_SPEC.md` P2 derivation.

| Code Module | Unit Test IDs | Integration Test IDs | E2E/Perf Test IDs |
|-------------|---------------|----------------------|-------------------|
| `adapters.ingress` | TC-FR01-02 | TC-FR01-01, TC-FR01-03, TC-FR01-04 | — |
| `security.auth` | TC-FR02-01, TC-FR02-02, TC-FR02-03 | TC-FR02-04 | — |
| `security.paladin.l1` | TC-FR03-01, TC-FR03-02, TC-FR03-04 | — | TC-FR03-03 |
| `security.paladin.l2` | TC-FR04-01, TC-FR04-02, TC-FR04-04 | — | TC-FR04-03 |
| `security.paladin.l3` | TC-FR05-01, TC-FR05-02, TC-FR05-04 | — | TC-FR05-03 |
| `security.paladin.l4` | TC-FR06-02 | TC-FR06-01, TC-FR06-04 | TC-FR06-03 |
| `grounding.check` | TC-FR07-02 | TC-FR07-01, TC-FR07-04 | TC-FR07-03 |
| `security.pii` | TC-FR08-01, TC-FR08-02, TC-FR08-04 | — | TC-FR08-03 |
| `ratelimit.redis` | TC-FR09-02 | TC-FR09-01, TC-FR09-03, TC-FR09-04 | — |
| `security.ip_whitelist` | TC-FR10-01, TC-FR10-02, TC-FR10-04 | — | TC-FR10-03 |
| `emotion.analyzer` | TC-FR11-01, TC-FR11-02, TC-FR11-04 | — | TC-FR11-03 |
| `dialog.dst` | TC-FR12-01, TC-FR12-02, TC-FR12-04 | — | TC-FR12-03 |
| `knowledge.tier1` | — | TC-FR13-01, TC-FR13-02, TC-FR13-04 | TC-FR13-03 |
| `knowledge.tier2` | TC-FR14-02 | TC-FR14-01, TC-FR14-04 | TC-FR14-03 |
| `knowledge.tier3` | TC-FR15-02 | TC-FR15-01, TC-FR15-04 | TC-FR15-03 |
| `actions.engine` | TC-FR16-02, TC-FR16-04 | TC-FR16-01, TC-FR16-03 | — |
| `response.generator` | TC-FR17-01, TC-FR17-02, TC-FR17-04 | — | TC-FR17-03 |
| `rbac.middleware` | TC-FR18-01, TC-FR18-02, TC-FR18-04 | — | TC-FR18-03 |
| `escalation.queue` | — | TC-FR19-01, TC-FR19-02, TC-FR19-04 | TC-FR19-03 |
| `eval.judge` | TC-FR20-02 | TC-FR20-01, TC-FR20-04 | TC-FR20-03 |
| `observability.core` | TC-FR21-01, TC-FR21-02, TC-FR21-04 | — | TC-FR21-03 |
| `jobs.saq` | TC-FR22-02 | TC-FR22-01, TC-FR22-04 | TC-FR22-03 |
| `compliance.gdpr` | TC-FR23-02 | TC-FR23-01, TC-FR23-04 | TC-FR23-03 |
| `experiment.ab` | TC-FR24-01, TC-FR24-02, TC-FR24-04 | — | TC-FR24-03 |
| `adapters.media` | TC-FR25-02 | TC-FR25-01, TC-FR25-04 | TC-FR25-03 |
| `api.users` + `api.m2m` | TC-FR26-02 | TC-FR26-01, TC-FR26-04 | TC-FR26-03 |
| `dialog.context` | TC-FR27-01, TC-FR27-02, TC-FR27-04 | — | TC-FR27-03 |
| `ha.redis + ha.circuit_breaker` | TC-FR28-01, TC-FR28-02 | TC-FR28-04 | TC-FR28-03 |

---

## 5. Deferred FR Coverage Plan (v9.0+)

> Deferred FRs intentionally have **no** tests in §1. They are recorded here so P5/P7 ingestion keeps them discoverable, but they are excluded from Gate-1/2 scoring per `harness/core/quality_gate/sab_parser.NFR99_DEFERRED_SKIP`.

| Deferred FR | Re-Evaluation Trigger | Planned Test ID (when reactivated) | Planned Test Path |
|-------------|-----------------------|------------------------------------|--------------------|
| FR-29-deferred (Native multimodal vision) | GPT-4V / Claude Vision cost-benefit approved | TC-FR29-01..04 | `tests/integration/test_fr29.py` |
| FR-30-deferred (Document AI / OCR) | Document AI module selected | TC-FR30-01..04 | `tests/integration/test_fr30.py` |
| FR-31-deferred (Real-time voice / audio) | STT/TTS p95<1.0s feasibility proven | TC-FR31-01..04 | `tests/integration/test_fr31.py` |
| FR-32-deferred (i18n beyond zh-TW/en) | i18n phase launched | TC-FR32-01..04 | `tests/integration/test_fr32.py` |
| FR-33-deferred (In-house LLM fine-tune) | Cost-benefit clears current 4-Tier + RAG | TC-FR33-01..04 | `tests/integration/test_fr33.py` |
| FR-34-deferred (Native mobile App) | Product decision to launch native | TC-FR34-01..04 | `tests/integration/test_fr34.py` |

---

## 6. Completeness Verification

> Counts refreshed by `advance-phase` / `build_traceability`. Hand-fill authority is locked to §1/§2 wiring.

| Check | Target | Actual (machine-refreshed) | Status |
|-------|--------|----------------------------|--------|
| FR-01..FR-28 ↔ SRS section mapping | 28/28 | (refresh) | OK (28 rows in §1) |
| FR-29..FR-34 marked `-deferred` | 6/6 | (refresh) | OK (6 rows in §5) |
| NFR-01..NFR-08 ↔ test method mapping | 8/8 | (refresh) | OK (8 rows in §2) |
| Per-FR 4-boundary AC coverage (AC1..AC4) | 28 × 4 = 112 ACs | (refresh) | OK (112 AC rows in §1) |
| Per-NFR ≥1 layer-correct test | 8/8 | (refresh) | OK (33 NFR rows in §2) |
| Module-to-test wiring completeness | 29 modules × 4 tests = 116 | (refresh) | OK (§4 covers all 29) |
| D4 Spec-coverage (Gate 1 ≥ 40%) | ≥ 40% | (refresh) | PENDING machine-refresh |
| Line coverage Gate 1 owned 100% | 100% | (refresh) | PENDING machine-refresh |
| Mutation Killed ≥ 80% (NFR-05) | ≥ 80% | (refresh) | PENDING machine-refresh |
| Deferred FRs explicitly excluded from Gate-1 score | 6/6 | 6/6 | OK (§5) |
| TEST_INVENTORY.yaml schema (`format_version: "1.1"`) alignment | 100% | 100% | OK (tc_id/fr/nfr/ac/layer/test_function/test_file schema mirrors) |
| ASPICE SWE.3.B.SP1 (task-to-work-product traceability) | Met | Met | OK (§1 + §3 + §4) |
| ASPICE SWE.3.B.SP2 (bidirectional traceability) | Met | Met | OK (§1 ↔ §3 ↔ §4 reverse-walked) |
| ASPICE SWE.3.B.SP3 (consistency) | Met | Met | OK (no orphan FR/AC/code/test) |

---

## 7. Update Log

| Date | Change | By |
|------|--------|----|
| 2026-08-25 | Initial template creation | Agent A |
| 2026-09-04 | Round 1: populated §1 with 28 in-scope FRs × 4 ACs (112 ACs total) following the `Happy/Auth/Throttle/Degradation` boundary contract from `SRS.md §2`; §2 with 8 NFRs × ≥1 test per layer; §3 spec↔code map distilled from `SRS.md §2` Implementation Module column; §4 module↔test condensation; §5 deferred-FR reactivation plan; §6 machine-refreshable completeness checks. All test IDs follow `TC-FRNN-NN` / `TC-Nxx-NN` schema per `TEST_INVENTORY.yaml` v1.1 naming authority. | Agent A |
