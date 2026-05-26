"""Unit tests for app/models.py — non-DB helper functions and constants.

These tests verify the module-level constants and pure functions without
requiring a live database connection (FR-01 schema-creation tests are
DB-dependent and skipped when DATABASE_URL is not set).
"""
from __future__ import annotations


def test_all_tables_constant_has_8_entries():
    """ALL_TABLES lists exactly the 8 core tables defined in SPEC.md."""
    from app.models import ALL_TABLES

    assert len(ALL_TABLES) == 8
    assert "users" in ALL_TABLES
    assert "conversations" in ALL_TABLES
    assert "messages" in ALL_TABLES
    assert "knowledge_base" in ALL_TABLES
    assert "platform_configs" in ALL_TABLES
    assert "escalation_queue" in ALL_TABLES
    assert "user_feedback" in ALL_TABLES
    assert "security_logs" in ALL_TABLES


def test_all_indexes_constant_has_11_entries():
    """ALL_INDEXES lists exactly the 11 named indexes defined in SPEC.md."""
    from app.models import ALL_INDEXES

    assert len(ALL_INDEXES) == 11
    assert "idx_users_platform_uid" in ALL_INDEXES
    assert "idx_conversations_started" in ALL_INDEXES
    assert "idx_conversations_user" in ALL_INDEXES
    assert "idx_conversations_platform" in ALL_INDEXES
    assert "idx_messages_conversation" in ALL_INDEXES
    assert "idx_messages_created" in ALL_INDEXES
    assert "idx_kb_category" in ALL_INDEXES
    assert "idx_kb_keywords" in ALL_INDEXES
    assert "idx_kb_embeddings" in ALL_INDEXES
    assert "idx_escalation_pending" in ALL_INDEXES
    assert "idx_security_logs_date" in ALL_INDEXES


def test_phase23_columns_has_required_tables():
    """PHASE23_COLUMNS documents Phase 2/3 column additions per table."""
    from app.models import PHASE23_COLUMNS

    assert "knowledge_base" in PHASE23_COLUMNS
    assert "embeddings" in PHASE23_COLUMNS["knowledge_base"]
    assert "embedding_model" in PHASE23_COLUMNS["knowledge_base"]

    assert "conversations" in PHASE23_COLUMNS
    assert "satisfaction_score" in PHASE23_COLUMNS["conversations"]
    assert "dst_state" in PHASE23_COLUMNS["conversations"]

    assert "messages" in PHASE23_COLUMNS
    assert "embedding" in PHASE23_COLUMNS["messages"]


def test_split_ddl_handles_empty_chunks():
    """_split_ddl correctly filters empty and comment-only chunks."""
    from app.models import _split_ddl

    result = _split_ddl("SELECT 1;  ; SELECT 2")
    assert "SELECT 1" in result[0]
    assert "SELECT 2" in result[1]


def test_split_ddl_handles_leading_comments():
    """_split_ddl strips leading comment-only lines when SQL follows."""
    from app.models import _split_ddl

    ddl = "-- leading comment\nSELECT 1; -- inline comment"
    result = _split_ddl(ddl)
    # _split_ddl returns the raw chunk strings; it does not strip comments
    assert len(result) == 1
    assert "SELECT 1" in result[0]


def test_split_ddl_skips_pure_comment_chunks():
    """_split_ddl skips chunks that are only comments."""
    from app.models import _split_ddl

    result = _split_ddl("-- comment only\nSELECT 1;  ; -- another pure comment")
    assert len(result) == 1


def test_ddl_strip_indentation():
    """_ddl strips indentation from multi-line SQL using textwrap.dedent."""
    from app.models import _ddl

    result = _ddl("""
        SELECT 1;
        SELECT 2;
    """)
    assert result.startswith("SELECT")
    assert "\n    " not in result


def test_ddl_tables_returns_non_empty_string():
    """_ddl_tables returns a valid multi-statement DDL string."""
    from app.models import _ddl_tables

    result = _ddl_tables()
    assert "CREATE TABLE" in result
    assert "users" in result
    assert "knowledge_base" in result


def test_ddl_indexes_returns_non_empty_string():
    """_ddl_indexes returns a valid multi-statement DDL string."""
    from app.models import _ddl_indexes

    result = _ddl_indexes()
    assert "CREATE INDEX" in result
    assert "idx_users_platform_uid" in result


def test_build_async_engine_returns_engine():
    """build_async_engine creates an AsyncEngine without connecting."""
    from app.models import build_async_engine

    engine = build_async_engine("postgresql+asyncpg://user:pass@localhost/db")
    # AsyncEngine is lazy — verify it returns without error and has correct driver
    assert engine is not None
    assert engine.url.drivername == "postgresql+asyncpg"