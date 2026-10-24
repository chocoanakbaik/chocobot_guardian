"""Small, bounded network diagnostics using operating-system facilities only."""
from __future__ import annotations

import ipaddress
import os
import socket
import subprocess


def _clean_host(host: str) -> str:
    if not isinstance(host, str):
        raise ValueError("Host harus berupa nama domain atau alamat IP.")
    value = host.strip().rstrip(".")
    if not value or len(value) > 253 or any(ch.isspace() for ch in value):
        raise ValueError("Nama host kosong, terlalu panjang, atau mengandung spasi.")
    if "://" in value or "/" in value or "@" in value:
        raise ValueError("Masukkan host saja, tanpa skema URL, path, atau kredensial.")
    return value


def lookup_host(host: str) -> dict:
    """Resolve a host through the system resolver. No HTTP request is made."""
    value = _clean_host(host)
    try:
        addresses = sorted({result[4][0] for result in socket.getaddrinfo(value, None, type=socket.SOCK_STREAM)})
    except socket.gaierror as exc:
        return {"ok": False, "host": value, "addresses": [], "error": f"Resolusi DNS gagal: {exc}"}
    return {"ok": bool(addresses), "host": value, "addresses": addresses, "error": None if addresses else "Tidak ada alamat ditemukan."}


def local_network_info() -> dict:
    """Return host name and IP addresses reported by the local resolver."""
    hostname = socket.gethostname()
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)})
    except socket.gaierror:
        addresses = []
    return {"hostname": hostname, "addresses": addresses}


def probe_tcp_port(host: str, port: int, timeout_seconds: float = 2.0) -> dict:
    """Attempt one TCP connection and report only whether it connected."""
    value = _clean_host(host)
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("Port harus berupa bilangan bulat 1–65535.")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not 0.1 <= timeout_seconds <= 5:
        raise ValueError("Timeout harus berada pada rentang 0,1–5 detik.")
    try:
        with socket.create_connection((value, port), timeout=float(timeout_seconds)):
            return {"ok": True, "host": value, "port": port, "message": "Koneksi TCP berhasil dibuka."}
    except (OSError, socket.timeout) as exc:
        return {"ok": False, "host": value, "port": port, "message": f"Koneksi TCP gagal atau ditolak: {exc}"}


def ping_host(host: str, timeout_seconds: float = 3.0) -> dict:
    """Send at most one ICMP echo via the platform ping utility."""
    value = _clean_host(host)
    try:
        ipaddress.ip_address(value)
    except ValueError:
        if not all(part and all(ch.isalnum() or ch == "-" for ch in part) for part in value.split(".")):
            raise ValueError("Nama host berisi karakter yang tidak didukung.")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not 0.5 <= timeout_seconds <= 5:
        raise ValueError("Timeout harus berada pada rentang 0,5–5 detik.")
    if os.name == "nt":
        command = ["ping", "-n", "1", "-w", str(int(timeout_seconds * 1000)), value]
    else:
        command = ["ping", "-c", "1", "-W", str(max(1, int(timeout_seconds))), value]
    try:
        result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=float(timeout_seconds) + 1, check=False)
        output = (result.stdout + "\n" + result.stderr).strip()
        return {"ok": result.returncode == 0, "host": value, "returncode": result.returncode, "output": output[-6000:]}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "host": value, "returncode": None, "output": f"Ping tidak dapat dijalankan: {exc}"}


__all__ = ["lookup_host", "local_network_info", "probe_tcp_port", "ping_host"]
