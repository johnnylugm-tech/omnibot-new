"""FR-01: Create complete PostgreSQL schema with all core tables and indexes.

SRS.md §FR-01:
  "Create complete PostgreSQL schema with all core tables (users, conversations,
   messages, knowledge_base, platform_configs, escalation_queue, user_feedback,
   security_logs) plus indexes (idx_users_platform_uid, idx_conversations_started,
   idx_conversations_user, idx_conversations_platform, idx_messages_conversation,
   idx_messages_created, idx_kb_category, idx_kb_keywords, idx_kb_embeddings,
   idx_escalation_pending, idx_security_logs_date) as defined in SPEC.md §Database
   Schema. Phase 2/3 columns (e.g. embeddings, embedding_model, satisfaction_score,
   dst_state) are included with defaults to avoid ALTER TABLE later."

Verification method (SRS):
  psql schema inspection: all 8 tables + 11 indexes exist;
  information_schema.columns confirms Phase2/3 columns present with defaults

TEST_INVENTORY.yaml unit tests for FR-01:
  - test_fr01_all_eight_core_tables_exist
  - test_fr01_all_eleven_indexes_exist
  - test_fr01_phase2_phase3_columns_present_with_defaults
"""

from __future__ import annotations

import textwrap

import pytest


# ---------------------------------------------------------------------------
# Expected schema definitions
# ---------------------------------------------------------------------------

EXPECTED_TABLES = [
    "users",
    "conversations",
    "messages",
    "knowledge_base",
    "platform_configs",
    "escalation_queue",
    "user_feedback",
    "security_logs",
]

EXPECTED_INDEXES = [
    "idx_users_platform_uid",
    "idx_conversations_started",
    "idx_conversations_user",
    "idx_conversations_platform",
    "idx_messages_conversation",
    "idx_messages_created",
    "idx_kb_category",
    "idx_kb_keywords",
    "idx_kb_embeddings",
    "idx_escalation_pending",
    "idx_security_logs_date",
]

# Phase 2/3 columns that must exist with DEFAULT values
PHASE2_PHASE3_COLUMNS = [
    ("knowledge_base", "embeddings"),
    ("knowledge_base", "embedding_model"),
    ("conversations", "satisfaction_score"),
    ("conversations", "dst_state"),
    ("messages", "embedding"),
]


# ---------------------------------------------------------------------------
# Test 1 — all 8 core tables exist
# ---------------------------------------------------------------------------

def test_fr01_all_eight_core_tables_exist():
    """FR-01: PostgreSQL schema must contain all 8 core tables listed above.

    The schema is created by create_schema() in migration 001_phase1_core.py.
    This test verifies the schema by querying information_schema.tables.
    """
    from omnibot.config import get_database_url
    from omnibot.db import create_schema, AsyncEngine, async_session

    # Attempt to create schema — if the function doesn't exist yet (RED phase),
    # this import will raise ImportError and the test fails.
    # In GREEN phase the schema will be created; in RED phase the test fails.

    # Verify all 8 tables are present in the database
    async def _check_tables():
        engine = AsyncEngine(get_database_url())
        async with async_session(engine) as session:
            result = await session.execute(
                textwrap.dedent("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                """)
            )
            rows = [row[0] for row in result.fetchall()]
            return rows

    import asyncio
    table_names = asyncio.get_event_loop().run_until_complete(_check_tables())

    for table in EXPECTED_TABLES:
        assert table in table_names, (
            f"Table '{table}' not found in database schema. "
            f"Found tables: {sorted(table_names)}"
        )


# ---------------------------------------------------------------------------
# Test 2 — all 11 indexes exist
# ---------------------------------------------------------------------------

def test_fr01_all_eleven_indexes_exist():
    """FR-01: PostgreSQL schema must contain all 11 indexes listed above.

    Verifies indexes via pg_indexes WHERE schemaname = 'public'.
    """
    from omnibot.config import get_database_url
    from omnibot.db import AsyncEngine, async_session

    async def _check_indexes():
        engine = AsyncEngine(get_database_url())
        async with async_session(engine) as session:
            result = await session.execute(
                textwrap.dedent("""
                    SELECT indexname
                    FROM pg_indexes
                    WHERE schemaname = 'public'
                """)
            )
            rows = [row[0] for row in result.fetchall()]
            return rows

    import asyncio
    index_names = asyncio.get_event_loop().run_until_complete(_check_indexes())

    for idx in EXPECTED_INDEXES:
        assert idx in index_names, (
            f"Index '{idx}' not found in database schema. "
            f"Found indexes: {sorted(index_names)}"
        )


# ---------------------------------------------------------------------------
# Test 3 — Phase 2/3 columns exist with DEFAULT values
# ---------------------------------------------------------------------------

def test_fr01_phase2_phase3_columns_present_with_defaults():
    """FR-01: Phase 2/3 columns must be present in schema with DEFAULT values
    to avoid ALTER TABLE in later phases.

    Verifies via information_schema.columns that each column exists and has
    a non-null column_default.
    """
    from omnibot.config import get_database_url
    from omnibot.db import AsyncEngine, async_session

    async def _check_columns():
        engine = AsyncEngine(get_database_url())
        async with async_session(engine) as session:
            result = await session.execute(
                textwrap.dedent("""
                    SELECT table_name, column_name, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    ORDER BY table_name, column_name
                """)
            )
            return [(row[0], row[1], row[2]) for row in result.fetchall()]

    import asyncio
    columns = asyncio.get_event_loop().run_until_complete(_check_columns())

    col_map = {(tbl, col): default for tbl, col, default in columns}

    for table, column in PHASE2_PHASE3_COLUMNS:
        assert (table, column) in col_map, (
            f"Phase 2/3 column '{table}.{column}' not found in schema. "
            f"Available columns: {col_map}"
        )
        default_val = col_map[(table, column)]
        assert default_val is not None, (
            f"Column '{table}.{column}' must have a DEFAULT value "
            f"(Phase 2/3 columns must not require ALTER TABLE later). "
            f"Got default: {default_val}"
        )