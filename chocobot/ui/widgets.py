# -*- coding: utf-8 -*-
"""
widgets.py — Chocobot Guardian UI Widget System
================================================

Reusable futuristic UI components for Chocobot Guardian.

Design goals:
    - Premium enterprise appearance
    - Smooth interaction
    - Lightweight rendering
    - Tkinter-compatible
    - Windows 7/8.1/10/11 friendly
    - No external UI framework required
    - Centralized styling through ui.styles
    - Safe fallbacks when optional functionality is unavailable

This module intentionally keeps visual rendering inside reusable widgets.
Individual screens should compose these widgets rather than rebuilding
their own visual components.
"""

from __future__ import annotations

import math
import tkinter as tk
from typing import Any, Callable, Dict, List, Optional, Tuple

from . import styles


# ============================================================================
# TYPE ALIASES
# ============================================================================

Color = str
Callback = Optional[Callable[..., Any]]


# ============================================================================
# INTERNAL HELPERS
# ============================================================================

def _safe_int(value: Any, default: int = 0) -> int:
    """Safely convert a value to integer."""

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a numeric value into a specified range."""

    return max(minimum, min(maximum, value))


def _hex_to_rgb(value: str) -> Tuple[int, int, int]:
    """Convert a hexadecimal color into RGB."""

    value = str(value).strip().lstrip("#")

    if len(value) != 6:
        return 255, 255, 255

    try:
        return (
            int(value[0:2], 16),
            int(value[2:4], 16),
            int(value[4:6], 16),
        )
    except ValueError:
        return 255, 255, 255


def _rgb_to_hex(red: int, green: int, blue: int) -> str:
    """Convert RGB values into hexadecimal color."""

    red = max(0, min(255, int(red)))
    green = max(0, min(255, int(green)))
    blue = max(0, min(255, int(blue)))

    return "#{:02x}{:02x}{:02x}".format(
        red,
        green,
        blue,
    )


def _blend_colors(
    first: str,
    second: str,
    amount: float,
) -> str:
    """
    Blend two hexadecimal colors.

    amount:
        0.0 = first color
        1.0 = second color
    """

    amount = _clamp(amount)

    r1, g1, b1 = _hex_to_rgb(first)
    r2, g2, b2 = _hex_to_rgb(second)

    return _rgb_to_hex(
        r1 + (r2 - r1) * amount,
        g1 + (g2 - g1) * amount,
        b1 + (b2 - b1) * amount,
    )


def _ease_linear(progress: float) -> float:
    return _clamp(progress)


def _ease_in(progress: float) -> float:
    progress = _clamp(progress)
    return progress * progress


def _ease_out(progress: float) -> float:
    progress = _clamp(progress)
    return 1.0 - ((1.0 - progress) ** 2)


def _ease_in_out(progress: float) -> float:
    progress = _clamp(progress)

    if progress < 0.5:
        return 2.0 * progress * progress

    return 1.0 - ((-2.0 * progress + 2.0) ** 2) / 2.0


def _ease_cubic(progress: float) -> float:
    progress = _clamp(progress)

    return (
        3.0 * progress * progress
        - 2.0 * progress * progress * progress
    )


def _apply_easing(progress: float, easing: str) -> float:
    """Apply a named easing curve."""

    easing = str(easing).lower()

    if easing == styles.EASING_LINEAR:
        return _ease_linear(progress)

    if easing == styles.EASING_EASE_IN:
        return _ease_in(progress)

    if easing == styles.EASING_EASE_OUT:
        return _ease_out(progress)

    if easing == styles.EASING_EASE_IN_OUT:
        return _ease_in_out(progress)

    if easing == styles.EASING_CUBIC:
        return _ease_cubic(progress)

    return _ease_cubic(progress)


# ============================================================================
# ANIMATION MIXIN
# ============================================================================

class AnimationMixin:
    """
    Lightweight animation controller based on tkinter.after().

    Every animation owns an identifier so a newer animation can safely
    replace an older one without leaving multiple animation loops running.
    """

    def __init__(self) -> None:
        self._animation_jobs: Dict[str, str] = {}
        self._animation_generation: Dict[str, int] = {}

    def cancel_animation(self, name: str) -> None:
        """Cancel a currently running animation."""

        job = self._animation_jobs.pop(name, None)

        if job is not None:
            try:
                self.after_cancel(job)
            except (tk.TclError, ValueError):
                pass

        self._animation_generation[name] = (
            self._animation_generation.get(name, 0) + 1
        )

    def cancel_all_animations(self) -> None:
        """Cancel every registered animation."""

        for name in list(self._animation_jobs.keys()):
            self.cancel_animation(name)

    def animate(
        self,
        name: str,
        duration: int,
        steps: int,
        update: Callable[[float], None],
        complete: Callback = None,
        easing: str = styles.DEFAULT_EASING,
    ) -> None:
        """
        Run a lightweight normalized animation.

        update receives a value between 0.0 and 1.0.
        """

        self.cancel_animation(name)

        if not styles.ANIMATIONS_ENABLED:
            update(1.0)

            if complete is not None:
                complete()

            return

        steps = max(1, int(steps))
        duration = max(1, int(duration))

        generation = self._animation_generation.get(name, 0)

        interval = max(
            1,
            int(duration / steps),
        )

        state = {
            "step": 0,
        }

        def tick() -> None:
            if self._animation_generation.get(name, 0) != generation:
                return

            state["step"] += 1

            raw_progress = _clamp(
                state["step"] / float(steps),
            )

            progress = _apply_easing(
                raw_progress,
                easing,
            )

            update(progress)

            if state["step"] >= steps:
                self._animation_jobs.pop(name, None)

                update(1.0)

                if complete is not None:
                    complete()

                return

            self._animation_jobs[name] = self.after(
                interval,
                tick,
            )

        self._animation_jobs[name] = self.after(
            interval,
            tick,
        )


# ============================================================================
# BASE FRAME
# ============================================================================

class PremiumFrame(tk.Frame, AnimationMixin):
    """
    Base frame for Chocobot visual components.

    Provides:
        - consistent background
        - animation management
        - safe destruction
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        background: Optional[str] = None,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        bg = background or styles.PANEL

        kwargs.setdefault("bg", bg)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bd", 0)

        tk.Frame.__init__(
            self,
            master,
            **kwargs,
        )

    def destroy(self) -> None:
        """Cancel visual animations before destroying the widget."""

        self.cancel_all_animations()

        try:
            super().destroy()
        except tk.TclError:
            pass


# ============================================================================
# SHADOW CARD
# ============================================================================

