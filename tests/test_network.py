"""Tests for safe, bounded network diagnostic input validation."""
import pytest

from chocobot.engine.network.diagnostics import local_network_info, lookup_host, ping_host, probe_tcp_port


def test_localhost_dns_resolution_uses_local_resolver():
    result = lookup_host("localhost")
    assert result["ok"] is True
    assert result["addresses"]
    assert any(":" in address or address.startswith("127.") for address in result["addresses"])


def test_url_or_path_is_rejected_when_host_only_is_required():
    with pytest.raises(ValueError):
        lookup_host("https://example.com/path")
    with pytest.raises(ValueError):
        ping_host("example.com/path")


def test_tcp_port_validation_is_strict():
    with pytest.raises(ValueError):
        probe_tcp_port("localhost", 0)
    with pytest.raises(ValueError):
        probe_tcp_port("localhost", True)
    with pytest.raises(ValueError):
        probe_tcp_port("localhost", 65536)


def test_local_network_snapshot_has_stable_shape():
    result = local_network_info()
    assert isinstance(result["hostname"], str) and result["hostname"]
    assert isinstance(result["addresses"], list)
