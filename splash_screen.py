# -*- coding: utf-8 -*-
"""
splash_screen.py
Chocobot Guardian — Futuristic Startup Experience

Splash screen utama Chocobot Guardian.

Karakteristik:
- Pure Tkinter.
- Tidak membutuhkan server/API.
- Tidak melakukan instalasi package saat startup.
- Mendukung logo PNG.
- Otomatis mencoba membuat ICO untuk Windows.
- Fade in / fade out.
- Animated progress.
- Animated scan line.
- Animated glow.
- Status startup dinamis.
- Tetap kompatibel dengan main.py lama.

Public API yang dipertahankan:

    show_splash(
        duration_ms=2500,
        logo_path=...,
        bg_color="#0d0d0d",
        text_color="#00ffcc",
        app_name="Chocobot Guardian",
        version="1.0 Beta",
    )
"""

from __future__ import annotations

import math
import os
import sys
import time
import tkinter as tk
from pathlib import Path
from typing import Optional


# ============================================================================
# KONFIGURASI VISUAL
# ============================================================================

BG_COLOR = "#070a0e"
PANEL_COLOR = "#0b1015"
PANEL_2_COLOR = "#0e151c"

CYAN = "#00e5ff"
CYAN_SOFT = "#6ff7ff"
CYAN_DARK = "#07343c"

PURPLE = "#9b6cff"
MAGENTA = "#ff3cac"

TEXT = "#edfaff"
MUTED = "#71818e"
MUTED_2 = "#43515c"

WHITE = "#ffffff"

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 440

FPS_MS = 16

FADE_IN_MS = 420
FADE_OUT_MS = 360

GLOW_STEPS = 8
PROGRESS_STEPS = 120

CORNER_RADIUS = 24


# ============================================================================
# UTILITAS
# ============================================================================

