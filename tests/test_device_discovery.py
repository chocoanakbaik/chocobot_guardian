# -*- coding: utf-8 -*-
"""Regression tests for the local device discovery layer."""

from chocobot.engine.system import device_discovery


class TestDeviceDiscovery:
    def test_discover_device_returns_stable_top_level_profile(self, monkeypatch):
        system_info = {
            "os": {
                "name": "Windows",
                "release": "10",
                "version": "10.0.19045",
                "architecture": "AMD64",
                "hostname": "TEST-PC",
            },
            "runtime": {
                "version": "3.11.0",
                "implementation": "CPython",
            },
            "cpu": {
                "name": "Test CPU",
                "logical_processors": 4,
            },
            "memory": {
                "total_gib": 4.0,
            },
            "gpu": {"available": False},
            "storage": {"free_gib": 50.0},
        }

        monkeypatch.setattr(device_discovery, "get_system_info", lambda: system_info)
        monkeypatch.setattr(
            device_discovery,
            "_get_permission_profile",
            lambda: {
                "current_directory_readable": True,
                "current_directory_writable": True,
                "is_windows_admin": False,
            },
        )
        monkeypatch.setattr(device_discovery, "_get_windows_build", lambda: "19045")
        monkeypatch.setattr(device_discovery, "_get_process_architecture", lambda: "64-bit")

        profile = device_discovery.discover_device()

        assert profile["profile_version"] == device_discovery.PROFILE_VERSION
        assert profile["device"]["hostname"] == "TEST-PC"
        assert profile["device"]["memory_gib"] == 4.0
        assert profile["device"]["memory_tier"] == "low"
        assert profile["device"]["windows_build"] == "19045"
        assert profile["capabilities"]["python_runtime"] is True
        assert profile["capabilities"]["writable_working_directory"] is True
        assert profile["recommendations"]

    def test_discover_device_survives_malformed_system_info(self, monkeypatch):
        monkeypatch.setattr(device_discovery, "get_system_info", lambda: {
            "os": "malformed",
            "cpu": None,
            "memory": {"total_gib": "not-a-number"},
            "runtime": [],
            "gpu": "malformed",
            "storage": None,
        })
        monkeypatch.setattr(
            device_discovery,
            "_get_permission_profile",
            lambda: {
                "current_directory_readable": False,
                "current_directory_writable": False,
                "is_windows_admin": None,
            },
        )

        profile = device_discovery.discover_device()

        assert isinstance(profile, dict)
        assert profile["device"]["memory_gib"] == 0.0
        assert profile["device"]["memory_tier"] == "unknown"
        assert profile["device"]["logical_processors"] == 0
        assert profile["capabilities"]["python_runtime"] is False
        assert profile["capabilities"]["writable_working_directory"] is False
        assert profile["recommendations"]

    def test_get_compatibility_profile_is_public_alias(self, monkeypatch):
        expected = {"profile_version": 1}
        monkeypatch.setattr(device_discovery, "discover_device", lambda: expected)

        assert device_discovery.get_compatibility_profile() is expected
