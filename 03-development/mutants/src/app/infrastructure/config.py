"""[FR-01] PostgreSQL database configuration.

Citations:
  - SPEC.md lines 1772-1787 (users table schema)
"""
from __future__ import annotations

import os
from typing import Final

DATABASE_URL_ENV_VAR: Final[str] = "DATABASE_URL"
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


def x_get_database_url__mutmut_orig() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if not url:
        raise ValueError(f"Environment variable {DATABASE_URL_ENV_VAR!r} is not set")
    return url


def x_get_database_url__mutmut_1() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = None
    if not url:
        raise ValueError(f"Environment variable {DATABASE_URL_ENV_VAR!r} is not set")
    return url


def x_get_database_url__mutmut_2() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = os.environ.get(None)
    if not url:
        raise ValueError(f"Environment variable {DATABASE_URL_ENV_VAR!r} is not set")
    return url


def x_get_database_url__mutmut_3() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if url:
        raise ValueError(f"Environment variable {DATABASE_URL_ENV_VAR!r} is not set")
    return url


def x_get_database_url__mutmut_4() -> str:
    """Return the DATABASE_URL from environment variables.

    Raises:
        ValueError: If DATABASE_URL is not set.

    Returns:
        The database connection URL string.
    """
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if not url:
        raise ValueError(None)
    return url

x_get_database_url__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_database_url__mutmut_1': x_get_database_url__mutmut_1, 
    'x_get_database_url__mutmut_2': x_get_database_url__mutmut_2, 
    'x_get_database_url__mutmut_3': x_get_database_url__mutmut_3, 
    'x_get_database_url__mutmut_4': x_get_database_url__mutmut_4
}

def get_database_url(*args, **kwargs):
    result = _mutmut_trampoline(x_get_database_url__mutmut_orig, x_get_database_url__mutmut_mutants, args, kwargs)
    return result 

get_database_url.__signature__ = _mutmut_signature(x_get_database_url__mutmut_orig)
x_get_database_url__mutmut_orig.__name__ = 'x_get_database_url'