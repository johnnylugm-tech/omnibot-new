"""[FR-11] Layer 1 rule-based knowledge matcher."""
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


def x__compute_confidence__mutmut_orig(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_1(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = None
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_2(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower not in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_3(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_4(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(None, text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_5(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', None) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_6(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_7(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', ) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_8(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) - r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_9(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' - re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_10(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'XX\bXX' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_11(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_12(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_13(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(None) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_14(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'XX\bXX', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_15(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_16(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_17(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is None
    return 0.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_18(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 1.95 if (word_match or boundary_match) else 0.70


def x__compute_confidence__mutmut_19(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match and boundary_match) else 0.70


def x__compute_confidence__mutmut_20(kw_lower: str, text_lower: str, words: set) -> float:
    """Compute confidence tier for a keyword match."""
    word_match = kw_lower in words
    boundary_match = re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower) is not None
    return 0.95 if (word_match or boundary_match) else 1.7

x__compute_confidence__mutmut_mutants : ClassVar[MutantDict] = {
'x__compute_confidence__mutmut_1': x__compute_confidence__mutmut_1, 
    'x__compute_confidence__mutmut_2': x__compute_confidence__mutmut_2, 
    'x__compute_confidence__mutmut_3': x__compute_confidence__mutmut_3, 
    'x__compute_confidence__mutmut_4': x__compute_confidence__mutmut_4, 
    'x__compute_confidence__mutmut_5': x__compute_confidence__mutmut_5, 
    'x__compute_confidence__mutmut_6': x__compute_confidence__mutmut_6, 
    'x__compute_confidence__mutmut_7': x__compute_confidence__mutmut_7, 
    'x__compute_confidence__mutmut_8': x__compute_confidence__mutmut_8, 
    'x__compute_confidence__mutmut_9': x__compute_confidence__mutmut_9, 
    'x__compute_confidence__mutmut_10': x__compute_confidence__mutmut_10, 
    'x__compute_confidence__mutmut_11': x__compute_confidence__mutmut_11, 
    'x__compute_confidence__mutmut_12': x__compute_confidence__mutmut_12, 
    'x__compute_confidence__mutmut_13': x__compute_confidence__mutmut_13, 
    'x__compute_confidence__mutmut_14': x__compute_confidence__mutmut_14, 
    'x__compute_confidence__mutmut_15': x__compute_confidence__mutmut_15, 
    'x__compute_confidence__mutmut_16': x__compute_confidence__mutmut_16, 
    'x__compute_confidence__mutmut_17': x__compute_confidence__mutmut_17, 
    'x__compute_confidence__mutmut_18': x__compute_confidence__mutmut_18, 
    'x__compute_confidence__mutmut_19': x__compute_confidence__mutmut_19, 
    'x__compute_confidence__mutmut_20': x__compute_confidence__mutmut_20
}

def _compute_confidence(*args, **kwargs):
    result = _mutmut_trampoline(x__compute_confidence__mutmut_orig, x__compute_confidence__mutmut_mutants, args, kwargs)
    return result 

_compute_confidence.__signature__ = _mutmut_signature(x__compute_confidence__mutmut_orig)
x__compute_confidence__mutmut_orig.__name__ = 'x__compute_confidence'


class KnowledgeMatcher:
    @staticmethod
    def match(text: str, rules: list[dict]) -> dict | None:
        """Match text against keyword rules (case-insensitive substring).

        Confidence tiers:
        - 0.95: exact keyword boundary match (word-boundary match)
        - 0.70: ILIKE-style partial substring match
        - inactive rules are skipped
        - results ordered by version desc, top-5 limit
        - empty query returns None
        """
        if not text:
            return None

        try:
            text_lower = text.lower()
            words = set(re.findall(r'\b\w+\b', text_lower))
            active_rules = [r for r in rules if r.get("active", True)]
            for rule in sorted(active_rules, key=lambda r: r.get("version", 0), reverse=True)[:5]:
                for keyword in rule.get("keywords", []):
                    kw_lower = keyword.lower()
                    if kw_lower in text_lower:
                        confidence = _compute_confidence(kw_lower, text_lower, words)
                        return {
                            "question": rule.get("question", ""),
                            "answer": rule.get("answer", ""),
                            "category": rule.get("category", "general"),
                            "confidence": confidence,
                            "source": "rule",
                        }
        except Exception:
            pass
        return None
