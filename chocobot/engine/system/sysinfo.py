# -*- coding: utf-8 -*-
"""
sysinfo.py — System Information Engine Chocobot Guardian.

Modul ini mengumpulkan informasi dasar perangkat secara lokal tanpa
ketergantungan pihak ketiga. Engine ini sengaja hanya melakukan discovery:
modul tidak mengubah konfigurasi, memasang komponen, atau menjalankan
operasi administratif pada sistem.

Informasi yang dikumpulkan meliputi:
- Sistem operasi dan versi/build
- Arsitektur dan informasi Python/runtime
- CPU dan jumlah logical processor
- Memori fisik yang tersedia
- Kapasitas storage pada drive sistem
- Adapter grafis yang dapat ditemukan melalui Windows Registry
- Nama host

Semua pengambilan informasi bersifat best-effort. Jika suatu informasi tidak
tersedia karena perbedaan OS, permission, atau keterbatasan environment,
engine mengembalikan nilai aman dan tetap menyediakan informasi lain.
"""

from __future__ import annotations

import ctypes
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List


UNKNOWN = "-"
BYTES_PER_GIB = 1024 ** 3


def _safe_text(value: Any, default: str = UNKNOWN) -> str:
    """Mengubah nilai menjadi teks yang aman untuk hasil engine."""
    if value is None:
        return default

    try:
        text = str(value).strip()
    except Exception:
        return default

    return text or default


def _bytes_to_gib(value: int) -> float:
    """Mengubah byte menjadi GiB dengan pembulatan konsisten."""
    if value < 0:
        return 0.0
    return round(value / BYTES_PER_GIB, 2)


def get_os_info() -> Dict[str, str]:
    """Mengambil identitas sistem operasi dan versi runtime platform."""
    try:
        uname = platform.uname()
    except Exception:
        uname = None

    try:
        system = _safe_text(platform.system())
        release = _safe_text(platform.release())
        version = _safe_text(platform.version())
        machine = _safe_text(platform.machine())
        node = _safe_text(platform.node())
    except Exception:
        system = release = version = machine = node = UNKNOWN

    if uname is not None:
        system = _safe_text(getattr(uname, "system", system), system)
        release = _safe_text(getattr(uname, "release", release), release)
        version = _safe_text(getattr(uname, "version", version), version)
        machine = _safe_text(getattr(uname, "machine", machine), machine)
        node = _safe_text(getattr(uname, "node", node), node)

    return {
        "name": system,
        "release": release,
        "version": version,
        "architecture": machine,
        "hostname": node,
        "platform": _safe_text(platform.platform()),
    }


def get_runtime_info() -> Dict[str, str]:
    """Mengambil informasi Python/runtime yang sedang menjalankan CG."""
    implementation = UNKNOWN
    python_version = UNKNOWN
    executable = UNKNOWN

    try:
        implementation = _safe_text(platform.python_implementation())
    except Exception:
        pass

    try:
        python_version = _safe_text(platform.python_version())
    except Exception:
        pass

    try:
        executable = _safe_text(Path(sys.executable).resolve())
    except Exception:
        executable = _safe_text(sys.executable)

    return {
        "implementation": implementation,
        "version": python_version,
        "executable": executable,
    }


def get_cpu_info() -> Dict[str, Any]:
    """Mengambil informasi CPU yang tersedia melalui standard library."""
    processor = UNKNOWN
    architecture = UNKNOWN
    logical_processors = 0

    try:
        processor = _safe_text(platform.processor())
    except Exception:
        pass

    try:
        architecture = _safe_text(platform.machine())
    except Exception:
        pass

    try:
        logical_processors = os.cpu_count() or 0
    except Exception:
        logical_processors = 0

    return {
        "name": processor,
        "architecture": architecture,
        "logical_processors": logical_processors,
    }


def _get_windows_memory() -> Dict[str, Any] | None:
    """Mengambil memori fisik Windows menggunakan GlobalMemoryStatusEx."""
    if os.name != "nt":
        return None

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    try:
        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

        result = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
        if not result:
            return None

        return {
            "total_bytes": int(status.ullTotalPhys),
            "available_bytes": int(status.ullAvailPhys),
            "used_percent": int(status.dwMemoryLoad),
        }
    except (AttributeError, OSError, TypeError, ValueError):
        return None
    except Exception:
        return None


