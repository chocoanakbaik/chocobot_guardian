# -*- coding: utf-8 -*-
"""
logger.py — Pencatat Aktivitas & Error Chocobot Guardian.

Modul ini menyediakan sistem logging lokal sederhana namun andal.
Seluruh pesan dicatat ke dalam file teks di folder data/logs/ tanpa
membutuhkan koneksi internet.

Fitur:
- Log dengan level INFO, WARNING, ERROR, DEBUG.
- Format waktu yang konsisten.
- Nama modul asal pesan dapat disertakan.
- Aman dipanggil dari modul mana pun.
- Tidak menghentikan aplikasi jika penulisan log gagal.

Cara penggunaan umum:

    from chocobot.engine.utils import logger

    logger.info("Aplikasi berjalan normal.", source="main")
    logger.warning("Terdapat indikasi risiko.", source="link_inspector")
    logger.error("Gagal membuka file.", source="file_analyzer")
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from chocobot import constants as const

# ---------------------------------------------------------------------------
# KONFIGURASI LOG
# ---------------------------------------------------------------------------

LOG_FILE = const.LOG_DIR / const.LOG_FILE_NAME

# Level yang diizinkan
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


# ---------------------------------------------------------------------------
# FUNGSI UTAMA
# ---------------------------------------------------------------------------

def _write(level: str, message: str, source: Optional[str] = None) -> None:
    """
    Menulis satu baris log ke file.

    Args:
        level: Jenis pesan (DEBUG, INFO, WARNING, ERROR).
        message: Isi pesan yang akan dicatat.
        source: Nama modul atau fungsi asal pesan. Boleh kosong.
    """
    if level not in LOG_LEVELS:
        level = "INFO"

    # Pastikan folder log tersedia
    try:
        const.LOG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        # Jika folder tidak bisa dibuat, log tidak dapat disimpan.
        return

    timestamp = datetime.now().strftime(const.LOG_TIME_FORMAT)
    source_text = f"[{source}] " if source else ""

    line = f"[{timestamp}] [{level}] {source_text}{message}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        # Kegagalan menulis log tidak boleh mengganggu aplikasi.
        pass


def debug(message: str, source: Optional[str] = None) -> None:
    """
    Mencatat pesan debug untuk keperluan pengembangan.
    """
    _write("DEBUG", message, source)


def info(message: str, source: Optional[str] = None) -> None:
    """
    Mencatat informasi umum.
    """
    _write("INFO", message, source)


def warning(message: str, source: Optional[str] = None) -> None:
    """
    Mencatat peringatan yang perlu diperhatikan.
    """
    _write("WARNING", message, source)


def error(message: str, source: Optional[str] = None) -> None:
    """
    Mencatat pesan kesalahan.
    """
    _write("ERROR", message, source)


def read_log(max_lines: int = 100) -> str:
    """
    Membaca isi file log dari baris terakhir.

    Args:
        max_lines: Jumlah baris terakhir yang ingin dibaca.

    Returns:
        String berisi potongan log terakhir, atau pesan kosong
        jika file tidak tersedia.
    """
    if not LOG_FILE.exists():
        return ""

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[-max_lines:])
    except OSError:
        return ""


def clear_log() -> bool:
    """
    Menghapus isi file log.

    Returns:
        True jika berhasil, False jika gagal.
    """
    try:
        const.LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
        return True
    except OSError:
        return False