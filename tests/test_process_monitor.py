# -*- coding: utf-8 -*-
"""Regression tests for local process monitoring."""

from chocobot.engine.system import process_monitor


def test_normalize_process_sanitizes_values():
    result = process_monitor._normalize_process(" demo ", "42", "1024")
    assert result == {"name": "demo", "pid": 42, "memory_bytes": 1024}


def test_list_processes_sorts_and_limits(monkeypatch):
    monkeypatch.setattr(
        process_monitor,
        "_read_proc_processes",
        lambda: [
            {"name": "small", "pid": 1, "memory_bytes": 10},
            {"name": "large", "pid": 2, "memory_bytes": 20},
        ],
    )
    monkeypatch.setattr(process_monitor.os, "name", "posix")

    result = process_monitor.list_processes(limit=1)

    assert result == [{"name": "large", "pid": 2, "memory_bytes": 20}]


def test_list_processes_ignores_invalid_limit(monkeypatch):
    monkeypatch.setattr(
        process_monitor,
        "_read_proc_processes",
        lambda: [{"name": "demo", "pid": 1, "memory_bytes": 0}],
    )
    monkeypatch.setattr(process_monitor.os, "name", "posix")

    assert process_monitor.list_processes(limit="bad")
    assert process_monitor.list_processes(limit=True)


def test_snapshot_has_stable_shape(monkeypatch):
    monkeypatch.setattr(
        process_monitor,
        "list_processes",
        lambda limit=None: [{"name": "demo", "pid": 1, "memory_bytes": 0}],
    )

    result = process_monitor.get_process_snapshot(limit=5)

    assert result["count"] == 1
    assert result["available"] is True
    assert result["processes"][0]["pid"] == 1
    assert result["platform"]