class GlassCard(PremiumFrame):
    """
    Premium card with layered border/depth treatment.

    Tkinter does not provide real blur or native shadows, so the component
    uses lightweight nested layers instead.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        background: Optional[str] = None,
        border_color: Optional[str] = None,
        radius: Optional[int] = None,
        shadow: bool = True,
        hover: bool = False,
        hover_color: Optional[str] = None,
        padding_x: int = styles.CARD_PAD_X,
        padding_y: int = styles.CARD_PAD_Y,
        **kwargs: Any,
    ) -> None:

        self.radius = radius or styles.RADIUS_CARD
        self.border_color = border_color or styles.BORDER
        self.normal_background = background or styles.CARD_BG
        self.hover_background = hover_color or styles.CARD_BG_HOVER

        self._hover_enabled = hover
        self._shadow_enabled = (
            shadow and styles.SHADOW_ENABLED
        )

        self._current_background = self.normal_background

        super().__init__(
            master,
            background=self.normal_background,
            **kwargs,
        )

        self._outer_border = tk.Frame(
            self,
            bg=self.border_color,
            bd=0,
            highlightthickness=0,
        )

        self._outer_border.pack(
            fill="both",
            expand=True,
        )

        self._inner = tk.Frame(
            self._outer_border,
            bg=self.normal_background,
            bd=0,
            highlightthickness=0,
        )

        self._inner.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1,
        )

        self.content = tk.Frame(
            self._inner,
            bg=self.normal_background,
            bd=0,
            highlightthickness=0,
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=padding_x,
            pady=padding_y,
        )

        if hover:
            self._bind_recursive_hover(
                self,
            )

    def _bind_recursive_hover(
        self,
        widget: tk.Misc,
    ) -> None:
        """Bind hover events to card and its child widgets."""

        widget.bind(
            "<Enter>",
            self._on_mouse_enter,
            add="+",
        )

        widget.bind(
            "<Leave>",
            self._on_mouse_leave,
            add="+",
        )

        for child in widget.winfo_children():
            self._bind_recursive_hover(child)

    def _on_mouse_enter(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self._hover_enabled:
            return

        self.animate(
            name="card_hover",
            duration=styles.ANIMATION_SMOOTH_MS,
            steps=styles.HOVER_TRANSITION_STEPS,
            update=self._animate_hover_in,
            easing=styles.HOVER_EASING,
        )

    def _on_mouse_leave(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self._hover_enabled:
            return

        self.animate(
            name="card_hover",
            duration=styles.ANIMATION_SMOOTH_MS,
            steps=styles.HOVER_TRANSITION_STEPS,
            update=self._animate_hover_out,
            easing=styles.HOVER_EASING,
        )

    def _animate_hover_in(
        self,
        progress: float,
    ) -> None:

        color = _blend_colors(
            self.normal_background,
            self.hover_background,
            progress,
        )

        self._set_card_background(color)

    def _animate_hover_out(
        self,
        progress: float,
    ) -> None:

        color = _blend_colors(
            self.hover_background,
            self.normal_background,
            progress,
        )

        self._set_card_background(color)

    def _set_card_background(
        self,
        color: str,
    ) -> None:

        self._current_background = color

        try:
            self.configure(bg=color)
            self._inner.configure(bg=color)
            self.content.configure(bg=color)
        except tk.TclError:
            return

        self._update_children_background(
            self.content,
            color,
        )

    def _update_children_background(
        self,
        widget: tk.Misc,
        color: str,
    ) -> None:

        for child in widget.winfo_children():
            try:
                child.configure(bg=color)
            except (tk.TclError, TypeError):
                pass

            self._update_children_background(
                child,
                color,
            )


# ============================================================================
# SECTION HEADER
# ============================================================================

class SectionHeader(PremiumFrame):
    """
    Consistent title/subtitle block used across application screens.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        title: str = "",
        subtitle: str = "",
        accent: str = styles.CYAN,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.CONTENT_BG,
            **kwargs,
        )

        self.columnconfigure(
            1,
            weight=1,
        )

        self.accent_bar = tk.Frame(
            self,
            bg=accent,
            width=3,
            height=38,
        )

        self.accent_bar.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="ns",
            padx=(0, 12),
        )

        self.title_label = tk.Label(
            self,
            text=title,
            bg=styles.CONTENT_BG,
            fg=styles.TEXT_PRIMARY,
            font=styles.FONT_TITLE_SMALL,
            anchor="w",
        )

        self.title_label.grid(
            row=0,
            column=1,
            sticky="w",
        )

        self.subtitle_label = tk.Label(
            self,
            text=subtitle,
            bg=styles.CONTENT_BG,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_SUBTITLE,
            anchor="w",
        )

        self.subtitle_label.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(3, 0),
        )


# ============================================================================
# PREMIUM BUTTON
# ============================================================================

