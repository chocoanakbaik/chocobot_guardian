
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
            "protected": "Terlindungi",
            "interface_ready":
                "Antarmuka siap • Mode local-first",

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

        lang_file = const.LANGUAGE_DIR / f"{lang}.json"

        if lang_file.exists():
            try:
                with open(
                    lang_file,
                    "r",
                    encoding="utf-8",
                ) as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    default_texts.update(data)

            except Exception:
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
        """Security center interface."""

        self._page_title(
            parent,
            "Security Center",
            "Security tools and protection interface",
        )

        f = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        f.pack(
            fill="both",
            expand=True,
        )

        items = [
            (
                "Quick Scan",
                "Start a standard security scan workflow",
                styles.RED,
            ),
            (
                "Custom Scan",
                "Choose scan scope and options",
                styles.MAGENTA,
            ),
            (
                "File Analysis",
                "Inspect a selected file",
                styles.PURPLE,
            ),
            (
                "Quarantine",
                "View isolated suspicious files",
                styles.YELLOW,
            ),
            (
                "Whitelist",
                "Manage trusted items",
                styles.GREEN,
            ),
            (
                "Security Report",
                "View analysis summaries and results",
                styles.CYAN,
            ),
        ]

        self._card_grid(
            f,
            items,
            "security",
            columns=2,
        )

    # ==================================================================
    # LINK INSPECTOR
    # ==================================================================

    def page_link(
        self,
        parent: tk.Frame,
    ) -> None:
        """Link inspector."""

        self._page_title(
            parent,
            "Link Inspector",
            "Detailed URL analysis interface",
        )

        box = tk.Frame(
            parent,
            bg=styles.PANEL,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        box.pack(
            fill="x",
            pady=(0, 14),
        )

        tk.Label(
            box,
            text=self.t("url_label"),
            fg=styles.MUTED,
            bg=styles.PANEL,
            font=styles.FONT_SUBTITLE,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 6),
        )

        entry_frame = tk.Frame(
            box,
            bg=styles.ENTRY_BG,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
        )

        entry_frame.pack(
            fill="x",
            padx=18,
        )

        entry = tk.Entry(
            entry_frame,
            bg=styles.ENTRY_BG,
            fg=styles.TEXT,
            insertbackground=styles.CYAN,
            selectbackground=styles.CYAN,
            selectforeground="#071014",
            relief="flat",
            bd=0,
            font=styles.FONT_ENTRY,
        )

        entry.pack(
            fill="x",
            ipady=10,
            padx=10,
        )

        entry.insert(
            0,
            "https://example.com/path?query=value",
        )

        def analyze():
            self.link_result.configure(
                text=(
                    "Analysis placeholder — "
                    "backend will be connected later"
                ),
                fg=styles.CYAN,
            )

        RoundedButton(
            box,
            text=self.t("analyze"),
            command=analyze,
            width=130,
            height=34,
            bg=styles.CYAN,
            fg="#071014",
        ).pack(
            anchor="w",
            padx=18,
            pady=12,
        )

        self.link_result = tk.Label(
            parent,
            text=self.t("result_area"),
            fg=styles.MUTED,
            bg=styles.APP_BG,
            font=styles.FONT_SUBTITLE,
        )

        self.link_result.pack(
            anchor="w",
            pady=(5, 8),
        )

        r = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        r.pack(
            fill="both",
            expand=True,
        )

        cards = [
            (
                "URL Structure",
                "Protocol, domain, subdomain, port, "
                "path, query and fragment",
                styles.CYAN,
            ),
            (
                "Suspicious Patterns",
                "Pattern indicators and brand "
                "impersonation indicators",
                styles.RED,
            ),
            (
                "Risk Score",
                "Score range, Risk Level "
                "and explanation",
                styles.YELLOW,
            ),
        ]

        for i, (
            title,
            description,
            accent,
        ) in enumerate(cards):

            r.grid_columnconfigure(
                i,
                weight=1,
                uniform="link",
            )

            wrapper = self._create_card_wrapper(
                r,
                title=title,
                text=description,
                accent=accent,
                command=None,
                width=300,
                height=115,
            )

            wrapper.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(
                    (0, 7)
                    if i == 0
                    else (
                        7 if i == 1
                        else (7, 0)
                    )
                ),
            )

    # ==================================================================
    # FILE TOOLS
    # ==================================================================

    def page_files(
        self,
        parent: tk.Frame,
    ) -> None:
        """File utility interface."""

        self._page_title(
            parent,
            "File Tools",
            "File and folder utility interface",
        )

        f = tk.Frame(
            parent,
            bg=styles.APP_BG,
        )

        f.pack(
            fill="both",
            expand=True,
        )

        items = [
            (
                "File Information",
                "Name, size, format, location and date",
                styles.CYAN,
            ),
            (
                "File Analysis",
                "Analysis result and file metadata",
                styles.PURPLE,
            ),
            (
                "Folder Analysis",
                "Inspect folder contents",
                styles.MAGENTA,
            ),
            (
                "File Search",
                "Find files by selected criteria",
                styles.GREEN,
            ),
            (
                "Hash / SHA-256",
                "Hash generation and verification",
                styles.YELLOW,
            ),
            (
                "Large File Check",
                "Identify large files",
                styles.RED,
            ),
        ]

        self._card_grid(
            f,
            items,
            "files",
            columns=2,
        )

    # ==================================================================
    # CONVERTER
    # ==================================================================

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
        """System page."""

        self._simple_info(
            parent,
            "System",
            "Windows version, architecture, CPU, RAM, "
            "storage and device information",
            [
                (
                    "Windows",
                    "Operating system details",
                ),
                (
                    "Architecture",
                    "System architecture",
                ),
                (
                    "CPU",
                    "Processor information",
                ),
                (
                    "RAM",
                    "Memory information",
                ),
                (
                    "Storage",
                    "Storage overview",
                ),
            ],
        )

    # ==================================================================
    # NETWORK
    # ==================================================================

    def page_network(
        self,
        parent: tk.Frame,
    ) -> None:
        """Network page."""

        self._simple_info(
            parent,
            "Network",
            "Basic network diagnostics and inspection",
            [
                (
                    "IP Information",
                    "IP details",
                ),
                (
                    "DNS Lookup",
                    "DNS query interface",
                ),
                (
                    "Ping",
                    "Connectivity test interface",
                ),
                (
                    "Connection Information",
                    "Current connection view",
                ),
                (
                    "Port Inspection",
                    "Basic port inspection",
                ),
            ],
        )

    # ==================================================================
    # MONITOR
    # ==================================================================

    def page_monitor(
        self,
        parent: tk.Frame,
    ) -> None:
        """Monitor page."""

        self._simple_info(
            parent,
            "Monitor",
            "Process and system monitoring interface",
            [
                (
                    "Process Monitor",
                    "Process list and status",
                ),
                (
                    "CPU",
                    "CPU usage view",
                ),
                (
                    "RAM",
                    "Memory usage view",
                ),
                (
                    "Disk",
                    "Disk activity view",
                ),
                (
                    "Network Usage",
                    "Network activity view",
                ),
            ],
        )

    # ==================================================================
    # SETTINGS
    # ==================================================================

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
