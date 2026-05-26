# BASELINE.md - omnibot-new

> On-demand Lazy Load template.

## 1. Baseline Overview
- Author: Johnny
- Reviewer: harness (automated)
- session_id: P5-entry-20260526
- Date: 2026-05-26

## 2. Functional Baseline (maps to SRS FR, 100% complete)

| FR ID | Feature Description | Baseline Status | Notes |
|-------|--------------------|-----------------| ------|
| FR-01 | PostgreSQL schema — 8 tables + 11 indexes, Phase 2/3 columns | PASS | Gate1 score=100.0 |
| FR-02 | Telegram webhook handler — UnifiedMessage parsing | PASS | Gate1 score=100.0 |
| FR-03 | LINE webhook handler — UnifiedMessage parsing | PASS | Gate1 score=100.0 |
| FR-04 | Telegram HMAC-SHA256 signature verification | PASS | Gate1 score=100.0 |
| FR-05 | LINE HMAC-SHA256 signature verification | PASS | Gate1 score=100.0 |
| FR-06 | UnifiedMessage dataclass + Platform/MessageType enums | PASS | Gate1 score=100.0 |
| FR-07 | ApiResponse[T] + PaginatedResponse[T] dataclasses | PASS | Gate1 score=100.0 |
| FR-08 | Input sanitizer — NFKC normalization, fullwidth→ASCII | PASS | Gate1 score=100.0 |
| FR-09 | PII masker — Taiwan phone/email/address masking | PASS | Gate1 score=100.0 |
| FR-10 | Token-bucket rate limiter — per-platform per-user | PASS | Gate1 score=100.0 |
| FR-11 | Knowledge base query — ILIKE + keyword array match | PASS | Gate1 score=100.0 |
| FR-12 | Basic escalation — no_rule_match → escalation_queue | PASS | Gate1 score=100.0 |
| FR-13 | Structured JSON logger — single-line JSON per log entry | PASS | Gate1 score=100.0 |
| FR-14 | Health check endpoint — /api/v1/health | PASS | Gate1 score=100.0 |
| FR-15 | Docker Compose — omnibot-api + postgres + redis | PASS | Gate1 score=100.0 |
| FR-16 | ODD SQL scripts — FCR/latency/knowledge_hits | PASS | Gate1 score=100.0 |
| FR-17 | Standardized error codes + ApiResponse error format | PASS | Gate1 score=100.0 |
| FR-18 | Code conventions — ruff zero violations, CC ≤ 10 | PASS | Gate1 score=100.0 |
| FR-19 | AI pipeline — 11-stage orchestration | PASS | Gate1 score=99.08 |
| FR-20 | UnifiedResponse dataclass + KnowledgeSource enum | PASS | Gate1 score=100.0 |
| FR-21 | Config loader — env vars + config.yaml validation | PASS | Gate1 score=100.0 |
| FR-22 | IP whitelist middleware — blocks before HMAC | PASS | Gate1 score=99.21 |

> **ASPICE Traceability**: This document references `TEST_PLAN.md` (04-testing/TEST_PLAN.md) for test case specifications and `TEST_RESULTS.md` (04-testing/TEST_RESULTS.md) for test execution records, establishing full forward traceability from requirements to test artifacts per ASPICE PA-2.

## 3. Quality Baseline

| Metric | Threshold | Actual | Status |
|--------|-----------|--------|--------|
| Constitution (P5+) | >= 80% | See note 1 | REVIEW |
| Coverage | >= 80% | 100% | PASS |
| Logic Correctness | >= 90 | 99.6 (avg) | PASS |

> Note 1: Constitution keyword density is measured via Phase End Audit (audit-phase). The 12% overall audit score reflects deliverable completeness gaps (missing BASELINE.md/VERIFICATION_REPORT.md at audit time). All 22 FRs passed Gate 1 re-evaluation in Phase 5 with zero code changes detected since Phase 4. Constitution structural requirements (§1-§4) are enforced by ruff, pyright, and cyclomatic complexity guards in the codebase.
>
> **ASPICE Traceability**: Quality baseline references `TEST_PLAN.md` (test planning) and `TEST_RESULTS.md` (test execution records) for metric derivation.

## 4. Performance Baseline (A/B monitoring)

| Metric | Baseline Value |
|--------|---------------|
| Response Time | N/A — verification phase |
| Memory | N/A — verification phase |
| Error Rate | N/A — verification phase |

## 5. Known Issues
| Severity | Count | Description |
|----------|-------|-------------|
| HIGH | 0 | No known HIGH severity issues |

## 6. Acceptance Sign-off
- Agent A: Johnny (session: P5-entry-20260526) - 2026-05-26
- Approver: (pending)
