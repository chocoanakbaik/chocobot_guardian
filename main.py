# -*- coding: utf-8 -*-
"""
main.py — Gerbang Masuk Utama Chocobot Guardian.

File ini adalah titik awal saat aplikasi dijalankan. Tugasnya:
- Memastikan folder dasar dan konfigurasi tersedia.
- Menemukan kondisi perangkat secara lokal sebelum UI dimulai.
- Menampilkan splash screen Chocobot Guardian.
- Menjalankan aplikasi utama.
- Menangani error yang mungkin terjadi agar aplikasi tidak langsung mati
  tanpa pesan yang jelas.

Cara menjalankan:
    py main.py
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path

# Pastikan root proyek dapat ditemukan oleh Python.
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from chocobot import constants as const   # noqa: E402
from chocobot import config               # noqa: E402


def _append_log(text: str) -> None:
    """Menambahkan satu blok teks ke log lokal secara best-effort."""
    try:
        const.LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = const.LOG_DIR / const.LOG_FILE_NAME
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(text)
    except (OSError, TypeError):
        # Kegagalan logging tidak boleh menghentikan aplikasi.
        pass


def _log_startup() -> None:
    """Mencatat waktu mulai aplikasi ke folder log."""
    _append_log(
        "\n"
        + "=" * 60
        + "\n"
        + f"[{datetime.now().strftime(const.LOG_TIME_FORMAT)}] "
        + "Aplikasi dijalankan.\n"
        + f"Versi: {const.APP_VERSION}\n"
        + f"Status: {const.DEVELOPMENT_STATUS}\n"
        + "=" * 60
        + "\n"
    )


def _discover_device() -> dict:
    """
    Mengambil compatibility profile lokal sebelum splash ditampilkan.

    Discovery bersifat read-only dan best-effort. Jika modul discovery gagal
    dimuat atau mengalami error, aplikasi tetap dapat melanjutkan startup.
    """
    try:
        from chocobot.engine.system.device_discovery import (
            get_compatibility_profile,
        )

        profile = get_compatibility_profile()
        if isinstance(profile, dict):
            return profile

        _append_log(
            "DEVICE DISCOVERY\n"
            "Status: invalid profile type; expected dict.\n"
            + "=" * 60
            + "\n"
        )
        return {}
    except Exception as exc:
        _append_log(
            "DEVICE DISCOVERY\n"
            "Status: unavailable; startup continued in degraded mode.\n"
            f"Reason: {type(exc).__name__}: {exc}\n"
            + "=" * 60
            + "\n"
        )
        return {}


def _log_device_profile(profile: dict) -> None:
    """Mencatat ringkasan profile perangkat tanpa menghentikan aplikasi."""
    if not profile:
        return

    try:
        device = profile.get("device", {})
        permissions = profile.get("permissions", {})
        capabilities = profile.get("capabilities", {})
        recommendations = profile.get("recommendations", [])

        _append_log(
            "DEVICE DISCOVERY\n"
            f"Profile version: {profile.get('profile_version', '-')}\n"
            f"OS: {device.get('os', '-')}\n"
            f"OS version: {device.get('os_version', '-')}\n"
            f"Architecture: {device.get('architecture', '-')}\n"
            f"CPU: {device.get('cpu', '-')}\n"
            f"RAM: {device.get('ram_gb', '-')} GB\n"
            f"Admin: {permissions.get('is_admin', False)}\n"
            f"Capabilities: {capabilities}\n"
            f"Recommendations: {recommendations}\n"
            + "=" * 60
            + "\n"
        )
    except (AttributeError, TypeError):
        # Profile malformed; startup tetap berjalan tanpa memaksa struktur.
        _append_log(
            "DEVICE DISCOVERY\n"
            "Status: malformed profile; profile logging skipped.\n"
            + "=" * 60
            + "\n"
        )


def _run_app() -> None:
    """Menjalankan jendela utama aplikasi."""
    from chocobot.app import ChocobotApp

    app = ChocobotApp()
    app.run()


def main() -> None:
    """Titik masuk utama aplikasi."""
    _log_startup()

    # Observasi perangkat dilakukan sebelum UI dimulai.
    device_profile = _discover_device()
    _log_device_profile(device_profile)

    # Muat konfigurasi awal.
    cfg = config.load_config()

    # Tampilkan splash screen jika diaktifkan.
    if cfg.get("show_splash", True):
        from splash_screen import show_splash

        show_splash(
            duration_ms=const.SPLASH_DURATION_MS,
            logo_path=const.LOGO_PATH,
            bg_color=const.SPLASH_BG_COLOR,
            text_color=const.SPLASH_TEXT_COLOR,
            app_name=const.APP_NAME,
            version=const.APP_VERSION,
        )

    # Jalankan aplikasi utama.
    _run_app()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Jika terjadi error tak terduga, catat ke log dan tampilkan pesan.
        _append_log(
            f"[{datetime.now().strftime(const.LOG_TIME_FORMAT)}] "
            "ERROR TAK TERDUGA:\n"
            f"{traceback.format_exc()}\n"
        )

        print("Terjadi kesalahan tak terduga saat menjalankan Chocobot.")
        print("Detail error telah dicatat di folder log.")
        sys.exit(1)
