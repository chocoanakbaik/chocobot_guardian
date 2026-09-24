# -*- coding: utf-8 -*-
"""Lightweight local process observation with safe fallbacks.

The module is intentionally read-only and uses only the Python standard library.
"""

from __future__ import annotations

import csv
import io
import os
import re
import subprocess
from typing import Any, Dict, List, Optional


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _parse_tasklist_memory(value: Any) -> int:
    """Convert localized tasklist memory text into bytes safely.

    Windows tasklist may emit values such as ``12,345 K``, ``12.345 KB``
    or values with non-breaking spaces depending on the system locale.
    The parser keeps only the numeric portion and treats the value as KiB,
    matching the documented tasklist CSV output.
    """
    text = str(value or "").replace("\u00a0", " ").strip().upper()
    if not text:
        return 0

    numeric = re.sub(r"[^0-9]", "", text)
    if not numeric:
        return 0
    return max(0, _as_int(numeric) * 1024)


def _normalize_process(name: Any, pid: Any, memory_bytes: Any = 0) -> Dict[str, Any]:
    return {
        "name": str(name or "").strip() or "unknown",
        "pid": _as_int(pid),
        "memory_bytes": max(0, _as_int(memory_bytes)),
    }


def _read_windows_processes() -> Optional[List[Dict[str, Any]]]:
    """Read process data through tasklist CSV without shell execution."""
    try:
        completed = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            encoding="mbcs",
            errors="replace",
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if completed.returncode != 0 or not completed.stdout:
        return None

    processes: List[Dict[str, Any]] = []
    for row in csv.reader(io.StringIO(completed.stdout)):
        if len(row) < 5:
            continue
        processes.append(
            _normalize_process(
                row[0],
                row[1],
                _parse_tasklist_memory(row[4]),
            )
        )
    return processes


def _read_proc_processes() -> Optional[List[Dict[str, Any]]]:
    """Best-effort Linux-like fallback for development and testing."""
    proc_root = "/proc"
    if not os.path.isdir(proc_root):
        return None

    processes: List[Dict[str, Any]] = []
    for entry in os.listdir(proc_root):
        if not entry.isdigit():
            continue
        pid = _as_int(entry)
        name = "unknown"
        try:
            with open(os.path.join(proc_root, entry, "comm"), "r", encoding="utf-8") as handle:
                name = handle.readline().strip() or name
        except (OSError, UnicodeError):
            pass
        processes.append(_normalize_process(name, pid))
    return processes


def list_processes(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Return a normalized list of local processes, sorted by memory usage."""
    processes = _read_windows_processes() if os.name == "nt" else None
    if processes is None:
        processes = _read_proc_processes() or []
    processes.sort(key=lambda item: (item["memory_bytes"], item["pid"]), reverse=True)
    if isinstance(limit, bool) or (limit is not None and not isinstance(limit, int)):
        limit = None
    if limit is not None and limit > 0:
        return processes[:limit]
    return processes


def get_process_snapshot(limit: Optional[int] = 25) -> Dict[str, Any]:
    """Return a stable snapshot payload suitable for logging or UI consumption."""
    processes = list_processes(limit=limit)
    return {
        "processes": processes,
        "count": len(processes),
        "available": bool(processes),
        "platform": os.name,
    }
