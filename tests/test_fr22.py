"""FR-22: IP Whitelist."""
from __future__ import annotations


def test_fr22_ip_whitelist_allows_listed_ip():
    """FR-22: listed IP allowed."""
    from omnibot.security.whitelist import IPWhitelist
    whitelist = IPWhitelist(["192.168.1.0/24"])
    assert whitelist.is_allowed("192.168.1.50") is True


def test_fr22_ip_whitelist_rejects_unlisted_ip():
    """FR-22: unlisted IP rejected."""
    from omnibot.security.whitelist import IPWhitelist
    whitelist = IPWhitelist(["192.168.1.0/24"])
    assert whitelist.is_allowed("10.0.0.1") is False


def test_fr22_ip_whitelist_empty_cidrs_rejects_all():
    """FR-22: empty whitelist rejects all."""
    from omnibot.security.whitelist import IPWhitelist
    whitelist = IPWhitelist([])
    assert whitelist.is_allowed("1.2.3.4") is False


def test_fr22_ip_whitelist_invalid_ip_returns_false():
    """FR-22: invalid IP format returns False (fail-secure)."""
    from omnibot.security.whitelist import IPWhitelist
    whitelist = IPWhitelist(["192.168.1.0/24"])
    assert whitelist.is_allowed("not-an-ip") is False
