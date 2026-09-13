# -*- coding: utf-8 -*-
"""
device_discovery.py - Local device discovery and compatibility profiling.

This module builds a deterministic, read-only snapshot of the environment in
which Chocobot Guardian is running. It does not install, enable, disable, or
modify system components.

The discovery layer deliberately reuses the existing system-information
engine instead of duplicating hardware probes. Its responsibility is to turn
those observations into a compatibility-oriented profile that future CG
component-selection logic can consume.
"""

from __future__ import annotations

import ctypes
import os
import platform
import struct
from typing import Any, Dict, List

from .sysinfo import get_system_info


PROFILE_VERSION = 1
UNKNOWN = "-"


def _safe_text(value: Any, default: str = UNKNOWN) -> str:
    """Return a non-empty string without allowing discovery to fail."""
    if value is None:
        return default
    try:
        text = str(value).strip()
    except Exception:
        return default
    return text or default


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convert numeric observations defensively, preserving best-effort discovery."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if number >= 0 else default


def _safe_int(value: Any, default: int = 0) -> int:
    """Convert integer observations defensively."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number >= 0 else default


def _get_windows_build() -> str:
    """Return the Windows build number when Python exposes it."""
    if os.name != "nt":
        return UNKNOWN

    try:
        _, _, build, _ = platform.win32_ver()
        return _safe_text(build)
    except Exception:
        return UNKNOWN


def _get_process_architecture() -> str:
    """Return the architecture of the current Python process."""
    try:
        return "64-bit" if struct.calcsize("P") * 8 == 64 else "32-bit"
    except Exception:
        return UNKNOWN


def _is_windows_admin() -> bool | None:
    """Best-effort Windows administrator detection without changing the system."""
    if os.name != "nt":
        return None

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError, TypeError):
        return None
    except Exception:
        return None


def _get_permission_profile() -> Dict[str, Any]:
    """Describe useful local permissions without requesting elevation."""
    try:
        cwd = os.getcwd()
    except (OSError, FileNotFoundError):
        cwd = None

    if not cwd:
        readable = False
        writable = False
    else:
        try:
            readable = bool(os.access(cwd, os.R_OK))
            writable = bool(os.access(cwd, os.W_OK))
        except (OSError, TypeError):
            readable = False
            writable = False

    return {
        "current_directory_readable": readable,
        "current_directory_writable": writable,
        "is_windows_admin": _is_windows_admin(),
    }


def _memory_tier(total_gib: float) -> str:
    """Classify memory capacity for future lightweight component selection."""
    if total_gib <= 0:
        return "unknown"
    if total_gib < 4:
        return "very_low"
    if total_gib < 8:
        return "low"
    if total_gib < 16:
        return "standard"
    return "high"


def _build_capabilities(system_info: Dict[str, Any], permissions: Dict[str, Any]) -> Dict[str, bool]:
    """Derive conservative capabilities from already-detected facts."""
    memory = system_info.get("memory", {})
    storage = system_info.get("storage", {})
    runtime = system_info.get("runtime", {})
    gpu = system_info.get("gpu", {})

    total_memory = _safe_float(memory.get("total_gib"))
    free_storage = _safe_float(storage.get("free_gib"))
    runtime_available = runtime.get("version", UNKNOWN) != UNKNOWN
    gpu_available = bool(gpu.get("available", False))

    return {
        "python_runtime": runtime_available,
        "local_storage_available": free_storage > 0,
        "gpu_information_available": gpu_available,
        "writable_working_directory": bool(permissions.get("current_directory_writable", False)),
        "lightweight_mode_recommended": 0 < total_memory < 8,
    }


def _build_recommendations(system_info: Dict[str, Any], capabilities: Dict[str, bool]) -> List[str]:
    """Return deterministic, non-invasive recommendations for future selection."""
    recommendations: List[str] = []
    memory = system_info.get("memory", {})
    total_memory = _safe_float(memory.get("total_gib"))

    if 0 < total_memory < 4:
        recommendations.append("Use the most lightweight compatible component variants.")
    elif 0 < total_memory < 8:
        recommendations.append("Prefer lightweight background processing and conservative polling.")

    if not capabilities.get("writable_working_directory", False):
        recommendations.append("Avoid workflows that require writing to the current directory.")

    if not capabilities.get("python_runtime", False):
        recommendations.append("Runtime information is incomplete; avoid automatic component decisions.")

    if not recommendations:
        recommendations.append("No immediate compatibility restriction detected by the discovery layer.")

    return recommendations


def discover_device() -> Dict[str, Any]:
    """
    Build the current local device compatibility profile.

    The function is read-only. It may inspect the local environment, but it
    does not install packages, request administrator elevation, edit files, or
    change operating-system settings.
    """
    try:
        system_info = get_system_info()
    except Exception:
        system_info = {}

    if not isinstance(system_info, dict):
        system_info = {}

    permissions = _get_permission_profile()

    os_info = system_info.get("os", {})
    cpu_info = system_info.get("cpu", {})
    memory_info = system_info.get("memory", {})
    runtime_info = system_info.get("runtime", {})

    if not isinstance(os_info, dict):
        os_info = {}
    if not isinstance(cpu_info, dict):
        cpu_info = {}
    if not isinstance(memory_info, dict):
        memory_info = {}
    if not isinstance(runtime_info, dict):
        runtime_info = {}

    architecture = _safe_text(os_info.get("architecture"))
    process_architecture = _get_process_architecture()
    total_memory = _safe_float(memory_info.get("total_gib"))

    capabilities = _build_capabilities(system_info, permissions)
    recommendations = _build_recommendations(system_info, capabilities)

    return {
        "profile_version": PROFILE_VERSION,
        "device": {
            "hostname": _safe_text(os_info.get("hostname")),
            "os": _safe_text(os_info.get("name")),
            "os_release": _safe_text(os_info.get("release")),
            "os_version": _safe_text(os_info.get("version")),
            "windows_build": _get_windows_build(),
            "architecture": architecture,
            "process_architecture": process_architecture,
            "cpu": _safe_text(cpu_info.get("name")),
            "logical_processors": _safe_int(cpu_info.get("logical_processors")),
            "memory_gib": total_memory,
            "memory_tier": _memory_tier(total_memory),
            "python_version": _safe_text(runtime_info.get("version")),
            "python_implementation": _safe_text(runtime_info.get("implementation")),
        },
        "permissions": permissions,
        "capabilities": capabilities,
        "recommendations": recommendations,
        "system_info": system_info,
    }


def get_compatibility_profile() -> Dict[str, Any]:
    """Public alias for callers that need the compatibility profile."""
    return discover_device()


if __name__ == "__main__":
    import json

    print(json.dumps(discover_device(), indent=2, ensure_ascii=False))
