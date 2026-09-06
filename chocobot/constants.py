# -*- coding: utf-8 -*-
"""
constants.py — Pusat Konstanta Global Chocobot Guardian.

Modul ini berisi seluruh nilai tetap yang digunakan di berbagai bagian
aplikasi. Tujuannya agar perubahan nilai penting cukup dilakukan di satu
tempat, tanpa harus mencari dan mengubah satu per satu di banyak file.

Seluruh modul dalam proyek ini boleh mengimpor konstanta dari sini dengan
cara:

    from chocobot import constants as const

Pastikan tidak mengubah nilai konstanta ini pada saat aplikasi berjalan,
karena dapat menyebabkan ketidakkonsistenan antar modul.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# INFORMASI APLIKASI
# ---------------------------------------------------------------------------

APP_NAME = "Chocobot Guardian"
APP_VERSION = "1.0 Beta"
APP_CODENAME = "Guardian"
APP_TAGLINE = "Local Windows Utility & Security Platform"

APP_DESCRIPTION = (
    "Chocobot Guardian adalah aplikasi desktop Windows yang dikembangkan "
    "sebagai platform utilitas dan keamanan lokal dengan pendekatan "
    "local-first dan privacy-focused. Aplikasi ini dirancang agar pengguna "
    "dapat melakukan analisis keamanan, pemeriksaan tautan, pengelolaan "
    "file, konversi dokumen, serta berbagai kebutuhan utilitas lainnya "
    "langsung dari perangkat mereka."
)

DEVELOPER_NAME = "Hasby Prasetya Saprudin"
DEVELOPER_PEN_NAME = "Choco"
OFFICIAL_INSTAGRAM = "@burungkaki4"

# ---------------------------------------------------------------------------
# STATUS PENGEMBANGAN
# ---------------------------------------------------------------------------

DEVELOPMENT_STATUS = "In Development / Public Beta"
RELEASE_DATE = "To be announced"

# ---------------------------------------------------------------------------
# PATH DASAR
# ---------------------------------------------------------------------------

# Folder dasar tempat file ini berada (chocobot/)
BASE_DIR = Path(__file__).resolve().parent

# Folder root proyek (satu tingkat di atas folder chocobot/)
ROOT_DIR = BASE_DIR.parent

# Folder data lokal aplikasi (log, konfigurasi, karantina, whitelist, bahasa)
DATA_DIR = BASE_DIR / "data"

# Subfolder data
LOG_DIR = DATA_DIR / "logs"
QUARANTINE_DIR = DATA_DIR / "quarantine"
WHITELIST_DIR = DATA_DIR / "whitelist"
LANGUAGE_DIR = DATA_DIR / "language"

# Folder aset visual
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"

# File logo utama
LOGO_PATH = IMAGES_DIR / "logo.png"

# File ikon Windows (dikonversi dari logo.png)
LOGO_ICO_PATH = ICONS_DIR / "logo.ico"

# ---------------------------------------------------------------------------
# FILE KONFIGURASI
# ---------------------------------------------------------------------------

CONFIG_FILE = DATA_DIR / "config.json"

# ---------------------------------------------------------------------------
# BAHASA YANG DIDUKUNG (7 BAHASA RESMI)
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = {
    "id": "Bahasa Indonesia",
    "en": "English",
    "ar": "العربية",
    "zh": "中文 (简体)",
    "fr": "Français",
    "ru": "Русский",
    "es": "Español",
}

DEFAULT_LANGUAGE = "id"

# ---------------------------------------------------------------------------
# PENGATURAN JENDELA UTAMA
# ---------------------------------------------------------------------------

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# ---------------------------------------------------------------------------
# SPLASH SCREEN
# ---------------------------------------------------------------------------

SPLASH_DURATION_MS = 2500              # Lama tampil splash (milidetik)
SPLASH_BG_COLOR = "#0d0d0d"            # Warna latar gelap
SPLASH_TEXT_COLOR = "#00ffcc"          # Warna teks neon
SPLASH_LOGO_SIZE = (200, 200)          # Ukuran logo di splash

# ---------------------------------------------------------------------------
# KEAMANAN & ANALISIS
# ---------------------------------------------------------------------------

# Algoritma hash yang digunakan untuk pemeriksaan integritas file.
# SHA-256 menjadi algoritma utama. MD5 dan SHA-1 tetap disediakan
# hanya untuk keperluan komparasi cepat, bukan jaminan keamanan.
HASH_ALGORITHMS = ["SHA-256", "SHA-1", "MD5"]

# Batas ukuran file maksimum untuk pemindaian penuh (dalam byte)
# 100 MB = 100 * 1024 * 1024
MAX_SCAN_FILE_SIZE = 104_857_600

# Rentang Risk Score untuk Link Inspector
RISK_LEVELS = {
    "LOW":      (0, 19),
    "MODERATE": (20, 39),
    "MEDIUM":   (40, 59),
    "HIGH":     (60, 79),
    "CRITICAL": (80, 100),
}

# ---------------------------------------------------------------------------
# KONVERSI FILE
# ---------------------------------------------------------------------------

# Format konversi yang direncanakan pada versi awal
SUPPORTED_CONVERSIONS = [
    "pdf_to_word",
    "pdf_to_jpg",
    "pdf_to_png",
    "word_to_pdf",
    "jpg_to_pdf",
    "png_to_pdf",
]

# ---------------------------------------------------------------------------
# PEMANTAUAN SISTEM
# ---------------------------------------------------------------------------

# Interval pembaruan data monitor (dalam milidetik)
MONITOR_REFRESH_MS = 1000

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_NAME = "chocobot.log"

# ---------------------------------------------------------------------------
# TAUTAN RESMI
# ---------------------------------------------------------------------------

BLOG_HOME_URL = "https://chocobotofficial.blogspot.com/"
ABOUT_URL = "https://chocobotofficial.blogspot.com/p/about-chocobot-local-windows-utility_0283961939.html"
USER_GUIDE_URL = "https://chocobotofficial.blogspot.com/p/chocobot-user-guide-panduan-penggunaan.html"
DEVELOPER_URL = "https://chocobotofficial.blogspot.com/p/about-developer-chocobot.html"
LICENSE_URL = "https://chocobotofficial.blogspot.com/p/chocobot-license-terms-of-use.html"
CONTACT_URL = "https://chocobotofficial.blogspot.com/p/contact-feedback-chocobot.html"

# ---------------------------------------------------------------------------
# LAIN-LAIN
# ---------------------------------------------------------------------------

# Teks yang muncul ketika nilai belum tersedia
UNKNOWN_VALUE = "-"