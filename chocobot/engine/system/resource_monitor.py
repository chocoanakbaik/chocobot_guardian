# -*- coding: utf-8 -*-
"""
resource_monitor.py - Lightweight local resource monitoring for Chocobot Guardian.

This module provides read-only observations of the current machine's CPU,
memory, and storage state. It intentionally uses the Python standard library
and Windows-native ctypes calls where available so the monitor remains
suitable for low-spec devices and offline operation.

The monitor does not terminate processes, change priorities, modify files,
or alter operating-system settings.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import os
import platform
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


DEFAULT_CPU_SAMPLE_INTERVAL = 0.20


def _safe_non_negative_int(value: Any, default: int = 0) -> int:
    """Convert an observation into a non-negative integer safely."""
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return number if number >= 0 else default


def _safe_percentage(value: Any) -> Optional[float]:
    """Normalize a percentage observation to the inclusive 0..100 range."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if number < 0 or number > 100:
        return None
    return round(number, 2)


def _filetime_to_uint64(filetime: ctypes.wintypes.FILETIME) -> int:
    """Convert a Windows FILETIME structure into a 64-bit integer."""
    high = _safe_non_negative_int(filetime.dwHighDateTime)
    low = _safe_non_negative_int(filetime.dwLowDateTime)
    return (high << 32) | low


def _read_windows_cpu_times() -> Optional[Tuple[int, int]]:
    """Read cumulative Windows idle and total CPU time counters."""
    if os.name != "nt":
        return None

    try:
        idle = ctypes.wintypes.FILETIME()
        kernel = ctypes.wintypes.FILETIME()
        user = ctypes.wintypes.FILETIME()

        if not ctypes.windll.kernel32.GetSystemTimes(
            ctypes.byref(idle),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            return None

        idle_ticks = _filetime_to_uint64(idle)
        kernel_ticks = _filetime_to_uint64(kernel)
        user_ticks = _filetime_to_uint64(user)
        active_ticks = max(0, kernel_ticks + user_ticks - idle_ticks)
        total_ticks = max(0, active_ticks + idle_ticks)
        return idle_ticks, total_ticks
    except (AttributeError, OSError, TypeError, ValueError):
        return None
    except Exception:
        return None


def _read_proc_cpu_times() -> Optional[Tuple[int, int]]:
    """Read cumulative CPU counters from Linux-like /proc environments."""
    try:
        with open("/proc/stat", "r", encoding="utf-8") as handle:
            first_line = handle.readline().strip()
    except (OSError, UnicodeError):
        return None

    if not first_line.startswith("cpu "):
        return None

    parts = first_line.split()
    if len(parts) < 5:
        return None

    try:
        user = int(parts[1])
        nice = int(parts[2])
        system = int(parts[3])
        idle = int(parts[4])
        iowait = int(parts[5]) if len(parts) > 5 else 0
        irq = int(parts[6]) if len(parts) > 6 else 0
        softirq = int(parts[7]) if len(parts) > 7 else 0
        steal = int(parts[8]) if len(parts) > 8 else 0
    except (TypeError, ValueError):
        return None

    idle_ticks = max(0, idle + iowait)
    active_ticks = max(0, user + nice + system + irq + softirq + steal)
    total_ticks = idle_ticks + active_ticks
    return idle_ticks, total_ticks


def _read_cpu_times() -> Optional[Tuple[int, int]]:
    """Return cumulative idle and total CPU counters for the current platform."""
    windows_times = _read_windows_cpu_times()
    if windows_times is not None:
        return windows_times
    return _read_proc_cpu_times()


def _calculate_cpu_percent(
    before: Optional[Tuple[int, int]],
    after: Optional[Tuple[int, int]],
) -> Optional[float]:
    """Calculate CPU utilization from two cumulative counter samples."""
    if before is None or after is None:
        return None

    before_idle, before_total = before
    after_idle, after_total = after
    idle_delta = after_idle - before_idle
    total_delta = after_total - before_total

    if total_delta <= 0 or idle_delta < 0 or idle_delta > total_delta:
        return None

    usage = ((total_delta - idle_delta) / total_delta) * 100.0
    return _safe_percentage(usage)


def get_cpu_usage_percent(interval_seconds: float = DEFAULT_CPU_SAMPLE_INTERVAL) -> Optional[float]:
    """Measure aggregate CPU utilization over a short sampling interval."""
    try:
        interval = float(interval_seconds)
    except (TypeError, ValueError, OverflowError):
        return None

    if interval <= 0 or interval > 5:
        return None

    before = _read_cpu_times()
    if before is None:
        return None

    try:
        time.sleep(interval)
    except (OSError, ValueError):
        return None

    after = _read_cpu_times()
    return _calculate_cpu_percent(before, after)


def _get_windows_memory() -> Optional[Dict[str, int]]:
    """Read physical memory counters from Windows GlobalMemoryStatusEx."""
    if os.name != "nt":
        return None

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.wintypes.DWORD),
            ("dwMemoryLoad", ctypes.wintypes.DWORD),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_longlong),
        ]

    try:
        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None

        total = _safe_non_negative_int(status.ullTotalPhys)
        available = _safe_non_negative_int(status.ullAvailPhys)
        used = max(0, total - available)
        percent = (used / total * 100.0) if total else None

        return {
            "total_bytes": total,
            "available_bytes": available,
            "used_bytes": used,
            "percent": round(percent, 2) if percent is not None else None,
        }
    except (AttributeError, OSError, TypeError, ValueError):
        return None
    except Exception:
        return None


