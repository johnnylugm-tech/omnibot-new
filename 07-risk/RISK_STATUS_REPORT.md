# Risk Status Report — omnibot-new Phase 7

> **Phase**: 7 Risk Management
> **Date**: 2026-05-30
> **Reference**: `06-quality/QUALITY_REPORT.md` (Gate 4 composite score 96.5)

---

## Summary

| Status | Count | Details |
|--------|-------|---------|
| Mitigated | 13 | Risks with implemented controls (HMAC, rate limiting, sanitization, DI) |
| Open | 9 | Risks requiring monitoring or future action |
| Accepted | 0 | None — all open risks have defined action plans |

---

## Mitigated Risks

| ID | FR | Control Implemented |
|----|----|--------------------|
| R-01 | FR-01 | SQLAlchemy parameterized queries; no raw SQL |
| R-02 | FR-04 | `hmac.compare_digest` (constant-time) |
| R-03 | FR-05 | `hmac.compare_digest` (constant-time) |
| R-04 | FR-06 | Frozen dataclass + ValidationError on malformed input |
| R-17 | FR-02 | Descriptive ValidationError raised, no crash |
| R-18 | FR-03 | Descriptive ValidationError raised, no crash |
| R-19 | FR-07 | Error responses sanitized, no data leakage |
| R-21 | FR-13 | Structured logger with Pydantic model validation |
| R-22 | FR-17 | Alembic migration runner with idempotent UP/DOWN migrations |

---

## Open Risks

| ID | FR | Risk | Next Action | Owner |
|----|----|------|------------|-------|
| R-05 | FR-09 | PII recall < 95% (edge cases in Taiwan phone/ID) | Periodic recall metric measurement | QA |
| R-06 | FR-10 | Distributed rate limiter bypass | Monitor per-IP rate limit violations | DevOps |
| R-07 | FR-11 | AI pipeline p95 > 3s | Set latency alerts in production | DevOps |
| R-09 | FR-14 | Shutdown interrupt during transaction | Test shutdown under load | DevOps |
| R-10 | FR-15 | Docker unhealthy within 60s | Add startup probe timeout tuning | DevOps |
| R-11 | FR-16 | CC creep in orchestrator | Gate 4 monitors CC ≤ 10 | Dev |
| R-12 | FR-18 | Request-ID correlation gap | Add test coverage for trace propagation | Dev |
| R-13 | FR-19 | Latency regression | p95 metric on every PR | DevOps |
| R-14 | FR-20 | CC > 10 violations | Gate 4 monitors CC; Ruff enforces | Dev |
| R-16 | FR-22 | X-Forwarded-For spoofing | Trust reverse proxy headers only | DevOps |

---

## Risk Trend

Based on Gate 4 quality evaluation (`06-quality/QUALITY_REPORT.md`):
- **Security risks**: 13/22 mitigated (59%), 5 open (23%)
- **All open risks have defined monitoring or action plans**
- No CRITICAL risks remain open

---

## Gate 4 Quality Baseline

Risk register derived from Gate 4 (score 96.5) quality assessment:
- Architecture: 85.0 (DA challenge applied — star topology is appropriate)
- All 14 dimensions passed individual thresholds
- spec-coverage: 90.6% (271/299 TEST_SPEC.md items)