class PremiumButton(tk.Frame, AnimationMixin):
    """
    Futuristic lightweight button.

    Features:
        - hover transition
        - press feedback
        - optional accent
        - optional icon
        - disabled state
        - keyboard focus
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        text: str = "",
        command: Callback = None,
        icon: str = "",
        accent: str = styles.CYAN,
        width: Optional[int] = None,
        height: int = styles.BUTTON_HEIGHT,
        variant: str = "default",
        enabled: bool = True,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self.command = command
        self.text = text
        self.icon = icon
        self.accent = accent
        self.variant = variant
        self.enabled = enabled

        self.button_width = width
        self.button_height = height

        self._pressed = False
        self._hovered = False
        self._focused = False

        self.normal_bg = self._resolve_background()
        self.hover_bg = self._resolve_hover_background()

        self.normal_fg = self._resolve_foreground()
        self.hover_fg = styles.TEXT_PRIMARY

        self.normal_border = self._resolve_border()
        self.hover_border = accent

        kwargs.setdefault(
            "bg",
            self.normal_bg,
        )

        kwargs.setdefault(
            "highlightthickness",
            0,
        )

        kwargs.setdefault(
            "bd",
            0,
        )

        tk.Frame.__init__(
            self,
            master,
            width=width,
            height=height,
            **kwargs,
        )

        self.pack_propagate(False)

        self._button = tk.Label(
            self,
            text=self._build_text(),
            bg=self.normal_bg,
            fg=self.normal_fg,
            font=(
                styles.FONT_BUTTON
                if variant != "small"
                else styles.FONT_BUTTON_SMALL
            ),
            anchor="center",
            justify="center",
            cursor="hand2" if enabled else "arrow",
            bd=0,
            highlightthickness=0,
        )

        self._button.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1,
        )

        self._bind_events()

        if not enabled:
            self._apply_disabled_state()

    def _build_text(self) -> str:
        if self.icon and self.text:
            return "{}  {}".format(
                self.icon,
                self.text,
            )

        if self.icon:
            return self.icon

        return self.text

    def _resolve_background(self) -> str:
        variant = self.variant.lower()

        if variant == "primary":
            return self.accent

        if variant == "danger":
            return styles.RED_DARK

        if variant == "success":
            return styles.GREEN_DARK

        if variant == "ghost":
            return styles.APP_BG

        if variant == "transparent":
            return styles.APP_BG

        return styles.BUTTON_BG

    def _resolve_hover_background(self) -> str:
        variant = self.variant.lower()

        if variant == "primary":
            return _blend_colors(
                self.accent,
                styles.TEXT_PRIMARY,
                0.12,
            )

        if variant == "danger":
            return _blend_colors(
                styles.RED_DARK,
                styles.RED,
                0.30,
            )

        if variant == "success":
            return _blend_colors(
                styles.GREEN_DARK,
                styles.GREEN,
                0.30,
            )

        if variant in ("ghost", "transparent"):
            return styles.NAV_HOVER_BG

        return styles.BUTTON_HOVER_BG

    def _resolve_foreground(self) -> str:
        variant = self.variant.lower()

        if variant in (
            "primary",
            "danger",
            "success",
        ):
            return styles.APP_BG

        return styles.TEXT_SECONDARY

    def _resolve_border(self) -> str:
        variant = self.variant.lower()

        if variant == "ghost":
            return styles.BORDER

        if variant == "transparent":
            return styles.APP_BG

        return styles.BORDER

    def _bind_events(self) -> None:

        self.bind(
            "<Enter>",
            self._on_enter,
        )

        self.bind(
            "<Leave>",
            self._on_leave,
        )

        self.bind(
            "<ButtonPress-1>",
            self._on_press,
        )

        self.bind(
            "<ButtonRelease-1>",
            self._on_release,
        )

        self._button.bind(
            "<Enter>",
            self._on_enter,
        )

        self._button.bind(
            "<Leave>",
            self._on_leave,
        )

        self._button.bind(
            "<ButtonPress-1>",
            self._on_press,
        )

        self._button.bind(
            "<ButtonRelease-1>",
            self._on_release,
        )

        self.bind(
            "<FocusIn>",
            self._on_focus_in,
        )

        self.bind(
            "<FocusOut>",
            self._on_focus_out,
        )

    def _on_enter(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self.enabled:
            return

        self._hovered = True

        self.animate(
            name="button_hover",
            duration=styles.ANIMATION_QUICK_MS,
            steps=styles.HOVER_TRANSITION_STEPS,
            update=self._animate_hover_in,
            easing=styles.HOVER_EASING,
        )

    def _on_leave(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self.enabled:
            return

        self._hovered = False

        self.animate(
            name="button_hover",
            duration=styles.ANIMATION_QUICK_MS,
            steps=styles.HOVER_TRANSITION_STEPS,
            update=self._animate_hover_out,
            easing=styles.HOVER_EASING,
        )

    def _animate_hover_in(
        self,
        progress: float,
    ) -> None:

        bg = _blend_colors(
            self.normal_bg,
            self.hover_bg,
            progress,
        )

        fg = _blend_colors(
            self.normal_fg,
            self.hover_fg,
            progress,
        )

        self._apply_colors(
            bg,
            fg,
        )

    def _animate_hover_out(
        self,
        progress: float,
    ) -> None:

        bg = _blend_colors(
            self.hover_bg,
            self.normal_bg,
            progress,
        )

        fg = _blend_colors(
            self.hover_fg,
            self.normal_fg,
            progress,
        )

        self._apply_colors(
            bg,
            fg,
        )

    def _apply_colors(
        self,
        background: str,
        foreground: str,
    ) -> None:

        try:
            self.configure(
                bg=background,
            )

            self._button.configure(
                bg=background,
                fg=foreground,
            )
        except tk.TclError:
            pass

    def _on_press(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self.enabled:
            return

        self._pressed = True

        try:
            self._button.place_configure(
                y=styles.BUTTON_PRESS_OFFSET,
            )
        except tk.TclError:
            pass

    def _on_release(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if not self.enabled:
            return

        self._pressed = False

        try:
            self._button.place_configure(
                y=0,
            )
        except tk.TclError:
            pass

        if self._hovered and self.command is not None:
            try:
                self.command()
            except TypeError:
                self.command(event)

    def _on_focus_in(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self._focused = True

    def _on_focus_out(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self._focused = False

    def _apply_disabled_state(self) -> None:

        try:
            self._button.configure(
                bg=styles.PANEL_SOFT,
                fg=styles.DISABLED,
                cursor="arrow",
            )

            self.configure(
                bg=styles.PANEL_SOFT,
            )
        except tk.TclError:
            pass

    def configure(
        self,
        cnf: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:

        if cnf:
            kwargs.update(cnf)

        if "command" in kwargs:
            self.command = kwargs.pop("command")

        if "text" in kwargs:
            self.text = kwargs.pop("text")

            if hasattr(self, "_button"):
                self._button.configure(
                    text=self._build_text(),
                )

        if "enabled" in kwargs:
            self.enabled = bool(
                kwargs.pop("enabled")
            )

            if hasattr(self, "_button"):
                if self.enabled:
                    self._button.configure(
                        cursor="hand2",
                    )
                else:
                    self._apply_disabled_state()

        return super().configure(**kwargs)


# ============================================================================
# ICON BUTTON
# ============================================================================

class IconButton(PremiumButton):
    """Compact button designed for icons."""

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        icon: str = "•",
        command: Callback = None,
        size: int = 36,
        accent: str = styles.CYAN,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            text="",
            icon=icon,
            command=command,
            accent=accent,
            width=size,
            height=size,
            variant="ghost",
            **kwargs,
        )


# ============================================================================
# NAVIGATION ITEM
# ============================================================================

class NavigationItem(tk.Frame, AnimationMixin):
    """
    Sidebar navigation item.

    Visual behavior:
        - subtle hover transition
        - active indicator
        - active background
        - icon and text color transition
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        text: str = "",
        icon: str = "",
        command: Callback = None,
        active: bool = False,
        accent: str = styles.CYAN,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self.text = text
        self.icon = icon
        self.command = command
        self.accent = accent

        self.active = active
        self.hovered = False

        tk.Frame.__init__(
            self,
            master,
            bg=styles.NAV_BG,
            height=styles.NAV_ITEM_HEIGHT,
            bd=0,
            highlightthickness=0,
            **kwargs,
        )

        self.pack_propagate(False)

        self._indicator = tk.Frame(
            self,
            bg=(
                accent
                if active
                else styles.NAV_BG
            ),
            width=styles.NAV_INDICATOR_WIDTH,
        )

        self._indicator.pack(
            side="left",
            fill="y",
        )

        self._body = tk.Frame(
            self,
            bg=(
                styles.ACTIVE_NAV_BG
                if active
                else styles.NAV_BG
            ),
            bd=0,
            highlightthickness=0,
        )

        self._body.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(3, 0),
        )

        self._icon = tk.Label(
            self._body,
            text=icon,
            bg=self._body["bg"],
            fg=(
                styles.NAV_ICON_ACTIVE
                if active
                else styles.NAV_ICON
            ),
            font=styles.FONT_SIDEBAR_ITEM_BOLD,
            width=2,
            anchor="center",
        )

        self._icon.pack(
            side="left",
            padx=(8, 5),
        )

        self._label = tk.Label(
            self._body,
            text=text,
            bg=self._body["bg"],
            fg=(
                styles.NAV_TEXT_ACTIVE
                if active
                else styles.NAV_TEXT
            ),
            font=(
                styles.FONT_SIDEBAR_ITEM_BOLD
                if active
                else styles.FONT_SIDEBAR_ITEM
            ),
            anchor="w",
        )

        self._label.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
        )

        self._bind_recursive(
            self,
        )

    def _bind_recursive(
        self,
        widget: tk.Misc,
    ) -> None:

        widget.bind(
            "<Enter>",
            self._on_enter,
            add="+",
        )

        widget.bind(
            "<Leave>",
            self._on_leave,
            add="+",
        )

        widget.bind(
            "<Button-1>",
            self._on_click,
            add="+",
        )

        for child in widget.winfo_children():
            self._bind_recursive(child)

    def _on_enter(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self.hovered = True

        if not self.active:
            self.animate(
                name="nav_hover",
                duration=styles.ANIMATION_QUICK_MS,
                steps=styles.NAV_TRANSITION_STEPS,
                update=self._animate_hover_in,
                easing=styles.HOVER_EASING,
            )

    def _on_leave(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self.hovered = False

        if not self.active:
            self.animate(
                name="nav_hover",
                duration=styles.ANIMATION_QUICK_MS,
                steps=styles.NAV_TRANSITION_STEPS,
                update=self._animate_hover_out,
                easing=styles.HOVER_EASING,
            )

    def _animate_hover_in(
        self,
        progress: float,
    ) -> None:

        body_bg = _blend_colors(
            styles.NAV_BG,
            styles.NAV_HOVER_BG,
            progress,
        )

        icon_fg = _blend_colors(
            styles.NAV_ICON,
            styles.NAV_ICON_HOVER,
            progress,
        )

        text_fg = _blend_colors(
            styles.NAV_TEXT,
            styles.NAV_TEXT_HOVER,
            progress,
        )

        self._apply_colors(
            body_bg,
            icon_fg,
            text_fg,
        )

    def _animate_hover_out(
        self,
        progress: float,
    ) -> None:

        body_bg = _blend_colors(
            styles.NAV_HOVER_BG,
            styles.NAV_BG,
            progress,
        )

        icon_fg = _blend_colors(
            styles.NAV_ICON_HOVER,
            styles.NAV_ICON,
            progress,
        )

        text_fg = _blend_colors(
            styles.NAV_TEXT_HOVER,
            styles.NAV_TEXT,
            progress,
        )

        self._apply_colors(
            body_bg,
            icon_fg,
            text_fg,
        )

    def _apply_colors(
        self,
        background: str,
        icon_color: str,
        text_color: str,
    ) -> None:

        try:
            self._body.configure(
                bg=background,
            )

            self._icon.configure(
                bg=background,
                fg=icon_color,
            )

            self._label.configure(
                bg=background,
                fg=text_color,
            )
        except tk.TclError:
            pass

    def _on_click(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if self.command is None:
            return

        try:
            self.command()
        except TypeError:
            self.command(event)

    def set_active(
        self,
        active: bool,
    ) -> None:

        self.active = bool(active)

        if self.active:
            self._indicator.configure(
                bg=self.accent,
            )

            self._body.configure(
                bg=styles.ACTIVE_NAV_BG,
            )

            self._icon.configure(
                bg=styles.ACTIVE_NAV_BG,
                fg=styles.NAV_ICON_ACTIVE,
                font=styles.FONT_SIDEBAR_ITEM_BOLD,
            )

            self._label.configure(
                bg=styles.ACTIVE_NAV_BG,
                fg=styles.NAV_TEXT_ACTIVE,
                font=styles.FONT_SIDEBAR_ITEM_BOLD,
            )

        else:
            self._indicator.configure(
                bg=styles.NAV_BG,
            )

            self._body.configure(
                bg=styles.NAV_BG,
            )

            self._icon.configure(
                bg=styles.NAV_BG,
                fg=styles.NAV_ICON,
                font=styles.FONT_SIDEBAR_ITEM,
            )

            self._label.configure(
                bg=styles.NAV_BG,
                fg=styles.NAV_TEXT,
                font=styles.FONT_SIDEBAR_ITEM,
            )


# ============================================================================
# STATUS INDICATOR
# ============================================================================

class StatusIndicator(PremiumFrame):
    """
    Compact status component.

    Displays:
        ● PROTECTED
        ● WARNING
        ● ERROR
        etc.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        status: str = styles.STATUS_READY,
        text: Optional[str] = None,
        pulse: bool = False,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.APP_BG,
            **kwargs,
        )

        self.status = status
        self.status_text = text or status
        self.pulse_enabled = pulse

        self._dot = tk.Canvas(
            self,
            width=10,
            height=10,
            bg=styles.APP_BG,
            highlightthickness=0,
            bd=0,
        )

        self._dot.pack(
            side="left",
            padx=(0, 7),
        )

        self._label = tk.Label(
            self,
            text=self.status_text,
            bg=styles.APP_BG,
            fg=styles.get_status_color(status),
            font=styles.FONT_STATUS_TITLE,
        )

        self._label.pack(
            side="left",
        )

        self._draw_dot()

        if pulse:
            self._start_pulse()

    def _draw_dot(
        self,
        intensity: float = 1.0,
    ) -> None:

        color = styles.get_status_color(
            self.status,
        )

        if intensity < 1.0:
            color = _blend_colors(
                styles.APP_BG,
                color,
                intensity,
            )

        self._dot.delete(
            "all",
        )

        self._dot.create_oval(
            2,
            2,
            8,
            8,
            fill=color,
            outline="",
        )

    def _start_pulse(self) -> None:

        if not self.pulse_enabled:
            return

        phase = getattr(
            self,
            "_pulse_phase",
            0.0,
        )

        phase += 0.15

        if phase > math.pi * 2:
            phase = 0.0

        self._pulse_phase = phase

        intensity = (
            0.55
            + (
                math.sin(phase)
                * 0.45
            )
        )

        self._draw_dot(
            intensity,
        )

        try:
            self.after(
                styles.SPLASH_PULSE_MS,
                self._start_pulse,
            )
        except tk.TclError:
            pass

    def set_status(
        self,
        status: str,
        text: Optional[str] = None,
    ) -> None:

        self.status = status
        self.status_text = text or status

        try:
            self._label.configure(
                text=self.status_text,
                fg=styles.get_status_color(
                    status,
                ),
            )

            self._draw_dot()
        except tk.TclError:
            pass


# ============================================================================
# METRIC CARD
# ============================================================================

class MetricCard(GlassCard):
    """
    Dashboard metric card.

    Example:
        CPU
        42%
        Current processor usage
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        title: str = "",
        value: str = "--",
        description: str = "",
        accent: str = styles.CYAN,
        icon: str = "",
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.CARD_BG,
            border_color=styles.BORDER,
            hover=True,
            **kwargs,
        )

        self.accent = accent

        self._accent = tk.Frame(
            self.content,
            bg=accent,
            width=3,
        )

        self._accent.pack(
            side="left",
            fill="y",
            padx=(0, 14),
        )

        self._main = tk.Frame(
            self.content,
            bg=styles.CARD_BG,
        )

        self._main.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self._top = tk.Frame(
            self._main,
            bg=styles.CARD_BG,
        )

        self._top.pack(
            fill="x",
        )

        self._title = tk.Label(
            self._top,
            text=title.upper(),
            bg=styles.CARD_BG,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_STATUS_TITLE,
            anchor="w",
        )

        self._title.pack(
            side="left",
        )

        if icon:
            self._icon = tk.Label(
                self._top,
                text=icon,
                bg=styles.CARD_BG,
                fg=accent,
                font=styles.FONT_CARD_TITLE,
            )

            self._icon.pack(
                side="right",
            )

        self._value = tk.Label(
            self._main,
            text=value,
            bg=styles.CARD_BG,
            fg=styles.TEXT_PRIMARY,
            font=styles.FONT_STATUS_VALUE_LARGE,
            anchor="w",
        )

        self._value.pack(
            fill="x",
            pady=(8, 2),
        )

        self._description = tk.Label(
            self._main,
            text=description,
            bg=styles.CARD_BG,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_STATUS_DESC,
            anchor="w",
        )

        self._description.pack(
            fill="x",
        )

    def set_value(
        self,
        value: Any,
    ) -> None:

        try:
            self._value.configure(
                text=str(value),
            )
        except tk.TclError:
            pass

    def set_title(
        self,
        title: str,
    ) -> None:

        try:
            self._title.configure(
                text=str(title).upper(),
            )
        except tk.TclError:
            pass

    def set_description(
        self,
        description: str,
    ) -> None:

        try:
            self._description.configure(
                text=str(description),
            )
        except tk.TclError:
            pass


# ============================================================================
# STATUS CARD
# ============================================================================

class StatusCard(GlassCard):
    """
    Large system/security status card.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        title: str = "SYSTEM STATUS",
        status: str = styles.STATUS_PROTECTED,
        description: str = "",
        accent: Optional[str] = None,
        **kwargs: Any,
    ) -> None:

        resolved_accent = (
            accent
            or styles.get_status_color(status)
        )

        super().__init__(
            master,
            background=styles.CARD_BG,
            border_color=styles.BORDER,
            hover=True,
            **kwargs,
        )

        self._accent_color = resolved_accent

        self._top = tk.Frame(
            self.content,
            bg=styles.CARD_BG,
        )

        self._top.pack(
            fill="x",
        )

        self._title = tk.Label(
            self._top,
            text=title.upper(),
            bg=styles.CARD_BG,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_STATUS_TITLE,
            anchor="w",
        )

        self._title.pack(
            side="left",
        )

        self._indicator = StatusIndicator(
            self._top,
            status=status,
            pulse=True,
        )

        self._indicator.pack(
            side="right",
        )

        self._status = tk.Label(
            self.content,
            text=status,
            bg=styles.CARD_BG,
            fg=resolved_accent,
            font=styles.FONT_STATUS_VALUE_LARGE,
            anchor="w",
        )

        self._status.pack(
            fill="x",
            pady=(14, 4),
        )

        self._description = tk.Label(
            self.content,
            text=description,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
            font=styles.FONT_CARD_DESC,
            anchor="w",
            justify="left",
            wraplength=500,
        )

        self._description.pack(
            fill="x",
        )

    def set_status(
        self,
        status: str,
        description: Optional[str] = None,
    ) -> None:

        accent = styles.get_status_color(
            status,
        )

        try:
            self._indicator.set_status(
                status,
            )

            self._status.configure(
                text=status,
                fg=accent,
            )

            if description is not None:
                self._description.configure(
                    text=description,
                )
        except tk.TclError:
            pass


# ============================================================================
# SEARCH / ENTRY
# ============================================================================

class ModernEntry(tk.Frame):
    """
    Modern input field.

    Uses a framed Entry instead of the default Tkinter border treatment.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        placeholder: str = "",
        icon: str = "",
        show: Optional[str] = None,
        command: Callback = None,
        **kwargs: Any,
    ) -> None:

        self.placeholder = placeholder
        self.command = command
        self._placeholder_active = False

        super().__init__(
            master,
            bg=styles.ENTRY_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
            highlightcolor=styles.CYAN,
            **kwargs,
        )

        if icon:
            self._icon = tk.Label(
                self,
                text=icon,
                bg=styles.ENTRY_BG,
                fg=styles.MUTED,
                font=styles.FONT_ENTRY,
            )

            self._icon.pack(
                side="left",
                padx=(12, 5),
            )

        self._entry = tk.Entry(
            self,
            bg=styles.ENTRY_BG,
            fg=styles.TEXT_PRIMARY,
            insertbackground=styles.CYAN,
            selectbackground=styles.CYAN_DARK,
            selectforeground=styles.TEXT_PRIMARY,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=styles.FONT_ENTRY,
            show=show or "",
        )

        self._entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(
                8 if not icon else 2,
                12,
            ),
            pady=8,
        )

        self._entry.bind(
            "<FocusIn>",
            self._on_focus_in,
        )

        self._entry.bind(
            "<FocusOut>",
            self._on_focus_out,
        )

        self._entry.bind(
            "<Return>",
            self._on_return,
        )

        if placeholder:
            self._set_placeholder()

    def _set_placeholder(self) -> None:

        self._placeholder_active = True

        self._entry.delete(
            0,
            "end",
        )

        self._entry.insert(
            0,
            self.placeholder,
        )

        self._entry.configure(
            fg=styles.MUTED_2,
        )

    def _on_focus_in(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self.configure(
            highlightbackground=styles.BORDER_HOVER,
            highlightcolor=styles.CYAN,
        )

        if self._placeholder_active:
            self._placeholder_active = False

            self._entry.delete(
                0,
                "end",
            )

            self._entry.configure(
                fg=styles.TEXT_PRIMARY,
            )

    def _on_focus_out(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self.configure(
            highlightbackground=styles.BORDER,
        )

        if not self._entry.get():
            self._set_placeholder()

    def _on_return(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        if self.command is None:
            return

        try:
            self.command(
                self.get(),
            )
        except TypeError:
            self.command()

    def get(self) -> str:

        if self._placeholder_active:
            return ""

        return self._entry.get()

    def set(
        self,
        value: str,
    ) -> None:

        self._placeholder_active = False

        self._entry.delete(
            0,
            "end",
        )

        self._entry.insert(
            0,
            value,
        )

        self._entry.configure(
            fg=styles.TEXT_PRIMARY,
        )

    def clear(self) -> None:

        self._entry.delete(
            0,
            "end",
        )

        if self.placeholder:
            self._set_placeholder()


# ============================================================================
# TOGGLE SWITCH
# ============================================================================

class ToggleSwitch(tk.Canvas, AnimationMixin):
    """
    Lightweight animated toggle switch.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        value: bool = False,
        command: Callback = None,
        width: int = styles.TOGGLE_WIDTH,
        height: int = styles.TOGGLE_HEIGHT,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self._value = bool(value)
        self.command = command

        self._width = width
        self._height = height

        super().__init__(
            master,
            width=width,
            height=height,
            bg=styles.APP_BG,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **kwargs,
        )

        self.bind(
            "<Button-1>",
            self._toggle,
        )

        self._draw(
            1.0 if self._value else 0.0,
        )

    def _toggle(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self.set(
            not self._value,
            animate=True,
        )

        if self.command is not None:
            try:
                self.command(
                    self._value,
                )
            except TypeError:
                self.command()

    def _draw(
        self,
        progress: float,
    ) -> None:

        progress = _clamp(progress)

        off_color = styles.TOGGLE_BG_OFF
        on_color = styles.TOGGLE_BG_ON

        background = _blend_colors(
            off_color,
            on_color,
            progress,
        )

        knob_size = styles.TOGGLE_KNOB_SIZE

        left = 2
        right = self._width - 2

        center_y = self._height / 2.0

        knob_start = (
            left
            + knob_size / 2
        )

        knob_end = (
            right
            - knob_size / 2
        )

        knob_x = (
            knob_start
            + (
                knob_end
                - knob_start
            )
            * progress
        )

        self.delete(
            "all",
        )

        self.create_rounded_rect(
            0,
            0,
            self._width,
            self._height,
            radius=self._height / 2,
            fill=background,
            outline="",
        )

        self.create_oval(
            knob_x - knob_size / 2,
            center_y - knob_size / 2,
            knob_x + knob_size / 2,
            center_y + knob_size / 2,
            fill=styles.TOGGLE_KNOB,
            outline="",
        )

    def create_rounded_rect(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        radius: float,
        **kwargs: Any,
    ) -> int:
        """
        Draw a rounded rectangle using Canvas polygons and arcs.
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

        return self.create_polygon(
            points,
            smooth=True,
            **kwargs,
        )

    def set(
        self,
        value: bool,
        animate: bool = True,
    ) -> None:

        value = bool(value)

        if value == self._value and animate:
            return

        old_value = 1.0 if self._value else 0.0
        new_value = 1.0 if value else 0.0

        self._value = value

        if not animate or not styles.ANIMATIONS_ENABLED:
            self._draw(
                new_value,
            )

            return

        def update(progress: float) -> None:

            current = (
                old_value
                + (
                    new_value
                    - old_value
                )
                * progress
            )

            self._draw(
                current,
            )

        self.animate(
            name="toggle",
            duration=styles.ANIMATION_SMOOTH_MS,
            steps=styles.TOGGLE_ANIMATION_STEPS,
            update=update,
            easing=styles.EASING_EASE_OUT,
        )

    def get(self) -> bool:
        return self._value


# ============================================================================
# PROGRESS BAR
# ============================================================================

class AnimatedProgressBar(tk.Canvas, AnimationMixin):
    """
    Lightweight animated progress bar.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        value: float = 0.0,
        maximum: float = 100.0,
        accent: str = styles.CYAN,
        height: int = styles.PROGRESS_HEIGHT,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self._value = float(value)
        self._maximum = max(
            0.0001,
            float(maximum),
        )

        self._accent = accent
        self._bar_height = height

        super().__init__(
            master,
            height=height,
            bg=styles.PROGRESS_BG,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )

        self.bind(
            "<Configure>",
            lambda event: self._draw(
                self._value / self._maximum
            ),
        )

        self._draw(
            self._value / self._maximum,
        )

    def _draw(
        self,
        progress: float,
    ) -> None:

        progress = _clamp(
            progress,
        )

        width = max(
            1,
            self.winfo_width(),
        )

        height = max(
            self._bar_height,
            self.winfo_height(),
        )

        self.delete(
            "all",
        )

        self.create_rectangle(
            0,
            0,
            width,
            height,
            fill=styles.PROGRESS_BG,
            outline="",
        )

        fill_width = width * progress

        if fill_width > 0:
            self.create_rectangle(
                0,
                0,
                fill_width,
                height,
                fill=self._accent,
                outline="",
            )

    def set(
        self,
        value: float,
        animate: bool = True,
    ) -> None:

        value = max(
            0.0,
            min(
                float(value),
                self._maximum,
            ),
        )

        old = self._value
        self._value = value

        if not animate or not styles.ANIMATIONS_ENABLED:
            self._draw(
                value / self._maximum,
            )

            return

        def update(progress: float) -> None:

            current = (
                old
                + (
                    value
                    - old
                )
                * progress
            )

            self._draw(
                current / self._maximum,
            )

        self.animate(
            name="progress",
            duration=styles.ANIMATION_NORMAL_MS,
            steps=14,
            update=update,
            easing=styles.EASING_EASE_OUT,
        )

    def get(self) -> float:
        return self._value


# ============================================================================
# DIVIDER
# ============================================================================

class Divider(tk.Frame):
    """Simple visual divider."""

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        color: str = styles.DIVIDER,
        height: int = 1,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            bg=color,
            height=height,
            bd=0,
            highlightthickness=0,
            **kwargs,
        )

        self.pack_propagate(False)


# ============================================================================
# LABEL
# ============================================================================

class PremiumLabel(tk.Label):
    """
    Standardized label with Chocobot typography defaults.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        text: str = "",
        variant: str = "body",
        **kwargs: Any,
    ) -> None:

        variant = variant.lower()

        font_map = {
            "display": styles.FONT_DISPLAY,
            "title": styles.FONT_TITLE_SMALL,
            "subtitle": styles.FONT_SUBTITLE,
            "body": styles.FONT_CARD_DESC,
            "small": styles.FONT_CARD_DESC_SMALL,
            "label": styles.FONT_LABEL,
            "micro": styles.FONT_MICRO,
            "mono": styles.FONT_MONO,
            "mono_large": styles.FONT_MONO_LARGE,
        }

        kwargs.setdefault(
            "bg",
            styles.APP_BG,
        )

        kwargs.setdefault(
            "fg",
            styles.TEXT_SECONDARY,
        )

        kwargs.setdefault(
            "font",
            font_map.get(
                variant,
                styles.FONT_CARD_DESC,
            ),
        )

        kwargs.setdefault(
            "anchor",
            "w",
        )

        kwargs.setdefault(
            "bd",
            0,
        )

        kwargs.setdefault(
            "highlightthickness",
            0,
        )

        super().__init__(
            master,
            text=text,
            **kwargs,
        )


# ============================================================================
# TOOL CARD
# ============================================================================

class ToolCard(GlassCard):
    """
    Reusable tool tile for pages such as:
        Security
        File Tools
        Converter
        Network
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        title: str = "",
        description: str = "",
        icon: str = "",
        command: Callback = None,
        accent: str = styles.CYAN,
        action_text: str = "OPEN",
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.CARD_BG,
            border_color=styles.BORDER,
            hover=True,
            **kwargs,
        )

        self._accent = accent
        self._command = command

        self._header = tk.Frame(
            self.content,
            bg=styles.CARD_BG,
        )

        self._header.pack(
            fill="x",
        )

        self._icon = tk.Label(
            self._header,
            text=icon,
            bg=styles.CARD_BG,
            fg=accent,
            font=styles.FONT_BRAND,
            width=3,
            anchor="w",
        )

        self._icon.pack(
            side="left",
        )

        self._title = tk.Label(
            self._header,
            text=title,
            bg=styles.CARD_BG,
            fg=styles.TEXT_PRIMARY,
            font=styles.FONT_CARD_TITLE_LARGE,
            anchor="w",
        )

        self._title.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self._description = tk.Label(
            self.content,
            text=description,
            bg=styles.CARD_BG,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_CARD_DESC,
            anchor="w",
            justify="left",
            wraplength=330,
        )

        self._description.pack(
            fill="x",
            pady=(10, 14),
        )

        self._action = PremiumButton(
            self.content,
            text=action_text,
            command=self._execute,
            accent=accent,
            variant="ghost",
            height=styles.BUTTON_HEIGHT_SMALL,
        )

        self._action.pack(
            anchor="w",
        )

        self._bind_action_recursive(
            self,
        )

    def _bind_action_recursive(
        self,
        widget: tk.Misc,
    ) -> None:

        widget.bind(
            "<Double-Button-1>",
            self._on_double_click,
            add="+",
        )

        for child in widget.winfo_children():
            self._bind_action_recursive(
                child,
            )

    def _on_double_click(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self._execute()

    def _execute(self) -> None:

        if self._command is None:
            return

        try:
            self._command()
        except TypeError:
            self._command(self)


# ============================================================================
# INFO ROW
# ============================================================================

class InfoRow(tk.Frame):
    """
    Compact key/value information row.

    Useful for:
        System information
        Network details
        License information
        File details
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        label: str = "",
        value: str = "",
        value_color: str = styles.TEXT_PRIMARY,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            bg=styles.PANEL,
            bd=0,
            highlightthickness=0,
            **kwargs,
        )

        self.columnconfigure(
            1,
            weight=1,
        )

        self._label = tk.Label(
            self,
            text=label,
            bg=styles.PANEL,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_LABEL,
            anchor="w",
        )

        self._label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 20),
            pady=7,
        )

        self._value = tk.Label(
            self,
            text=value,
            bg=styles.PANEL,
            fg=value_color,
            font=styles.FONT_MONO_SMALL,
            anchor="e",
        )

        self._value.grid(
            row=0,
            column=1,
            sticky="e",
            pady=7,
        )

    def set_value(
        self,
        value: Any,
    ) -> None:

        try:
            self._value.configure(
                text=str(value),
            )
        except tk.TclError:
            pass


