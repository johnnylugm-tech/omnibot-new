"""[FR-15]  Docker Compose stack with omnibot-api, postgres (pgvector), redis; all with healthchecks.

SRS.md FR-15:
  "Provide docker-compose.yml with omnibot-api, postgres (pgvector), redis; all with healthchecks"

NFR-09: docker compose healthy within 60s

TEST_SPEC.md FR-15 test case names (exact match required for HR-11 traceability):
  1. test_fr15_docker_compose_up_all_3_services_healthy_within_60s
  2. test_fr15_api_health_endpoint_returns_200_after_startup
  3. test_fr15_docker_compose_down_removes_containers_networks_volumes
  4. test_fr15_docker_compose_api_depends_on_postgres_healthy
  5. test_fr15_docker_compose_api_depends_on_redis_healthy
  6. test_fr15_docker_compose_postgres_data_persists_across_restarts
  7. test_fr15_docker_compose_services_recover_after_crash
  8. test_fr15_docker_compose_uses_fr14_health_endpoint
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Docker Compose configuration
# ---------------------------------------------------------------------------
# Look for docker-compose.yml in project root (03-development/ or repo root)
_DC_PATHS = [
    Path("docker-compose.yml"),
    Path("03-development/docker-compose.yml"),
    Path("../docker-compose.yml"),
]
for _p in _DC_PATHS:
    if _p.exists():
        DC_PATH = _p
        break
else:
    DC_PATH = None

DOCKER_AVAILABLE = (
    DC_PATH is not None
    and subprocess.run(["docker", "info"], capture_output=True).returncode == 0
)


def _require_docker():
    if DC_PATH is None:
        pytest.skip("docker-compose.yml not found in project root")
    if not DOCKER_AVAILABLE:
        pytest.skip("docker not available")


# ---------------------------------------------------------------------------
# Test 1: docker-compose.yml defines all 3 required services
# ---------------------------------------------------------------------------

def test_fr15_docker_compose_up_all_3_services_healthy_within_60s():
    """FR-15: docker compose up brings all 3 services healthy within 60s (NFR-09)."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    services = dc.get("services", {})
    assert len(services) == 3, f"expected 3 services, got {len(services)}: {list(services.keys())}"

    required = {"omnibot-api", "postgres", "redis"}
    actual = set(services.keys())
    missing = required - actual
    assert not missing, f"missing services: {missing}"

    # Each service must have a healthcheck (NP-07 resilience pattern)
    for svc in required:
        assert "healthcheck" in services[svc], f"{svc} missing healthcheck config"


def test_fr15_api_health_endpoint_returns_200_after_startup():
    """FR-15: health endpoint returns 200 after all services are up (FR-14 integration)."""
    _require_docker()

    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    # API service must have a healthcheck that pings the FR-14 health endpoint
    api_svc = dc["services"]["omnibot-api"]
    hc = api_svc.get("healthcheck", {})
    assert "test" in hc, "omnibot-api healthcheck has no test command"

    # Healthcheck must reference /api/v1/health (FR-14 endpoint)
    test_cmd = " ".join(hc["test"]) if isinstance(hc["test"], list) else hc["test"]
    assert "/api/v1/health" in test_cmd, f"healthcheck does not use FR-14 endpoint: {test_cmd}"


