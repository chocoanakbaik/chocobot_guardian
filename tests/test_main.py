# -*- coding: utf-8 -*-
"""Regression tests for startup profile logging."""

import main


def test_log_device_profile_uses_discovery_field_names(monkeypatch):
    logs = []
    monkeypatch.setattr(main, "_append_log", logs.append)

    main._log_device_profile(
        {
            "profile_version": 1,
            "device": {
                "os": "Windows",
                "os_version": "10.0",
                "architecture": "AMD64",
                "cpu": "Test CPU",
                "memory_gib": 7.5,
            },
            "permissions": {"is_windows_admin": True},
            "capabilities": {"python_runtime": True},
            "recommendations": ["Prefer lightweight background processing and conservative polling."],
        }
    )

    output = "".join(logs)
    assert "RAM: 7.5 GiB" in output
    assert "Admin: True" in output
    assert "RAM: - GB" not in output
    assert "Admin: False" not in output


def test_log_device_profile_handles_malformed_sections(monkeypatch):
    logs = []
    monkeypatch.setattr(main, "_append_log", logs.append)

    main._log_device_profile(
        {
            "device": [],
            "permissions": "invalid",
            "capabilities": None,
            "recommendations": "invalid",
        }
    )

    output = "".join(logs)
    assert "RAM: - GiB" in output
    assert "Admin: unknown" in output
    assert "Recommendations: []" in output
