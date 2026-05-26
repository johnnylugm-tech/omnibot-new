"""FR-17: Standardized error codes."""
from __future__ import annotations

AUTH_INVALID_SIGNATURE = "AUTH_INVALID_SIGNATURE"
RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
KNOWLEDGE_NOT_FOUND = "KNOWLEDGE_NOT_FOUND"
VALIDATION_ERROR = "VALIDATION_ERROR"
INTERNAL_ERROR = "INTERNAL_ERROR"
IP_WHITELIST_VIOLATION = "IP_WHITELIST_VIOLATION"
IP_WHITELIST_INVALID = "IP_WHITELIST_INVALID"

HTTP_STATUS_MAP = {
    AUTH_INVALID_SIGNATURE: 401,
    RATE_LIMIT_EXCEEDED: 429,
    KNOWLEDGE_NOT_FOUND: 404,
    VALIDATION_ERROR: 422,
    INTERNAL_ERROR: 500,
    IP_WHITELIST_VIOLATION: 403,
    IP_WHITELIST_INVALID: 400,
}
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
