# Risk Assessment — omnibot-new Phase 7

> **Phase**: 7 Risk Management
> **Date**: 2026-05-30
> **Reference**: `06-quality/QUALITY_REPORT.md` (Gate 4 composite score 96.5)

---

## Assessment Methodology

Risks assessed using **likelihood × impact** matrix aligned with Gate 4 quality dimensions:
- **Likelihood**: High (>60%), Medium (20-60%), Low (<20%)
- **Impact**: Critical, High, Medium, Low
- **Severity = Likelihood × Impact**

---

## Per-FR Risk Assessments

### FR-01: PostgreSQL Schema
**Risk**: SQL injection via unsanitized `raw_payload` or dynamic query construction.
**Assessment**: LOW — SQLAlchemy ORM used exclusively; no raw SQL. Schema defined in `omnibot/db/__init__.py` with async engine.
**Residual Risk**: Low

### FR-04: Telegram HMAC Verification
**Risk**: Timing attack on signature comparison.
**Assessment**: LOW — `hmac.compare_digest` used (constant-time). `security/verifiers.py` verified by Gate 4 mutation testing (518 mutants, 100% killed).
**Residual Risk**: Low

### FR-05: LINE HMAC Verification
**Risk**: Same as FR-04.
**Assessment**: LOW — Same implementation pattern as FR-04.
**Residual Risk**: Low

### FR-09: PII Masker
**Risk**: Taiwan phone/ID/email false negatives (recall < 95%).
**Assessment**: MEDIUM — PII recall/precision metrics not measured in automated tests. Manual validation required.
**Mitigation**: Production monitoring with periodic sample-based recall measurement.
**Residual Risk**: Medium

### FR-10: Token-Bucket Rate Limiter
**Risk**: Distributed attack bypassing per-user bucket via IP rotation.
**Assessment**: MEDIUM — Rate limiter is per-user, not per-IP, but IP spoofing is possible.
**Mitigation**: IP whitelist (FR-22) as additional layer.
**Residual Risk**: Medium

### FR-11: AI Response Pipeline
**Risk**: p95 latency > 3s due to OpenAI API timeout or fallback chain.
**Assessment**: MEDIUM — OpenAI fallback is implemented; latency is measured (FR-19).
**Mitigation**: Production p95 alert threshold at 2.5s.
**Residual Risk**: Medium

### FR-14: Graceful Shutdown
**Risk**: Mid-flight transaction interrupted on SIGTERM.
**Assessment**: LOW — Shutdown handler implemented; DI-based cleanup.
**Mitigation**: Test under load before production.
**Residual Risk**: Low

### FR-16: Ruff Zero-Violation Enforcement
**Risk**: CC creep in orchestrator increases maintainability burden.
**Assessment**: LOW — Gate 4 monitors CC ≤ 10; Ruff enforces on every commit.
**Residual Risk**: Low

### FR-18: Request-ID Correlation
**Risk**: Correlation broken when request-ID header missing or stripped.
**Assessment**: LOW — Middleware implemented; needs test coverage.
**Mitigation**: Add trace propagation test.
**Residual Risk**: Low

### FR-19: AI Pipeline Latency Metrics
**Risk**: p95 regression not caught before production.
**Assessment**: MEDIUM — Metrics exist; alert threshold not confirmed.
**Mitigation**: Set production alerts at 2.5s.
**Residual Risk**: Medium

### FR-20: Cyclomatic Complexity Guard
**Risk**: CC > 10 violations accumulate in processing modules.
**Assessment**: LOW — Gate 4 monitors CC; Ruff enforces.
**Residual Risk**: Low

### FR-21: Escalation Queue Worker
**Risk**: Queue stuck when Redis unavailable.
**Assessment**: LOW — Fail-open implemented; queue worker retries.
**Mitigation**: Redis health monitoring.
**Residual Risk**: Low

### FR-22: IP Whitelist Middleware
**Risk**: X-Forwarded-For spoofing bypassing whitelist.
**Assessment**: MEDIUM — Reverse proxy must sanitize X-Forwarded-For.
**Mitigation**: Trust only proxy-reported headers; document deployment requirement.
**Residual Risk**: Medium

---

## Top 3 Risks Requiring Monitoring

1. **FR-09 PII Masker** — requires periodic manual recall audit
2. **FR-11/FR-19 AI Pipeline** — requires production latency alert
3. **FR-22 IP Whitelist** — requires deployment documentation of proxy header requirement

---

## Assessment Basis

Gate 4 quality evaluation (`06-quality/QUALITY_REPORT.md`, score 96.5):
- Security dimensions: 100 (linting, security, secrets_scanning)
- Performance dimensions: 100 (mutation_testing, performance)
- Architecture: 85.0 (star topology confirmed appropriate by DA challenge)