def get_memory_info() -> Dict[str, Any]:
    """Mengambil informasi RAM fisik tanpa dependency eksternal."""
    windows_memory = _get_windows_memory()
    if windows_memory is not None:
        total = windows_memory["total_bytes"]
        available = windows_memory["available_bytes"]
        used = max(total - available, 0)

        return {
            "total_bytes": total,
            "available_bytes": available,
            "used_bytes": used,
            "total_gib": _bytes_to_gib(total),
            "available_gib": _bytes_to_gib(available),
            "used_gib": _bytes_to_gib(used),
            "used_percent": windows_memory["used_percent"],
        }

    # Fallback ringan untuk environment non-Windows. Linux biasanya
    # menyediakan /proc/meminfo, sementara environment lain dapat gagal.
    try:
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            values: Dict[str, int] = {}
            for line in meminfo.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) >= 2 and parts[0].rstrip(":") in {
                    "MemTotal",
                    "MemAvailable",
                }:
                    values[parts[0].rstrip(":")] = int(parts[1]) * 1024

            total = values.get("MemTotal", 0)
            available = values.get("MemAvailable", 0)
            if total > 0:
                used = max(total - available, 0)
                return {
                    "total_bytes": total,
                    "available_bytes": available,
                    "used_bytes": used,
                    "total_gib": _bytes_to_gib(total),
                    "available_gib": _bytes_to_gib(available),
                    "used_gib": _bytes_to_gib(used),
                    "used_percent": round((used / total) * 100, 1),
                }
    except (OSError, ValueError, UnicodeError):
        pass

    return {
        "total_bytes": 0,
        "available_bytes": 0,
        "used_bytes": 0,
        "total_gib": 0.0,
        "available_gib": 0.0,
        "used_gib": 0.0,
        "used_percent": 0.0,
    }


def _get_windows_gpus() -> List[str]:
    """Mencoba membaca nama display adapter dari Windows Registry."""
    if os.name != "nt":
        return []

    try:
        import winreg
    except ImportError:
        return []

    root_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
    gpus: List[str] = []

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root_path) as root:
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(root, index)
                except OSError:
                    break

                index += 1
                if not subkey_name[:4].isdigit():
                    continue

                try:
                    with winreg.OpenKey(root, subkey_name) as adapter:
                        value, _ = winreg.QueryValueEx(adapter, "DriverDesc")
                        name = _safe_text(value)
                        if name != UNKNOWN and name not in gpus:
                            gpus.append(name)
                except (OSError, FileNotFoundError):
                    continue
    except (OSError, FileNotFoundError, PermissionError):
        return []

    return gpus


def get_gpu_info() -> Dict[str, Any]:
    """Mengambil nama GPU/display adapter jika tersedia secara lokal."""
    adapters = _get_windows_gpus()
    return {
        "adapters": adapters,
        "count": len(adapters),
        "available": bool(adapters),
    }


def get_storage_info(path: str | os.PathLike[str] | None = None) -> Dict[str, Any]:
    """Mengambil kapasitas, ruang terpakai, dan ruang kosong sebuah volume."""
    target = path

    if target is None:
        if os.name == "nt":
            target = os.environ.get("SystemDrive", "C:") + "\\"
        else:
            target = os.path.abspath(os.sep)

    try:
        usage = shutil.disk_usage(target)
        total = int(usage.total)
        free = int(usage.free)
        used = max(total - free, 0)

        return {
            "path": _safe_text(target),
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "total_gib": _bytes_to_gib(total),
            "used_gib": _bytes_to_gib(used),
            "free_gib": _bytes_to_gib(free),
            "used_percent": round((used / total) * 100, 1) if total else 0.0,
        }
    except (OSError, ValueError, TypeError):
        return {
            "path": _safe_text(target),
            "total_bytes": 0,
            "used_bytes": 0,
            "free_bytes": 0,
            "total_gib": 0.0,
            "used_gib": 0.0,
            "free_gib": 0.0,
            "used_percent": 0.0,
        }


def get_system_info() -> Dict[str, Any]:
    """
    Mengambil snapshot informasi perangkat secara lokal.

    Fungsi ini merupakan entry point utama untuk engine system information.
    Tidak ada operasi yang mengubah sistem.
    """
    return {
        "os": get_os_info(),
        "runtime": get_runtime_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "gpu": get_gpu_info(),
        "storage": get_storage_info(),
    }


def collect_system_info() -> Dict[str, Any]:
    """Alias eksplisit untuk pengambilan snapshot sistem."""
    return get_system_info()


if __name__ == "__main__":
    import json

    print(json.dumps(get_system_info(), indent=2, ensure_ascii=False))