# ============================================================================
# CHIP
# ============================================================================

class StatusChip(tk.Frame):
    """
    Small status badge.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        text: str = "",
        status: str = styles.STATUS_READY,
        **kwargs: Any,
    ) -> None:

        self.status = status

        background = _blend_colors(
            styles.APP_BG,
            styles.get_status_color(status),
            0.10,
        )

        super().__init__(
            master,
            bg=background,
            bd=0,
            highlightthickness=0,
            **kwargs,
        )

        self._dot = tk.Canvas(
            self,
            width=8,
            height=8,
            bg=background,
            highlightthickness=0,
            bd=0,
        )

        self._dot.pack(
            side="left",
            padx=(8, 5),
            pady=6,
        )

        self._label = tk.Label(
            self,
            text=text or status,
            bg=background,
            fg=styles.get_status_color(status),
            font=styles.FONT_MICRO_BOLD,
        )

        self._label.pack(
            side="left",
            padx=(0, 9),
            pady=5,
        )

        self._draw_dot()

    def _draw_dot(self) -> None:

        self._dot.delete(
            "all",
        )

        color = styles.get_status_color(
            self.status,
        )

        self._dot.create_oval(
            2,
            2,
            7,
            7,
            fill=color,
            outline="",
        )

    def set_status(
        self,
        status: str,
        text: Optional[str] = None,
    ) -> None:

        self.status = status

        background = _blend_colors(
            styles.APP_BG,
            styles.get_status_color(status),
            0.10,
        )

        try:
            self.configure(
                bg=background,
            )

            self._dot.configure(
                bg=background,
            )

            self._label.configure(
                bg=background,
                fg=styles.get_status_color(status),
                text=text or status,
            )

            self._draw_dot()
        except tk.TclError:
            pass


# ============================================================================
# LOADING INDICATOR
# ============================================================================

class LoadingIndicator(tk.Canvas, AnimationMixin):
    """
    Small animated loading indicator.

    Designed to be inexpensive:
        - no image assets
        - no blur
        - no particle system
        - small number of canvas objects
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        size: int = 28,
        accent: str = styles.CYAN,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self.size = size
        self.accent = accent
        self._angle = 0.0

        super().__init__(
            master,
            width=size,
            height=size,
            bg=styles.APP_BG,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )

        self._draw()
        self._animate()

    def _draw(self) -> None:

        self.delete(
            "all",
        )

        center = self.size / 2.0

        outer = self.size * 0.42
        inner = self.size * 0.25

        for index in range(8):

            angle = (
                self._angle
                + index * 45
            )

            radians = math.radians(
                angle,
            )

            distance = (
                inner
                + (
                    outer
                    - inner
                )
                * 0.50
            )

            x = (
                center
                + math.cos(radians)
                * distance
            )

            y = (
                center
                + math.sin(radians)
                * distance
            )

            intensity = (
                index + 1
            ) / 8.0

            color = _blend_colors(
                styles.APP_BG,
                self.accent,
                intensity,
            )

            radius = max(
                1.5,
                self.size * 0.055,
            )

            self.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=color,
                outline="",
            )

    def _animate(self) -> None:

        self._angle += 15

        if self._angle >= 360:
            self._angle -= 360

        self._draw()

        try:
            self.after(
                50,
                self._animate,
            )
        except tk.TclError:
            pass


