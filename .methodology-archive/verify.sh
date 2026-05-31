#!/bin/bash
set -e

RESULTS_FILE="/Users/johnny/projects/omnibot-new/.sessi-work/env_check_result.json"
SESSI_WORK="/Users/johnny/projects/omnibot-new/.sessi-work"

# Initialize arrays for results
env_vars_found=()
env_vars_missing=()
cli_tools_found=()
cli_tools_missing=()
infra_checks=()

# ─── ENV VARS ───────────────────────────────────────────────────────────────
echo "=== CHECKING REQUIRED ENV VARS ==="

check_env() {
    local var="$1"
    if [[ -n "${!var}" ]]; then
        echo "  [FOUND] $var"
        env_vars_found+=("\"$var\"")
    else
        echo "  [MISSING] $var"
        env_vars_missing+=("$var")
    fi
}

# Required env vars from FR-21
check_env TELEGRAM_BOT_TOKEN
check_env LINE_CHANNEL_ACCESS_TOKEN
check_env LINE_CHANNEL_SECRET
check_env DATABASE_URL
check_env REDIS_URL

echo ""
echo "=== CHECKING OPTIONAL ENV VARS ==="
for var in TELEGRAM_WEBHOOK_SECRET RATE_LIMIT_CAPACITY RATE_LIMIT_REFILL_RATE SERVICE_NAME IP_WHITELIST_CIDRS; do
    if [[ -n "${!var}" ]]; then
        echo "  [SET] $var = ${!var}"
    else
        echo "  [DEFAULT] $var (not overridden)"
    fi
done

# ─── CLI TOOLS ──────────────────────────────────────────────────────────────
echo ""
echo "=== CHECKING CLI TOOLS ==="

check_cmd() {
    local cmd="$1"
    local version_flag="$2"

    if command -v "$cmd" &>/dev/null; then
        if [[ -n "$version_flag" ]]; then
            ver=$(eval "$cmd $version_flag" 2>/dev/null | head -1 || echo "found")
            echo "  [FOUND] $cmd: $ver"
        else
            echo "  [FOUND] $cmd"
        fi
        cli_tools_found+=("\"$cmd\"")
    else
        echo "  [MISSING] $cmd"
        cli_tools_missing+=("$cmd")
    fi
}

# Python (any 3.9+)
if command -v python3 &>/dev/null; then
    py_ver=$(python3 --version 2>&1 | awk '{print $2}')
    py_major=$(echo "$py_ver" | cut -d. -f1)
    py_minor=$(echo "$py_ver" | cut -d. -f2)
    if [[ "$py_major" -ge 3 && "$py_minor" -ge 9 ]]; then
        echo "  [FOUND] python3: $py_ver (>= 3.9 required)"
        cli_tools_found+=("python3@$py_ver")
    else
        echo "  [MISSING] python3: $py_ver (need >= 3.9)"
        cli_tools_missing+=("python3")
    fi
else
    echo "  [MISSING] python3"
    cli_tools_missing+=("python3")
fi

check_cmd docker "--version"
check_cmd docker-compose "--version"
check_cmd psql "--version"
check_cmd pg_isready "--version"
check_cmd redis-cli "--version"
check_cmd curl "--version"
check_cmd ruff "--version"
check_cmd radon "--version"
check_cmd pytest "--version"
check_cmd k6 "version"
check_cmd node "--version"
check_cmd npm "--version"
check_cmd git "--version"

# ─── INFRA SERVICES ─────────────────────────────────────────────────────────
echo ""
echo "=== CHECKING INFRA SERVICES ==="

