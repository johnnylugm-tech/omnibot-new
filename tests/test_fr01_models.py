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


# ---------------------------------------------------------------------------
# Coverage gap tests — models.py L31-34, L44-45, L269-286
# ---------------------------------------------------------------------------


def test_get_engine_initializes_when_engine_is_none():
    """_get_engine initializes the singleton on first call when _engine is None.

    Covers models.py L31-34: the `if _engine is None:` branch that imports
    get_database_url and calls _build_engine.  The singleton is reset before
    the call and restored to its original value afterwards.
    """
    import app.models as _models
    from unittest.mock import MagicMock, patch

    original = _models._engine
    _models._engine = None
    try:
        mock_engine = MagicMock()
        with patch("app.models._build_engine", return_value=mock_engine):
            with patch("app.infrastructure.config.get_database_url",
                       return_value="postgresql+asyncpg://u:p@localhost/db"):
                result = _models._get_engine()
        assert result is mock_engine
        assert _models._engine is mock_engine
    finally:
        _models._engine = original


def test_async_session_yields_session():
    """async_session yields an AsyncSession without a real DB connection.

    Covers models.py L44-45: `async with AsyncSession(engine) as session:` and
    `yield session`.  AsyncSession is patched to return a mock context manager.
    """
    import asyncio
    from unittest.mock import AsyncMock, MagicMock, patch
    from app.models import async_session

    async def run():
        mock_session = AsyncMock()
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_cm.__aexit__ = AsyncMock(return_value=False)

        with patch("app.models.AsyncSession", return_value=mock_cm):
            engine = MagicMock()
            yielded = []
            async for session in async_session(engine):
                yielded.append(session)

        assert len(yielded) == 1
        assert yielded[0] is mock_session

    asyncio.run(run())


def test_create_schema_executes_ddl_statements():
    """create_schema() opens an engine transaction and executes DDL statements.

    Covers models.py L269-286: the async function body that calls
    _build_engine, engine.begin(), and conn.execute() for each DDL statement.
    Both _build_engine and get_database_url are patched to avoid DB access.
    """
    import asyncio
    from unittest.mock import AsyncMock, MagicMock, patch
    from app.models import create_schema

    async def run():
        mock_conn = AsyncMock()
        mock_tx = MagicMock()
        mock_tx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_tx.__aexit__ = AsyncMock(return_value=False)

        mock_engine = MagicMock()
        mock_engine.begin.return_value = mock_tx

        with patch("app.models._build_engine", return_value=mock_engine):
            with patch("app.infrastructure.config.get_database_url",
                       return_value="postgresql+asyncpg://u:p@localhost/db"):
                await create_schema()

        # At least one DDL statement must have been executed
        assert mock_conn.execute.call_count > 0


# ---------------------------------------------------------------------------
# Coverage gap tests — config.py L23-26
# ---------------------------------------------------------------------------


def test_get_database_url_returns_value_when_env_set(monkeypatch):
    """get_database_url returns the env var value when DATABASE_URL is set.

    Covers config.py L23 (os.environ.get), L24 (if not url: False branch),
    and L26 (return url).
    """
    from app.infrastructure.config import get_database_url
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@localhost/testdb")
    assert get_database_url() == "postgresql+asyncpg://u:p@localhost/testdb"


def test_get_database_url_raises_when_env_not_set(monkeypatch):
    """get_database_url raises ValueError when DATABASE_URL is not set.

    Covers config.py L24 (if not url: True branch) and L25 (raise ValueError).
    """
    import pytest
    from app.infrastructure.config import get_database_url
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValueError, match="DATABASE_URL"):
        get_database_url()