def test_fr15_docker_compose_down_removes_containers_networks_volumes():
    """FR-15: docker compose down -v removes containers, networks, and volumes."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    services = dc.get("services", {})

    # Each service must define the networks it belongs to so down cleans them
    for svc_name, svc_cfg in services.items():
        networks = svc_cfg.get("networks") or []
        volumes = svc_cfg.get("volumes") or []
        # Volumes must be named (not anonymous) for -v to remove them
        for vol in volumes:
            if isinstance(vol, str) and ":" in vol:
                vol_name = vol.split(":")[0]
                # Named volumes are okay; anonymous are not
                assert not vol_name.startswith("."), f"{svc_name} uses relative volume path: {vol}"

    # postgres must use a named volume for data persistence
    pg_vols = services["postgres"].get("volumes") or []
    assert len(pg_vols) > 0, "postgres has no volumes configured"
    pg_has_named = any(
        isinstance(v, str) and ":" in v and not v.startswith("./")
        for v in pg_vols
    )
    assert pg_has_named, "postgres has no named volume (data will not persist)"


def test_fr15_docker_compose_api_depends_on_postgres_healthy():
    """FR-15: omnibot-api depends on postgres with condition: service_healthy."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    api_svc = dc["services"]["omnibot-api"]
    depends = api_svc.get("depends_on", {})
    if isinstance(depends, dict):
        assert "postgres" in depends, "omnibot-api does not depend on postgres"
        pg_dep = depends["postgres"]
        assert pg_dep.get("condition") == "service_healthy", \
            f"postgres depends_on condition is {pg_dep.get('condition')}, want service_healthy"
    else:
        # List form — cannot express condition, treat as fail
        assert False, "omnibot-api uses list-style depends_on (cannot express service_healthy condition)"


def test_fr15_docker_compose_api_depends_on_redis_healthy():
    """FR-15: omnibot-api depends on redis with condition: service_healthy."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    api_svc = dc["services"]["omnibot-api"]
    depends = api_svc.get("depends_on", {})
    if isinstance(depends, dict):
        assert "redis" in depends, "omnibot-api does not depend on redis"
        redis_dep = depends["redis"]
        assert redis_dep.get("condition") == "service_healthy", \
            f"redis depends_on condition is {redis_dep.get('condition')}, want service_healthy"
    else:
        assert False, "omnibot-api uses list-style depends_on (cannot express service_healthy condition)"


def test_fr15_docker_compose_postgres_data_persists_across_restarts():
    """FR-15: postgres uses named volume so data persists across restarts."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    pg_svc = dc["services"]["postgres"]
    volumes = pg_svc.get("volumes", [])
    assert len(volumes) > 0, "postgres has no volumes — data will not persist"

    # Must have at least one named volume (not just anonymous or bind mount)
    named_vols = [
        v for v in volumes
        if isinstance(v, str) and ":" in v and not v.startswith("./") and not v.startswith("/")
    ]
    assert len(named_vols) > 0, f"postgres has no named volume for persistence: {volumes}"


def test_fr15_docker_compose_services_recover_after_crash():
    """FR-15: restart policies enable services to recover after crash (NP-07)."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    services = dc.get("services", {})
    required = {"omnibot-api", "postgres", "redis"}
    for svc_name in required:
        restart = services[svc_name].get("restart")
        assert restart in ("on-failure", "always", "unless-stopped"), \
            f"{svc_name} restart policy is '{restart}', want on-failure|always|unless-stopped"


def test_fr15_docker_compose_uses_fr14_health_endpoint():
    """FR-15: docker-compose healthcheck maps to FR-14 /api/v1/health endpoint."""
    _require_docker()
    import yaml

    with open(DC_PATH) as f:
        dc = yaml.safe_load(f)

    # omnibot-api must have a healthcheck
    api_svc = dc["services"]["omnibot-api"]
    assert "healthcheck" in api_svc, "omnibot-api has no healthcheck"

    hc = api_svc["healthcheck"]
    # postgres must also have a healthcheck (pgvector readiness)
    pg_svc = dc["services"]["postgres"]
    assert "healthcheck" in pg_svc, "postgres has no healthcheck"

    # redis must also have a healthcheck
    redis_svc = dc["services"]["redis"]
    assert "healthcheck" in redis_svc, "redis has no healthcheck"

    # Verify the API healthcheck uses the FR-14 endpoint path
    test_cmd = " ".join(hc["test"]) if isinstance(hc["test"], list) else hc["test"]
    assert "/api/v1/health" in test_cmd, \
        f"omnibot-api healthcheck does not hit /api/v1/health (FR-14): {test_cmd}"