# -*- coding: utf-8 -*-
"""
main.py — Gerbang Masuk Utama Chocobot Guardian.

File ini adalah titik awal saat aplikasi dijalankan. Tugasnya:
- Memastikan folder dasar dan konfigurasi tersedia.
- Menampilkan splash screen ChocoEngine.
- Menjalankan aplikasi utama.
- Menangani error yang mungkin terjadi agar aplikasi tidak langsung mati
  tanpa pesan yang jelas.

Cara menjalankan:
    python main.py
"""

import sys
import traceback
from datetime import datetime

# Pastikan root proyek dapat ditemukan oleh Python.
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from chocobot import constants as const   # noqa: E402
from chocobot import config               # noqa: E402


def _log_startup() -> None:
    """
    Mencatat waktu mulai aplikasi ke folder log.
    Berguna untuk penelusuran masalah di kemudian hari.
    """
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


def _run_app() -> None:
    """
    Menjalankan jendela utama aplikasi.
    Fungsi ini diimpor dari app.py setelah splash screen selesai.
    """
    from chocobot.app import ChocobotApp

    app = ChocobotApp()
    app.run()


def main() -> None:
    """
    Titik masuk utama.
    Memanggil splash screen terlebih dahulu, lalu aplikasi utama.
    """
    _log_startup()

    # Muat konfigurasi awal
    cfg = config.load_config()

    # Tampilkan splash screen jika diaktifkan
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

    # Jalankan aplikasi utama
    _run_app()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
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