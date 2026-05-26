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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_orig(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(database_url, echo=False)


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_1(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(None, echo=False)


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_2(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(database_url, echo=None)


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_3(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(echo=False)


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_4(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(database_url, )


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def x__build_engine__mutmut_5(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from a URL string."""
    return create_async_engine(database_url, echo=True)

x__build_engine__mutmut_mutants : ClassVar[MutantDict] = {
'x__build_engine__mutmut_1': x__build_engine__mutmut_1, 
    'x__build_engine__mutmut_2': x__build_engine__mutmut_2, 
    'x__build_engine__mutmut_3': x__build_engine__mutmut_3, 
    'x__build_engine__mutmut_4': x__build_engine__mutmut_4, 
    'x__build_engine__mutmut_5': x__build_engine__mutmut_5
}

def _build_engine(*args, **kwargs):
    result = _mutmut_trampoline(x__build_engine__mutmut_orig, x__build_engine__mutmut_mutants, args, kwargs)
    return result 

_build_engine.__signature__ = _mutmut_signature(x__build_engine__mutmut_orig)
x__build_engine__mutmut_orig.__name__ = 'x__build_engine'


_engine: AsyncEngine | None = None


def x__get_engine__mutmut_orig() -> AsyncEngine:
    global _engine
    if _engine is None:
        from app.infrastructure.config import get_database_url
        _engine = _build_engine(get_database_url())
    return _engine


def x__get_engine__mutmut_1() -> AsyncEngine:
    global _engine
    if _engine is not None:
        from app.infrastructure.config import get_database_url
        _engine = _build_engine(get_database_url())
    return _engine


def x__get_engine__mutmut_2() -> AsyncEngine:
    global _engine
    if _engine is None:
        from app.infrastructure.config import get_database_url
        _engine = None
    return _engine


def x__get_engine__mutmut_3() -> AsyncEngine:
    global _engine
    if _engine is None:
        from app.infrastructure.config import get_database_url
        _engine = _build_engine(None)
    return _engine

x__get_engine__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_engine__mutmut_1': x__get_engine__mutmut_1, 
    'x__get_engine__mutmut_2': x__get_engine__mutmut_2, 
    'x__get_engine__mutmut_3': x__get_engine__mutmut_3
}

def _get_engine(*args, **kwargs):
    result = _mutmut_trampoline(x__get_engine__mutmut_orig, x__get_engine__mutmut_mutants, args, kwargs)
    return result 

_get_engine.__signature__ = _mutmut_signature(x__get_engine__mutmut_orig)
x__get_engine__mutmut_orig.__name__ = 'x__get_engine'


def x_build_async_engine__mutmut_orig(database_url: str) -> AsyncEngine:
    """Build an async engine from a database URL."""
    return _build_engine(database_url)


def x_build_async_engine__mutmut_1(database_url: str) -> AsyncEngine:
    """Build an async engine from a database URL."""
    return _build_engine(None)

x_build_async_engine__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_async_engine__mutmut_1': x_build_async_engine__mutmut_1
}

def build_async_engine(*args, **kwargs):
    result = _mutmut_trampoline(x_build_async_engine__mutmut_orig, x_build_async_engine__mutmut_mutants, args, kwargs)
    return result 

build_async_engine.__signature__ = _mutmut_signature(x_build_async_engine__mutmut_orig)
x_build_async_engine__mutmut_orig.__name__ = 'x_build_async_engine'


async def x_async_session__mutmut_orig(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Create an async session context manager."""
    async with AsyncSession(engine) as session:
        yield session


async def x_async_session__mutmut_1(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Create an async session context manager."""
    async with AsyncSession(None) as session:
        yield session

x_async_session__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_session__mutmut_1': x_async_session__mutmut_1
}

def async_session(*args, **kwargs):
    result = _mutmut_trampoline(x_async_session__mutmut_orig, x_async_session__mutmut_mutants, args, kwargs)
    return result 

async_session.__signature__ = _mutmut_signature(x_async_session__mutmut_orig)
x_async_session__mutmut_orig.__name__ = 'x_async_session'


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

def x__ddl__mutmut_orig(sql: str) -> str:
    """Strip indentation from a multi-line SQL string."""
    return textwrap.dedent(sql).strip()


# ---------------------------------------------------------------------------
# DDL builders
# ---------------------------------------------------------------------------

def x__ddl__mutmut_1(sql: str) -> str:
    """Strip indentation from a multi-line SQL string."""
    return textwrap.dedent(None).strip()

x__ddl__mutmut_mutants : ClassVar[MutantDict] = {
'x__ddl__mutmut_1': x__ddl__mutmut_1
}

def _ddl(*args, **kwargs):
    result = _mutmut_trampoline(x__ddl__mutmut_orig, x__ddl__mutmut_mutants, args, kwargs)
    return result 

_ddl.__signature__ = _mutmut_signature(x__ddl__mutmut_orig)
x__ddl__mutmut_orig.__name__ = 'x__ddl'


def x__ddl_tables__mutmut_orig() -> str:
    return _ddl("""
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
    """)


def x__ddl_tables__mutmut_1() -> str:
    return _ddl(None)

x__ddl_tables__mutmut_mutants : ClassVar[MutantDict] = {
'x__ddl_tables__mutmut_1': x__ddl_tables__mutmut_1
}

def _ddl_tables(*args, **kwargs):
    result = _mutmut_trampoline(x__ddl_tables__mutmut_orig, x__ddl_tables__mutmut_mutants, args, kwargs)
    return result 

_ddl_tables.__signature__ = _mutmut_signature(x__ddl_tables__mutmut_orig)
x__ddl_tables__mutmut_orig.__name__ = 'x__ddl_tables'


def x__ddl_indexes__mutmut_orig() -> str:
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
            ON knowledge_base USING GIN (embeddings gin_trgm_ops);

        CREATE INDEX IF NOT EXISTS idx_escalation_pending
            ON escalation_queue (queued_at)
            WHERE resolved_at IS NULL;

        CREATE INDEX IF NOT EXISTS idx_security_logs_date
            ON security_logs (created_at);
    """)


def x__ddl_indexes__mutmut_1() -> str:
    return _ddl(None)

x__ddl_indexes__mutmut_mutants : ClassVar[MutantDict] = {
'x__ddl_indexes__mutmut_1': x__ddl_indexes__mutmut_1
}

def _ddl_indexes(*args, **kwargs):
    result = _mutmut_trampoline(x__ddl_indexes__mutmut_orig, x__ddl_indexes__mutmut_mutants, args, kwargs)
    return result 

_ddl_indexes.__signature__ = _mutmut_signature(x__ddl_indexes__mutmut_orig)
x__ddl_indexes__mutmut_orig.__name__ = 'x__ddl_indexes'


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_orig(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_1(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = None
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_2(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(None)
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_3(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split("XX;XX")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_4(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = None
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_5(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = None
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_6(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_7(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            break
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_8(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = None
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_9(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            None
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_10(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "XX\nXX".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_11(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split(None)
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_12(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("XX\nXX")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_13(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_14(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith(None)
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_15(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("XX--XX")
        ).strip()
        if sql_only:
            out.append(stripped)
    return out


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def x__split_ddl__mutmut_16(ddl: str) -> list[str]:
    """Split a multi-statement DDL string into individual SQL statements.

    Each chunk may contain leading comment lines (e.g. \"-- Core tables\");
    only skip chunks that are *pure* comments with no SQL content.
    """
    chunks = ddl.split(";")
    out: list[str] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        # Remove leading comment lines to test whether any SQL follows them
        sql_only = "\n".join(
            line for line in stripped.split("\n")
            if not line.strip().startswith("--")
        ).strip()
        if sql_only:
            out.append(None)
    return out

x__split_ddl__mutmut_mutants : ClassVar[MutantDict] = {
'x__split_ddl__mutmut_1': x__split_ddl__mutmut_1, 
    'x__split_ddl__mutmut_2': x__split_ddl__mutmut_2, 
    'x__split_ddl__mutmut_3': x__split_ddl__mutmut_3, 
    'x__split_ddl__mutmut_4': x__split_ddl__mutmut_4, 
    'x__split_ddl__mutmut_5': x__split_ddl__mutmut_5, 
    'x__split_ddl__mutmut_6': x__split_ddl__mutmut_6, 
    'x__split_ddl__mutmut_7': x__split_ddl__mutmut_7, 
    'x__split_ddl__mutmut_8': x__split_ddl__mutmut_8, 
    'x__split_ddl__mutmut_9': x__split_ddl__mutmut_9, 
    'x__split_ddl__mutmut_10': x__split_ddl__mutmut_10, 
    'x__split_ddl__mutmut_11': x__split_ddl__mutmut_11, 
    'x__split_ddl__mutmut_12': x__split_ddl__mutmut_12, 
    'x__split_ddl__mutmut_13': x__split_ddl__mutmut_13, 
    'x__split_ddl__mutmut_14': x__split_ddl__mutmut_14, 
    'x__split_ddl__mutmut_15': x__split_ddl__mutmut_15, 
    'x__split_ddl__mutmut_16': x__split_ddl__mutmut_16
}

def _split_ddl(*args, **kwargs):
    result = _mutmut_trampoline(x__split_ddl__mutmut_orig, x__split_ddl__mutmut_mutants, args, kwargs)
    return result 

_split_ddl.__signature__ = _mutmut_signature(x__split_ddl__mutmut_orig)
x__split_ddl__mutmut_orig.__name__ = 'x__split_ddl'


async def x_create_schema__mutmut_orig() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(ddl):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_1() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = None
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(ddl):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_2() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(None)
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(ddl):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_3() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = None
        for statement in _split_ddl(ddl):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_4() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(None)
        for statement in _split_ddl(ddl):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_5() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(None):
            await conn.execute(text(statement))


async def x_create_schema__mutmut_6() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(ddl):
            await conn.execute(None)


async def x_create_schema__mutmut_7() -> None:
    """Create the complete Phase 1 PostgreSQL schema.

    Creates all 8 core tables and 11 indexes as defined in SPEC.md §Database
    Schema. Phase 2/3 columns (embeddings, embedding_model, satisfaction_score,
    dst_state, embedding) are included with DEFAULT values to avoid ALTER TABLE
    later.

    Citations:
      - SPEC.md lines 1772-1913 (tables and indexes)
      - SRS.md §FR-01 (requirement description)
    """
    from app.infrastructure.config import get_database_url
    from sqlalchemy import text

    engine = _build_engine(get_database_url())
    async with engine.begin() as conn:
        # DDL split into individual statements — asyncpg forbids multiple
        # commands in a prepared statement.
        ddl = _ddl(f"""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;

            -- Core tables
            {_ddl_tables()}

            -- Indexes
            {_ddl_indexes()}
        """)
        for statement in _split_ddl(ddl):
            await conn.execute(text(None))

x_create_schema__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_schema__mutmut_1': x_create_schema__mutmut_1, 
    'x_create_schema__mutmut_2': x_create_schema__mutmut_2, 
    'x_create_schema__mutmut_3': x_create_schema__mutmut_3, 
    'x_create_schema__mutmut_4': x_create_schema__mutmut_4, 
    'x_create_schema__mutmut_5': x_create_schema__mutmut_5, 
    'x_create_schema__mutmut_6': x_create_schema__mutmut_6, 
    'x_create_schema__mutmut_7': x_create_schema__mutmut_7
}

def create_schema(*args, **kwargs):
    result = _mutmut_trampoline(x_create_schema__mutmut_orig, x_create_schema__mutmut_mutants, args, kwargs)
    return result 

create_schema.__signature__ = _mutmut_signature(x_create_schema__mutmut_orig)
x_create_schema__mutmut_orig.__name__ = 'x_create_schema'