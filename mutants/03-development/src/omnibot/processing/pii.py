"""[FR-09] PII masking L4."""
from __future__ import annotations

import re
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


class PIIMasker:
    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{6,8}\d")
    TAIWAN_ADDRESS_RE = re.compile(
        r"[一-鿿]+(?:市|縣)[一-鿿]+(?:區|鎮|鄉)[一-鿿]+(?:路|街|大道)",  # noqa: E501
    )
    SENSITIVE_KEYWORDS = frozenset(["密碼", "信用卡", "身份證", "護照", "password", "credit card", "ssn"])

    @staticmethod
    def mask(text: str) -> str:
        """Replace emails and phone numbers with '[REDACTED]'."""
        if text is None:
            return ""
        text = PIIMasker.EMAIL_RE.sub("[REDACTED]", text)
        text = PIIMasker.PHONE_RE.sub("[REDACTED]", text)
        text = PIIMasker.TAIWAN_ADDRESS_RE.sub("[REDACTED]", text)
        return text

    @staticmethod
    def mask_count(text: str) -> int:
        """Return the number of PII redactions made."""
        if text is None:
            return 0
        return (
            len(PIIMasker.EMAIL_RE.findall(text))
            + len(PIIMasker.PHONE_RE.findall(text))
            + len(PIIMasker.TAIWAN_ADDRESS_RE.findall(text))
        )

    @staticmethod
    def should_escalate(text: str) -> bool:
        """Return True if text contains sensitive keywords requiring escalation."""
        if text is None:
            return False
        lower = text.lower()
        return any(kw.lower() in lower for kw in PIIMasker.SENSITIVE_KEYWORDS)
