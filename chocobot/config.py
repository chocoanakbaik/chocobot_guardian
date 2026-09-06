# -*- coding: utf-8 -*-
"""
config.py — Pengelola Konfigurasi Aplikasi Chocobot Guardian.

Modul ini bertanggung jawab untuk:
- Menyediakan konfigurasi bawaan (default).
- Membaca konfigurasi dari file JSON.
- Menyimpan perubahan konfigurasi ke file JSON.
- Menyediakan akses mudah ke nilai konfigurasi bagi modul lain.

Format penyimpanan menggunakan JSON agar mudah dibaca, diedit manual
jika diperlukan, dan tidak membutuhkan pustaka tambahan.

Cara penggunaan umum:

    from chocobot import config

    cfg = config.load_config()
    bahasa = cfg.get("language", "id")
"""

import json
from pathlib import Path
from typing import Any, Dict

from chocobot import constants as const

# ---------------------------------------------------------------------------
# KONFIGURASI BAWAAN
# ---------------------------------------------------------------------------
# Nilai-nilai ini dipakai saat file config.json belum ada atau rusak.

DEFAULT_CONFIG: Dict[str, Any] = {
    "language": const.DEFAULT_LANGUAGE,        # Bahasa aktif (id, en, ar, ...)
    "theme": "dark",                           # Tema tampilan (dark/light)
    "check_updates": False,                    # Cek pembaruan (offline default)
    "scan_auto_quarantine": False,             # Karantina otomatis (default mati)
    "monitor_refresh_ms": const.MONITOR_REFRESH_MS,  # Interval monitor
    "show_splash": True,                       # Tampilkan splash saat mulai
    "window_width": const.WINDOW_WIDTH,        # Lebar jendela utama
    "window_height": const.WINDOW_HEIGHT,      # Tinggi jendela utama
    "max_scan_file_size": const.MAX_SCAN_FILE_SIZE,  # Batas ukuran scan
    "log_enabled": True,                       # Aktifkan pencatatan log
    "last_version": "",                        # Versi terakhir yang dijalankan
}

# ---------------------------------------------------------------------------
# FUNGSI UTAMA
# ---------------------------------------------------------------------------

def _ensure_data_dir() -> None:
    """
    Memastikan folder data dan subfolder penting tersedia.
    Dipanggil sebelum membaca atau menulis konfigurasi.
    """
    const.DATA_DIR.mkdir(parents=True, exist_ok=True)
    const.LOG_DIR.mkdir(parents=True, exist_ok=True)
    const.QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    const.WHITELIST_DIR.mkdir(parents=True, exist_ok=True)
    const.LANGUAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Memuat konfigurasi dari file JSON.

    Jika file tidak ada, akan dibuat otomatis dengan nilai bawaan.
    Jika file ada tetapi tidak valid, nilai bawaan akan digunakan
    dan file baru akan ditulis ulang.

    Returns:
        dict: Konfigurasi yang siap digunakan.
    """
    _ensure_data_dir()

    config = DEFAULT_CONFIG.copy()

    if const.CONFIG_FILE.exists():
        try:
            with open(const.CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                # Gabungkan nilai bawaan dengan nilai dari file.
                # Nilai dari file akan menimpa bawaan bila tersedia.
                config.update(data)
        except (json.JSONDecodeError, OSError):
            # File rusak atau tidak bisa dibaca. Gunakan default.
            pass

    # Pastikan bahasa yang dipilih termasuk bahasa yang didukung.
    if config.get("language") not in const.SUPPORTED_LANGUAGES:
        config["language"] = const.DEFAULT_LANGUAGE

    return config


def save_config(config: Dict[str, Any]) -> bool:
    """
    Menyimpan konfigurasi ke file JSON.

    Args:
        config: Dictionary konfigurasi yang akan disimpan.

    Returns:
        bool: True jika berhasil, False jika terjadi kesalahan.
    """
    _ensure_data_dir()

    try:
        with open(const.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False


def get_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Mengambil nilai konfigurasi dengan aman.

    Args:
        config: Dictionary konfigurasi aktif.
        key: Nama kunci yang ingin diambil.
        default: Nilai cadangan jika kunci tidak ditemukan.

    Returns:
        Nilai konfigurasi atau default.
    """
    return config.get(key, default)


def set_value(config: Dict[str, Any], key: str, value: Any) -> None:
    """
    Mengubah nilai konfigurasi pada dictionary.

    Args:
        config: Dictionary konfigurasi aktif.
        key: Nama kunci yang diubah.
        value: Nilai baru.
    """
    config[key] = value


def reset_config() -> Dict[str, Any]:
    """
    Mengembalikan konfigurasi ke nilai bawaan.

    Returns:
        dict: Salinan konfigurasi bawaan.
    """
    return DEFAULT_CONFIG.copy()