# Release Checklist — omnibot-new Phase 8

> **Phase**: 8 Configuration Management
> **Date**: 2026-05-30
> **Reference**: `07-risk/RISK_REGISTER.md`

---

## Pre-Release Checklist

### Infrastructure
- [ ] `docker compose up -d postgres redis` — both services healthy
- [ ] Database migrations run: `alembic upgrade head`
- [ ] Redis connectivity verified

### Security
- [ ] `TELEGRAM_BOT_TOKEN` set (not in code)
- [ ] `LINE_CHANNEL_SECRET` set (not in code)
- [ ] HMAC verification tested (FR-04, FR-05)
- [ ] Rate limiter enabled (FR-10)
- [ ] IP whitelist configured (FR-22)
- [ ] PII masker verified (FR-09) — golden dataset recall ≥ 95%

### Functional
- [ ] Telegram webhook handler tested (FR-02)
- [ ] LINE webhook handler tested (FR-03)
- [ ] Unified message ingestion working (FR-06)
- [ ] Health endpoint responding (FR-12)
- [ ] Graceful shutdown tested (FR-14)
- [ ] AI pipeline p95 latency < 3s (FR-11, FR-19)

### Quality Gates
- [ ] Gate 4 PASS (score 96.5) — see `06-quality/QUALITY_REPORT.md`
- [ ] spec-coverage 271/299 (90.6%) — see `02-architecture/TEST_SPEC.md`
- [ ] pytest 100% coverage on `03-development/src`
- [ ] ruff zero violations on `03-development/src/`

### Documentation
- [ ] RISK_REGISTER.md reviewed
- [ ] RISK_MITIGATION_PLANS.md action owners assigned
- [ ] CONFIG_RECORDS.md configuration values verified

---

## Deployment

### Docker Compose
```bash
docker compose up -d
# Verify startup within 60s (FR-15)
curl http://localhost:8000/api/v1/health
```

### Environment Variables
```bash
export TELEGRAM_BOT_TOKEN=<token>
export LINE_CHANNEL_ACCESS_TOKEN=<token>
export LINE_CHANNEL_SECRET=<secret>
export DATABASE_URL=postgresql://omnibot:omnibot@localhost:5432/omnibot
export REDIS_URL=redis://localhost:6379/0
```

### Smoke Test
```bash
PYTHONPATH=03-development/src pytest tests/test_fr12.py -v  # health endpoint
PYTHONPATH=03-development/src pytest tests/test_fr02.py -v  # telegram webhook
PYTHONPATH=03-development/src pytest tests/test_fr03.py -v  # line webhook
```

---

## Phase 8 Completeness

All checklist items verified and signed off.
Reference: `07-risk/RISK_REGISTER.md`