def _clamp(value: float, minimum: float, maximum: float) -> float:
    """Membatasi nilai ke rentang tertentu."""
    return max(minimum, min(maximum, value))


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    """Mengubah HEX menjadi RGB."""
    value = value.lstrip("#")

    if len(value) != 6:
        return 0, 0, 0

    try:
        return (
            int(value[0:2], 16),
            int(value[2:4], 16),
            int(value[4:6], 16),
        )
    except ValueError:
        return 0, 0, 0


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Mengubah RGB menjadi HEX."""
    r, g, b = rgb

    r = int(_clamp(r, 0, 255))
    g = int(_clamp(g, 0, 255))
    b = int(_clamp(b, 0, 255))

    return f"#{r:02x}{g:02x}{b:02x}"


def _blend(
    first: str,
    second: str,
    amount: float,
) -> str:
    """Interpolasi warna HEX."""
    amount = _clamp(amount, 0.0, 1.0)

    r1, g1, b1 = _hex_to_rgb(first)
    r2, g2, b2 = _hex_to_rgb(second)

    return _rgb_to_hex(
        (
            r1 + (r2 - r1) * amount,
            g1 + (g2 - g1) * amount,
            b1 + (b2 - b1) * amount,
        )
    )


def _ease_out_cubic(value: float) -> float:
    """Kurva easing halus."""
    value = _clamp(value, 0.0, 1.0)
    return 1.0 - pow(1.0 - value, 3)


def _ease_in_out(value: float) -> float:
    """Ease in/out sederhana."""
    value = _clamp(value, 0.0, 1.0)

    if value < 0.5:
        return 4.0 * value * value * value

    return 1.0 - pow(-2.0 * value + 2.0, 3) / 2.0


def _rounded_rectangle(
    canvas: tk.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    radius: float,
    **kwargs,
) -> int:
    """
    Menggambar rounded rectangle menggunakan Canvas polygon + arcs.

    Tkinter Canvas tidak mempunyai rounded_rectangle native,
    sehingga bentuk dibuat dari beberapa bagian.
    """
    radius = min(
        radius,
        abs(x2 - x1) / 2,
        abs(y2 - y1) / 2,
    )

    points = [
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=24,
        **kwargs,
    )


# ============================================================================
# PENCARIAN LOGO
# ============================================================================

def _resolve_logo_path(
    logo_path: Optional[Path | str],
) -> Optional[Path]:
    """
    Mencari logo dari beberapa kemungkinan lokasi.

    Ini sengaja dibuat robust karena project Chocobot saat ini
    memiliki kemungkinan logo berada di:

        chocobot/assets/images/logo.png

    maupun:

        project_root/assets/images/logo.png
    """

    candidates: list[Path] = []

    if logo_path:
        try:
            candidates.append(Path(logo_path))
        except (TypeError, ValueError):
            pass

    current_file = Path(__file__).resolve()

    # Folder chocobot/
    package_dir = current_file.parent

    # Root project/
    project_dir = package_dir.parent

    # Kemungkinan langsung di package.
    candidates.extend(
        [
            package_dir / "assets" / "images" / "logo.png",
            package_dir / "assets" / "logo.png",
            project_dir / "assets" / "images" / "logo.png",
            project_dir / "assets" / "logo.png",
        ]
    )

    checked: set[str] = set()

    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue

        key = str(candidate).lower()

        if key in checked:
            continue

        checked.add(key)

        if candidate.is_file():
            return candidate

    return None


# ============================================================================
# PILLOW / IMAGE SUPPORT
# ============================================================================

def _load_pillow():
    """
    Mencoba memuat Pillow.

    Tidak pernah melakukan pip install otomatis.

    Return:
        Image, ImageTk jika tersedia.
        (None, None) jika Pillow tidak tersedia.
    """
    try:
        from PIL import Image, ImageTk

        return Image, ImageTk
    except ImportError:
        return None, None


def _create_ico_from_png(
    png_path: Path,
    ico_path: Path,
) -> Optional[Path]:
    """
    Membuat file ICO dari PNG jika Pillow tersedia.

    Jika gagal, fungsi hanya mengembalikan None.
    Splash tetap dapat berjalan.
    """
    Image, _ = _load_pillow()

    if Image is None:
        return None

    try:
        ico_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.open(png_path).convert("RGBA")

        sizes = [
            (256, 256),
            (128, 128),
            (64, 64),
            (48, 48),
            (32, 32),
            (24, 24),
            (16, 16),
        ]

        image.save(
            ico_path,
            format="ICO",
            sizes=sizes,
        )

        return ico_path if ico_path.exists() else None

    except Exception:
        return None


def _prepare_icon(
    logo_path: Optional[Path],
) -> Optional[Path]:
    """
    Menyiapkan ICO untuk Windows.

    ICO disimpan di:

        assets/icons/logo.ico

    berdasarkan lokasi logo yang ditemukan.
    """
    if logo_path is None:
        return None

    try:
        icon_dir = logo_path.parent.parent / "icons"
        ico_path = icon_dir / "logo.ico"

        if ico_path.exists():
            try:
                if ico_path.stat().st_mtime >= logo_path.stat().st_mtime:
                    return ico_path
            except OSError:
                pass

        return _create_ico_from_png(
            logo_path,
            ico_path,
        )

    except Exception:
        return None


# ============================================================================
# WINDOW POSITION
# ============================================================================

def _center_window(
    window: tk.Tk,
    width: int,
    height: int,
) -> None:
    """Memusatkan splash screen pada monitor aktif."""
    try:
        window.update_idletasks()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = max(
            0,
            int((screen_width - width) / 2),
        )

        y = max(
            0,
            int((screen_height - height) / 2),
        )

        window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    except Exception:
        window.geometry(
            f"{width}x{height}"
        )


# ============================================================================
# SPLASH SCREEN CLASS
# ============================================================================

class FuturisticSplash:
    """
    Engine visual splash screen Chocobot Guardian.

    Semua animasi dijalankan melalui Tkinter after(),
    sehingga tidak membutuhkan thread tambahan.
    """

    def __init__(
        self,
        root: tk.Tk,
        logo_path: Optional[Path],
        bg_color: str,
        text_color: str,
        app_name: str,
        version: str,
        duration_ms: int,
    ) -> None:

        self.root = root

        self.logo_path = logo_path
        self.bg_color = bg_color or BG_COLOR
        self.text_color = text_color or CYAN
        self.app_name = app_name or "Chocobot Guardian"
        self.version = version or ""
        self.duration_ms = max(
            1000,
            int(duration_ms or 2500),
        )

        self.start_time = time.perf_counter()

        self.animation_job = None
        self.fade_job = None
        self.close_job = None

        self.finished = False
        self.closing = False

        self.progress = 0.0
        self.scan_position = 0.0
        self.pulse_phase = 0.0
        self.rotation_phase = 0.0

        self.logo_image = None

        self.canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            highlightthickness=0,
            bd=0,
        )

        self.canvas.pack(
            fill="both",
            expand=True,
        )

        self._configure_window()
        self._load_logo()
        self._build_scene()
        self._start_animations()

    # ------------------------------------------------------------------
    # WINDOW
    # ------------------------------------------------------------------

    def _configure_window(self) -> None:
        """Konfigurasi jendela splash."""

        self.root.overrideredirect(True)

        try:
            self.root.resizable(False, False)
        except Exception:
            pass

        try:
            self.root.attributes(
                "-alpha",
                0.0,
            )
        except tk.TclError:
            pass

        try:
            self.root.attributes(
                "-topmost",
                True,
            )
        except tk.TclError:
            pass

        _center_window(
            self.root,
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self._set_window_icon()

    def _set_window_icon(self) -> None:
        """Memasang icon window."""
        if self.logo_path is None:
            return

        ico_path = _prepare_icon(
            self.logo_path
        )

        if ico_path and os.name == "nt":
            try:
                self.root.iconbitmap(
                    str(ico_path)
                )
                return
            except Exception:
                pass

        Image, ImageTk = _load_pillow()

        if Image is None or ImageTk is None:
            return

        try:
            image = Image.open(
                self.logo_path
            ).convert("RGBA")

            image.thumbnail(
                (64, 64),
                Image.LANCZOS,
            )

            self.window_icon_image = ImageTk.PhotoImage(
                image
            )

            self.root.iconphoto(
                True,
                self.window_icon_image,
            )

        except Exception:
            pass

    # ------------------------------------------------------------------
    # LOGO
    # ------------------------------------------------------------------

    def _load_logo(self) -> None:
        """Memuat logo PNG jika Pillow tersedia."""

        if self.logo_path is None:
            return

        Image, ImageTk = _load_pillow()

        if Image is None or ImageTk is None:
            return

        try:
            image = Image.open(
                self.logo_path
            ).convert("RGBA")

            image.thumbnail(
                (180, 180),
                Image.LANCZOS,
            )

            self.logo_image = ImageTk.PhotoImage(
                image
            )

        except Exception:
            self.logo_image = None

    # ------------------------------------------------------------------
    # SCENE
    # ------------------------------------------------------------------

    def _build_scene(self) -> None:
        """Membangun seluruh elemen visual splash."""

        width = WINDOW_WIDTH
        height = WINDOW_HEIGHT

        # --------------------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------------------

        self.canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=self.bg_color,
            outline="",
        )

        # Background atmospheric glow.
        self._draw_background_glow()

        # Grid futuristik.
        self._draw_grid()

        # Outer frame.
        self.canvas.create_rectangle(
            1,
            1,
            width - 2,
            height - 2,
            outline=_blend(
                self.bg_color,
                CYAN,
                0.18,
            ),
            width=1,
        )

        # Inner frame.
        self.canvas.create_rectangle(
            10,
            10,
            width - 10,
            height - 10,
            outline=_blend(
                self.bg_color,
                PURPLE,
                0.13,
            ),
            width=1,
        )

        # Corner decorations.
        self._draw_corner_decorations()

        # --------------------------------------------------------------
        # TOP STATUS
        # --------------------------------------------------------------

        self.status_dot = self.canvas.create_oval(
            34,
            31,
            41,
            38,
            fill=CYAN,
            outline="",
        )

        self.canvas.create_text(
            51,
            35,
            text="LOCAL CORE",
            anchor="w",
            fill=CYAN_SOFT,
            font=("Segoe UI", 8, "bold"),
        )

        self.canvas.create_text(
            width - 34,
            35,
            text="OFFLINE / SECURE",
            anchor="e",
            fill=MUTED,
            font=("Segoe UI", 8, "bold"),
        )

        # --------------------------------------------------------------
        # CENTRAL LOGO AREA
        # --------------------------------------------------------------

        self.logo_glow_items = []

        center_x = width / 2
        center_y = 170

        # Glow layers.
        glow_colors = [
            _blend(
                self.bg_color,
                CYAN,
                0.035,
            ),
            _blend(
                self.bg_color,
                CYAN,
                0.055,
            ),
            _blend(
                self.bg_color,
                CYAN,
                0.075,
            ),
            _blend(
                self.bg_color,
                PURPLE,
                0.055,
            ),
        ]

        glow_sizes = [
            178,
            166,
            154,
            142,
        ]

        for size, color in zip(
            glow_sizes,
            glow_colors,
        ):
            half = size / 2

            item = self.canvas.create_oval(
                center_x - half,
                center_y - half,
                center_x + half,
                center_y + half,
                fill=color,
                outline="",
            )

            self.logo_glow_items.append(item)

        # Outer tech ring.
        self.outer_ring = self.canvas.create_oval(
            center_x - 108,
            center_y - 108,
            center_x + 108,
            center_y + 108,
            outline=_blend(
                self.bg_color,
                CYAN,
                0.22,
            ),
            width=1,
        )

        self.inner_ring = self.canvas.create_oval(
            center_x - 96,
            center_y - 96,
            center_x + 96,
            center_y + 96,
            outline=_blend(
                self.bg_color,
                PURPLE,
                0.20,
            ),
            width=1,
        )

        # Logo.
        if self.logo_image is not None:
            self.logo_canvas_item = self.canvas.create_image(
                center_x,
                center_y,
                image=self.logo_image,
            )
        else:
            self.logo_canvas_item = None

            # Fallback jika logo tidak tersedia.
            self.canvas.create_oval(
                center_x - 58,
                center_y - 58,
                center_x + 58,
                center_y + 58,
                fill=PANEL_2_COLOR,
                outline=CYAN,
                width=2,
            )

            self.canvas.create_text(
                center_x,
                center_y - 5,
                text="C",
                fill=CYAN,
                font=("Segoe UI", 38, "bold"),
            )

            self.canvas.create_text(
                center_x,
                center_y + 28,
                text="CH",
                fill=MUTED,
                font=("Segoe UI", 7, "bold"),
            )

        # Scan line.
        self.scan_line = self.canvas.create_line(
            center_x - 82,
            center_y - 82,
            center_x + 82,
            center_y - 82,
            fill=_blend(
                self.bg_color,
                CYAN,
                0.48,
            ),
            width=1,
        )

        # --------------------------------------------------------------
        # APP TITLE
        # --------------------------------------------------------------

        self.canvas.create_text(
            center_x,
            286,
            text=self.app_name,
            fill=TEXT,
            font=("Segoe UI", 21, "bold"),
        )

        self.canvas.create_text(
            center_x,
            311,
            text="GUARDIAN  •  LOCAL WINDOWS PLATFORM",
            fill=MUTED,
            font=("Segoe UI", 8, "bold"),
        )

        # Version.
        version_text = self.version.strip()

        if version_text:
            self.canvas.create_text(
                center_x,
                333,
                text=version_text.upper(),
                fill=_blend(
                    MUTED,
                    CYAN,
                    0.45,
                ),
                font=("Segoe UI", 7, "bold"),
            )

        # --------------------------------------------------------------
        # PROGRESS AREA
        # --------------------------------------------------------------

        self.progress_x1 = 165
        self.progress_x2 = width - 165
        self.progress_y = 363

        # Track.
        self.canvas.create_line(
            self.progress_x1,
            self.progress_y,
            self.progress_x2,
            self.progress_y,
            fill=MUTED_2,
            width=3,
        )

        self.progress_fill = self.canvas.create_line(
            self.progress_x1,
            self.progress_y,
            self.progress_x1,
            self.progress_y,
            fill=CYAN,
            width=3,
        )

        # Progress percentage.
        self.progress_text = self.canvas.create_text(
            width / 2,
            385,
            text="0%",
            fill=MUTED,
            font=("Segoe UI", 8, "bold"),
        )

        # Startup status.
        self.status_text = self.canvas.create_text(
            self.progress_x1,
            385,
            text="INITIALIZING...",
            anchor="w",
            fill=MUTED,
            font=("Segoe UI", 7),
        )

        # Bottom brand.
        self.canvas.create_text(
            width - 34,
            406,
            text="CHOCOENGINE",
            anchor="e",
            fill=_blend(
                MUTED_2,
                CYAN,
                0.25,
            ),
            font=("Segoe UI", 7, "bold"),
        )

        self.canvas.create_text(
            34,
            406,
            text="ZERO API  •  ZERO SERVER",
            anchor="w",
            fill=MUTED_2,
            font=("Segoe UI", 7, "bold"),
        )

    # ------------------------------------------------------------------
    # BACKGROUND
    # ------------------------------------------------------------------

    def _draw_background_glow(self) -> None:
        """Membuat atmospheric background."""
        cx = WINDOW_WIDTH / 2
        cy = 155

        layers = [
            (420, _blend(self.bg_color, CYAN, 0.018)),
            (350, _blend(self.bg_color, CYAN, 0.024)),
            (280, _blend(self.bg_color, PURPLE, 0.020)),
            (220, _blend(self.bg_color, CYAN, 0.025)),
        ]

        for size, color in layers:
            half = size / 2

            self.canvas.create_oval(
                cx - half,
                cy - half,
                cx + half,
                cy + half,
                fill=color,
                outline="",
            )

    def _draw_grid(self) -> None:
        """Grid tipis di background."""

        spacing = 36

        for x in range(
            18,
            WINDOW_WIDTH - 18,
            spacing,
        ):
            self.canvas.create_line(
                x,
                18,
                x,
                WINDOW_HEIGHT - 18,
                fill=_blend(
                    self.bg_color,
                    CYAN,
                    0.025,
                ),
                width=1,
            )

        for y in range(
            18,
            WINDOW_HEIGHT - 18,
            spacing,
        ):
            self.canvas.create_line(
                18,
                y,
                WINDOW_WIDTH - 18,
                y,
                fill=_blend(
                    self.bg_color,
                    CYAN,
                    0.025,
                ),
                width=1,
            )

    def _draw_corner_decorations(self) -> None:
        """Dekorasi sudut ala futuristic HUD."""

        length = 28
        offset = 18

        color = _blend(
            self.bg_color,
            CYAN,
            0.42,
        )

        # Top-left.
        self.canvas.create_line(
            offset,
            offset,
            offset + length,
            offset,
            fill=color,
            width=2,
        )

        self.canvas.create_line(
            offset,
            offset,
            offset,
            offset + length,
            fill=color,
            width=2,
        )

        # Top-right.
        self.canvas.create_line(
            WINDOW_WIDTH - offset,
            offset,
            WINDOW_WIDTH - offset - length,
            offset,
            fill=color,
            width=2,
        )

        self.canvas.create_line(
            WINDOW_WIDTH - offset,
            offset,
            WINDOW_WIDTH - offset,
            offset + length,
            fill=color,
            width=2,
        )

        # Bottom-left.
        self.canvas.create_line(
            offset,
            WINDOW_HEIGHT - offset,
            offset + length,
            WINDOW_HEIGHT - offset,
            fill=color,
            width=2,
        )

        self.canvas.create_line(
            offset,
            WINDOW_HEIGHT - offset,
            offset,
            WINDOW_HEIGHT - offset - length,
            fill=color,
            width=2,
        )

        # Bottom-right.
        self.canvas.create_line(
            WINDOW_WIDTH - offset,
            WINDOW_HEIGHT - offset,
            WINDOW_WIDTH - offset - length,
            WINDOW_HEIGHT - offset,
            fill=color,
            width=2,
        )

        self.canvas.create_line(
            WINDOW_WIDTH - offset,
            WINDOW_HEIGHT - offset,
            WINDOW_WIDTH - offset,
            WINDOW_HEIGHT - offset - length,
            fill=color,
            width=2,
        )

    # ------------------------------------------------------------------
    # ANIMATION START
    # ------------------------------------------------------------------

    def _start_animations(self) -> None:
        """Memulai semua animasi."""

        self._fade_in()

        self.animation_job = self.root.after(
            FPS_MS,
            self._animation_loop,
        )

        # Durasi utama splash.
        self.close_job = self.root.after(
            self.duration_ms,
            self.finish,
        )

    # ------------------------------------------------------------------
    # MAIN ANIMATION LOOP
    # ------------------------------------------------------------------

    def _animation_loop(self) -> None:
        """Loop animasi utama."""

        if self.finished:
            return

        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        self.pulse_phase += 0.075
        self.scan_position += 0.018
        self.rotation_phase += 0.035

        if self.scan_position > 1.0:
            self.scan_position = 0.0

        # --------------------------------------------------------------
        # PROGRESS
        # --------------------------------------------------------------

        usable_time = max(
            1,
            self.duration_ms - 600,
        )

        raw_progress = (
            elapsed * 1000.0
        ) / usable_time

        # Jangan langsung menyentuh 100%.
        self.progress = _clamp(
            raw_progress,
            0.0,
            0.96,
        )

        eased_progress = _ease_out_cubic(
            self.progress
        )

        self._update_progress(
            eased_progress
        )

        # --------------------------------------------------------------
        # LOGO GLOW
        # --------------------------------------------------------------

        self._update_logo_glow()

        # --------------------------------------------------------------
        # SCAN LINE
        # --------------------------------------------------------------

        self._update_scan_line()

        # --------------------------------------------------------------
        # STATUS DOT
        # --------------------------------------------------------------

        self._update_status_dot()

        # --------------------------------------------------------------
        # STATUS TEXT
        # --------------------------------------------------------------

        self._update_status(
            self.progress
        )

        self.animation_job = self.root.after(
            FPS_MS,
            self._animation_loop,
        )

    # ------------------------------------------------------------------
    # PROGRESS
    # ------------------------------------------------------------------

    def _update_progress(
        self,
        progress: float,
    ) -> None:
        """Update progress bar."""

        x1 = self.progress_x1
        x2 = self.progress_x1 + (
            self.progress_x2
            - self.progress_x1
        ) * progress

        self.canvas.coords(
            self.progress_fill,
            x1,
            self.progress_y,
            x2,
            self.progress_y,
        )

        percentage = int(
            _clamp(
                progress * 100,
                0,
                100,
            )
        )

        self.canvas.itemconfigure(
            self.progress_text,
            text=f"{percentage}%",
        )

    # ------------------------------------------------------------------
    # LOGO GLOW
    # ------------------------------------------------------------------

    def _update_logo_glow(self) -> None:
        """Animasi pulsasi glow logo."""

        pulse = (
            math.sin(self.pulse_phase)
            + 1.0
        ) / 2.0

        colors = [
            _blend(
                self.bg_color,
                CYAN,
                0.028 + pulse * 0.020,
            ),
            _blend(
                self.bg_color,
                CYAN,
                0.045 + pulse * 0.025,
            ),
            _blend(
                self.bg_color,
                CYAN,
                0.060 + pulse * 0.030,
            ),
            _blend(
                self.bg_color,
                PURPLE,
                0.045 + pulse * 0.020,
            ),
        ]

        for item, color in zip(
            self.logo_glow_items,
            colors,
        ):
            self.canvas.itemconfigure(
                item,
                fill=color,
            )

        # Outer ring opacity illusion.
        ring_amount = 0.18 + (
            pulse * 0.18
        )

        self.canvas.itemconfigure(
            self.outer_ring,
            outline=_blend(
                self.bg_color,
                CYAN,
                ring_amount,
            ),
        )

        inner_amount = 0.16 + (
            (1.0 - pulse) * 0.16
        )

        self.canvas.itemconfigure(
            self.inner_ring,
            outline=_blend(
                self.bg_color,
                PURPLE,
                inner_amount,
            ),
        )

    # ------------------------------------------------------------------
    # SCAN LINE
    # ------------------------------------------------------------------

    def _update_scan_line(self) -> None:
        """Gerakan scan line melewati logo."""

        center_x = WINDOW_WIDTH / 2
        center_y = 170

        start = -82
        end = 82

        y = center_y + (
            start
            + (end - start)
            * self.scan_position
        )

        # Sedikit easing agar gerak tidak terlalu mekanis.
        eased = _ease_in_out(
            self.scan_position
        )

        y = center_y + (
            start
            + (end - start)
            * eased
        )

        self.canvas.coords(
            self.scan_line,
            center_x - 82,
            y,
            center_x + 82,
            y,
        )

        glow_amount = 0.32 + (
            0.20
            * math.sin(
                self.pulse_phase
            )
            + 0.20
        )

        self.canvas.itemconfigure(
            self.scan_line,
            fill=_blend(
                self.bg_color,
                CYAN,
                _clamp(
                    glow_amount,
                    0.20,
                    0.70,
                ),
            ),
        )

    # ------------------------------------------------------------------
    # STATUS DOT
    # ------------------------------------------------------------------

    def _update_status_dot(self) -> None:
        """Animasi indikator status."""

        pulse = (
            math.sin(
                self.pulse_phase * 1.4
            )
            + 1.0
        ) / 2.0

        color = _blend(
            CYAN_DARK,
            CYAN,
            0.45 + pulse * 0.55,
        )

        self.canvas.itemconfigure(
            self.status_dot,
            fill=color,
        )

    # ------------------------------------------------------------------
    # STATUS TEXT
    # ------------------------------------------------------------------

    def _update_status(
        self,
        progress: float,
    ) -> None:
        """Mengubah status berdasarkan progress."""

        if progress < 0.15:
            text = "INITIALIZING CORE..."
        elif progress < 0.30:
            text = "LOADING GUARDIAN MODULES..."
        elif progress < 0.45:
            text = "CHECKING LOCAL SYSTEM..."
        elif progress < 0.60:
            text = "PREPARING SECURITY ENGINE..."
        elif progress < 0.75:
            text = "LOADING USER INTERFACE..."
        elif progress < 0.88:
            text = "SYNCING LOCAL COMPONENTS..."
        else:
            text = "SYSTEM READY..."

        self.canvas.itemconfigure(
            self.status_text,
            text=text,
        )

    # ------------------------------------------------------------------
    # FADE IN
    # ------------------------------------------------------------------

    def _fade_in(self) -> None:
        """Fade in splash."""

        if self.finished:
            return

        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        progress = _clamp(
            elapsed * 1000.0 / FADE_IN_MS,
            0.0,
            1.0,
        )

        eased = _ease_out_cubic(
            progress
        )

        try:
            self.root.attributes(
                "-alpha",
                eased,
            )
        except tk.TclError:
            return

        if progress < 1.0:
            self.fade_job = self.root.after(
                16,
                self._fade_in,
            )

    # ------------------------------------------------------------------
    # FINISH
    # ------------------------------------------------------------------

    def finish(self) -> None:
        """
        Menutup splash dengan fade-out.

        Aman dipanggil lebih dari satu kali.
        """

        if self.finished or self.closing:
            return

        self.closing = True

        if self.close_job is not None:
            try:
                self.root.after_cancel(
                    self.close_job
                )
            except Exception:
                pass

            self.close_job = None

        if self.animation_job is not None:
            try:
                self.root.after_cancel(
                    self.animation_job
                )
            except Exception:
                pass

            self.animation_job = None

        self._fade_out(
            1.0
        )

    # ------------------------------------------------------------------
    # FADE OUT
    # ------------------------------------------------------------------

    def _fade_out(
        self,
        opacity: float,
    ) -> None:
        """Fade-out kemudian destroy."""

        if self.finished:
            return

        opacity = _clamp(
            opacity,
            0.0,
            1.0,
        )

        try:
            self.root.attributes(
                "-alpha",
                opacity,
            )
        except tk.TclError:
            self._destroy()
            return

        if opacity <= 0.0:
            self._destroy()
            return

        step = 16.0 / FADE_OUT_MS

        opacity -= step

        self.fade_job = self.root.after(
            16,
            lambda: self._fade_out(
                opacity
            ),
        )

    # ------------------------------------------------------------------
    # DESTROY
    # ------------------------------------------------------------------

    def _destroy(self) -> None:
        """Menghancurkan splash dengan aman."""

        if self.finished:
            return

        self.finished = True

        for job in (
            self.animation_job,
            self.fade_job,
            self.close_job,
        ):
            if job is None:
                continue

            try:
                self.root.after_cancel(
                    job
                )
            except Exception:
                pass

        self.animation_job = None
        self.fade_job = None
        self.close_job = None

        try:
            self.root.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # RUN
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Menjalankan event loop splash."""

        try:
            self.root.mainloop()
        except tk.TclError:
            pass


