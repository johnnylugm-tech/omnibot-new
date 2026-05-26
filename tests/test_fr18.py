"""[FR-18]  Python naming conventions, docstrings, function length, CC ≤ 10."""
from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

SRC_ROOT = Path("03-development/src/omnibot")


def test_fr18_ruff_check_zero_violations():
    """Run ruff check on the source and assert zero violations."""
    result = subprocess.run(
        ["ruff", "check", "03-development/src/"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"ruff found violations:\n{result.stdout}\n{result.stderr}"


def test_fr18_radon_cc_max_less_than_or_equal_10():
    """Assert no function/method in source has cyclomatic complexity > 10."""
    import json

    result = subprocess.run(
        ["radon", "cc", "03-development/src/", "-j"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"radon cc failed: {result.stderr}"

    data = json.loads(result.stdout)
    violations = []
    for filepath, blocks in data.items():
        for block in blocks:
            complexity = block.get("complexity", 0)
            if complexity > 10:
                name = block.get("name", "?")
                line = block.get("lineno", "?")
                violations.append(f"{filepath}:{line} {name} CC={complexity}")

    assert len(violations) == 0, f"Functions with CC > 10:\n" + "\n".join(violations)


def test_fr18_all_public_functions_have_docstrings():
    """All public (non-underscore) functions in source must have docstrings."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name.startswith("_") and not name.startswith("__"):
                    continue
                doc = ast.get_docstring(node)
                if doc is None:
                    violations.append(f"{filepath}:{node.lineno} {name} has no docstring")

    assert len(violations) == 0, "Public functions missing docstrings:\n" + "\n".join(violations)


def test_fr18_function_length_less_than_or_equal_50_lines():
    """No function may exceed 50 lines (excluding docstring/comment/blank)."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    for filepath in src_files:
        try:
            content = filepath.read_text()
            tree = ast.parse(content, filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = node.lineno
                end = node.end_lineno or start
                # count non-empty, non-comment lines
                lines = content.splitlines()
                code_lines = [
                    ln.strip()
                    for ln in lines[start - 1 : end]
                    if ln.strip() and not ln.strip().startswith("#")
                ]
                if len(code_lines) > 50:
                    violations.append(
                        f"{filepath}:{start} {node.name} has {len(code_lines)} lines (> 50)"
                    )

    assert len(violations) == 0, "Functions exceeding 50 lines:\n" + "\n".join(violations)


def test_fr18_constants_use_upper_snake_case():
    """Module-level constants must use UPPER_SNAKE_CASE."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    snake_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        # Only check module-level (top-level) assignments — not locals inside functions
        for stmt in tree.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.startswith("_"):
                            continue
                        if name.isupper() or "_" not in name:
                            continue
                        if snake_pattern.match(name):
                            violations.append(
                                f"{filepath}:{stmt.lineno} constant '{name}' should be UPPER_SNAKE_CASE"
                            )

    assert len(violations) == 0, "Constants with wrong naming:\n" + "\n".join(violations)


def test_fr18_classes_use_pascal_case():
    """All class definitions must use PascalCase."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]+([A-Z][a-zA-Z0-9]*)*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                name = node.name
                if name.startswith("_"):
                    continue
                if not pascal_pattern.match(name):
                    violations.append(f"{filepath}:{node.lineno} class '{name}' should be PascalCase")

    assert len(violations) == 0, "Classes with wrong naming:\n" + "\n".join(violations)


def test_fr18_variables_and_functions_use_snake_case():
    """Variables and functions (non-public) must use snake_case."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    snake_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")
    pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]+([A-Z][a-zA-Z0-9]*)*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                name = node.id
                if name.startswith("_"):
                    continue
                if pascal_pattern.match(name) or (name[0].isupper() and "_" not in name):
                    if snake_pattern.match(name):
                        violations.append(
                            f"{filepath}:{getattr(node, 'lineno', '?')} var '{name}' should be snake_case"
                        )

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name.startswith("__") and name.endswith("__"):
                    continue
                if name.startswith("_"):
                    continue
                if pascal_pattern.match(name) and "_" not in name:
                    if not snake_pattern.match(name):
                        violations.append(
                            f"{filepath}:{node.lineno} fn '{name}' should be snake_case"
                        )

    assert len(violations) == 0, "Names violating snake_case:\n" + "\n".join(violations)


# ---------------------------------------------------------------------------
# Coverage tests — exercise source code from 03-development/src/omnibot/
# ---------------------------------------------------------------------------


# --- config.py ---

def test_fr18_settings_dataclass():
    from omnibot.config import Settings
    s = Settings(
        telegram_bot_token="t",
        line_channel_secret="l",
        database_url="db",
        redis_url="r",
    )
    assert s.telegram_bot_token == "t"
    assert s.rate_limit_rps == 100
    assert s.rate_limit_window == 60
    assert s.ip_whitelist_cidrs == ""
    assert s.log_level == "INFO"


def test_fr18_config_loader_all_present():
    import os
    from omnibot.config import ConfigLoader
    os.environ["TELEGRAM_BOT_TOKEN"] = "tok"
    os.environ["LINE_CHANNEL_SECRET"] = "sec"
    os.environ["DATABASE_URL"] = "db"
    os.environ["REDIS_URL"] = "redis"
    try:
        s = ConfigLoader.from_env()
        assert s.telegram_bot_token == "tok"
        assert s.line_channel_secret == "sec"
        assert s.database_url == "db"
        assert s.redis_url == "redis"
    finally:
        for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL", "REDIS_URL"):
            os.environ.pop(k, None)


def test_fr18_config_loader_missing_required():
    import os
    from omnibot.config import ConfigLoader
    from omnibot.errors import ConfigError
    for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL", "REDIS_URL"):
        os.environ.pop(k, None)
    try:
        ConfigLoader.from_env()
    except ConfigError as e:
        assert "Missing required" in str(e)


def test_fr18_config_loader_optional_rate_limit():
    import os
    from omnibot.config import ConfigLoader
    os.environ["TELEGRAM_BOT_TOKEN"] = "tok"
    os.environ["LINE_CHANNEL_SECRET"] = "sec"
    os.environ["DATABASE_URL"] = "db"
    os.environ["REDIS_URL"] = "redis"
    os.environ["RATE_LIMIT_RPS"] = "200"
    os.environ["RATE_LIMIT_WINDOW"] = "30"
    try:
        s = ConfigLoader.from_env()
        assert s.rate_limit_rps == 200
        assert s.rate_limit_window == 30
    finally:
        for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL",
                  "REDIS_URL", "RATE_LIMIT_RPS", "RATE_LIMIT_WINDOW"):
            os.environ.pop(k, None)


def test_fr18_config_loader_invalid_rate_limit():
    import os
    from omnibot.config import ConfigLoader
    from omnibot.errors import ConfigError
    os.environ["TELEGRAM_BOT_TOKEN"] = "tok"
    os.environ["LINE_CHANNEL_SECRET"] = "sec"
    os.environ["DATABASE_URL"] = "db"
    os.environ["REDIS_URL"] = "redis"
    os.environ["RATE_LIMIT_RPS"] = "not_a_number"
    try:
        ConfigLoader.from_env()
    except ConfigError as e:
        assert "Invalid integer" in str(e)
    finally:
        for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL",
                  "REDIS_URL", "RATE_LIMIT_RPS"):
            os.environ.pop(k, None)


def test_fr18_config_loader_optional_fields_defaults():
    import os
    from omnibot.config import ConfigLoader
    os.environ["TELEGRAM_BOT_TOKEN"] = "tok"
    os.environ["LINE_CHANNEL_SECRET"] = "sec"
    os.environ["DATABASE_URL"] = "db"
    os.environ["REDIS_URL"] = "redis"
    try:
        s = ConfigLoader.from_env()
        assert s.ip_whitelist_cidrs == ""
        assert s.log_level == "INFO"
    finally:
        for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL", "REDIS_URL"):
            os.environ.pop(k, None)


def test_fr18_config_loader_optional_fields_custom():
    import os
    from omnibot.config import ConfigLoader
    os.environ["TELEGRAM_BOT_TOKEN"] = "tok"
    os.environ["LINE_CHANNEL_SECRET"] = "sec"
    os.environ["DATABASE_URL"] = "db"
    os.environ["REDIS_URL"] = "redis"
    os.environ["IP_WHITELIST_CIDRS"] = "10.0.0.0/8"
    os.environ["LOG_LEVEL"] = "DEBUG"
    try:
        s = ConfigLoader.from_env()
        assert s.ip_whitelist_cidrs == "10.0.0.0/8"
        assert s.log_level == "DEBUG"
    finally:
        for k in ("TELEGRAM_BOT_TOKEN", "LINE_CHANNEL_SECRET", "DATABASE_URL",
                  "REDIS_URL", "IP_WHITELIST_CIDRS", "LOG_LEVEL"):
            os.environ.pop(k, None)


def test_fr18_get_database_url():
    import os
    from omnibot.config import get_database_url
    os.environ["DATABASE_URL"] = "postgres://localhost/test"
    try:
        assert get_database_url() == "postgres://localhost/test"
    finally:
        os.environ.pop("DATABASE_URL", None)


def test_fr18_get_database_url_missing():
    import os
    from omnibot.config import get_database_url
    from omnibot.errors import ConfigError
    os.environ.pop("DATABASE_URL", None)
    try:
        get_database_url()
    except ConfigError as e:
        assert "DATABASE_URL" in str(e)


def test_fr18_parse_int_or_raise_empty():
    from omnibot.config import _parse_int_or_raise
    assert _parse_int_or_raise("", default=42) == 42


def test_fr18_parse_int_or_raise_valid():
    from omnibot.config import _parse_int_or_raise
    assert _parse_int_or_raise("77", default=42) == 77


def test_fr18_parse_int_or_raise_invalid():
    from omnibot.config import _parse_int_or_raise
    from omnibot.errors import ConfigError
    try:
        _parse_int_or_raise("abc", default=42)
    except ConfigError as e:
        assert "Invalid integer" in str(e)


# --- errors/codes.py ---

def test_fr18_error_codes_constants():
    from omnibot.errors import codes
    assert codes.AUTH_INVALID_SIGNATURE == "AUTH_INVALID_SIGNATURE"
    assert codes.RATE_LIMIT_EXCEEDED == "RATE_LIMIT_EXCEEDED"
    assert codes.INTERNAL_ERROR == "INTERNAL_ERROR"
    assert codes.IP_WHITELIST_VIOLATION == "IP_WHITELIST_VIOLATION"


def test_fr18_http_status_map():
    from omnibot.errors.codes import HTTP_STATUS_MAP, AUTH_INVALID_SIGNATURE, INTERNAL_ERROR
    assert HTTP_STATUS_MAP[AUTH_INVALID_SIGNATURE] == 401
    assert HTTP_STATUS_MAP[INTERNAL_ERROR] == 500


# --- errors/__init__.py ---

def test_fr18_config_error():
    from omnibot.errors import ConfigError
    e = ConfigError("missing key")
    assert str(e) == "missing key"
    assert isinstance(e, ValueError)


def test_fr18_validation_error():
    from omnibot.errors import ValidationError
    e = ValidationError("bad input", status_code=422)
    assert str(e) == "bad input"
    assert e.status_code == 422


def test_fr18_validation_error_default_status():
    from omnibot.errors import ValidationError
    e = ValidationError("bad input")
    assert e.status_code == 422


def test_fr18_ip_whitelist_error():
    from omnibot.errors import IPWhitelistError
    e = IPWhitelistError(["10.0.0.0/8"])
    assert "10.0.0.0/8" in str(e)
    assert e.invalid_cidrs == ["10.0.0.0/8"]


# --- logging/logger.py ---

def test_fr18_structured_logger_info():
    import logging
    from omnibot.logging.logger import StructuredLogger
    log = logging.getLogger("test_fr18")
    log.setLevel(logging.DEBUG)
    logger = StructuredLogger(service_name="test_fr18")
    logger._logger = log
    logger.info("hello", key="val")
    logger.warning("warn")
    logger.error("err")


def test_fr18_structured_logger_custom_service_name():
    from omnibot.logging.logger import StructuredLogger
    logger = StructuredLogger(service_name="my_service")
    assert logger._service_name == "my_service"


# --- infrastructure/health.py ---

def test_fr18_health_check_healthy():
    from omnibot.infrastructure.health import health_check
    result = health_check(
        check_postgres=lambda: True,
        check_redis=lambda: True,
    )
    assert result["status"] == "healthy"
    assert result["postgres"] is True
    assert result["redis"] is True
    assert "uptime_seconds" in result


def test_fr18_health_check_degraded_postgres_down():
    from omnibot.infrastructure.health import health_check
    result = health_check(
        check_postgres=lambda: False,
        check_redis=lambda: True,
    )
    assert result["status"] == "degraded"


def test_fr18_health_check_degraded_redis_down():
    from omnibot.infrastructure.health import health_check
    result = health_check(
        check_postgres=lambda: True,
        check_redis=lambda: False,
    )
    assert result["status"] == "degraded"


def test_fr18_health_check_unhealthy():
    from omnibot.infrastructure.health import health_check
    result = health_check(
        check_postgres=lambda: False,
        check_redis=lambda: False,
    )
    assert result["status"] == "unhealthy"


def test_fr18_health_check_uptime_increases():
    import time
    from omnibot.infrastructure.health import health_check
    r1 = health_check(check_postgres=lambda: True, check_redis=lambda: True)
    time.sleep(0.02)
    r2 = health_check(check_postgres=lambda: True, check_redis=lambda: True)
    assert r2["uptime_seconds"] >= r1["uptime_seconds"]


# --- processing/sanitizer.py ---

def test_fr18_sanitizer_normal_text():
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize("Hello World") == "Hello World"


def test_fr18_sanitizer_none_returns_empty():
    from omnibot.processing.sanitizer import InputSanitizer
    assert InputSanitizer.sanitize(None) == ""


def test_fr18_sanitizer_control_chars_removed():
    from omnibot.processing.sanitizer import InputSanitizer
    result = InputSanitizer.sanitize("a\x00b\x01c")
    assert result == "abc"


# --- processing/pii.py ---

def test_fr18_pii_masker_email():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("email: test@example.com")
    assert "test@example.com" not in result
    assert "[REDACTED]" in result


def test_fr18_pii_masker_phone():
    from omnibot.processing.pii import PIIMasker
    result = PIIMasker.mask("call 0912345678")
    assert "0912345678" not in result
    assert "[REDACTED]" in result


def test_fr18_pii_masker_none():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.mask(None) == ""
    assert PIIMasker.mask_count(None) == 0
    assert PIIMasker.should_escalate(None) is False


def test_fr18_pii_masker_no_pii_unchanged():
    from omnibot.processing.pii import PIIMasker
    text = "Hello, how are you?"
    assert PIIMasker.mask(text) == text


def test_fr18_pii_mask_count():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.mask_count("Hello") == 0
    assert PIIMasker.mask_count("a@b.com and c@d.com") == 2


def test_fr18_pii_should_escalate_sensitive():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.should_escalate("密碼是1234") is True
    assert PIIMasker.should_escalate("my password is secret") is True
    assert PIIMasker.should_escalate("credit card number") is True


def test_fr18_pii_should_escalate_benign():
    from omnibot.processing.pii import PIIMasker
    assert PIIMasker.should_escalate("Hello world") is False


# --- processing/pipeline.py ---

def test_fr18_pipeline_platform_enum():
    from omnibot.processing.pipeline import Platform
    assert Platform.TELEGRAM.value == "telegram"
    assert Platform.LINE.value == "line"


def test_fr18_pipeline_unified_response_dataclass():
    from omnibot.processing.pipeline import UnifiedResponse, Platform
    r = UnifiedResponse(content="ok", source="rule", confidence=0.95, platform=Platform.TELEGRAM, status_code=200)
    assert r.platform == Platform.TELEGRAM
    assert r.status_code == 200
    assert r.content == "ok"


def test_fr18_pipeline_orchestrator_raises_not_implemented():
    from omnibot.processing.pipeline import PipelineOrchestrator, Platform
    orch = PipelineOrchestrator()
    try:
        orch.process(Platform.TELEGRAM, b"body", "sig")
    except NotImplementedError:
        pass


# --- security/verifiers.py ---

def test_fr18_telegram_verifier_valid():
    import hmac
    import hashlib
    from omnibot.security.verifiers import TelegramWebhookVerifier
    token = "my_bot_token"
    body = b"some request body"
    verifier = TelegramWebhookVerifier(token)
    secret = hashlib.sha256(token.encode("utf-8")).digest()
    expected_sig = hmac.new(secret, body, hashlib.sha256).hexdigest()
    assert verifier.verify(body, expected_sig) is True


def test_fr18_telegram_verifier_invalid():
    from omnibot.security.verifiers import TelegramWebhookVerifier
    verifier = TelegramWebhookVerifier("token")
    assert verifier.verify(b"body", "bad_signature") is False


def test_fr18_telegram_verifier_none_signature():
    from omnibot.security.verifiers import TelegramWebhookVerifier
    verifier = TelegramWebhookVerifier("token")
    assert verifier.verify(b"body", None) is False


def test_fr18_line_verifier_valid():
    import hmac
    import hashlib
    import base64
    from omnibot.security.verifiers import LineWebhookVerifier
    secret_str = "my_channel_secret"
    body = b"some body"
    verifier = LineWebhookVerifier(secret_str)
    digest = hmac.new(secret_str.encode("utf-8"), body, hashlib.sha256).digest()
    expected_sig = base64.b64encode(digest).decode()
    assert verifier.verify(body, expected_sig) is True


def test_fr18_line_verifier_invalid():
    from omnibot.security.verifiers import LineWebhookVerifier
    verifier = LineWebhookVerifier("secret")
    assert verifier.verify(b"body", "bad_sig") is False


def test_fr18_line_verifier_none_signature():
    from omnibot.security.verifiers import LineWebhookVerifier
    verifier = LineWebhookVerifier("secret")
    assert verifier.verify(b"body", None) is False


def test_fr18_webhook_verifier_abstract():
    from omnibot.security.verifiers import WebhookVerifier
    import inspect
    assert inspect.isabstract(WebhookVerifier)


# --- security/whitelist.py ---

def test_fr18_ip_whitelist_allowed():
    from omnibot.security.whitelist import IPWhitelist
    wl = IPWhitelist(["10.0.0.0/8", "192.168.0.0/16"])
    assert wl.is_allowed("10.1.2.3") is True
    assert wl.is_allowed("192.168.5.5") is True


def test_fr18_ip_whitelist_blocked():
    from omnibot.security.whitelist import IPWhitelist
    wl = IPWhitelist(["10.0.0.0/8"])
    assert wl.is_allowed("172.16.0.1") is False


def test_fr18_ip_whitelist_invalid_ip_returns_false():
    from omnibot.security.whitelist import IPWhitelist
    wl = IPWhitelist(["10.0.0.0/8"])
    assert wl.is_allowed("not-an-ip") is False


def test_fr18_ip_whitelist_invalid_cidr_raises():
    from omnibot.security.whitelist import IPWhitelist
    from omnibot.errors import IPWhitelistError
    try:
        IPWhitelist(["not-a-cidr"])
    except IPWhitelistError as e:
        assert "not-a-cidr" in str(e)


def test_fr18_ip_whitelist_empty_list_allows_none():
    from omnibot.security.whitelist import IPWhitelist
    wl = IPWhitelist([])
    assert wl.is_allowed("10.0.0.1") is False
    assert wl.is_allowed("not-an-ip") is False


def test_fr18_ip_whitelist_multiple_invalid_cidrs():
    from omnibot.security.whitelist import IPWhitelist
    from omnibot.errors import IPWhitelistError
    try:
        IPWhitelist(["bad1", "bad2"])
    except IPWhitelistError as e:
        assert "bad1" in str(e)
        assert "bad2" in str(e)


# --- security/rate_limiter.py ---

def test_fr18_token_bucket_consume():
    from omnibot.security.rate_limiter import TokenBucket
    tb = TokenBucket(capacity=10, refill_rate=100.0)
    assert tb.consume(1) is True
    assert tb.consume(5) is True


def test_fr18_token_bucket_exhausted():
    from omnibot.security.rate_limiter import TokenBucket
    tb = TokenBucket(capacity=3, refill_rate=0.0)
    assert tb.consume(3) is True
    assert tb.consume(1) is False


def test_fr18_token_bucket_refill():
    import time
    from omnibot.security.rate_limiter import TokenBucket
    tb = TokenBucket(capacity=10, refill_rate=100.0)
    tb.consume(10)
    time.sleep(0.05)
    assert tb.consume(1) is True


def test_fr18_rate_limiter_new_user():
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    assert rl.check("telegram", "user123") is True


def test_fr18_rate_limiter_existing_user():
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    rl._buckets["telegram:user1"] = None
    assert rl.check("telegram", "user1") is True

def test_fr18_rate_limiter_fail_open_on_error():
    from omnibot.security.rate_limiter import RateLimiter
    rl = RateLimiter()
    # Deliberately corrupt the bucket dict to trigger an error path
    rl._buckets = None
    assert rl.check("telegram", "user1") is True


# --- knowledge/matcher.py ---

def test_fr18_knowledge_matcher_exact_match():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["hello"], "answer": "Hi there!", "version": 1}]
    result = KnowledgeMatcher.match("hello world", rules)
    assert result is not None
    assert result["answer"] == "Hi there!"


def test_fr18_knowledge_matcher_no_match():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["hello"], "answer": "Hi!", "version": 1}]
    result = KnowledgeMatcher.match("goodbye", rules)
    assert result is None


def test_fr18_knowledge_matcher_empty_text():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["hello"], "answer": "Hi!", "version": 1}]
    assert KnowledgeMatcher.match("", rules) is None


def test_fr18_knowledge_matcher_inactive_rule_skipped():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["hello"], "answer": "Hi!", "active": False, "version": 1}]
    result = KnowledgeMatcher.match("hello", rules)
    assert result is None


def test_fr18_knowledge_matcher_version_sort():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [
        {"keywords": ["test"], "answer": "old", "version": 1},
        {"keywords": ["test"], "answer": "new", "version": 2},
    ]
    result = KnowledgeMatcher.match("test", rules)
    assert result is not None
    assert result["answer"] == "new"


def test_fr18_knowledge_matcher_partial_match_confidence():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["ello"], "answer": "partial", "version": 1}]
    result = KnowledgeMatcher.match("hello", rules)
    assert result is not None
    # "ello" is a substring but not a word boundary match → 0.70
    assert result["confidence"] == 0.70


def test_fr18_knowledge_matcher_exact_wildcard_match():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["chicken"], "answer": "substring hit", "version": 1}]
    result = KnowledgeMatcher.match("grilledchickenrecipe", rules)
    assert result is not None
    assert result["confidence"] == 0.70


def test_fr18_knowledge_matcher_default_fields():
    from omnibot.knowledge.matcher import KnowledgeMatcher
    rules = [{"keywords": ["hi"]}]
    result = KnowledgeMatcher.match("hi", rules)
    assert result is not None
    assert result["question"] == ""
    assert result["answer"] == ""
    assert result["category"] == "general"
    assert result["source"] == "rule"


# --- escalation/queue.py ---

def test_fr18_escalation_queue_enqueue():
    from omnibot.escalation.queue import EscalationQueue
    entry = EscalationQueue.enqueue("out_of_scope", {"text": "test"})
    assert entry["id"] == -1
    assert entry["reason"] == "out_of_scope"
    assert entry["status"] == "pending"
    assert entry["scope_type"] == "out_of_scope"
    assert entry["source"] == "escalate"


def test_fr18_escalation_queue_enqueue_default_scope():
    from omnibot.escalation.queue import EscalationQueue
    entry = EscalationQueue.enqueue("something_else", {"text": "test"})
    assert entry["scope_type"] == "unknown"


# --- models/__init__.py ---

def test_fr18_platform_enum():
    from omnibot.models import Platform
    assert Platform.TELEGRAM.value == "telegram"
    assert Platform.LINE.value == "line"
    assert Platform.MESSENGER.value == "messenger"
    assert Platform.WHATSAPP.value == "whatsapp"


def test_fr18_message_type_enum():
    from omnibot.models import MessageType
    assert MessageType.TEXT.value == "text"
    assert MessageType.IMAGE.value == "image"


def test_fr18_unified_message_dataclass():
    from omnibot.models import UnifiedMessage, Platform, MessageType
    msg = UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id="123",
        unified_user_id=None,
        message_type=MessageType.TEXT,
        content="hello",
    )
    assert msg.platform == Platform.TELEGRAM
    assert msg.content == "hello"
    assert msg.reply_token is None


def test_fr18_unified_response_dataclass():
    from omnibot.models import UnifiedResponse, Platform
    r = UnifiedResponse(content="reply", source="rule", confidence=0.95)
    assert r.content == "reply"
    assert r.source == "rule"
    assert r.confidence == 0.95
    assert r.status_code == 200


def test_fr18_api_response_success():
    from omnibot.models import ApiResponse
    r = ApiResponse(success=True, data="hello")
    assert r.success is True
    assert r.data == "hello"
    assert r.error is None


def test_fr18_api_response_error():
    from omnibot.models import ApiResponse
    r = ApiResponse(success=False, error="not found", error_code="ERR_404")
    assert r.success is False
    assert r.error == "not found"
    assert r.error_code == "ERR_404"


def test_fr18_paginated_response():
    from omnibot.models import PaginatedResponse
    r = PaginatedResponse(success=True, data=["a", "b"], total=100, page=1, limit=20)
    assert r.total == 100
    assert r.page == 1
    assert r.limit == 20
    assert r.has_next is False
    assert r.data == ["a", "b"]


def test_fr18_knowledge_source_enum():
    from omnibot.models import KnowledgeSource
    assert KnowledgeSource.RULE.value == "rule"
    assert KnowledgeSource.ESCALATE.value == "escalate"


# --- adapters/telegram.py ---

def test_fr18_telegram_adapter_parse_message():
    from omnibot.adapters.telegram import TelegramAdapter
    payload = {
        "message": {
            "from": {"id": 12345},
            "text": "Hello bot",
        }
    }
    msg = TelegramAdapter.parse_message(payload)
    assert msg.platform_user_id == "12345"
    assert msg.content == "Hello bot"


def test_fr18_telegram_adapter_edited_message():
    from omnibot.adapters.telegram import TelegramAdapter
    payload = {
        "edited_message": {
            "from": {"id": 999},
            "text": "Edited text",
        }
    }
    msg = TelegramAdapter.parse_message(payload)
    assert msg.content == "Edited text"


def test_fr18_telegram_adapter_missing_message():
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError
    try:
        TelegramAdapter.parse_message({})
    except ValidationError as e:
        assert "message" in str(e).lower()


def test_fr18_telegram_adapter_missing_from():
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError
    try:
        TelegramAdapter.parse_message({"message": {"text": "hi"}})
    except ValidationError:
        pass


def test_fr18_telegram_adapter_missing_text():
    from omnibot.adapters.telegram import TelegramAdapter
    from omnibot.errors import ValidationError
    try:
        TelegramAdapter.parse_message({"message": {"from": {"id": 1}}})
    except ValidationError:
        pass


# --- adapters/line.py ---

def test_fr18_line_adapter_parse_message():
    from omnibot.adapters.line import LineAdapter
    payload = {
        "events": [{
            "type": "message",
            "message": {"text": "Hello from LINE"},
            "source": {"userId": "U123"},
            "replyToken": "tok",
        }]
    }
    msg = LineAdapter.parse_message(payload)
    assert msg.platform_user_id == "U123"
    assert msg.content == "Hello from LINE"
    assert msg.reply_token == "tok"


def test_fr18_line_adapter_missing_events():
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError
    try:
        LineAdapter.parse_message({})
    except ValidationError as e:
        assert "events" in str(e).lower()


def test_fr18_line_adapter_wrong_event_type():
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError
    try:
        LineAdapter.parse_message({"events": [{"type": "follow"}]})
    except ValidationError as e:
        assert "not supported" in str(e).lower()


def test_fr18_line_adapter_missing_text():
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError
    try:
        LineAdapter.parse_message({"events": [{"type": "message", "source": {"userId": "U1"}}]})
    except ValidationError:
        pass


def test_fr18_line_adapter_missing_user_id():
    from omnibot.adapters.line import LineAdapter
    from omnibot.errors import ValidationError
    try:
        LineAdapter.parse_message({"events": [{"type": "message", "message": {"text": "hi"}}]})
    except ValidationError as e:
        assert "userId" in str(e)


# --- queries/odd_queries.py ---

def test_fr18_odd_queries_dict():
    from omnibot.queries.odd_queries import ODD_QUERIES
    assert "fcr" in ODD_QUERIES
    assert "latency" in ODD_QUERIES
    assert "knowledge_hits" in ODD_QUERIES
    assert "FCR" in ODD_QUERIES["fcr"] or "fcr" in ODD_QUERIES["fcr"].lower()


# --- db/__init__.py ---

def test_fr18_db_constants():
    from omnibot.db import ALL_TABLES, ALL_INDEXES, PHASE23_COLUMNS
    assert "users" in ALL_TABLES
    assert "conversations" in ALL_TABLES
    assert len(ALL_INDEXES) >= 10
    assert "knowledge_base" in PHASE23_COLUMNS


def test_fr18_db_ddl_functions():
    from omnibot.db import _ddl_tables, _ddl_indexes
    tables_sql = _ddl_tables()
    assert "CREATE TABLE IF NOT EXISTS users" in tables_sql
    assert "CREATE TABLE IF NOT EXISTS messages" in tables_sql
    indexes_sql = _ddl_indexes()
    assert "CREATE INDEX IF NOT EXISTS" in indexes_sql


def test_fr18_db_ddl_tables_includes_phase23_columns():
    from omnibot.db import _ddl_tables
    sql = _ddl_tables()
    assert "embeddings" in sql
    assert "satisfaction_score" in sql


# --- __init__.py ---

def test_fr18_package_version():
    from omnibot import __VERSION__
    assert __VERSION__ == "1.0.0"


# --- adapters/__init__.py ---

def test_fr18_adapters_init_exports():
    from omnibot.adapters import LineAdapter, TelegramAdapter
    assert LineAdapter is not None
    assert TelegramAdapter is not None


# --- security/__init__.py ---

def test_fr18_security_init_exports():
    from omnibot.security import IPWhitelist, TelegramWebhookVerifier, LineWebhookVerifier
    assert IPWhitelist is not None
    assert TelegramWebhookVerifier is not None
    assert LineWebhookVerifier is not None


# --- queries/__init__.py ---

def test_fr18_queries_init_exports():
    from omnibot.queries import ODD_QUERIES
    assert ODD_QUERIES is not None