# ============================================================================
# TOOLTIP
# ============================================================================

class Tooltip:
    """
    Lightweight tooltip manager.

    Usage:
        Tooltip(widget, "Example information")
    """

    def __init__(
        self,
        widget: tk.Misc,
        text: str,
        delay: int = styles.TOOLTIP_DELAY_MS,
    ) -> None:

        self.widget = widget
        self.text = text
        self.delay = delay

        self._after_id: Optional[str] = None
        self._window: Optional[tk.Toplevel] = None

        widget.bind(
            "<Enter>",
            self._on_enter,
            add="+",
        )

        widget.bind(
            "<Leave>",
            self._on_leave,
            add="+",
        )

        widget.bind(
            "<ButtonPress>",
            self._on_leave,
            add="+",
        )

    def _on_enter(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self._cancel()

        try:
            self._after_id = self.widget.after(
                self.delay,
                self._show,
            )
        except tk.TclError:
            pass

    def _on_leave(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        self._cancel()
        self.hide()

    def _cancel(self) -> None:

        if self._after_id is None:
            return

        try:
            self.widget.after_cancel(
                self._after_id,
            )
        except (tk.TclError, ValueError):
            pass

        self._after_id = None

    def _show(self) -> None:

        self._after_id = None

        if self._window is not None:
            return

        try:
            x = (
                self.widget.winfo_rootx()
                + self.widget.winfo_width()
                + 8
            )

            y = (
                self.widget.winfo_rooty()
                + self.widget.winfo_height()
                + 4
            )
        except tk.TclError:
            return

        self._window = tk.Toplevel(
            self.widget,
        )

        self._window.overrideredirect(
            True,
        )

        self._window.attributes(
            "-topmost",
            True,
        )

        self._window.configure(
            bg=styles.TOOLTIP_BORDER,
        )

        container = tk.Frame(
            self._window,
            bg=styles.TOOLTIP_BG,
            bd=0,
            highlightthickness=0,
        )

        container.pack(
            padx=1,
            pady=1,
        )

        label = tk.Label(
            container,
            text=self.text,
            bg=styles.TOOLTIP_BG,
            fg=styles.TOOLTIP_TEXT,
            font=styles.TOOLTIP_FONT,
            padx=9,
            pady=6,
        )

        label.pack()

        self._window.geometry(
            "+{}+{}".format(
                x,
                y,
            )
        )

        try:
            self._window.after(
                styles.TOOLTIP_DURATION_MS,
                self.hide,
            )
        except tk.TclError:
            pass

    def hide(self) -> None:

        if self._window is None:
            return

        try:
            self._window.destroy()
        except tk.TclError:
            pass

        self._window = None

    def destroy(self) -> None:

        self._cancel()
        self.hide()


# ============================================================================
# SCROLLABLE FRAME
# ============================================================================

class ScrollableFrame(tk.Frame):
    """
    Lightweight scrollable content container.

    Structure:

        ScrollableFrame
            └── Canvas
                └── content_frame
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        background: str = styles.CONTENT_BG,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            bg=background,
            bd=0,
            highlightthickness=0,
            **kwargs,
        )

        self.background = background

        self.canvas = tk.Canvas(
            self,
            bg=background,
            highlightthickness=0,
            bd=0,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            width=styles.SCROLLBAR_WIDTH,
            bg=styles.SCROLLBAR_TRACK,
            troughcolor=styles.SCROLLBAR_BG,
            activebackground=styles.SCROLLBAR_THUMB_HOVER,
            highlightthickness=0,
            bd=0,
        )

        self.scrollbar.pack(
            side="right",
            fill="y",
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set,
        )

        self.content = tk.Frame(
            self.canvas,
            bg=background,
            bd=0,
            highlightthickness=0,
        )

        self._window_id = self.canvas.create_window(
            0,
            0,
            anchor="nw",
            window=self.content,
        )

        self.content.bind(
            "<Configure>",
            self._on_content_configure,
        )

        self.canvas.bind(
            "<Configure>",
            self._on_canvas_configure,
        )

        self.canvas.bind(
            "<MouseWheel>",
            self._on_mousewheel,
        )

        self.content.bind(
            "<MouseWheel>",
            self._on_mousewheel,
        )

    def _on_content_configure(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        try:
            self.canvas.configure(
                scrollregion=self.canvas.bbox(
                    "all",
                )
            )
        except tk.TclError:
            pass

    def _on_canvas_configure(
        self,
        event: Optional[tk.Event] = None,
    ) -> None:

        try:
            self.canvas.itemconfigure(
                self._window_id,
                width=self.canvas.winfo_width(),
            )
        except tk.TclError:
            pass

    def _on_mousewheel(
        self,
        event: tk.Event,
    ) -> str:

        delta = _safe_int(
            getattr(
                event,
                "delta",
                0,
            ),
        )

        if delta:
            self.canvas.yview_scroll(
                int(-delta / 120),
                "units",
            )

        return "break"

    def scroll_to_top(self) -> None:

        try:
            self.canvas.yview_moveto(
                0.0,
            )
        except tk.TclError:
            pass


# ============================================================================
# PAGE CONTAINER
# ============================================================================

class PageContainer(PremiumFrame):
    """
    Standard content container for application pages.

    Provides:
        - consistent background
        - content padding
        - optional header
        - scrollable content
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        background: str = styles.CONTENT_BG,
        scrollable: bool = False,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=background,
            **kwargs,
        )

        self.background = background

        if scrollable:
            self.body = ScrollableFrame(
                self,
                background=background,
            )

            self.body.pack(
                fill="both",
                expand=True,
            )

            self.content = self.body.content

        else:
            self.content = tk.Frame(
                self,
                bg=background,
                bd=0,
                highlightthickness=0,
            )

            self.content.pack(
                fill="both",
                expand=True,
                padx=styles.CONTENT_PAD_X,
                pady=(
                    styles.CONTENT_PAD_TOP,
                    styles.CONTENT_PAD_BOTTOM,
                ),
            )


# ============================================================================
# SEARCH BAR
# ============================================================================

class SearchBar(PremiumFrame):
    """
    Search input with optional search button.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        placeholder: str = "Search...",
        command: Callback = None,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.APP_BG,
            **kwargs,
        )

        self.entry = ModernEntry(
            self,
            placeholder=placeholder,
            icon="⌕",
            command=command,
        )

        self.entry.pack(
            fill="both",
            expand=True,
        )

    def get(self) -> str:
        return self.entry.get()

    def clear(self) -> None:
        self.entry.clear()


# ============================================================================
# ACTION ROW
# ============================================================================

class ActionRow(PremiumFrame):
    """
    Horizontal action container.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        spacing: int = styles.ELEMENT_GAP,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.APP_BG,
            **kwargs,
        )

        self.spacing = spacing

    def add(
        self,
        widget: tk.Widget,
        **pack_kwargs: Any,
    ) -> tk.Widget:

        if "padx" not in pack_kwargs:
            pack_kwargs["padx"] = (
                0,
                self.spacing,
            )

        widget.pack(
            side="left",
            **pack_kwargs,
        )

        return widget


