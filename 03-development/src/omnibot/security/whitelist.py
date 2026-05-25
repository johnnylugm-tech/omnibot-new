"""FR-22: IP Whitelist."""
from __future__ import annotations

import ipaddress

from omnibot.errors import IPWhitelistError


class IPWhitelist:
    def __init__(self, cidrs: list[str]):
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

    def is_allowed(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(addr in net for net in self._networks)
