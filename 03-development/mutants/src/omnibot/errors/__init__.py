"""Custom exception classes."""
from __future__ import annotations
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


class ConfigError(ValueError):
    """Raised when required configuration keys are missing."""

    def xǁConfigErrorǁ__init____mutmut_orig(self, message: str) -> None:
        """Initialize with error message."""
        super().__init__(message)

    def xǁConfigErrorǁ__init____mutmut_1(self, message: str) -> None:
        """Initialize with error message."""
        super().__init__(None)
    
    xǁConfigErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigErrorǁ__init____mutmut_1': xǁConfigErrorǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConfigErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConfigErrorǁ__init____mutmut_orig)
    xǁConfigErrorǁ__init____mutmut_orig.__name__ = 'xǁConfigErrorǁ__init__'


class ValidationError(Exception):
    """Raised when a payload fails validation."""

    def xǁValidationErrorǁ__init____mutmut_orig(self, message: str, status_code: int = 422) -> None:
        """Initialize with message and optional HTTP status code."""
        super().__init__(message)
        self.status_code = status_code

    def xǁValidationErrorǁ__init____mutmut_1(self, message: str, status_code: int = 423) -> None:
        """Initialize with message and optional HTTP status code."""
        super().__init__(message)
        self.status_code = status_code

    def xǁValidationErrorǁ__init____mutmut_2(self, message: str, status_code: int = 422) -> None:
        """Initialize with message and optional HTTP status code."""
        super().__init__(None)
        self.status_code = status_code

    def xǁValidationErrorǁ__init____mutmut_3(self, message: str, status_code: int = 422) -> None:
        """Initialize with message and optional HTTP status code."""
        super().__init__(message)
        self.status_code = None
    
    xǁValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidationErrorǁ__init____mutmut_1': xǁValidationErrorǁ__init____mutmut_1, 
        'xǁValidationErrorǁ__init____mutmut_2': xǁValidationErrorǁ__init____mutmut_2, 
        'xǁValidationErrorǁ__init____mutmut_3': xǁValidationErrorǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁValidationErrorǁ__init____mutmut_orig)
    xǁValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁValidationErrorǁ__init__'


class IPWhitelistError(Exception):
    """Raised when IP whitelist contains invalid CIDR at startup."""

    def xǁIPWhitelistErrorǁ__init____mutmut_orig(self, invalid_cidrs: list[str]) -> None:
        """Initialize with list of invalid CIDR strings."""
        self.invalid_cidrs = invalid_cidrs
        super().__init__(f"Invalid CIDR in whitelist config: {invalid_cidrs}")

    def xǁIPWhitelistErrorǁ__init____mutmut_1(self, invalid_cidrs: list[str]) -> None:
        """Initialize with list of invalid CIDR strings."""
        self.invalid_cidrs = None
        super().__init__(f"Invalid CIDR in whitelist config: {invalid_cidrs}")

    def xǁIPWhitelistErrorǁ__init____mutmut_2(self, invalid_cidrs: list[str]) -> None:
        """Initialize with list of invalid CIDR strings."""
        self.invalid_cidrs = invalid_cidrs
        super().__init__(None)
    
    xǁIPWhitelistErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIPWhitelistErrorǁ__init____mutmut_1': xǁIPWhitelistErrorǁ__init____mutmut_1, 
        'xǁIPWhitelistErrorǁ__init____mutmut_2': xǁIPWhitelistErrorǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIPWhitelistErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁIPWhitelistErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁIPWhitelistErrorǁ__init____mutmut_orig)
    xǁIPWhitelistErrorǁ__init____mutmut_orig.__name__ = 'xǁIPWhitelistErrorǁ__init__'
