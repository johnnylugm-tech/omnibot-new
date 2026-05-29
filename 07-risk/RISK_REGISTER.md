# Risk Register — omnibot-new Phase 7

> **Phase**: 7 Risk Management
> **Date**: 2026-05-30
> **Reference**: `06-quality/QUALITY_REPORT.md` (Gate 4 composite score 96.5)

---

## Overview

22 functional requirements assessed across 4 risk categories. Gate 4 quality score: 96.5/100.

| Category | Count | High | Medium | Low |
|----------|-------|------|--------|-----|
| Security | 8 | 3 | 4 | 1 |
| Reliability | 5 | 1 | 3 | 1 |
| Performance | 4 | 1 | 2 | 1 |
| Maintainability | 5 | 0 | 3 | 2 |
| **Total** | **22** | **5** | **12** | **5** |

---

## Risk Entries

| ID | FR | Category | Risk Description | Severity | Likelihood | Status |
|----|----|---------|----------------|----------|------------|--------|
| R-01 | FR-01 | Security | SQL injection via unsanitized raw_payload | High | Low | Mitigated |
| R-02 | FR-04 | Security | HMAC bypass via timing attack | High | Low | Mitigated |
| R-03 | FR-05 | Security | LINE signature bypass | High | Low | Mitigated |
| R-04 | FR-06 | Security | UnifiedMessage poisoning from malformed payload | High | Medium | Mitigated |
| R-05 | FR-09 | Security | PII recall < 95% (Taiwan phone/ID/email false negatives) | High | Medium | Open |
| R-06 | FR-10 | Security | Rate limiter bypass via distributed attack | Medium | Medium | Open |
| R-07 | FR-11 | Performance | AI pipeline p95 latency > 3s (OpenAI fallback slow) | Medium | Medium | Open |
| R-08 | FR-12 | Reliability | Health endpoint false positive (DB up but degraded) | Medium | Low | Mitigated |
| R-09 | FR-14 | Reliability | Graceful shutdown interrupted mid-transaction | Medium | Low | Open |
| R-10 | FR-15 | Reliability | Docker compose unhealthy within 60s startup window | Medium | Low | Open |
| R-11 | FR-16 | Maintainability | Cyclomatic complexity creep in pipeline orchestrator | Medium | Low | Open |
| R-12 | FR-18 | Security | Request-ID correlation broken (missing trace) | Medium | Low | Open |
| R-13 | FR-19 | Performance | AI pipeline latency regression | Medium | Low | Open |
| R-14 | FR-20 | Maintainability | CC > 10 in processing modules | Medium | Low | Open |
| R-15 | FR-21 | Reliability | Escalation queue stuck (Redis unavailable) | Medium | Low | Open |
| R-16 | FR-22 | Security | IP whitelist bypass (X-Forwarded-For spoofing) | High | Low | Open |
| R-17 | FR-02 | Security | Telegram payload parsing crash | Low | Low | Mitigated |
| R-18 | FR-03 | Security | LINE payload parsing crash | Low | Low | Mitigated |
| R-19 | FR-07 | Security | REST response data leakage via error message | Low | Low | Mitigated |
| R-20 | FR-08 | Security | Input sanitization bypass (edge case Unicode) | Low | Low | Open |
| R-21 | FR-13 | Reliability | Structured logger JSON corruption | Low | Low | Mitigated |
| R-22 | FR-17 | Reliability | DB migration failure on fresh schema | Low | Low | Mitigated |

---

## Reference

Risk assessment based on Gate 4 quality evaluation documented in
`06-quality/QUALITY_REPORT.md` (composite score 96.5, architecture score 85.0 after DA challenge).

All security risks follow the pipeline stage order: IP whitelist → HMAC → sanitize → PII → process.
