# Risk Mitigation Plans — omnibot-new Phase 7

> **Phase**: 7 Risk Management
> **Date**: 2026-05-30
> **Reference**: `06-quality/QUALITY_REPORT.md` (Gate 4 composite score 96.5)

---

## Mitigation Plans

### R-05: PII Masker Recall < 95% (FR-09) — OPEN

**Risk**: Taiwan phone/ID/email false negatives in `processing/pii.py`.
**Mitigation Plan**:
1. Add production-side recall measurement using golden dataset
2. Set alert if recall drops below 95% on sample batches
3. Quarterly manual audit of masked vs. raw logs

**Residual Risk**: Medium (automated detection supplemented by manual review)

---

### R-06: Distributed Rate Limiter Bypass (FR-10) — OPEN

**Risk**: IP rotation bypasses per-user rate limiter.
**Mitigation Plan**:
1. IP whitelist as secondary layer (FR-22) — blocks IPs not in whitelist before rate check
2. Monitor failed auth rate as proxy signal
3. Consider per-user device fingerprinting for future enhancement

**Residual Risk**: Medium

---

### R-07 / R-13: AI Pipeline Latency Regression (FR-11 / FR-19) — OPEN

**Risk**: p95 latency > 3s due to OpenAI API or fallback chain.
**Mitigation Plan**:
1. Production p95 alert at 2.5s threshold (before Gate 4 threshold of 3s)
2. Fallback to rule-based response when AI latency exceeds 1s
3. Monitor OpenAI API status page during peak hours

**Residual Risk**: Medium

---

### R-09: Graceful Shutdown Interrupt (FR-14) — OPEN

**Risk**: SIGTERM received mid-transaction.
**Mitigation Plan**:
1. Add integration test: run load test + SIGTERM simultaneously
2. Verify no orphaned DB transactions or Redis locks on shutdown
3. Document shutdown sequence for production operators

**Residual Risk**: Low (with test coverage)

---

### R-10: Docker Unhealthy Within 60s (FR-15) — OPEN

**Risk**: `depends_on` not sufficient for app readiness.
**Mitigation Plan**:
1. Add explicit `start_period: 30s` to docker-compose healthcheck
2. Add readiness probe to `/api/v1/health`
3. Document expected startup time in RUNBOOK.md

**Residual Risk**: Low

---

### R-11 / R-14: CC Creep (FR-16 / FR-20) — OPEN

**Risk**: Cyclomatic complexity increases in `pipeline.py`.
**Mitigation Plan**:
1. Gate 4 CRG monitoring on every FR commit
2. Ruff `max-complexity = 10` enforced in pre-commit
3. Refactor complex stages into isolated helper functions when CC > 8

**Residual Risk**: Low (enforced by gate)

---

### R-12: Request-ID Correlation Gap (FR-18) — OPEN

**Risk**: Missing trace when `X-Request-ID` header absent.
**Mitigation Plan**:
1. Middleware auto-generates Request-ID if absent
2. Add integration test for Request-ID propagation through pipeline
3. Log correlation verified in test_fr18.py

**Residual Risk**: Low (with test coverage)

---

### R-16: X-Forwarded-For Spoofing (FR-22) — OPEN

**Risk**: Attacker spoofs X-Forwarded-For to bypass IP whitelist.
**Mitigation Plan**:
1. Document deployment requirement: reverse proxy must strip external X-Forwarded-For
2. Middleware accepts only trusted proxy IPs
3. Add deployment checklist item in RUNBOOK.md

**Residual Risk**: Medium (requires operator compliance)

---

## All Mitigated Risks

For completeness, the following risks have confirmed controls in code and do not require ongoing mitigation plans:

| ID | FR | Control |
|----|----|---------|
| R-01 | FR-01 | SQLAlchemy ORM, parameterized queries |
| R-02 | FR-04 | `hmac.compare_digest` (constant-time) |
| R-03 | FR-05 | `hmac.compare_digest` (constant-time) |
| R-04 | FR-06 | Frozen dataclass + ValidationError |
| R-17 | FR-02 | Descriptive ValidationError |
| R-18 | FR-03 | Descriptive ValidationError |
| R-19 | FR-07 | Error response sanitization |
| R-21 | FR-13 | Structured JSON logger |
| R-22 | FR-17 | Alembic idempotent migrations |

---

## Mitigation Tracking

Risk register: `07-risk/RISK_REGISTER.md`
Risk status: `07-risk/RISK_STATUS_REPORT.md`
Quality baseline: `06-quality/QUALITY_REPORT.md` (Gate 4 score 96.5)