def _get_proc_memory() -> Optional[Dict[str, int]]:
    """Read basic memory counters from Linux-like /proc environments."""
    values: Dict[str, int] = {}
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as handle:
            for line in handle:
                if ":" not in line:
                    continue
                name, raw_value = line.split(":", 1)
                parts = raw_value.strip().split()
                if not parts:
                    continue
                values[name] = int(parts[0]) * 1024
    except (OSError, UnicodeError, ValueError):
        return None

    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", values.get("MemFree", 0))
    if total <= 0:
        return None

    available = min(max(available, 0), total)
    used = total - available
    percent = used / total * 100.0
    return {
        "total_bytes": total,
        "available_bytes": available,
        "used_bytes": used,
        "percent": round(percent, 2),
    }


def get_memory_usage() -> Dict[str, Any]:
    """Return a normalized physical-memory snapshot with safe fallbacks."""
    memory = _get_windows_memory()
    if memory is None:
        memory = _get_proc_memory()
    if memory is None:
        return {
            "total_bytes": 0,
            "available_bytes": 0,
            "used_bytes": 0,
            "percent": None,
            "available": False,
        }

    return {**memory, "available": True}


def get_storage_usage(path: Optional[str] = None) -> Dict[str, Any]:
    """Return usage information for the filesystem containing ``path``."""
    try:
        target = Path(path) if path else Path.cwd()
    except (TypeError, ValueError):
        target = Path.cwd()

    try:
        usage = shutil.disk_usage(str(target))
    except (OSError, ValueError):
        return {
            "path": str(target),
            "total_bytes": 0,
            "free_bytes": 0,
            "used_bytes": 0,
            "percent": None,
            "available": False,
        }

    total = _safe_non_negative_int(usage.total)
    free = min(_safe_non_negative_int(usage.free), total) if total else 0
    used = max(0, total - free)
    percent = (used / total * 100.0) if total else None

    return {
        "path": str(target),
        "total_bytes": total,
        "free_bytes": free,
        "used_bytes": used,
        "percent": round(percent, 2) if percent is not None else None,
        "available": total > 0,
    }


def get_resource_snapshot(
    *,
    cpu_interval_seconds: float = DEFAULT_CPU_SAMPLE_INTERVAL,
    storage_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Return one normalized, read-only snapshot of CPU, memory, and storage."""
    cpu_usage = get_cpu_usage_percent(cpu_interval_seconds)
    memory = get_memory_usage()
    storage = get_storage_usage(storage_path)

    try:
        logical_processors = os.cpu_count() or 0
    except Exception:
        logical_processors = 0

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "platform": platform.system() or "-",
        "cpu": {
            "usage_percent": cpu_usage,
            "logical_processors": max(0, logical_processors),
            "available": cpu_usage is not None,
        },
        "memory": memory,
        "storage": storage,
    }


if __name__ == "__main__":
    import json

    print(
        json.dumps(
            get_resource_snapshot(),
            indent=2,
            ensure_ascii=False,
        )
    )
