"""FR-22: IP Whitelist."""
from __future__ import annotations

import ipaddress


class IPWhitelist:
    def __init__(self, cidrs: list[str]):
        self._networks = []
        for c in cidrs:
            try:
                self._networks.append(ipaddress.ip_network(c))
            except ValueError:
                continue

    def is_allowed(self, ip: str) -> bool:
        """Check if IP is in the whitelist. Returns False for invalid IPs."""
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(addr in net for net in self._networks)