# ============================================================================
# ANIMATED VALUE
# ============================================================================

class AnimatedValue(tk.Label, AnimationMixin):
    """
    Smoothly interpolated numeric/text value.

    Intended for:
        CPU
        memory
        network speed
        percentages
        counters
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        value: float = 0.0,
        suffix: str = "",
        decimals: int = 0,
        **kwargs: Any,
    ) -> None:

        self._animation_jobs = {}
        self._animation_generation = {}

        self._value = float(value)
        self._suffix = suffix
        self._decimals = decimals

        kwargs.setdefault(
            "bg",
            styles.CARD_BG,
        )

        kwargs.setdefault(
            "fg",
            styles.TEXT_PRIMARY,
        )

        kwargs.setdefault(
            "font",
            styles.FONT_STATUS_VALUE_LARGE,
        )

        kwargs.setdefault(
            "anchor",
            "w",
        )

        super().__init__(
            master,
            **kwargs,
        )

        self._refresh()

    def _format_value(
        self,
        value: float,
    ) -> str:

        if self._decimals <= 0:
            text = str(
                int(round(value))
            )
        else:
            text = (
                "{:."
                + str(self._decimals)
                + "f}"
            ).format(value)

        return text + self._suffix

    def _refresh(self) -> None:

        try:
            self.configure(
                text=self._format_value(
                    self._value,
                )
            )
        except tk.TclError:
            pass

    def set(
        self,
        value: float,
        animate: bool = True,
    ) -> None:

        target = float(value)
        start = self._value

        if not animate or not styles.ANIMATIONS_ENABLED:
            self._value = target
            self._refresh()
            return

        def update(progress: float) -> None:

            self._value = (
                start
                + (
                    target
                    - start
                )
                * progress
            )

            self._refresh()

        self.animate(
            name="value",
            duration=styles.ANIMATION_NORMAL_MS,
            steps=16,
            update=update,
            easing=styles.EASING_EASE_OUT,
        )

    def get(self) -> float:
        return self._value


# ============================================================================
# EMPTY STATE
# ============================================================================

class EmptyState(PremiumFrame):
    """
    Empty content state.

    Useful when a tool has no result yet.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        icon: str = "◇",
        title: str = "Nothing here yet",
        description: str = "",
        **kwargs: Any,
    ) -> None:

        super().__init__(
            master,
            background=styles.APP_BG,
            **kwargs,
        )

        self._icon = tk.Label(
            self,
            text=icon,
            bg=styles.APP_BG,
            fg=styles.MUTED,
            font=styles.FONT_DISPLAY_SMALL,
        )

        self._icon.pack(
            pady=(20, 10),
        )

        self._title = tk.Label(
            self,
            text=title,
            bg=styles.APP_BG,
            fg=styles.TEXT_PRIMARY,
            font=styles.FONT_TITLE_SMALL,
        )

        self._title.pack()

        if description:
            self._description = tk.Label(
                self,
                text=description,
                bg=styles.APP_BG,
                fg=styles.TEXT_TERTIARY,
                font=styles.FONT_CARD_DESC,
                justify="center",
                wraplength=500,
            )

            self._description.pack(
                pady=(7, 20),
            )


