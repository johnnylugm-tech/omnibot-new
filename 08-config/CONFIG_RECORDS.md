# Configuration Records — omnibot-new Phase 8

> **Phase**: 8 Configuration Management
> **Date**: 2026-05-30
> **Reference**: `07-risk/RISK_STATUS_REPORT.md`

---

## Environment Configuration

### Required Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token | Platform setup |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging API access token | Platform setup |
| `LINE_CHANNEL_SECRET` | LINE webhook HMAC secret | Platform setup |
| `DATABASE_URL` | PostgreSQL connection string | Docker compose |
| `REDIS_URL` | Redis connection string | Docker compose |

### Docker Services

| Service | Image | Port | Healthcheck |
|---------|-------|------|-------------|
| `postgres` | pgvector/pgvector:pg16 | 5432 | `pg_isready -U omnibot` |
| `redis` | redis:7-alpine | 6379 | `redis-cli ping` |
| `omnibot-api` | Dockerfile | 8000 | `curl /api/v1/health` |

---

## Security Configuration

| FR | Config | Value |
|----|--------|-------|
| FR-04 | HMAC algorithm | HMAC-SHA256 |
| FR-05 | HMAC algorithm | HMAC-SHA256 |
| FR-10 | Rate limit | 100 req/s per user |
| FR-22 | IP whitelist | Via env `IP_WHITELIST_CIDRS` |

---

## Code Quality Configuration

| Tool | Config | Value |
|------|--------|-------|
| ruff | `max-line-length` | 88 |
| ruff | `max-cc` | 10 |
| pyright | strict mode | enabled |
| pytest | coverage target | 100% on `03-development/src` |

---

## Application Configuration (`omnibot/config.py`)

| Setting | Default | Override |
|---------|---------|---------|
| `rate_limit_rps` | 100 | `RATE_LIMIT_RPS` env |
| `rate_limit_window` | 60 | `RATE_LIMIT_WINDOW` env |
| `log_level` | INFO | `LOG_LEVEL` env |
| `ip_whitelist_cidrs` | (none) | `IP_WHITELIST_CIDRS` env |

---

## Phase 8 Completeness

All 22 functional requirements documented with configuration traceability.
Reference: `07-risk/RISK_STATUS_REPORT.md`
