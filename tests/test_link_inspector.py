"""Tests for offline URL inspection heuristics."""
from chocobot.engine.link.inspector import inspect_url


def test_normal_https_url_is_valid_without_automatic_risk_label():
    result = inspect_url("https://example.com/path")
    assert result["valid"] is True
    assert result["host"] == "example.com"
    assert result["https"] is True
    assert result["score"] == 0
    assert result["indicators"] == []
    assert "not a malware" in result["notice"] or "bukan hasil" in result["notice"]


def test_userinfo_ip_host_http_and_port_are_explained():
    result = inspect_url("http://user:pass@192.0.2.1:8080/login/account")
    assert result["valid"] is True
    codes = {item["code"] for item in result["indicators"]}
    assert {"ip-host", "userinfo", "nonstandard-port", "no-https", "credential-words"} <= codes
    assert result["score"] <= 100
    assert result["level"] in {"Sedang", "Tinggi", "Sangat tinggi"}


def test_empty_and_non_http_urls_are_rejected():
    assert inspect_url("")["valid"] is False
    assert inspect_url("ftp://example.com")["valid"] is False
    assert inspect_url("https:///missing-host")["valid"] is False


def test_unicode_lookalike_domain_uses_punycode_indicator():
    result = inspect_url("https://xn--pple-43d.com/")
    assert result["valid"] is True
    assert "punycode" in {item["code"] for item in result["indicators"]}
