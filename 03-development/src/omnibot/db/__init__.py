"""[FR-01] Database module with schema creation and async engine support.

Citations:
  - SPEC.md lines 1772-1913 (full schema definition)
"""
from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def _build_engine(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(database_url, echo=False)


_engine: AsyncEngine | None = None


def _get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        from omnibot.config import get_database_url
        _engine = _build_engine(get_database_url())
    return _engine


def build_async_engine(database_url: str) -> AsyncEngine:
    """Build an async engine from a database URL."""
    return _build_engine(database_url)


async def async_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Create an async session context manager."""
    async with AsyncSession(engine) as session:
        yield session


# ---------------------------------------------------------------------------
# Schema constants
# ---------------------------------------------------------------------------

ALL_TABLES = [
    "users",
    "conversations",
    "messages",
    "knowledge_base",
    "platform_configs",
    "escalation_queue",
    "user_feedback",
    "security_logs",
]

ALL_INDEXES = [
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

# Phase 2/3 columns — must exist with DEFAULT values
PHASE23_COLUMNS = {
    "knowledge_base": ["embeddings", "embedding_model"],
    "conversations": ["satisfaction_score", "dst_state"],
    "messages": ["embedding"],
}


# ---------------------------------------------------------------------------
# DDL builders
# ---------------------------------------------------------------------------

def _ddl(sql: str) -> str:
    """Strip indentation from a multi-line SQL string."""
    return textwrap.dedent(sql).strip()


_DDL_TABLES_SQL = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            unified_user_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
            platform VARCHAR(20) NOT NULL,
            platform_user_id VARCHAR(100) NOT NULL,
            profile JSONB,
            preference_tags TEXT[],
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(platform, platform_user_id)
        );

        CREATE TABLE IF NOT EXISTS conversations (
            id SERIAL PRIMARY KEY,
            unified_user_id UUID REFERENCES users(unified_user_id),
            platform VARCHAR(20) NOT NULL,
            started_at TIMESTAMPTZ DEFAULT NOW(),
            ended_at TIMESTAMPTZ,
            status VARCHAR(20) DEFAULT 'active',
            satisfaction_score FLOAT DEFAULT NULL,
            first_contact_resolution BOOLEAN,
            resolution_cost FLOAT,
            response_time_ms INTEGER,
            scope_type VARCHAR(20) DEFAULT 'in_scope',
            dst_state JSONB DEFAULT '{}'::jsonb
        );

        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES conversations(id),
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            intent_detected VARCHAR(50),
            sentiment_category VARCHAR(20),
            sentiment_intensity FLOAT,
            confidence_score FLOAT,
            knowledge_source VARCHAR(20),
            user_feedback VARCHAR(20),
            embedding TEXT DEFAULT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS knowledge_base (
            id SERIAL PRIMARY KEY,
            category VARCHAR(50) NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            keywords TEXT[],
            embeddings TEXT DEFAULT NULL,
            embedding_model VARCHAR(100) NOT NULL
                DEFAULT 'paraphrase-multilingual-MiniLM-L12-v2',
            version INTEGER DEFAULT 1,
            contains_pii BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS platform_configs (
            platform VARCHAR(20) PRIMARY KEY,
            enabled BOOLEAN DEFAULT TRUE,
            config JSONB,
            rate_limit_rps INTEGER DEFAULT 100,
            max_session_duration_sec INTEGER DEFAULT 1800,
            webhook_secret_key_ref VARCHAR(100),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS escalation_queue (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES conversations(id) UNIQUE,
            reason VARCHAR(50) NOT NULL,
            priority INTEGER DEFAULT 0,
            assigned_agent UUID REFERENCES users(unified_user_id),
            queued_at TIMESTAMPTZ DEFAULT NOW(),
            picked_at TIMESTAMPTZ,
            resolved_at TIMESTAMPTZ,
            sla_deadline TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS user_feedback (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES conversations(id),
            message_id INTEGER REFERENCES messages(id),
            feedback VARCHAR(20) NOT NULL CHECK (feedback IN ('thumbs_up', 'thumbs_down')),
            comment TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS security_logs (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES conversations(id),
            layer VARCHAR(10) NOT NULL,
            blocked BOOLEAN DEFAULT FALSE,
            block_reason TEXT,
            source_ip INET,
            platform VARCHAR(20),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """


def _ddl_tables() -> str:
    return _ddl(_DDL_TABLES_SQL)


def _ddl_indexes() -> str:
    return _ddl("""
        CREATE INDEX IF NOT EXISTS idx_users_platform_uid
            ON users (platform, platform_user_id);

        CREATE INDEX IF NOT EXISTS idx_conversations_started
            ON conversations (started_at);
        CREATE INDEX IF NOT EXISTS idx_conversations_user
            ON conversations (unified_user_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_platform
            ON conversations (platform, started_at);

        CREATE INDEX IF NOT EXISTS idx_messages_conversation
            ON messages (conversation_id);
        CREATE INDEX IF NOT EXISTS idx_messages_created
            ON messages (created_at);

        CREATE INDEX IF NOT EXISTS idx_kb_category
            ON knowledge_base (category);
        CREATE INDEX IF NOT EXISTS idx_kb_keywords
            ON knowledge_base USING GIN (keywords);
        CREATE INDEX IF NOT EXISTS idx_kb_embeddings
            ON knowledge_base USING GIN (embeddings);

        CREATE INDEX IF NOT EXISTS idx_escalation_pending
            ON escalation_queue (queued_at)
            WHERE resolved_at IS NULL;

        CREATE INDEX IF NOT EXISTS idx_security_logs_date
            ON security_logs (created_at);
    """)


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

async def create_schema() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from omnibot.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        await conn.execute(text(_ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)))