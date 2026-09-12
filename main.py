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


def _log_startup() -> None:
    """Mencatat waktu mulai aplikasi ke folder log."""
    try:
        const.LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = const.LOG_DIR / const.LOG_FILE_NAME
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(
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
    except OSError:
        # Kegagalan menulis log tidak boleh menghentikan aplikasi.
        pass


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
        return profile if isinstance(profile, dict) else {}
    except Exception:
        return {}


def _log_device_profile(profile: dict) -> None:
    """Mencatat ringkasan profile perangkat tanpa menghentikan aplikasi."""
    if not profile:
        return

    try:
        const.LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = const.LOG_DIR / const.LOG_FILE_NAME
        device = profile.get("device", {})
        permissions = profile.get("permissions", {})
        capabilities = profile.get("capabilities", {})
        recommendations = profile.get("recommendations", [])

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(
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
                "=" * 60
                + "\n"
            )
    except (OSError, AttributeError, TypeError):
        # Kegagalan logging tidak boleh menghentikan startup.
        pass


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
        try:
            const.LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = const.LOG_DIR / const.LOG_FILE_NAME
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(
                    f"[{datetime.now().strftime(const.LOG_TIME_FORMAT)}] "
                    f"ERROR TAK TERDUGA:\n"
                    f"{traceback.format_exc()}\n"
                )
        except OSError:
            pass

        print("Terjadi kesalahan tak terduga saat menjalankan Chocobot.")
        print("Detail error telah dicatat di folder log.")
        sys.exit(1)