# ============================================================================
# PUBLIC FUNCTION
# ============================================================================

def show_splash(
    duration_ms: int = 2500,
    logo_path: Optional[Path | str] = None,
    bg_color: str = BG_COLOR,
    text_color: str = CYAN,
    app_name: str = "Chocobot Guardian",
    version: str = "",
) -> None:
    """
    Public API splash screen.

    Signature ini sengaja dipertahankan agar main.py lama
    tetap dapat memanggil splash tanpa perubahan.

    Parameters
    ----------
    duration_ms:
        Durasi splash sebelum mulai ditutup.

    logo_path:
        Path menuju logo PNG.

    bg_color:
        Warna background.

    text_color:
        Warna utama teks.

    app_name:
        Nama aplikasi.

    version:
        Versi aplikasi.
    """

    resolved_logo = _resolve_logo_path(
        logo_path
    )

    root = tk.Tk()

    splash = FuturisticSplash(
        root=root,
        logo_path=resolved_logo,
        bg_color=bg_color or BG_COLOR,
        text_color=text_color or CYAN,
        app_name=app_name,
        version=version,
        duration_ms=duration_ms,
    )

    splash.run()


# ============================================================================
# DIRECT EXECUTION TEST
# ============================================================================

if __name__ == "__main__":
    """
    Test manual.

    Bisa dijalankan langsung:

        python splash_screen.py

    tanpa harus menjalankan seluruh Chocobot Guardian.
    """

    show_splash(
        duration_ms=5000,
        logo_path=None,
        bg_color=BG_COLOR,
        text_color=CYAN,
        app_name="Chocobot Guardian",
        version="1.0 Beta",
    )
