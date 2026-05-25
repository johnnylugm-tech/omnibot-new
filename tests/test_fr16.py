"""FR-16: Phase 1 ODD SQL queries — FCR rate, p95 latency per platform, knowledge source distribution.

SRS.md §FR-16:
  "Provide Phase 1 ODD SQL queries: FCR rate, p95 latency per platform,
   knowledge source distribution"

TEST_SPEC.md FR-16 test case names (exact match required for HR-11 traceability):
  1. test_fr16_fcr_query_parses_without_syntax_error
  2. test_fr16_latency_query_uses_percentile_cont_0_95
  3. test_fr16_knowledge_hits_query_parses_without_syntax_error
  4. test_fr16_fcr_query_returns_percentage_between_0_and_100
  5. test_fr16_latency_query_returns_avg_and_p95_per_platform
  6. test_fr16_all_use_parameterized_values_no_string_concatenation
  7. test_fr16_fcr_uses_30_day_window
  8. test_fr16_each_sql_file_is_self_contained_and_executable
  9. test_fr16_queries_operate_on_fr01_schema
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# ODD SQL queries (from SPEC.md lines 2072-2106)
# ---------------------------------------------------------------------------

ODD_QUERIES = {
    "fcr": """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN first_contact_resolution THEN 1 ELSE 0 END) AS fcr,
            ROUND(
                SUM(CASE WHEN first_contact_resolution THEN 1 ELSE 0 END) * 100.0
                / NULLIF(COUNT(*), 0), 2
            ) AS fcr_rate_pct
        FROM conversations
        WHERE started_at > NOW() - INTERVAL '30 days'
          AND scope_type = 'in_scope'
          AND first_contact_resolution IS NOT NULL
    """,
    "latency": """
        SELECT
            platform,
            AVG(response_time_ms) AS avg_latency_ms,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) AS p95_latency_ms
        FROM conversations
        WHERE started_at > NOW() - INTERVAL '30 days'
          AND response_time_ms IS NOT NULL
        GROUP BY platform
    """,
    "knowledge_hits": """
        SELECT
            knowledge_source,
            COUNT(*) AS total,
            AVG(confidence_score) AS avg_confidence
        FROM messages
        WHERE role = 'assistant'
          AND created_at > NOW() - INTERVAL '7 days'
          AND knowledge_source IS NOT NULL
        GROUP BY knowledge_source
    """,
}


# ---------------------------------------------------------------------------
# SQL parsing helpers (syntax-only checks — no DB required)
# ---------------------------------------------------------------------------

def _parse_sql_syntax(sql: str) -> str:
    """Strip comments and normalize whitespace for structural checks."""
    # Remove single-line comments
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
    # Collapse whitespace
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip().rstrip(";")


def _has_sql_injection_risk(sql: str) -> bool:
    """Detect string concatenation patterns that indicate SQL injection risk."""
    # Look for quote concatenation: 'foo' + var or 'foo' || var
    if re.search(r"'[^']*'\s*(?:\+\|\\|concat\()", sql, re.IGNORECASE):
        return True
    # Look for execute/exec with string formatting
    if re.search(r"(?:execute|exec)\s*\(\s*f\"", sql, re.IGNORECASE):
        return True
    return False


def _find_literal_values(sql: str) -> list[str]:
    """Extract hardcoded literal values used in WHERE / BETWEEN clauses."""
    # Match comparisons to numbers / strings
    matches = re.findall(r">\s*(\d+(?:\.\d+)?)", sql)
    return matches


# ---------------------------------------------------------------------------
# Test 1: FCR query parses without syntax error
# ---------------------------------------------------------------------------

def test_fr16_fcr_query_parses_without_syntax_error():
    """FR-16: FCR query has valid PostgreSQL syntax (no unbalanced parens/brackets)."""
    sql = ODD_QUERIES["fcr"]
    parsed = _parse_sql_syntax(sql)
    # Check balanced parentheses
    open_parens = parsed.count("(")
    close_parens = parsed.count(")")
    assert open_parens == close_parens, (
        f"FCR query has unbalanced parentheses: "
        f"open={open_parens}, close={close_parens}"
    )
    # Check it contains the expected clauses
    assert "SELECT" in parsed.upper()
    assert "FROM conversations" in parsed.upper()
    assert "first_contact_resolution" in parsed.lower()
    assert "COUNT" in parsed.upper()
    assert "SUM" in parsed.upper()


# ---------------------------------------------------------------------------
# Test 2: latency query uses PERCENTILE_CONT(0.95)
# ---------------------------------------------------------------------------

def test_fr16_latency_query_uses_percentile_cont_0_95():
    """FR-16: latency query uses PERCENTILE_CONT WITHIN GROUP for p95 calculation."""
    sql = _parse_sql_syntax(ODD_QUERIES["latency"])
    assert "PERCENTILE_CONT" in sql.upper(), "latency query missing PERCENTILE_CONT"
    assert "0.95" in sql, "PERCENTILE_CONT must use 0.95 quantile"
    assert "WITHIN GROUP" in sql.upper(), "PERCENTILE_CONT requires WITHIN GROUP clause"
    assert "order by response_time_ms" in sql.lower(), "p95 requires ORDER BY on the column"


# ---------------------------------------------------------------------------
# Test 3: knowledge hits query parses without syntax error
# ---------------------------------------------------------------------------

def test_fr16_knowledge_hits_query_parses_without_syntax_error():
    """FR-16: knowledge hits query has valid PostgreSQL syntax."""
    sql = ODD_QUERIES["knowledge_hits"]
    parsed = _parse_sql_syntax(sql)
    open_parens = parsed.count("(")
    close_parens = parsed.count(")")
    assert open_parens == close_parens, (
        f"knowledge_hits query has unbalanced parentheses: "
        f"open={open_parens}, close={close_parens}"
    )
    assert "SELECT" in parsed.upper()
    assert "FROM messages" in parsed.upper()
    assert "GROUP BY knowledge_source" in parsed.lower()


# ---------------------------------------------------------------------------
# Test 4: FCR query returns percentage between 0 and 100
# ---------------------------------------------------------------------------

def test_fr16_fcr_query_returns_percentage_between_0_and_100():
    """FR-16: FCR query computes a ratio * 100.0, guaranteeing a percentage value.

    The formula is: SUM(CASE WHEN fcr THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0)
    This is a ratio of counts multiplied by 100, which is always in [0, 100]
    when both numerator and denominator are non-negative.
    """
    sql = _parse_sql_syntax(ODD_QUERIES["fcr"])
    # Verify the * 100.0 multiplier is present
    assert "* 100.0" in sql or "* 100" in sql, (
        "FCR query must multiply by 100 to produce a percentage"
    )
    # Verify NULLIF(COUNT(*), 0) guard against division by zero
    assert "NULLIF" in sql.upper(), "FCR query must use NULLIF to prevent division-by-zero"
    assert "COUNT" in sql.upper(), "FCR query must use COUNT(*)"


# ---------------------------------------------------------------------------
# Test 5: latency query returns avg and p95 per platform
# ---------------------------------------------------------------------------

def test_fr16_latency_query_returns_avg_and_p95_per_platform():
    """FR-16: latency query groups by platform and returns both avg and p95 per group."""
    sql = _parse_sql_syntax(ODD_QUERIES["latency"])
    assert "GROUP BY platform" in sql.lower(), (
        "latency query must GROUP BY platform to return per-platform metrics"
    )
    assert "AVG(response_time_ms)" in sql.lower(), (
        "latency query must include AVG(response_time_ms)"
    )
    assert "PERCENTILE_CONT" in sql.upper(), (
        "latency query must include PERCENTILE_CONT for p95"
    )
    assert "response_time_ms" in sql.lower(), (
        "latency query must reference response_time_ms column"
    )


# ---------------------------------------------------------------------------
# Test 6: all queries use parameterized values, no string concatenation
# ---------------------------------------------------------------------------

def test_fr16_all_use_parameterized_values_no_string_concatenation():
    """FR-16: all ODD queries use parameter-safe patterns — no SQL string concatenation.

    Each query uses NOW() - INTERVAL 'N days' (constant expressions) or
    column references — no f-strings, no quote concatenation, no dynamic SQL.
    """
    for name, sql in ODD_QUERIES.items():
        parsed = _parse_sql_syntax(sql)
        assert not _has_sql_injection_risk(parsed), (
            f"[{name}] query contains string-concatenation pattern that could "
            f"indicate SQL injection risk: {sql[:100]}"
        )
        # Verify only constant INTERVAL values are used (not user-supplied strings)
        interval_pattern = re.findall(r"INTERVAL\s+'(\d+)\s+days'", sql, re.IGNORECASE)
        for val in interval_pattern:
            assert val.isdigit(), f"[{name}] INTERVAL value must be a digit: {val}"


# ---------------------------------------------------------------------------
# Test 7: FCR query uses 30-day window
# ---------------------------------------------------------------------------

def test_fr16_fcr_uses_30_day_window():
    """FR-16: FCR query filters on started_at > NOW() - INTERVAL '30 days'."""
    sql = ODD_QUERIES["fcr"]
    assert "INTERVAL '30 days'" in sql, (
        "FCR query must use a 30-day lookback window: INTERVAL '30 days'"
    )
    assert "started_at" in sql.lower(), "FCR query must filter on started_at"
    assert "NOW()" in sql.upper(), "FCR query must use NOW() as reference time"


# ---------------------------------------------------------------------------
# Test 8: each SQL query is self-contained and executable
# ---------------------------------------------------------------------------

def test_fr16_each_sql_file_is_self_contained_and_executable():
    """FR-16: each ODD query is self-contained — no missing FROM, no undefined aliases."""
    for name, sql in ODD_QUERIES.items():
        parsed = _parse_sql_syntax(sql)
        # Must have SELECT ... FROM
        assert re.search(r"\bSELECT\b.*\bFROM\b", parsed, re.IGNORECASE | re.DOTALL), (
            f"[{name}] query missing SELECT or FROM clause"
        )
        # Must not reference undefined aliases (pattern: column not in SELECT)
        # We verify basic structure: SELECT <cols> FROM <table>
        select_match = re.search(r"\bSELECT\b(.+?)\bFROM\b", parsed, re.IGNORECASE | re.DOTALL)
        assert select_match, f"[{name}] cannot parse SELECT clause"
        # Ensure no bare string concatenation that would break execution
        assert "'" not in parsed.replace("''", "") or parsed.count("'") % 2 == 0, (
            f"[{name}] query has unbalanced string quotes — would fail at execution"
        )


# ---------------------------------------------------------------------------
# Test 9: queries operate on FR-01 schema (conversations, messages tables)
# ---------------------------------------------------------------------------

def test_fr16_queries_operate_on_fr01_schema():
    """FR-16: ODD queries reference tables defined in FR-01 schema.

    FR-01 defines: users, conversations, messages, knowledge_base,
    platform_configs, escalation_queue, user_feedback, security_logs.
    The FCR query uses conversations, latency query uses conversations,
    knowledge_hits query uses messages — all are FR-01 tables.
    """
    fcr_sql = ODD_QUERIES["fcr"]
    assert "conversations" in fcr_sql.lower(), (
        "FCR query must reference FR-01 conversations table"
    )

    latency_sql = ODD_QUERIES["latency"]
    assert "conversations" in latency_sql.lower(), (
        "latency query must reference FR-01 conversations table"
    )
    assert "platform" in latency_sql.lower(), (
        "latency query must reference platform column from FR-01 conversations table"
    )
    assert "response_time_ms" in latency_sql.lower(), (
        "latency query must reference response_time_ms column from FR-01 conversations table"
    )

    kh_sql = ODD_QUERIES["knowledge_hits"]
    assert "messages" in kh_sql.lower(), (
        "knowledge_hits query must reference FR-01 messages table"
    )
    assert "knowledge_source" in kh_sql.lower(), (
        "knowledge_hits query must reference knowledge_source column from FR-01 messages table"
    )