echo "--- Docker Compose Services ---"
if command -v docker &>/dev/null && docker info &>/dev/null; then
    echo "  [REACHABLE] Docker daemon running"

    for svc in postgres redis omnibot-api; do
        container_name="omnibot-$svc"
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${container_name}$"; then
            status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "no-healthcheck")
            echo "  [RUNNING] $svc: $status"
            infra_checks+=("{\"name\":\"$svc\",\"type\":\"container\",\"reachable\":true,\"checked_via\":\"docker ps\",\"fix\":\"docker compose up -d $svc\"}")
        else
            echo "  [NOT RUNNING] $svc"
            infra_checks+=("{\"name\":\"$svc\",\"type\":\"container\",\"reachable\":false,\"checked_via\":\"docker ps\",\"fix\":\"docker compose up -d $svc\"}")
        fi
    done

    if docker network ls --format '{{.Name}}' 2>/dev/null | grep -q omnibot-net; then
        echo "  [FOUND] omnibot-net network"
    fi

    if docker volume ls --format '{{.Name}}' 2>/dev/null | grep -q postgres_data; then
        echo "  [FOUND] postgres_data volume"
    fi
else
    echo "  [SKIP] Docker daemon not available"
fi

echo "--- PostgreSQL Connectivity ---"
if command -v psql &>/dev/null; then
    if [[ -n "$DATABASE_URL" ]]; then
        # Try localhost first
        if PGPASSWORD=omnibot psql -h localhost -p 5432 -U omnibot -d omnibot -c "SELECT 1" &>/dev/null; then
            echo "  [REACHABLE] PostgreSQL on localhost:5432"
            infra_checks+=("{\"name\":\"postgres\",\"type\":\"PostgreSQL 16\",\"reachable\":true,\"checked_via\":\"psql -c SELECT 1\",\"fix\":\"\"}")
        elif docker ps --format '{{.Names}}' 2>/dev/null | grep -q omnibot-postgres; then
            if docker exec omnibot-postgres psql -U omnibot -d omnibot -c "SELECT 1" &>/dev/null; then
                echo "  [REACHABLE] PostgreSQL (docker)"
                infra_checks+=("{\"name\":\"postgres\",\"type\":\"PostgreSQL 16\",\"reachable\":true,\"checked_via\":\"docker exec psql\",\"fix\":\"\"}")
            else
                echo "  [UNREACHABLE] PostgreSQL (docker exec failed)"
                infra_checks+=("{\"name\":\"postgres\",\"type\":\"PostgreSQL 16\",\"reachable\":false,\"checked_via\":\"docker exec psql\",\"fix\":\"docker compose up -d postgres\"}")
            fi
        else
            echo "  [NOT RUNNING] PostgreSQL container"
            infra_checks+=("{\"name\":\"postgres\",\"type\":\"PostgreSQL 16\",\"reachable\":false,\"checked_via\":\"psql\",\"fix\":\"docker compose up -d postgres\"}")
        fi
    else
        echo "  [SKIP] DATABASE_URL not set"
    fi
fi

echo "--- Redis Connectivity ---"
if command -v redis-cli &>/dev/null; then
    if redis-cli ping &>/dev/null; then
        echo "  [REACHABLE] Redis on localhost:6379"
        infra_checks+=("{\"name\":\"redis\",\"type\":\"Redis 7\",\"reachable\":true,\"checked_via\":\"redis-cli ping\",\"fix\":\"\"}")
    elif docker ps --format '{{.Names}}' 2>/dev/null | grep -q omnibot-redis; then
        if docker exec omnibot-redis redis-cli ping &>/dev/null; then
            echo "  [REACHABLE] Redis (docker)"
            infra_checks+=("{\"name\":\"redis\",\"type\":\"Redis 7\",\"reachable\":true,\"checked_via\":\"docker exec redis-cli\",\"fix\":\"\"}")
        else
            echo "  [UNREACHABLE] Redis (docker exec failed)"
            infra_checks+=("{\"name\":\"redis\",\"type\":\"Redis 7\",\"reachable\":false,\"checked_via\":\"docker exec redis-cli\",\"fix\":\"docker compose up -d redis\"}")
        fi
    else
        echo "  [NOT RUNNING] Redis container"
        infra_checks+=("{\"name\":\"redis\",\"type\":\"Redis 7\",\"reachable\":false,\"checked_via\":\"redis-cli\",\"fix\":\"docker compose up -d redis\"}")
    fi
