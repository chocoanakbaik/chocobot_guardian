# -*- coding: utf-8 -*-
"""Regression tests for the lightweight local resource monitor."""

from types import SimpleNamespace

from chocobot.engine.system import resource_monitor


def test_calculate_cpu_percent_normal_delta():
    before = (100, 1000)
    after = (250, 2000)

    assert resource_monitor._calculate_cpu_percent(before, after) == 85.0


def test_calculate_cpu_percent_rejects_invalid_delta():
    assert resource_monitor._calculate_cpu_percent((100, 1000), (50, 1000)) is None
    assert resource_monitor._calculate_cpu_percent((100, 1000), (1000, 100)) is None
    assert resource_monitor._calculate_cpu_percent(None, (100, 200)) is None


def test_get_cpu_usage_percent_handles_invalid_interval(monkeypatch):
    monkeypatch.setattr(
        resource_monitor,
        "_read_cpu_times",
        lambda: (100, 1000),
    )

    assert resource_monitor.get_cpu_usage_percent(0) is None
    assert resource_monitor.get_cpu_usage_percent(-1) is None
    assert resource_monitor.get_cpu_usage_percent("invalid") is None
    assert resource_monitor.get_cpu_usage_percent(6) is None


def test_get_cpu_usage_percent_uses_two_samples(monkeypatch):
    samples = iter([(100, 1000), (150, 1100)])

    monkeypatch.setattr(resource_monitor, "_read_cpu_times", lambda: next(samples))
    monkeypatch.setattr(resource_monitor.time, "sleep", lambda _: None)

    assert resource_monitor.get_cpu_usage_percent(0.1) == 50.0


def test_get_memory_usage_safe_fallback(monkeypatch):
    monkeypatch.setattr(resource_monitor, "_get_windows_memory", lambda: None)
    monkeypatch.setattr(resource_monitor, "_get_proc_memory", lambda: None)

    result = resource_monitor.get_memory_usage()

    assert result == {
        "total_bytes": 0,
        "available_bytes": 0,
        "used_bytes": 0,
        "percent": None,
        "available": False,
    }


def test_get_storage_usage_normalizes_usage(monkeypatch):
    monkeypatch.setattr(
        resource_monitor.shutil,
        "disk_usage",
        lambda _: SimpleNamespace(total=1000, used=700, free=300),
    )

    result = resource_monitor.get_storage_usage("C:/")

    assert result["total_bytes"] == 1000
    assert result["free_bytes"] == 300
    assert result["used_bytes"] == 700
    assert result["percent"] == 70.0
    assert result["available"] is True


def test_get_storage_usage_handles_unavailable_storage(monkeypatch):
    def raise_error(_):
        raise OSError("unavailable")

    monkeypatch.setattr(resource_monitor.shutil, "disk_usage", raise_error)

    result = resource_monitor.get_storage_usage("missing-path")

    assert result["total_bytes"] == 0
    assert result["free_bytes"] == 0
    assert result["used_bytes"] == 0
    assert result["percent"] is None
    assert result["available"] is False


def test_get_resource_snapshot_combines_observations(monkeypatch):
    monkeypatch.setattr(resource_monitor, "get_cpu_usage_percent", lambda _: 22.5)
    monkeypatch.setattr(
        resource_monitor,
        "get_memory_usage",
        lambda: {
            "total_bytes": 8_000,
            "available_bytes": 2_000,
            "used_bytes": 6_000,
            "percent": 75.0,
            "available": True,
        },
    )
    monkeypatch.setattr(
        resource_monitor,
        "get_storage_usage",
        lambda _: {
            "path": "C:/",
            "total_bytes": 10_000,
            "free_bytes": 4_000,
            "used_bytes": 6_000,
            "percent": 60.0,
            "available": True,
        },
    )
    monkeypatch.setattr(resource_monitor.os, "cpu_count", lambda: 4)

    result = resource_monitor.get_resource_snapshot(
        cpu_interval_seconds=0.1,
        storage_path="C:/",
    )

    assert result["cpu"]["usage_percent"] == 22.5
    assert result["cpu"]["logical_processors"] == 4
    assert result["cpu"]["available"] is True
    assert result["memory"]["percent"] == 75.0
    assert result["storage"]["percent"] == 60.0
    assert result["platform"]
    assert result["timestamp"]
