
# -*- coding: utf-8 -*-
"""
Chocobot Guardian — Main Application Window
============================================

UI utama Chocobot Guardian.

Prinsip desain:
- Tkinter native / ringan
- Offline-first
- Windows 7–11 friendly
- Futuristic dark interface
- Smooth navigation
- Animated sidebar
- Animated header
- Logo PNG -> ICO otomatis
- Taskbar/window icon memakai assets/images/logo.png
- Tidak membutuhkan server/API
"""

import json
import sys
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path

from chocobot import constants as const
from chocobot import config as config_module
from chocobot.ui import styles
from chocobot.ui.widgets import RoundedCard, RoundedButton


class ChocobotApp:
    """Main application window."""

    def __init__(self) -> None:
        self.root = tk.Tk()

        # --------------------------------------------------------------
        # STATE
        # --------------------------------------------------------------

        self.config = config_module.load_config()

        self.language = self.config.get(
            "language",
            const.DEFAULT_LANGUAGE,
        )

        self.texts = self._load_language(self.language)

        self.current = "HOME"
        self.current_page_frame = None

        self.nav_buttons = {}
        self.nav_indicators = {}

        self._clock_job = None
        self._slide_job = None
        self._pulse_job = None

        self._logo_img = None
        self._icon_img = None

        # --------------------------------------------------------------
        # WINDOW
        # --------------------------------------------------------------

        self.root.title(
            f"{const.APP_NAME} — {const.APP_TAGLINE}"
        )

        self.root.geometry("1220x760")
        self.root.minsize(1000, 640)

        self.root.configure(
            bg=styles.APP_BG
        )

        self.root.option_add(
            "*Font",
            styles.FONT_FAMILY + " 10"
        )

        # Windows-specific visual tuning
        try:
            self.root.wm_attributes("-alpha", 1.0)
        except Exception:
            pass

        # --------------------------------------------------------------
        # ICON
        # --------------------------------------------------------------

        self._ensure_icon_file()
        self._set_window_icon()

        # --------------------------------------------------------------
        # BUILD
        # --------------------------------------------------------------

        self._build_ui()

        # --------------------------------------------------------------
        # INITIAL PAGE
        # --------------------------------------------------------------

        self.root.after(
            80,
            lambda: self.show("HOME", animate=False)
        )

    # ==================================================================
    # LANGUAGE
    # ==================================================================

    def _load_language(self, lang: str) -> dict:
        """Load UI language JSON with safe fallback."""

        default_texts = {
            "home": "Beranda",
            "security": "Pusat Keamanan",
            "link": "Inspektur Tautan",
            "files": "Utilitas File",
            "converter": "Konverter",
            "system": "Sistem",
            "network": "Jaringan",
            "monitor": "Monitor",
            "settings": "Pengaturan",
            "developer": "Pengembang",
            "about": "Tentang",
            "license": "Lisensi",
            "blog": "Blog Resmi",
            "guide": "Panduan Pengguna",
            "contact": "Kontak & Masukan",

            "back": "Kembali",
            "home_nav": "Utama",
            "open": "Buka",
            "analyze": "Analisis",
            "url_label": "URL / Tautan",
            "result_area": "Area hasil",

            "system_status": "STATUS SISTEM",
            "protected": "Pemeriksaan lokal aktif",
            "interface_ready":
                "Utilitas berjalan lokal • beberapa modul masih tahap awal",

            "chocobot_title": "Chocobot",
            "chocobot_subtitle":
                "Platform Utilitas & Keamanan Windows Lokal",

            "chocoengine": "ChocoEngine",
            "chocoengine_desc": "Core interface engine",

            "blog_title": "Blog Resmi",
            "blog_subtitle": "Blog Resmi Chocobot",
            "blog_summary":
                "Kunjungi blog resmi Chocobot untuk informasi terbaru, "
                "pengumuman, dan dokumentasi lengkap.",
            "open_blog": "Buka Blog Resmi",

            "guide_title": "Panduan Pengguna",
            "guide_subtitle": "Panduan Penggunaan Chocobot",
            "guide_summary":
                "Panduan penggunaan resmi mencakup instalasi, navigasi, "
                "fitur, dan penjelasan hasil analisis.",
            "open_guide": "Buka Panduan Pengguna",

            "contact_title": "Kontak & Masukan",
            "contact_subtitle": "Kontak Resmi dan Masukan",
            "contact_summary":
                "Sampaikan laporan bug, saran, kritik, atau pertanyaan "
                "melalui halaman kontak resmi Chocobot.",
            "open_contact": "Buka Halaman Kontak",

            "about_title": "Tentang",
            "about_subtitle":
                "Identitas, filosofi, dan status pengembangan Chocobot",
            "about_summary":
                "Chocobot Guardian adalah aplikasi desktop Windows lokal "
                "untuk utilitas dan keamanan, dikembangkan secara "
                "independen dengan pendekatan local-first dan "
                "privacy-focused.\n\n"
                "Untuk informasi lengkap, kunjungi halaman About.",
            "open_about": "Buka Halaman Tentang",

            "developer_title": "Pengembang",
            "developer_subtitle":
                "Informasi dan kontak pengembang",
            "developer_summary":
                "Chocobot dikembangkan secara independen dengan nama "
                "pena Choco.\n\n"
                "Untuk profil lengkap dan kontak resmi, kunjungi "
                "halaman Developer.",
            "open_developer": "Buka Halaman Pengembang",

            "license_title": "Lisensi",
            "license_subtitle":
                "Informasi dan ketentuan lisensi",
            "license_summary":
                "Chocobot dilindungi oleh lisensi yang mengatur "
                "penggunaan, distribusi, dan modifikasi.",
            "open_license": "Buka Halaman Lisensi",
        }

        # Language packs are bundled read-only resources.
        lang_file = const.LANGUAGE_DIR / f"{lang}.json"
        if lang_file.is_file():
            try:
                with open(lang_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, dict):
                    default_texts.update(data)
            except (OSError, json.JSONDecodeError, TypeError):
                # Keep defaults if an optional language pack is invalid.
                pass

        return default_texts

    def t(self, key: str) -> str:
        """Return translated UI text."""

        return self.texts.get(key, key)

    # ==================================================================
    # ICON SYSTEM
    # ==================================================================

    def _ensure_icon_file(self) -> None:
        """
        Automatically convert logo.png -> logo.ico.

        This keeps the project simple:
        user only needs to maintain logo.png.
        """

        try:
            const.ICONS_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            if not const.LOGO_PATH.exists():
                return

            from PIL import Image

            source = Image.open(
                const.LOGO_PATH
            ).convert("RGBA")

            sizes = [
                (16, 16),
                (24, 24),
                (32, 32),
                (48, 48),
                (64, 64),
                (128, 128),
                (256, 256),
            ]

            source.save(
                const.LOGO_ICO_PATH,
                format="ICO",
                sizes=sizes,
            )

        except Exception:
            # Icon failure must never prevent application startup.
            pass

    def _set_window_icon(self) -> None:
        """Set application icon for Windows and Tk."""

        try:
            if (
                sys.platform == "win32"
                and const.LOGO_ICO_PATH.exists()
            ):
                self.root.iconbitmap(
                    default=str(
                        const.LOGO_ICO_PATH
                    )
                )

        except Exception:
            pass

        try:
            if const.LOGO_PATH.exists():
                from PIL import Image, ImageTk

                image = Image.open(
                    const.LOGO_PATH
                ).convert("RGBA")

                image.thumbnail(
                    (64, 64),
                    Image.Resampling.LANCZOS,
                )

                self._icon_img = ImageTk.PhotoImage(
                    image
                )

                self.root.iconphoto(
                    True,
                    self._icon_img,
                )

        except Exception:
            pass

    # ==================================================================
    # MAIN UI
    # ==================================================================

    def _build_ui(self) -> None:
        """Build the complete application shell."""

        # ==============================================================
        # SIDEBAR
        # ==============================================================

        self.sidebar = tk.Frame(
            self.root,
            bg=styles.SIDEBAR_BG,
            width=styles.SIDEBAR_WIDTH,
        )

        self.sidebar.pack(
            side="left",
            fill="y",
        )

        self.sidebar.pack_propagate(False)

        # --------------------------------------------------------------
        # Sidebar top glow
        # --------------------------------------------------------------

        self.sidebar_glow = tk.Frame(
            self.sidebar,
            bg=styles.CYAN,
            height=2,
        )

        self.sidebar_glow.pack(
            side="top",
            fill="x",
        )

        # --------------------------------------------------------------
        # BRAND
        # --------------------------------------------------------------

        self.brand = tk.Frame(
            self.sidebar,
            bg=styles.SIDEBAR_BG,
            height=92,
        )

        self.brand.pack(
            fill="x",
        )

        self.brand.pack_propagate(False)

        # Logo
        self._load_sidebar_logo()

        if self._logo_img is not None:
            self.logo_label = tk.Label(
                self.brand,
                image=self._logo_img,
                bg=styles.SIDEBAR_BG,
                bd=0,
            )

            self.logo_label.pack(
                side="left",
                padx=(18, 10),
                pady=15,
            )

        brand_text = tk.Frame(
            self.brand,
            bg=styles.SIDEBAR_BG,
        )

        brand_text.pack(
            side="left",
            fill="both",
            expand=True,
            pady=14,
        )

        tk.Label(
            brand_text,
            text="CHOCOBOT",
            fg=styles.TEXT,
            bg=styles.SIDEBAR_BG,
            font=styles.FONT_BRAND,
        ).pack(
            anchor="w",
        )

        tk.Label(
            brand_text,
            text="GUARDIAN",
            fg=styles.CYAN,
            bg=styles.SIDEBAR_BG,
            font=styles.FONT_BRAND_SUB,
        ).pack(
            anchor="w",
            pady=(1, 0),
        )

        # --------------------------------------------------------------
        # SIDEBAR STATUS
        # --------------------------------------------------------------

        status_frame = tk.Frame(
            self.sidebar,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        status_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 10),
        )

        self.status_dot = tk.Label(
            status_frame,
            text="●",
            fg=styles.GREEN,
            bg=styles.PANEL,
            font=("Segoe UI", 8, "bold"),
        )

        self.status_dot.pack(
            side="left",
            padx=(10, 5),
            pady=8,
        )

        tk.Label(
            status_frame,
            text="LOCAL CORE",
            fg=styles.TEXT,
            bg=styles.PANEL,
            font=("Segoe UI", 8, "bold"),
        ).pack(
            side="left",
            pady=8,
        )

        tk.Label(
            status_frame,
            text="ONLINE",
            fg=styles.GREEN,
            bg=styles.PANEL,
            font=("Segoe UI", 7, "bold"),
        ).pack(
            side="right",
            padx=10,
        )

        # --------------------------------------------------------------
        # NAVIGATION
        # --------------------------------------------------------------

        nav_outer = tk.Frame(
            self.sidebar,
            bg=styles.SIDEBAR_BG,
        )

        nav_outer.pack(
            fill="both",
            expand=True,
            padx=8,
        )

        for section_title, items in styles.NAV_SECTIONS:

            section = tk.Frame(
                nav_outer,
                bg=styles.SIDEBAR_BG,
            )

            section.pack(
                fill="x",
                pady=(5, 0),
            )

            tk.Label(
                section,
                text=section_title.upper(),
                fg="#66717d",
                bg=styles.SIDEBAR_BG,
                font=styles.FONT_SIDEBAR_SECTION,
            ).pack(
                anchor="w",
                padx=12,
                pady=(6, 4),
            )

            for key, label, icon in items:
                self._create_nav_button(
                    section,
                    key,
                    icon,
                )

        # --------------------------------------------------------------
        # SETTINGS
        # --------------------------------------------------------------

        separator = tk.Frame(
            self.sidebar,
            bg=styles.BORDER,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=15,
            pady=7,
        )

        self._create_nav_button(
            self.sidebar,
            "SETTINGS",
            "⚙",
        )

        # --------------------------------------------------------------
        # SIDEBAR FOOTER
        # --------------------------------------------------------------

        footer = tk.Frame(
            self.sidebar,
            bg=styles.SIDEBAR_BG,
        )

        footer.pack(
            fill="x",
            padx=18,
            pady=(5, 14),
        )

        tk.Label(
            footer,
            text="CHOCOENGINE",
            fg=styles.PURPLE,
            bg=styles.SIDEBAR_BG,
            font=styles.FONT_CARD_TITLE,
        ).pack(
            anchor="w",
        )

        tk.Label(
            footer,
            text="LOCAL CORE ENGINE",
            fg="#59636e",
            bg=styles.SIDEBAR_BG,
            font=styles.FONT_SUBTITLE,
        ).pack(
            anchor="w",
        )

        # ==============================================================
        # MAIN AREA
        # ==============================================================

        self.main = tk.Frame(
            self.root,
            bg=styles.APP_BG,
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True,
        )

        # --------------------------------------------------------------
        # TOP HEADER
        # --------------------------------------------------------------

        self.top = tk.Frame(
            self.main,
            bg=styles.APP_BG,
            height=64,
        )

        self.top.pack(
            fill="x",
            padx=styles.CONTENT_PAD_X,
        )

        self.top.pack_propagate(False)

        # Header left
        header_left = tk.Frame(
            self.top,
            bg=styles.APP_BG,
        )

        header_left.pack(
            side="left",
            fill="y",
        )

        self.header_page = tk.Label(
            header_left,
            text="CHOCObot",
            fg=styles.TEXT,
            bg=styles.APP_BG,
            font=("Segoe UI", 11, "bold"),
        )

        self.header_page.pack(
            side="left",
            pady=18,
        )

        # Header right
        header_right = tk.Frame(
            self.top,
            bg=styles.APP_BG,
        )

        header_right.pack(
            side="right",
            fill="y",
        )

        # Local indicator
        local_badge = tk.Frame(
            header_right,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        local_badge.pack(
            side="left",
            pady=13,
            padx=(0, 10),
        )

        tk.Label(
            local_badge,
            text="●",
            fg=styles.GREEN,
            bg=styles.PANEL,
            font=("Segoe UI", 8),
        ).pack(
            side="left",
            padx=(8, 4),
            pady=6,
        )

        tk.Label(
            local_badge,
            text="LOCAL",
            fg=styles.MUTED,
            bg=styles.PANEL,
            font=("Segoe UI", 7, "bold"),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        # Clock
        self.clock = tk.Label(
            header_right,
            text="00:00:00",
            fg=styles.MUTED,
            bg=styles.APP_BG,
            font=("Consolas", 9),
        )

        self.clock.pack(
            side="right",
            pady=19,
        )

        self.update_clock()

        # --------------------------------------------------------------
        # HEADER LINE
        # --------------------------------------------------------------

        self.header_line = tk.Frame(
            self.main,
            bg=styles.BORDER,
            height=1,
        )

        self.header_line.pack(
            fill="x",
            padx=styles.CONTENT_PAD_X,
        )

        # --------------------------------------------------------------
        # CONTENT
        # --------------------------------------------------------------

        self.content = tk.Frame(
            self.main,
            bg=styles.APP_BG,
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=styles.CONTENT_PAD_X,
            pady=(10, styles.CONTENT_PAD_BOTTOM),
        )

        # --------------------------------------------------------------
        # BOTTOM STATUS
        # --------------------------------------------------------------

        self.bottom_status = tk.Frame(
            self.main,
            bg=styles.APP_BG,
            height=25,
        )

        self.bottom_status.pack(
            fill="x",
            padx=styles.CONTENT_PAD_X,
        )

        self.bottom_status.pack_propagate(False)

        tk.Label(
            self.bottom_status,
            text="CHOCOBOT GUARDIAN  •  LOCAL-FIRST  •  PRIVACY FOCUSED",
            fg="#4f5a65",
            bg=styles.APP_BG,
            font=("Segoe UI", 7),
        ).pack(
            side="left",
            pady=4,
        )

        self.version_label = tk.Label(
            self.bottom_status,
            text="READY",
            fg=styles.GREEN,
            bg=styles.APP_BG,
            font=("Consolas", 7, "bold"),
        )

        self.version_label.pack(
            side="right",
            pady=4,
        )

        # Start subtle pulse
        self._pulse_status()

    def _load_sidebar_logo(self) -> None:
        """Load logo.png for sidebar."""

        try:
            if not const.LOGO_PATH.exists():
                return

            from PIL import Image, ImageTk

            image = Image.open(
                const.LOGO_PATH
            ).convert("RGBA")

            image.thumbnail(
                (48, 48),
                Image.Resampling.LANCZOS,
            )

            self._logo_img = ImageTk.PhotoImage(
                image
            )

        except Exception:
            self._logo_img = None

    # ==================================================================
    # NAVIGATION BUTTON
    # ==================================================================

    def _create_nav_button(
        self,
        parent,
        key: str,
        icon: str,
    ) -> None:
        """Create an animated sidebar navigation item."""

        holder = tk.Frame(
            parent,
            bg=styles.SIDEBAR_BG,
            height=34,
        )

        holder.pack(
            fill="x",
            pady=1,
        )

        holder.pack_propagate(False)

        indicator = tk.Frame(
            holder,
            bg=styles.SIDEBAR_BG,
            width=3,
        )

        indicator.pack(
            side="left",
            fill="y",
        )

        self.nav_indicators[key] = indicator

        button = tk.Button(
            holder,
            text=f"  {icon}   {self.t(key.lower())}",
            anchor="w",
            relief="flat",
            bd=0,
            bg=styles.SIDEBAR_BG,
            fg=styles.MUTED,
            activebackground=styles.PANEL_2,
            activeforeground=styles.TEXT,
            font=styles.FONT_SIDEBAR_ITEM,
            cursor="hand2",
            padx=5,
            pady=0,
            command=lambda k=key: self.show(k),
        )

        button.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.nav_buttons[key] = button

        button.bind(
            "<Enter>",
            lambda event, k=key:
            self._nav_hover(k, True),
        )

        button.bind(
            "<Leave>",
            lambda event, k=key:
            self._nav_hover(k, False),
        )

    def _nav_hover(
        self,
        key: str,
        active: bool,
    ) -> None:
        """Handle navigation hover animation."""

        button = self.nav_buttons.get(key)

        if button is None:
            return

        if key == self.current:
            return

        if active:
            button.configure(
                bg=styles.PANEL_2,
                fg=styles.TEXT,
            )
        else:
            button.configure(
                bg=styles.SIDEBAR_BG,
                fg=styles.MUTED,
            )

    # ==================================================================
    # CLOCK / STATUS
    # ==================================================================

    def update_clock(self) -> None:
        """Update digital clock."""

        try:
            self.clock.configure(
                text=datetime.now().strftime("%H:%M:%S")
            )

            self._clock_job = self.root.after(
                1000,
                self.update_clock,
            )

        except tk.TclError:
            pass

    def _pulse_status(self) -> None:
        """Subtle local-core status pulse."""

        try:
            current = self.status_dot.cget("fg")

            if current == styles.GREEN:
                self.status_dot.configure(
                    fg="#73f0bb"
                )
            else:
                self.status_dot.configure(
                    fg=styles.GREEN
                )

            self._pulse_job = self.root.after(
                900,
                self._pulse_status,
            )

        except tk.TclError:
            pass

    # ==================================================================
    # PAGE NAVIGATION
    # ==================================================================

    def show(
        self,
        key: str,
        animate: bool = True,
    ) -> None:
        """Display page with smooth slide animation."""

        key = key.upper()

        if (
            key == self.current
            and self.current_page_frame is not None
        ):
            return

        if not hasattr(
            self,
            "page_" + key.lower(),
        ):
            return

        old_page = self.current_page_frame

        self.current = key

        # --------------------------------------------------------------
        # Navigation highlight
        # --------------------------------------------------------------

        for nav_key, button in self.nav_buttons.items():

            indicator = self.nav_indicators.get(
                nav_key
            )

            if nav_key == key:
                button.configure(
                    bg=styles.ACTIVE_NAV_BG,
                    fg=styles.CYAN,
                )

                if indicator:
                    indicator.configure(
                        bg=styles.CYAN
                    )

            else:
                button.configure(
                    bg=styles.SIDEBAR_BG,
                    fg=styles.MUTED,
                )

                if indicator:
                    indicator.configure(
                        bg=styles.SIDEBAR_BG
                    )

        # --------------------------------------------------------------
        # Header
        # --------------------------------------------------------------

        page_name = self.t(key.lower())

        self.header_page.configure(
            text=page_name.upper()
        )

        self.version_label.configure(
            text="READY",
            fg=styles.GREEN,
        )

        # --------------------------------------------------------------
        # New page
        # --------------------------------------------------------------

        new_page = tk.Frame(
            self.content,
            bg=styles.APP_BG,
        )

        try:
            builder = getattr(
                self,
                "page_" + key.lower(),
            )

            builder(new_page)

        except Exception as error:
            self._show_page_error(
                new_page,
                error,
            )

        # --------------------------------------------------------------
        # Animation
        # --------------------------------------------------------------

        if not animate or old_page is None:
            new_page.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1,
            )

            self.current_page_frame = new_page

            if old_page:
                old_page.destroy()

            return

        self._animate_page_slide(
            new_page,
            old_page,
        )

    def _animate_page_slide(
        self,
        new_page: tk.Frame,
        old_page: tk.Frame,
    ) -> None:
        """Smooth page transition."""

        self.root.update_idletasks()

        width = self.content.winfo_width()
        height = self.content.winfo_height()

        if width <= 1:
            width = 800

        if height <= 1:
            height = 600

        new_page.place(
            x=width,
            y=0,
            width=width,
            height=height,
        )

        old_page.place(
            x=0,
            y=0,
            width=width,
            height=height,
        )

        self.current_page_frame = new_page

        self._slide_step(
            new_page,
            old_page,
            width,
            0,
        )

    def _slide_step(
        self,
        new_page,
        old_page,
        width: int,
        step: int,
    ) -> None:
        """Single animation frame."""

        steps = 16

        if step > steps:
            try:
                new_page.place_configure(
                    x=0,
                    y=0,
                )

                old_page.destroy()

            except tk.TclError:
                pass

            self._slide_job = None
            return

        # Smoothstep easing
        progress = step / float(steps)

        eased = (
            progress
            * progress
            * (3.0 - 2.0 * progress)
        )

        new_x = int(
            width * (1.0 - eased)
        )

        old_x = int(
            -width * 0.10 * eased
        )

        try:
            new_page.place_configure(
                x=new_x
            )

            old_page.place_configure(
                x=old_x
            )

            self._slide_job = self.root.after(
                12,
                lambda:
                self._slide_step(
                    new_page,
                    old_page,
                    width,
                    step + 1,
                ),
            )

        except tk.TclError:
            pass

    # ==================================================================
    # COMMON PAGE COMPONENTS
    # ==================================================================

    def _page_title(
        self,
        parent: tk.Frame,
        title: str,
        subtitle: str,
    ) -> None:
        """Modern page title."""

        header = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        header.pack(
            fill="x",
            pady=(2, 16),
        )

        # Accent line
        accent = tk.Frame(
            header,
            bg=styles.CYAN,
            width=3,
            height=40,
        )

        accent.pack(
            side="left",
            fill="y",
            padx=(0, 12),
        )

        text_frame = tk.Frame(
            header,
            bg=styles.APP_BG,
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
        )

        tk.Label(
            text_frame,
            text=title,
            fg=styles.TEXT,
            bg=styles.APP_BG,
            font=styles.FONT_TITLE,
        ).pack(
            anchor="w",
        )

        tk.Label(
            text_frame,
            text=subtitle,
            fg=styles.MUTED,
            bg=styles.APP_BG,
            font=styles.FONT_SUBTITLE,
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

    def _create_card_wrapper(
        self,
        parent: tk.Frame,
        title: str,
        text: str = "",
        accent: str = styles.CYAN,
        command=None,
        width: int = 340,
        height: int = 105,
    ) -> tk.Frame:
        """Create responsive RoundedCard wrapper."""

        wrapper = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        card = RoundedCard(
            wrapper,
            title=title,
            text=text,
            accent=accent,
            command=command,
            width=width,
            height=height,
        )

        card.pack(
            fill="both",
            expand=True,
        )

        return wrapper

    def _info_with_link(
        self,
        parent: tk.Frame,
        summary: str,
        url: str,
        button_text: str,
    ) -> None:
        """Information page with external link."""

        card = tk.Frame(
            parent,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        card.pack(
            fill="x",
            pady=5,
        )

        tk.Frame(
            card,
            bg=styles.CYAN,
            width=3,
        ).pack(
            side="left",
            fill="y",
        )

        body = tk.Frame(
            card,
            bg=styles.PANEL,
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        tk.Label(
            body,
            text=summary,
            fg=styles.TEXT,
            bg=styles.PANEL,
            justify="left",
            wraplength=760,
            font=styles.FONT_ENTRY,
        ).pack(
            anchor="w",
            pady=(0, 18),
        )

        RoundedButton(
            body,
            text=button_text,
            command=lambda: webbrowser.open(url),
            width=190,
            height=38,
            bg=styles.PANEL_2,
            fg=styles.CYAN,
        ).pack(
            anchor="w",
        )

    def _show_page_error(
        self,
        parent: tk.Frame,
        error: Exception,
    ) -> None:
        """Safe fallback page."""

        parent.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            parent,
            text="INTERFACE ERROR",
            fg=styles.RED,
            bg=styles.APP_BG,
            font=("Segoe UI", 18, "bold"),
        ).pack(
            anchor="w",
            pady=(30, 10),
        )

        tk.Label(
            parent,
            text=(
                "The selected interface could not be loaded.\n\n"
                f"{type(error).__name__}: {error}"
            ),
            fg=styles.MUTED,
            bg=styles.APP_BG,
            justify="left",
            font=styles.FONT_ENTRY,
        ).pack(
            anchor="w",
        )

    # ==================================================================
    # HOME
    # ==================================================================

    def page_home(
        self,
        parent: tk.Frame,
    ) -> None:
        """Main dashboard."""

        self._page_title(
            parent,
            self.t("chocobot_title"),
            self.t("chocobot_subtitle"),
        )

        # --------------------------------------------------------------
        # HERO STATUS
        # --------------------------------------------------------------

        status = tk.Frame(
            parent,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        status.pack(
            fill="x",
            pady=(0, 16),
        )

        tk.Frame(
            status,
            bg=styles.GREEN,
            width=4,
        ).pack(
            side="left",
            fill="y",
        )

        status_body = tk.Frame(
            status,
            bg=styles.PANEL,
        )

        status_body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=16,
        )

        top = tk.Frame(
            status_body,
            bg=styles.PANEL,
        )

        top.pack(
            fill="x",
        )

        tk.Label(
            top,
            text=self.t("system_status"),
            fg=styles.MUTED,
            bg=styles.PANEL,
            font=styles.FONT_STATUS_TITLE,
        ).pack(
            side="left",
        )

        tk.Label(
            top,
            text="LOCAL CORE • ACTIVE",
            fg=styles.GREEN,
            bg=styles.PANEL,
            font=("Consolas", 8, "bold"),
        ).pack(
            side="right",
        )

        tk.Label(
            status_body,
            text="●  " + self.t("protected"),
            fg=styles.GREEN,
            bg=styles.PANEL,
            font=styles.FONT_STATUS_VALUE,
        ).pack(
            anchor="w",
            pady=(3, 1),
        )

        tk.Label(
            status_body,
            text=self.t("interface_ready"),
            fg=styles.MUTED,
            bg=styles.PANEL,
            font=styles.FONT_SUBTITLE,
        ).pack(
            anchor="w",
        )

        # --------------------------------------------------------------
        # FEATURE GRID
        # --------------------------------------------------------------

        grid = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        grid.pack(
            fill="both",
            expand=True,
        )

        items = [
            (
                "SECURITY",
                "Quick Scan, Custom Scan, File Analysis, "
                "Quarantine, Whitelist and Security Report",
                styles.RED,
            ),
            (
                "LINK",
                "URL structure, suspicious patterns, "
                "Risk Score and Risk Level",
                styles.CYAN,
            ),
            (
                "FILES",
                "File information, analysis, hashes, "
                "folders, search and large-file checks",
                styles.PURPLE,
            ),
            (
                "CONVERTER",
                "PDF, Word, JPG and PNG conversion workflows",
                styles.MAGENTA,
            ),
            (
                "SYSTEM",
                "Windows, CPU, RAM, storage and "
                "device information",
                styles.GREEN,
            ),
            (
                "NETWORK",
                "IP information, DNS lookup, Ping, "
                "connections and port inspection",
                styles.YELLOW,
            ),
            (
                "MONITOR",
                "CPU, RAM, disk, network and "
                "process monitoring",
                styles.CYAN,
            ),
            (
                "SETTINGS",
                "Language, appearance, notifications "
                "and feature settings",
                styles.PURPLE,
            ),
        ]

        for i, (
            key,
            description,
            accent,
        ) in enumerate(items):

            row, column = divmod(i, 2)

            grid.grid_rowconfigure(
                row,
                weight=1,
                uniform="home_rows",
            )

            grid.grid_columnconfigure(
                column,
                weight=1,
                uniform="home_columns",
            )

            wrapper = self._create_card_wrapper(
                grid,
                title=self.t(key.lower()),
                text=description,
                accent=accent,
                command=lambda k=key: self.show(k),
                width=350,
                height=105,
            )

            wrapper.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=(
                    (0, 8)
                    if column == 0
                    else (8, 0)
                ),
                pady=(
                    (0, 8)
                    if row == 0
                    else (8, 0)
                ),
            )

    # ==================================================================
    # SECURITY
    # ==================================================================

    def page_security(
        self,
        parent: tk.Frame,
    ) -> None:
        """Local read-only file inspection; this is not an antivirus scanner."""
        self._page_title(
            parent,
            "Pusat Pemeriksaan File",
            "Pemeriksaan lokal berbasis metadata dan signature terbatas. Tidak menghapus atau mengarantina file.",
        )
        panel = tk.Frame(parent, bg=styles.PANEL, highlightthickness=1, highlightbackground=styles.BORDER)
        panel.pack(fill="both", expand=True, pady=(0, 12))
        tk.Label(
            panel,
            text="Pilih file untuk memeriksa hash SHA-256, ekstensi, signature umum, dan indikator sederhana.",
            bg=styles.PANEL, fg=styles.TEXT, font=styles.FONT_SUBTITLE, wraplength=780, justify="left",
        ).pack(anchor="w", padx=18, pady=(18, 10))
        output = tk.Text(
            panel, height=18, wrap="word", bg=styles.ENTRY_BG, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10),
        )
        output.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        output.insert("1.0", "Pemeriksaan ini bersifat read-only dan tidak membuktikan file aman.\n")
        output.configure(state="disabled")

        def inspect_selected() -> None:
            selected = filedialog.askopenfilename(parent=parent, title="Pilih file untuk diperiksa")
            if not selected:
                return
            try:
                from chocobot.engine.security.file_analyzer import analyze_file
                result = analyze_file(selected)
                info = result["file"]
                lines = [
                    "HASIL PEMERIKSAAN LOKAL",
                    "=" * 42,
                    f"Nama: {info['name']}",
                    f"Lokasi: {info['full_path']}",
                    f"Ukuran: {info['size_bytes']:,} byte",
                    f"Tipe: {info['mime_type']}",
                    f"Perhatian: {result['overall_attention']}",
                    f"SHA-256: {result['sha256']}",
                    "",
                    "INDIKATOR",
                ]
                if result["notes"]:
                    for note in result["notes"]:
                        lines.append(f"[{note['attention']}] {note['detail']}")
                else:
                    lines.append("Tidak ada indikator yang cocok dengan aturan sederhana.")
                lines.extend(["", result["notice"]])
                output.configure(state="normal")
                output.delete("1.0", "end")
                output.insert("1.0", "\n".join(lines))
                output.configure(state="disabled")
            except (OSError, ValueError) as exc:
                messagebox.showerror("Pemeriksaan gagal", f"File tidak dapat diperiksa: {exc}", parent=parent)

        tk.Button(
            panel, text="Pilih file dan periksa", command=inspect_selected,
            bg=styles.CYAN, fg="#071014", activebackground=styles.CYAN,
            relief="flat", padx=14, pady=8, cursor="hand2",
        ).pack(anchor="w", padx=18, pady=(0, 18))

    def page_link(
        self,
        parent: tk.Frame,
    ) -> None:
        """Offline URL structure and heuristic indicator inspection."""
        self._page_title(
            parent,
            "Inspektur Tautan",
            "Pemeriksaan struktur URL secara lokal. Tidak membuka tautan atau menghubungi domain.",
        )
        box = tk.Frame(parent, bg=styles.PANEL, highlightthickness=1, highlightbackground=styles.BORDER)
        box.pack(fill="x", pady=(0, 12))
        tk.Label(box, text="URL / Tautan", fg=styles.MUTED, bg=styles.PANEL, font=styles.FONT_SUBTITLE).pack(
            anchor="w", padx=18, pady=(16, 6)
        )
        entry = tk.Entry(
            box, bg=styles.ENTRY_BG, fg=styles.TEXT, insertbackground=styles.CYAN,
            relief="flat", bd=0, font=styles.FONT_ENTRY,
        )
        entry.pack(fill="x", padx=18, ipady=10)
        entry.insert(0, "https://example.com/path?query=value")
        result = tk.Text(
            parent, wrap="word", bg=styles.PANEL, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10), height=18,
        )
        result.pack(fill="both", expand=True, pady=(0, 8))

        def analyze() -> None:
            try:
                from chocobot.engine.link.inspector import inspect_url
                report = inspect_url(entry.get())
                lines = ["HASIL PEMERIKSAAN URL", "=" * 42]
                if not report.get("valid"):
                    lines.append(report.get("error", "URL tidak valid."))
                else:
                    lines.extend([
                        f"URL: {report['normalized_url']}",
                        f"Host: {report['host']}",
                        f"Skema: {report['scheme']}",
                        f"Port: {report['port']}",
                        f"Path: {report['path']}",
                        f"HTTPS: {'Ya' if report['https'] else 'Tidak'}",
                        f"Skor indikator: {report['score']}/100 ({report['level']})",
                        "",
                        "INDIKATOR YANG PERLU DITINJAU",
                    ])
                    if report["indicators"]:
                        for item in report["indicators"]:
                            lines.append(f"[+{item['points']}] {item['title']}: {item['detail']}")
                    else:
                        lines.append("Tidak ada indikator yang cocok dengan aturan sederhana.")
                    lines.extend(["", report["notice"]])
                result.delete("1.0", "end")
                result.insert("1.0", "\n".join(lines))
            except Exception as exc:
                result.delete("1.0", "end")
                result.insert("1.0", f"Pemeriksaan gagal: {type(exc).__name__}: {exc}")

        RoundedButton(
            box, text="Analisis", command=analyze, width=130, height=34,
            bg=styles.CYAN, fg="#071014",
        ).pack(anchor="w", padx=18, pady=12)
        analyze()

    def page_files(
        self,
        parent: tk.Frame,
    ) -> None:
        """Working local file metadata, hashing, and folder inventory."""
        self._page_title(
            parent,
            "Utilitas File",
            "Informasi file, SHA-256, dan ringkasan folder. Semua pemeriksaan bersifat lokal dan read-only.",
        )
        toolbar = tk.Frame(parent, bg=styles.APP_BG)
        toolbar.pack(fill="x", pady=(0, 12))
        output = tk.Text(
            parent, wrap="word", bg=styles.PANEL, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10),
        )
        output.pack(fill="both", expand=True)

        def show_text(text: str) -> None:
            output.delete("1.0", "end")
            output.insert("1.0", text)

        def inspect_file() -> None:
            selected = filedialog.askopenfilename(parent=parent, title="Pilih file")
            if not selected:
                return
            try:
                from chocobot.engine.file_tools.file_info import get_file_info
                from chocobot.engine.file_tools.hashing import hash_file
                info = get_file_info(selected)
                hashes = hash_file(selected, ("sha256",))
                size = info["size_bytes"]
                show_text(
                    "INFORMASI FILE\n" + "=" * 42 + "\n"
                    + f"Nama: {info['name']}\nLokasi: {info['full_path']}\n"
                    + f"Ekstensi: {info['extension'] or '[tanpa ekstensi]'}\n"
                    + f"Tipe MIME: {info['mime_type']}\nUkuran: {size:,} byte ({size / (1024 * 1024):.2f} MiB)\n"
                    + f"Dianggap tersembunyi: {info['is_hidden']}\n"
                    + f"SHA-256: {hashes['sha256']}\n\n"
                    + "Hash cocok untuk memverifikasi bahwa byte file tidak berubah. Hash bukan bukti file aman."
                )
            except (OSError, ValueError) as exc:
                messagebox.showerror("File tidak dapat diperiksa", str(exc), parent=parent)

        def inspect_folder() -> None:
            selected = filedialog.askdirectory(parent=parent, title="Pilih folder")
            if not selected:
                return
            try:
                from chocobot.engine.file_tools.folder_analysis import analyze_folder
                report = analyze_folder(selected)
                lines = [
                    "RINGKASAN FOLDER", "=" * 42, f"Folder: {report['root']}",
                    f"File ditemukan: {report['files_count']}",
                    f"Subfolder ditemukan: {report['directories_count']}",
                    f"Ukuran total yang dihitung: {report['total_bytes']:,} byte",
                    f"File tak bisa diakses: {report['inaccessible_count']}",
                    f"Hasil dibatasi: {'Ya' if report['truncated'] else 'Tidak'}",
                    "", "EKSTENSI",
                ]
                lines.extend(f"{ext}: {count}" for ext, count in report["extension_counts"].items())
                lines.extend(["", "10 FILE TERBESAR"])
                lines.extend(f"{row['size_bytes']:>12,} byte  {row['name']}" for row in report["largest_files"])
                lines.extend(["", "Ringkasan bersifat read-only; tautan simbolik dilewati."])
                show_text("\n".join(lines))
            except (OSError, ValueError) as exc:
                messagebox.showerror("Folder tidak dapat dianalisis", str(exc), parent=parent)

        for label, command in (
            ("Informasi file + SHA-256", inspect_file),
            ("Ringkasan folder", inspect_folder),
        ):
            tk.Button(
                toolbar, text=label, command=command,
                bg=styles.CYAN if label.startswith("Informasi") else styles.PANEL,
                fg="#071014" if label.startswith("Informasi") else styles.TEXT,
                relief="flat", padx=12, pady=8, cursor="hand2",
            ).pack(side="left", padx=(0, 8))
        show_text("Pilih salah satu utilitas di atas.\nFolder scan membatasi penelusuran hingga 10.000 file secara default.")

    def page_converter(
        self,
        parent: tk.Frame,
    ) -> None:
        """Converter interface."""

        self._page_title(
            parent,
            "Converter",
            "Document and image conversion workflow",
        )

        f = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        f.pack(
            fill="both",
            expand=True,
        )

        steps = [
            (
                "01",
                "Choose Converter",
                "Select the conversion engine",
            ),
            (
                "02",
                "Conversion Type",
                "Select source and destination format",
            ),
            (
                "03",
                "Source File",
                "Choose the input file",
            ),
            (
                "04",
                "Output Location",
                "Select where the result is saved",
            ),
            (
                "05",
                "Run Conversion",
                "Execute the conversion workflow",
            ),
            (
                "06",
                "Inspect Result",
                "Review the generated output",
            ),
        ]

        items = []

        for i, (
            number,
            title,
            description,
        ) in enumerate(steps):

            items.append(
                (
                    number + "  " + title,
                    description,
                    (
                        styles.MAGENTA
                        if i % 2
                        else styles.CYAN
                    ),
                )
            )

        self._card_grid(
            f,
            items,
            "converter",
            columns=2,
        )

    # ==================================================================
    # GENERIC CARD GRID
    # ==================================================================

    def _card_grid(
        self,
        parent,
        items,
        namespace,
        columns=2,
    ) -> None:
        """Responsive card grid."""

        for column in range(columns):
            parent.grid_columnconfigure(
                column,
                weight=1,
                uniform=namespace + "_columns",
            )

        rows = (
            len(items) + columns - 1
        ) // columns

        for row in range(rows):
            parent.grid_rowconfigure(
                row,
                weight=1,
                uniform=namespace + "_rows",
            )

        for index, (
            title,
            description,
            accent,
        ) in enumerate(items):

            row = index // columns
            column = index % columns

            wrapper = self._create_card_wrapper(
                parent,
                title=title,
                text=description,
                accent=accent,
                command=None,
                width=320,
                height=105,
            )

            wrapper.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=(
                    (0, 7)
                    if column == 0
                    else (7, 0)
                ),
                pady=7,
            )

    # ==================================================================
    # SIMPLE INFORMATION PAGES
    # ==================================================================

    def _simple_info(
        self,
        parent: tk.Frame,
        title: str,
        subtitle: str,
        items: list,
    ) -> None:
        """Generic information page."""

        self._page_title(
            parent,
            title,
            subtitle,
        )

        f = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        f.pack(
            fill="both",
            expand=True,
        )

        prepared = []

        accents = [
            styles.CYAN,
            styles.GREEN,
            styles.PURPLE,
            styles.YELLOW,
            styles.MAGENTA,
        ]

        for i, (
            card_title,
            description,
        ) in enumerate(items):

            prepared.append(
                (
                    card_title,
                    description,
                    accents[
                        i % len(accents)
                    ],
                )
            )

        self._card_grid(
            f,
            prepared,
            title.lower(),
            columns=2,
        )

    # ==================================================================
    # SYSTEM
    # ==================================================================

    def page_system(
        self,
        parent: tk.Frame,
    ) -> None:
        """Show a real, read-only device and operating-system snapshot."""
        self._page_title(
            parent,
            "Informasi Perangkat",
            "Informasi OS, runtime, CPU, memori, GPU, dan penyimpanan yang terbaca secara lokal.",
        )
        toolbar = tk.Frame(parent, bg=styles.APP_BG)
        toolbar.pack(fill="x", pady=(0, 12))
        output = tk.Text(
            parent, wrap="word", bg=styles.PANEL, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10),
        )
        output.pack(fill="both", expand=True)

        def show_text(value: str) -> None:
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.insert("1.0", value)
            output.configure(state="disabled")

        def refresh() -> None:
            try:
                from chocobot.engine.system.sysinfo import get_system_info
                from chocobot.engine.system.device_discovery import discover_device
                info = get_system_info()
                profile = discover_device()
                os_info = info.get("os", {})
                runtime = info.get("runtime", {})
                cpu = info.get("cpu", {})
                memory = info.get("memory", {})
                gpu = info.get("gpu", {})
                storage = info.get("storage", {})
                device = profile.get("device", {})
                capabilities = profile.get("capabilities", {})
                lines = [
                    "INFORMASI PERANGKAT",
                    "=" * 48,
                    f"Sistem operasi: {os_info.get('name', '-') } {os_info.get('release', '')}",
                    f"Versi/build OS: {os_info.get('version', '-')}",
                    f"Arsitektur: {os_info.get('architecture', '-')}",
                    f"Nama perangkat: {os_info.get('hostname', '-')}",
                    f"Python/runtime: {runtime.get('implementation', '-')} {runtime.get('version', '-')}",
                    "",
                    "PROSESOR",
                    f"Model: {cpu.get('name', '-')}",
                    f"Arsitektur CPU: {cpu.get('architecture', '-')}",
                    f"Prosesor logis: {cpu.get('logical_processors', 0)}",
                    "",
                    "MEMORI",
                    f"RAM total: {memory.get('total_gib', 0)} GiB",
                    f"RAM terpakai: {memory.get('used_gib', 0)} GiB ({memory.get('used_percent', 0)}%)",
                    f"RAM tersedia: {memory.get('available_gib', 0)} GiB",
                    "",
                    "GRAFIS",
                    *([f"- {item}" for item in gpu.get("adapters", [])] or ["GPU/display adapter tidak tersedia melalui metode standar."]),
                    "",
                    "PENYIMPANAN",
                    f"Lokasi: {storage.get('path', '-')}",
                    f"Total: {storage.get('total_gib', 0)} GiB",
                    f"Terpakai: {storage.get('used_gib', 0)} GiB ({storage.get('used_percent', 0)}%)",
                    f"Kosong: {storage.get('free_gib', 0)} GiB",
                    "",
                    f"Profil memori: {device.get('memory_tier', 'unknown')}",
                    f"Python runtime tersedia: {capabilities.get('python_runtime', False)}",
                    f"Folder kerja writable: {capabilities.get('writable_working_directory', False)}",
                    "",
                    "Data hanya dibaca secara lokal. Deteksi bukan jaminan kompatibilitas setiap fitur atau versi Windows.",
                ]
                show_text("\n".join(str(line) for line in lines))
            except Exception as exc:
                show_text(f"Snapshot gagal dibaca: {type(exc).__name__}: {exc}")

        tk.Button(
            toolbar, text="Perbarui informasi", command=refresh,
            bg=styles.CYAN, fg="#071014", relief="flat", padx=14, pady=8, cursor="hand2",
        ).pack(side="left")
        refresh()

    def page_network(
        self,
        parent: tk.Frame,
    ) -> None:
        """Interactive DNS, local-address, ping and TCP diagnostics."""
        self._page_title(
            parent,
            "Diagnostik Jaringan",
            "Utilitas diagnostik dasar. Tes koneksi menghubungi host/port yang lu masukkan; tidak memindai jaringan secara massal.",
        )
        controls = tk.Frame(parent, bg=styles.PANEL, highlightthickness=1, highlightbackground=styles.BORDER)
        controls.pack(fill="x", pady=(0, 12))
        tk.Label(controls, text="Host atau alamat IP", bg=styles.PANEL, fg=styles.MUTED).grid(
            row=0, column=0, sticky="w", padx=14, pady=(14, 4)
        )
        host_entry = tk.Entry(
            controls, bg=styles.ENTRY_BG, fg=styles.TEXT, insertbackground=styles.CYAN,
            relief="flat", font=styles.FONT_ENTRY,
        )
        host_entry.insert(0, "localhost")
        host_entry.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12), ipady=7)
        tk.Label(controls, text="Port TCP (untuk tes port)", bg=styles.PANEL, fg=styles.MUTED).grid(
            row=0, column=1, sticky="w", padx=14, pady=(14, 4)
        )
        port_entry = tk.Entry(
            controls, width=10, bg=styles.ENTRY_BG, fg=styles.TEXT, insertbackground=styles.CYAN,
            relief="flat", font=styles.FONT_ENTRY,
        )
        port_entry.insert(0, "443")
        port_entry.grid(row=1, column=1, sticky="ew", padx=14, pady=(0, 12), ipady=7)
        controls.columnconfigure(0, weight=1)

        output = tk.Text(
            parent, wrap="word", bg=styles.PANEL, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10),
        )
        output.pack(fill="both", expand=True)

        def render(title: str, lines: list[str]) -> None:
            output.delete("1.0", "end")
            output.insert("1.0", title + "\n" + "=" * 42 + "\n" + "\n".join(lines))

        def resolve() -> None:
            try:
                from chocobot.engine.network.diagnostics import lookup_host, local_network_info
                host = host_entry.get().strip()
                result = lookup_host(host)
                local = local_network_info()
                lines = [f"Host lokal: {local['hostname']}", "Alamat lokal yang terdeteksi:"]
                lines.extend("  " + address for address in local["addresses"] or ["Tidak tersedia"])
                lines.extend(["", f"Host target: {result['host']}"])
                if result["ok"]:
                    lines.append("Alamat hasil resolusi DNS:")
                    lines.extend("  " + address for address in result["addresses"])
                else:
                    lines.append(result["error"] or "Resolusi tidak berhasil.")
                lines.append("")
                lines.append("DNS menggunakan resolver sistem. Tidak ada permintaan HTTP yang dijalankan.")
                render("INFORMASI DNS DAN ALAMAT", lines)
            except (OSError, ValueError) as exc:
                messagebox.showerror("Diagnostik gagal", str(exc), parent=parent)

        def ping() -> None:
            try:
                from chocobot.engine.network.diagnostics import ping_host
                result = ping_host(host_entry.get().strip())
                render("HASIL PING", [
                    f"Host: {result['host']}",
                    f"Status: {'Berhasil' if result['ok'] else 'Tidak berhasil'}",
                    "",
                    result.get("output", ""),
                    "",
                    "Ping mengirim satu permintaan echo dan bukan pemeriksaan reputasi keamanan.",
                ])
            except (OSError, ValueError) as exc:
                messagebox.showerror("Ping gagal", str(exc), parent=parent)

        def tcp() -> None:
            try:
                from chocobot.engine.network.diagnostics import probe_tcp_port
                port = int(port_entry.get().strip())
                result = probe_tcp_port(host_entry.get().strip(), port)
                render("HASIL TES TCP", [
                    f"Host: {result['host']}",
                    f"Port: {result['port']}",
                    f"Status: {'Terhubung' if result['ok'] else 'Tidak terhubung'}",
                    result["message"],
                    "",
                    "Tes ini mencoba satu koneksi TCP dengan timeout terbatas.",
                ])
            except (OSError, ValueError) as exc:
                messagebox.showerror("Tes TCP gagal", str(exc), parent=parent)

        for label, command in (("DNS / IP lokal", resolve), ("Ping 1x", ping), ("Tes port TCP", tcp)):
            tk.Button(
                controls, text=label, command=command, bg=styles.CYAN if label == "DNS / IP lokal" else styles.PANEL,
                fg="#071014" if label == "DNS / IP lokal" else styles.TEXT,
                relief="flat", padx=12, pady=8, cursor="hand2",
            ).pack(side="left", padx=14, pady=(0, 14))
        render("DIAGNOSTIK SIAP", [
            "Masukkan host tanpa https:// atau path.",
            "Gunakan tes port hanya untuk host/perangkat yang memang berhak lu periksa.",
            "Tidak ada pemindaian massal dan tidak ada perubahan konfigurasi jaringan.",
        ])

    def page_monitor(
        self,
        parent: tk.Frame,
    ) -> None:
        """Display a manual, bounded snapshot of resource and process usage."""
        self._page_title(
            parent,
            "Monitor Sistem",
            "Snapshot CPU, RAM, disk, dan proses lokal. Pembaruan dilakukan hanya ketika tombol ditekan.",
        )
        toolbar = tk.Frame(parent, bg=styles.APP_BG)
        toolbar.pack(fill="x", pady=(0, 12))
        output = tk.Text(
            parent, wrap="none", bg=styles.PANEL, fg=styles.TEXT,
            insertbackground=styles.CYAN, relief="flat", font=("Consolas", 10),
        )
        output.pack(fill="both", expand=True)

        def show_text(value: str) -> None:
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.insert("1.0", value)
            output.configure(state="disabled")

        def refresh_resources() -> None:
            try:
                from chocobot.engine.system.resource_monitor import get_resource_snapshot
                snapshot = get_resource_snapshot(cpu_interval_seconds=0.2)
                cpu = snapshot.get("cpu", {})
                mem = snapshot.get("memory", {})
                disk = snapshot.get("storage", {})
                lines = [
                    "SNAPSHOT SUMBER DAYA",
                    "=" * 48,
                    f"Waktu lokal: {snapshot.get('timestamp', '-')}",
                    f"Platform: {snapshot.get('platform', '-')}",
                    f"CPU: {cpu.get('usage_percent') if cpu.get('usage_percent') is not None else 'tidak tersedia'}%",
                    f"Prosesor logis: {cpu.get('logical_processors', 0)}",
                    f"RAM terpakai: {mem.get('percent') if mem.get('percent') is not None else 'tidak tersedia'}%",
                    f"RAM digunakan: {mem.get('used_bytes', 0) / (1024**3):.2f} GiB",
                    f"RAM tersedia: {mem.get('available_bytes', 0) / (1024**3):.2f} GiB",
                    f"Disk terpakai: {disk.get('percent') if disk.get('percent') is not None else 'tidak tersedia'}%",
                    f"Lokasi disk: {disk.get('path', '-')}",
                    f"Disk terpakai: {disk.get('used_bytes', 0) / (1024**3):.2f} GiB",
                    f"Disk kosong: {disk.get('free_bytes', 0) / (1024**3):.2f} GiB",
                    "",
                    "Snapshot hanya mengamati metrik. Tidak ada proses dihentikan atau prioritas yang diubah.",
                ]
                show_text("\n".join(lines))
            except Exception as exc:
                show_text(f"Monitor sumber daya gagal: {type(exc).__name__}: {exc}")

        def refresh_processes() -> None:
            try:
                from chocobot.engine.system.process_monitor import get_process_snapshot
                snapshot = get_process_snapshot(limit=25)
                lines = [
                    "PROSES TERATAS BERDASARKAN MEMORI",
                    "=" * 76,
                    f"Proses ditampilkan: {snapshot.get('count', 0)}",
                    f"Platform: {snapshot.get('platform', '-')}",
                    "",
                    f"{'PID':>8}  {'MEMORI (MiB)':>14}  NAMA PROSES",
                    "-" * 76,
                ]
                for item in snapshot.get("processes", []):
                    lines.append(
                        f"{item.get('pid', 0):>8}  {item.get('memory_bytes', 0) / (1024**2):>14.1f}  {item.get('name', 'unknown')}"
                    )
                lines.extend([
                    "",
                    "Daftar ini bersifat observasi lokal. Tidak ada proses yang dihentikan atau dimodifikasi.",
                ])
                show_text("\n".join(lines))
            except Exception as exc:
                show_text(f"Daftar proses gagal dibaca: {type(exc).__name__}: {exc}")

        for label, command in (
            ("Snapshot CPU / RAM / Disk", refresh_resources),
            ("Daftar proses", refresh_processes),
        ):
            tk.Button(
                toolbar, text=label, command=command,
                bg=styles.CYAN if label.startswith("Snapshot") else styles.PANEL,
                fg="#071014" if label.startswith("Snapshot") else styles.TEXT,
                relief="flat", padx=12, pady=8, cursor="hand2",
            ).pack(side="left", padx=(0, 8))
        refresh_resources()

    def page_settings(
        self,
        parent: tk.Frame,
    ) -> None:
        """Settings page."""

        self._page_title(
            parent,
            "Settings",
            "Application preferences and interface configuration",
        )

        # Settings overview
        overview = tk.Frame(
            parent,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        overview.pack(
            fill="x",
            pady=(0, 15),
        )

        tk.Frame(
            overview,
            bg=styles.PURPLE,
            width=3,
        ).pack(
            side="left",
            fill="y",
        )

        body = tk.Frame(
            overview,
            bg=styles.PANEL,
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=16,
        )

        tk.Label(
            body,
            text="APPLICATION CONFIGURATION",
            fg=styles.MUTED,
            bg=styles.PANEL,
            font=styles.FONT_STATUS_TITLE,
        ).pack(
            anchor="w",
        )

        tk.Label(
            body,
            text="Local configuration • No cloud synchronization",
            fg=styles.TEXT,
            bg=styles.PANEL,
            font=styles.FONT_ENTRY,
        ).pack(
            anchor="w",
            pady=(5, 0),
        )

        f = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        f.pack(
            fill="both",
            expand=True,
        )

        self._card_grid(
            f,
            [
                (
                    "Language",
                    "Indonesian / English",
                    styles.CYAN,
                ),
                (
                    "Appearance",
                    "Visual appearance settings",
                    styles.PURPLE,
                ),
                (
                    "Notifications",
                    "Notification preferences",
                    styles.YELLOW,
                ),
                (
                    "Feature Settings",
                    "Feature configuration",
                    styles.GREEN,
                ),
            ],
            "settings",
            columns=2,
        )

    # ==================================================================
    # BLOG
    # ==================================================================

    def page_blog(
        self,
        parent: tk.Frame,
    ) -> None:
        """Official blog page."""

        self._page_title(
            parent,
            self.t("blog_title"),
            self.t("blog_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("blog_summary"),
            const.BLOG_HOME_URL,
            self.t("open_blog"),
        )

    # ==================================================================
    # GUIDE
    # ==================================================================

    def page_guide(
        self,
        parent: tk.Frame,
    ) -> None:
        """User guide page."""

        self._page_title(
            parent,
            self.t("guide_title"),
            self.t("guide_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("guide_summary"),
            const.USER_GUIDE_URL,
            self.t("open_guide"),
        )

    # ==================================================================
    # DEVELOPER
    # ==================================================================

    def page_developer(
        self,
        parent: tk.Frame,
    ) -> None:
        """Developer page."""

        self._page_title(
            parent,
            self.t("developer_title"),
            self.t("developer_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("developer_summary"),
            const.DEVELOPER_URL,
            self.t("open_developer"),
        )

    # ==================================================================
    # ABOUT
    # ==================================================================

    def page_about(
        self,
        parent: tk.Frame,
    ) -> None:
        """About page."""

        self._page_title(
            parent,
            self.t("about_title"),
            self.t("about_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("about_summary"),
            const.ABOUT_URL,
            self.t("open_about"),
        )

    # ==================================================================
    # LICENSE
    # ==================================================================

    def page_license(
        self,
        parent: tk.Frame,
    ) -> None:
        """License page."""

        self._page_title(
            parent,
            self.t("license_title"),
            self.t("license_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("license_summary"),
            const.LICENSE_URL,
            self.t("open_license"),
        )

    # ==================================================================
    # CONTACT
    # ==================================================================

    def page_contact(
        self,
        parent: tk.Frame,
    ) -> None:
        """Contact page."""

        self._page_title(
            parent,
            self.t("contact_title"),
            self.t("contact_subtitle"),
        )

        self._info_with_link(
            parent,
            self.t("contact_summary"),
            const.CONTACT_URL,
            self.t("open_contact"),
        )

    # ==================================================================
    # RUN
    # ==================================================================

    def run(self) -> None:
        """Start Tkinter main loop."""

        self.root.mainloop()


# ======================================================================
# DIRECT EXECUTION
# ======================================================================

if __name__ == "__main__":
    app = ChocobotApp()
    app.run()