fi

# ─── BUILD RESULT JSON ───────────────────────────────────────────────────────
echo ""
echo "=== BUILDING RESULT JSON ==="

missing_count=0
[[ ${#env_vars_missing[@]} -gt 0 ]] && ((missing_count++))
[[ ${#cli_tools_missing[@]} -gt 0 ]] && ((missing_count++))

ready="false"
[[ $missing_count -eq 0 ]] && ready="true"

# Build env found
env_found_json=""
for item in "${env_vars_found[@]}"; do
    env_found_json+="{\"name\":$item,\"present\":true},"
done
env_found_json=$(echo "$env_found_json" | sed 's/,$//')

# Build env missing
env_missing_json=""
for var in "${env_vars_missing[@]}"; do
    env_missing_json+="{\"name\":\"$var\",\"present\":false,\"fix\":\"export $var=<value>\"},"
done
env_missing_json=$(echo "$env_missing_json" | sed 's/,$//')

# Build cli found
cli_found_json=""
for item in "${cli_tools_found[@]}"; do
    cli_found_json+="{\"name\":$item,\"present\":true},"
done
cli_found_json=$(echo "$cli_found_json" | sed 's/,$//')

# Build cli missing
cli_missing_json=""
for cmd in "${cli_tools_missing[@]}"; do
    case "$cmd" in
        python3) fix="brew install python@3.12" ;;
        docker) fix="brew install --cask docker" ;;
        docker-compose) fix="brew install docker-compose" ;;
        psql|pg_isready) fix="brew install postgresql" ;;
        redis-cli) fix="brew install redis" ;;
        ruff) fix="pip install ruff" ;;
        radon) fix="pip install radon" ;;
        pytest) fix="pip install pytest pytest-asyncio" ;;
        k6) fix="brew install k6" ;;
        node|npm) fix="brew install node" ;;
        git) fix="brew install git" ;;
        *) fix="brew install $cmd" ;;
    esac
    cli_missing_json+="{\"name\":\"$cmd\",\"present\":false,\"fix\":\"$fix\"},"
done
cli_missing_json=$(echo "$cli_missing_json" | sed 's/,$//')

# Build infra
infra_json=$(printf '%s,' "${infra_checks[@]}" | sed 's/,$//')

# Optional missing
opt_set=0
for var in TELEGRAM_WEBHOOK_SECRET RATE_LIMIT_CAPACITY RATE_LIMIT_REFILL_RATE SERVICE_NAME IP_WHITELIST_CIDRS; do
    if [[ -z "${!var}" ]]; then
        opt_set=1
        break
    fi
done
if [[ $opt_set -eq 1 ]]; then
    optional_missing_json='["TELEGRAM_WEBHOOK_SECRET","RATE_LIMIT_CAPACITY","RATE_LIMIT_REFILL_RATE","SERVICE_NAME","IP_WHITELIST_CIDRS"]'
else
    optional_missing_json="[]"
fi

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
docker_svcs_json='["postgres","redis","omnibot-api"]'

summary="Environment readiness check complete. "
[[ ${#env_vars_missing[@]} -gt 0 ]] && summary+="Missing required env vars: ${env_vars_missing[*]}. "
[[ ${#cli_tools_missing[@]} -gt 0 ]] && summary+="Missing CLI tools: ${cli_tools_missing[*]}. "

# Write JSON
cat > "$RESULTS_FILE" << EOF
{
  "ready": $ready,
  "checked_at": "$timestamp",
  "env_vars": {
    "required": [$env_found_json $env_missing_json],
    "optional_missing": $optional_missing_json
  },
  "cli_tools": {
    "required": [$cli_found_json $cli_missing_json]
  },
  "infra_services": {
    "required": [$infra_json],
    "docker_compose_services": $docker_svcs_json
  },
  "summary": "$summary"
}
EOF

echo "Results written to: $RESULTS_FILE"
cat "$RESULTS_FILE"