# ============================================================================
# NOTIFICATION
# ============================================================================

class Notification(PremiumFrame):
    """
    Temporary application notification.

    It can be attached to the root window or another top-level container.
    """

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        title: str = "",
        message: str = "",
        status: str = styles.STATUS_READY,
        duration: int = styles.NOTIFICATION_DURATION_MS,
        **kwargs: Any,
    ) -> None:

        accent = styles.get_status_color(
            status,
        )

        super().__init__(
            master,
            background=styles.PANEL_ELEVATED,
            **kwargs,
        )

        self.configure(
            highlightthickness=1,
            highlightbackground=accent,
        )

        self._accent = tk.Frame(
            self,
            bg=accent,
            width=3,
        )

        self._accent.pack(
            side="left",
            fill="y",
        )

        self._body = tk.Frame(
            self,
            bg=styles.PANEL_ELEVATED,
        )

        self._body.pack(
            side="left",
            fill="both",
            expand=True,
            padx=14,
            pady=10,
        )

        self._title = tk.Label(
            self._body,
            text=title,
            bg=styles.PANEL_ELEVATED,
            fg=styles.TEXT_PRIMARY,
            font=styles.FONT_CARD_TITLE,
            anchor="w",
        )

        self._title.pack(
            fill="x",
        )

        self._message = tk.Label(
            self._body,
            text=message,
            bg=styles.PANEL_ELEVATED,
            fg=styles.TEXT_TERTIARY,
            font=styles.FONT_CARD_DESC_SMALL,
            anchor="w",
            justify="left",
        )

        self._message.pack(
            fill="x",
            pady=(3, 0),
        )

        if duration > 0:
            try:
                self.after(
                    duration,
                    self.destroy,
                )
            except tk.TclError:
                pass


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "AnimationMixin",
    "PremiumFrame",
    "GlassCard",
    "SectionHeader",
    "PremiumButton",
    "IconButton",
    "NavigationItem",
    "StatusIndicator",
    "MetricCard",
    "StatusCard",
    "ModernEntry",
    "ToggleSwitch",
    "AnimatedProgressBar",
    "Divider",
    "PremiumLabel",
    "ToolCard",
    "InfoRow",
    "StatusChip",
    "LoadingIndicator",
    "Tooltip",
    "ScrollableFrame",
    "PageContainer",
    "SearchBar",
    "ActionRow",
    "AnimatedValue",
    "EmptyState",
    "Notification",
]