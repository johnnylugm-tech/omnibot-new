"""[FR-22] IP Whitelist."""
from __future__ import annotations

import ipaddress

from omnibot.errors import IPWhitelistError
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


class IPWhitelist:
    def xǁIPWhitelistǁ__init____mutmut_orig(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_1(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = None
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_2(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = None
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_3(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(None)
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_4(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(None))
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_5(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                INVALID_CIDRS.append(None)
        if INVALID_CIDRS:
            raise IPWhitelistError(INVALID_CIDRS)
    def xǁIPWhitelistǁ__init____mutmut_6(self, cidrs: list[str]):
        """Initialize with list of CIDR strings to allow."""
        self._networks = []
        INVALID_CIDRS = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                INVALID_CIDRS.append(c)
        if INVALID_CIDRS:
            raise IPWhitelistError(None)
    
    xǁIPWhitelistǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIPWhitelistǁ__init____mutmut_1': xǁIPWhitelistǁ__init____mutmut_1, 
        'xǁIPWhitelistǁ__init____mutmut_2': xǁIPWhitelistǁ__init____mutmut_2, 
        'xǁIPWhitelistǁ__init____mutmut_3': xǁIPWhitelistǁ__init____mutmut_3, 
        'xǁIPWhitelistǁ__init____mutmut_4': xǁIPWhitelistǁ__init____mutmut_4, 
        'xǁIPWhitelistǁ__init____mutmut_5': xǁIPWhitelistǁ__init____mutmut_5, 
        'xǁIPWhitelistǁ__init____mutmut_6': xǁIPWhitelistǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIPWhitelistǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁIPWhitelistǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁIPWhitelistǁ__init____mutmut_orig)
    xǁIPWhitelistǁ__init____mutmut_orig.__name__ = 'xǁIPWhitelistǁ__init__'

    def xǁIPWhitelistǁis_allowed__mutmut_orig(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(addr in net for net in self._networks)

    def xǁIPWhitelistǁis_allowed__mutmut_1(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = None
        except ValueError:
            return False
        return any(addr in net for net in self._networks)

    def xǁIPWhitelistǁis_allowed__mutmut_2(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(None)
        except ValueError:
            return False
        return any(addr in net for net in self._networks)

    def xǁIPWhitelistǁis_allowed__mutmut_3(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return True
        return any(addr in net for net in self._networks)

    def xǁIPWhitelistǁis_allowed__mutmut_4(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(None)

    def xǁIPWhitelistǁis_allowed__mutmut_5(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(addr not in net for net in self._networks)
    
    xǁIPWhitelistǁis_allowed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIPWhitelistǁis_allowed__mutmut_1': xǁIPWhitelistǁis_allowed__mutmut_1, 
        'xǁIPWhitelistǁis_allowed__mutmut_2': xǁIPWhitelistǁis_allowed__mutmut_2, 
        'xǁIPWhitelistǁis_allowed__mutmut_3': xǁIPWhitelistǁis_allowed__mutmut_3, 
        'xǁIPWhitelistǁis_allowed__mutmut_4': xǁIPWhitelistǁis_allowed__mutmut_4, 
        'xǁIPWhitelistǁis_allowed__mutmut_5': xǁIPWhitelistǁis_allowed__mutmut_5
    }
    
    def is_allowed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIPWhitelistǁis_allowed__mutmut_orig"), object.__getattribute__(self, "xǁIPWhitelistǁis_allowed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_allowed.__signature__ = _mutmut_signature(xǁIPWhitelistǁis_allowed__mutmut_orig)
    xǁIPWhitelistǁis_allowed__mutmut_orig.__name__ = 'xǁIPWhitelistǁis_allowed'
