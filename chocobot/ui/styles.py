
# -*- coding: utf-8 -*-
"""
styles.py
Chocobot Guardian — Futuristic Enterprise Design System

Pusat seluruh konfigurasi visual Chocobot Guardian.

Prinsip desain:
    1. Futuristic
    2. Premium
    3. Clean
    4. Consistent
    5. Lightweight
    6. Tkinter compatible
    7. Windows 7 — Windows 11 friendly

CATATAN PENTING
---------------
File ini hanya menangani DESIGN SYSTEM.

Tidak ada:
    - API
    - server
    - database
    - network request
    - external UI framework

Seluruh komponen UI dapat menggunakan konstanta dari file ini.

Compatibility:
    Nama-nama konstanta lama tetap dipertahankan agar
    widgets.py dan screen lama tetap dapat berjalan.
"""

# ============================================================================
# 01. CORE APPLICATION COLORS
# ============================================================================

# Background utama.
APP_BG = "#080b0f"

# Background sekunder.
APP_BG_2 = "#0b0f14"

# Background ketiga untuk area transisi.
APP_BG_3 = "#0e141a"

# Sidebar.
SIDEBAR_BG = "#070a0e"

# Header.
HEADER_BG = "#090d12"

# Panel utama.
PANEL = "#10161d"

# Panel kedua.
PANEL_2 = "#141b23"

# Panel ketiga / elevated.
PANEL_3 = "#18212a"

# Panel sangat gelap.
PANEL_DARK = "#0a0e13"

# Entry / input.
ENTRY_BG = "#0a0f14"

# Tooltip.
TOOLTIP_BG = "#151e27"

# ============================================================================
# 02. BORDER SYSTEM
# ============================================================================

BORDER = "#202c35"

BORDER_SOFT = "#172129"

BORDER_STRONG = "#30414c"

BORDER_ACTIVE = "#3b5b66"

BORDER_CYAN = "#164954"

BORDER_PURPLE = "#3b2e58"

BORDER_MAGENTA = "#55233f"


# ============================================================================
# 03. TEXT SYSTEM
# ============================================================================

TEXT = "#edf5f8"

TEXT_PRIMARY = "#edf5f8"

TEXT_SECONDARY = "#b4c2ca"

TEXT_TERTIARY = "#7f909b"

MUTED = "#71818d"

MUTED_2 = "#52616c"

DISABLED = "#3e4b54"

WHITE = "#ffffff"


# ============================================================================
# 04. PRIMARY ACCENTS
# ============================================================================

CYAN = "#00e5ff"

CYAN_BRIGHT = "#54f4ff"

CYAN_SOFT = "#83f7ff"

CYAN_DIM = "#087d8a"

CYAN_DARK = "#07323a"


PURPLE = "#9b6cff"

PURPLE_BRIGHT = "#b18aff"

PURPLE_SOFT = "#c5adff"

PURPLE_DIM = "#62439b"

PURPLE_DARK = "#281b40"


MAGENTA = "#ff3cac"

MAGENTA_BRIGHT = "#ff69c2"

MAGENTA_SOFT = "#ff9bd5"

MAGENTA_DIM = "#a52a70"

MAGENTA_DARK = "#43132e"


# ============================================================================
# 05. SEMANTIC COLORS
# ============================================================================

GREEN = "#35e6a2"

GREEN_BRIGHT = "#68f6bd"

GREEN_DIM = "#218f68"

GREEN_DARK = "#123c30"


YELLOW = "#ffd166"

YELLOW_BRIGHT = "#ffe29a"

YELLOW_DIM = "#a88432"

YELLOW_DARK = "#443713"


RED = "#ff5577"

RED_BRIGHT = "#ff7893"

RED_DIM = "#a43852"

RED_DARK = "#421b27"


ORANGE = "#ff9f43"

ORANGE_BRIGHT = "#ffbd72"

ORANGE_DIM = "#a96528"

ORANGE_DARK = "#43270f"


# ============================================================================
# 06. INTERACTION COLORS
# ============================================================================

HOVER_GRADIENT_START = "#111c23"

HOVER_GRADIENT_END = "#18262f"

BUTTON_HOVER_BG = "#1a252d"

BUTTON_ACTIVE_BG = "#20323b"

ACTIVE_NAV_BG = "#10242b"

ACTIVE_NAV_BG_2 = "#132e36"

NAV_HOVER_BG = "#0e181e"

NAV_SELECTED_BORDER = "#00a9bc"

FOCUS_BG = "#10232a"

SELECTED_BG = "#13282f"


# ============================================================================
# 07. GLOW / ATMOSPHERE COLORS
# ============================================================================

GLOW_CYAN = "#00e5ff"

GLOW_PURPLE = "#9b6cff"

GLOW_MAGENTA = "#ff3cac"

GLOW_GREEN = "#35e6a2"

GLOW_YELLOW = "#ffd166"

GLOW_RED = "#ff5577"


# ============================================================================
# 08. GLASS / DEPTH COLORS
# ============================================================================

GLASS_1 = "#0c1218"

GLASS_2 = "#101820"

GLASS_3 = "#141e27"

GLASS_4 = "#19252f"

GLASS_HIGHLIGHT = "#22333e"

SHADOW = "#040608"

SHADOW_SOFT = "#06090c"


# ============================================================================
# 09. TYPOGRAPHY
# ============================================================================

# Tkinter paling aman menggunakan tuple untuk font configuration.
# Namun string lama tetap dipertahankan untuk compatibility.

FONT_FAMILY = "Segoe UI"

FONT_FAMILY_FALLBACK = "Arial"


# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

FONT_HERO = (
    FONT_FAMILY,
    27,
    "bold",
)

FONT_TITLE = (
    FONT_FAMILY,
    23,
    "bold",
)

FONT_TITLE_SMALL = (
    FONT_FAMILY,
    18,
    "bold",
)

FONT_SUBTITLE = (
    FONT_FAMILY,
    10,
)

FONT_SUBTITLE_SMALL = (
    FONT_FAMILY,
    9,
)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------

FONT_BRAND = (
    FONT_FAMILY,
    17,
    "bold",
)

FONT_BRAND_SUB = (
    FONT_FAMILY,
    7,
    "bold",
)

FONT_SIDEBAR_ITEM = (
    FONT_FAMILY,
    9,
)

FONT_SIDEBAR_ITEM_ACTIVE = (
    FONT_FAMILY,
    9,
    "bold",
)

FONT_SIDEBAR_SECTION = (
    FONT_FAMILY,
    7,
    "bold",
)


# ---------------------------------------------------------------------------
# CARDS
# ---------------------------------------------------------------------------

FONT_CARD_TITLE = (
    FONT_FAMILY,
    10,
    "bold",
)

FONT_CARD_TITLE_LARGE = (
    FONT_FAMILY,
    13,
    "bold",
)

FONT_CARD_DESC = (
    FONT_FAMILY,
    9,
)

FONT_CARD_VALUE = (
    FONT_FAMILY,
    18,
    "bold",
)

FONT_CARD_SMALL = (
    FONT_FAMILY,
    8,
)


# ---------------------------------------------------------------------------
# STATUS
# ---------------------------------------------------------------------------

FONT_STATUS_TITLE = (
    FONT_FAMILY,
    7,
    "bold",
)

FONT_STATUS_VALUE = (
    FONT_FAMILY,
    15,
    "bold",
)

FONT_STATUS_DESC = (
    FONT_FAMILY,
    9,
)


# ---------------------------------------------------------------------------
# FORM
# ---------------------------------------------------------------------------

FONT_ENTRY = (
    FONT_FAMILY,
    10,
)

FONT_BUTTON = (
    FONT_FAMILY,
    9,
    "bold",
)

FONT_BUTTON_SMALL = (
    FONT_FAMILY,
    8,
    "bold",
)

FONT_LABEL = (
    FONT_FAMILY,
    8,
    "bold",
)


# ---------------------------------------------------------------------------
# MONOSPACE / TECHNICAL
# ---------------------------------------------------------------------------

FONT_MONO = (
    "Consolas",
    9,
)

FONT_MONO_SMALL = (
    "Consolas",
    8,
)

FONT_MONO_TINY = (
    "Consolas",
    7,
)


# ============================================================================
# 10. LEGACY FONT STRING COMPATIBILITY
# ============================================================================

# widgets.py lama dapat menggunakan format string.
# Oleh karena itu kita tetap menyediakan versi string.

FONT_TITLE_STR = "Segoe UI 23 bold"
FONT_SUBTITLE_STR = "Segoe UI 10"
FONT_SIDEBAR_ITEM_STR = "Segoe UI 9"
FONT_SIDEBAR_SECTION_STR = "Segoe UI 7 bold"
FONT_CARD_TITLE_STR = "Segoe UI 10 bold"
FONT_CARD_DESC_STR = "Segoe UI 9"
FONT_BRAND_STR = "Segoe UI 17 bold"
FONT_BRAND_SUB_STR = "Segoe UI 7 bold"
FONT_STATUS_TITLE_STR = "Segoe UI 7 bold"
FONT_STATUS_VALUE_STR = "Segoe UI 15 bold"
FONT_ENTRY_STR = "Segoe UI 10"


# ============================================================================
# 11. LAYOUT DIMENSIONS
# ============================================================================

# Sidebar.
SIDEBAR_WIDTH = 238

# Header.
HEADER_HEIGHT = 58

# Main content.
CONTENT_PAD_X = 30
CONTENT_PAD_TOP = 25
CONTENT_PAD_BOTTOM = 30

# Card.
CARD_PAD_X = 17
CARD_PAD_Y = 15

# Navigation.
NAV_PAD_X = 18
NAV_PAD_Y = 6

# Sidebar internal padding.
SIDEBAR_PAD_X = 16
SIDEBAR_PAD_TOP = 18
SIDEBAR_PAD_BOTTOM = 16


# ============================================================================
# 12. COMPONENT DIMENSIONS
# ============================================================================

# Button.
BUTTON_HEIGHT = 36
BUTTON_MIN_WIDTH = 100

# Small button.
BUTTON_SMALL_HEIGHT = 30

# Input.
ENTRY_HEIGHT = 34

# Status indicator.
STATUS_DOT_SIZE = 8

# Navigation icon area.
NAV_ICON_WIDTH = 30

# Card minimum dimensions.
CARD_MIN_WIDTH = 210
CARD_MIN_HEIGHT = 125


# ============================================================================
# 13. CORNER RADIUS SYSTEM
# ============================================================================

RADIUS_XS = 5

RADIUS_SM = 9

RADIUS_MD = 13

RADIUS_LG = 18

RADIUS_XL = 24

RADIUS_XXL = 30


# Legacy aliases.
RADIUS_CARD = RADIUS_LG
RADIUS_BUTTON = RADIUS_MD
RADIUS_PANEL = RADIUS_XL


# ============================================================================
# 14. BORDER WIDTH
# ============================================================================

BORDER_WIDTH_THIN = 1

BORDER_WIDTH_NORMAL = 1

BORDER_WIDTH_ACTIVE = 2

BORDER_WIDTH_FOCUS = 2


# ============================================================================
# 15. SHADOW SYSTEM
# ============================================================================

SHADOW_OFFSET_X = 0

SHADOW_OFFSET_Y = 5

SHADOW_LAYERS = 5

SHADOW_ALPHA = 0.28

SHADOW_SOFT_ALPHA = 0.16


# ============================================================================
# 16. ANIMATION SYSTEM
# ============================================================================

# General animation frame interval.
ANIMATION_FRAME_MS = 16

# ~60 FPS.
ANIMATION_FPS = 60


# Navigation.
NAV_ANIMATION_MS = 180

NAV_TRANSITION_STEPS = 10


# Hover.
HOVER_ANIMATION_MS = 16

HOVER_TRANSITION_STEPS = 12

HOVER_LIFT_PX = 3

HOVER_GLOW_ALPHA = 0.28


# Page transitions.
PAGE_TRANSITION_MS = 220

PAGE_TRANSITION_STEPS = 14

PAGE_SLIDE_DISTANCE = 22


# Fade.
FADE_IN_MS = 220

FADE_OUT_MS = 180


# General smooth animation.
ANIMATION_SMOOTH_MS = 220


# ============================================================================
# 17. MICRO INTERACTION
# ============================================================================

# Hover scale simulation.
HOVER_SCALE = 1.015

# Button press movement.
BUTTON_PRESS_OFFSET = 1

# Tooltip delay.
TOOLTIP_DELAY_MS = 550

# Cursor transition delay.
CURSOR_DELAY_MS = 30


# ============================================================================
# 18. SIDEBAR SYSTEM
# ============================================================================

SIDEBAR_BORDER_WIDTH = 1

SIDEBAR_SECTION_GAP = 13

SIDEBAR_ITEM_HEIGHT = 38

SIDEBAR_ITEM_GAP = 3

SIDEBAR_ACTIVE_BAR_WIDTH = 3

SIDEBAR_ACTIVE_BAR_HEIGHT = 22


# ============================================================================
# 19. HEADER SYSTEM
# ============================================================================

HEADER_BORDER_WIDTH = 1

HEADER_TITLE_X = 28

HEADER_STATUS_GAP = 10


# ============================================================================
# 20. CONTENT GRID
# ============================================================================

GRID_GAP_X = 15

GRID_GAP_Y = 15

GRID_MIN_COLUMNS = 1

GRID_MAX_COLUMNS = 4


# ============================================================================
# 21. CARD SYSTEM
# ============================================================================

CARD_BORDER_WIDTH = 1

CARD_HOVER_BORDER_WIDTH = 1

CARD_SHADOW_OFFSET = 4

CARD_CONTENT_GAP = 8

CARD_ICON_SIZE = 34

CARD_ARROW_SIZE = 12


# ============================================================================
# 22. STATUS CARD
# ============================================================================

STATUS_CARD_HEIGHT = 110

STATUS_CARD_PADDING = 18

STATUS_INDICATOR_SIZE = 9


# ============================================================================
# 23. SCROLL / LIST SYSTEM
# ============================================================================

SCROLLBAR_WIDTH = 7

SCROLLBAR_MIN_HANDLE = 30

LIST_ROW_HEIGHT = 38

LIST_ROW_GAP = 2


# ============================================================================
# 24. NAVIGATION DATA
# ============================================================================

NAV_SECTIONS = [
    (
        "UTAMA",
        [
            (
                "HOME",
                "Home",
                "⌂",
            ),
        ],
    ),

    (
        "ALAT",
        [
            (
                "SECURITY",
                "Security Center",
                "◈",
            ),
            (
                "LINK",
                "Link Inspector",
                "↗",
            ),
            (
                "FILES",
                "File Tools",
                "□",
            ),
            (
                "CONVERTER",
                "Converter",
                "↻",
            ),
        ],
    ),

    (
        "SISTEM",
        [
            (
                "SYSTEM",
                "System",
                "▣",
            ),
            (
                "NETWORK",
                "Network",
                "◎",
            ),
            (
                "MONITOR",
                "Monitor",
                "◫",
            ),
        ],
    ),

    (
        "INFO & BANTUAN",
        [
            (
                "BLOG",
                "Official Blog",
                "◇",
            ),
            (
                "GUIDE",
                "User Guide",
                "?",
            ),
            (
                "DEVELOPER",
                "Developer",
                "◆",
            ),
            (
                "ABOUT",
                "About",
                "i",
            ),
            (
                "LICENSE",
                "License",
                "□",
            ),
            (
                "CONTACT",
                "Contact & Feedback",
                "✉",
            ),
        ],
    ),
]


# ============================================================================
# 25. FLAT PAGE LIST
# ============================================================================

PAGES = [
    (
        "HOME",
        "Home",
    ),

    (
        "SECURITY",
        "Security Center",
    ),

    (
        "LINK",
        "Link Inspector",
    ),

    (
        "FILES",
        "File Tools",
    ),

    (
        "CONVERTER",
        "Converter",
    ),

    (
        "SYSTEM",
        "System",
    ),

    (
        "NETWORK",
        "Network",
    ),

    (
        "MONITOR",
        "Monitor",
    ),

    (
        "SETTINGS",
        "Settings",
    ),

    (
        "BLOG",
        "Official Blog",
    ),

    (
        "GUIDE",
        "User Guide",
    ),

    (
        "DEVELOPER",
        "Developer",
    ),

    (
        "ABOUT",
        "About",
    ),

    (
        "LICENSE",
        "License",
    ),

    (
        "CONTACT",
        "Contact & Feedback",
    ),
]


# ============================================================================
# 26. PAGE ACCENT COLORS
# ============================================================================

PAGE_ACCENTS = {
    "HOME": CYAN,

    "SECURITY": GREEN,

    "LINK": CYAN,

    "FILES": PURPLE,

    "CONVERTER": MAGENTA,

    "SYSTEM": CYAN,

    "NETWORK": CYAN_BRIGHT,

    "MONITOR": PURPLE,

    "SETTINGS": MUTED,

    "BLOG": MAGENTA,

    "GUIDE": CYAN,

    "DEVELOPER": PURPLE,

    "ABOUT": CYAN,

    "LICENSE": YELLOW,

    "CONTACT": MAGENTA,
}


# ============================================================================
# 27. PAGE BACKGROUND TINTS
# ============================================================================

PAGE_TINTS = {
    "HOME": (
        APP_BG,
        "#0b151a",
    ),

    "SECURITY": (
        APP_BG,
        "#0b1512",
    ),

    "LINK": (
        APP_BG,
        "#0b1418",
    ),

    "FILES": (
        APP_BG,
        "#100d18",
    ),

    "CONVERTER": (
        APP_BG,
        "#160c13",
    ),

    "SYSTEM": (
        APP_BG,
        "#0b1418",
    ),

    "NETWORK": (
        APP_BG,
        "#09151a",
    ),

    "MONITOR": (
        APP_BG,
        "#100d18",
    ),

    "SETTINGS": (
        APP_BG,
        "#101215",
    ),

    "BLOG": (
        APP_BG,
        "#140b12",
    ),

    "GUIDE": (
        APP_BG,
        "#0b1418",
    ),

    "DEVELOPER": (
        APP_BG,
        "#100d18",
    ),

    "ABOUT": (
        APP_BG,
        "#0b1418",
    ),

    "LICENSE": (
        APP_BG,
        "#141109",
    ),

    "CONTACT": (
        APP_BG,
        "#140b12",
    ),
}


# ============================================================================
# 28. STATUS CONFIGURATION
# ============================================================================

STATUS_COLORS = {
    "protected": GREEN,
    "safe": GREEN,
    "healthy": GREEN,
    "ready": GREEN,

    "action": YELLOW,
    "warning": YELLOW,
    "attention": YELLOW,

    "danger": RED,
    "error": RED,
    "blocked": RED,

    "info": CYAN,
    "active": CYAN,

    "offline": MUTED,
    "disabled": MUTED,
}


# ============================================================================
# 29. BUTTON CONFIGURATION
# ============================================================================

BUTTON_STYLES = {
    "primary": {
        "bg": CYAN_DARK,
        "hover": "#0a5661",
        "active": "#0d6975",
        "fg": TEXT_PRIMARY,
        "border": CYAN_DIM,
    },

    "secondary": {
        "bg": PANEL_2,
        "hover": PANEL_3,
        "active": "#1d2a34",
        "fg": TEXT_PRIMARY,
        "border": BORDER,
    },

    "ghost": {
        "bg": APP_BG,
        "hover": NAV_HOVER_BG,
        "active": ACTIVE_NAV_BG,
        "fg": TEXT_SECONDARY,
        "border": BORDER_SOFT,
    },

    "danger": {
        "bg": RED_DARK,
        "hover": "#612536",
        "active": "#793044",
        "fg": TEXT_PRIMARY,
        "border": RED_DIM,
    },

    "success": {
        "bg": GREEN_DARK,
        "hover": "#18503d",
        "active": "#1d624a",
        "fg": TEXT_PRIMARY,
        "border": GREEN_DIM,
    },
}


# ============================================================================
# 30. CARD CONFIGURATION
# ============================================================================

CARD_STYLES = {
    "default": {
        "bg": PANEL,
        "hover": PANEL_2,
        "border": BORDER,
        "accent": CYAN,
    },

    "cyan": {
        "bg": "#0d171c",
        "hover": "#102027",
        "border": BORDER_CYAN,
        "accent": CYAN,
    },

    "purple": {
        "bg": "#120f19",
        "hover": "#171221",
        "border": BORDER_PURPLE,
        "accent": PURPLE,
    },

    "magenta": {
        "bg": "#160d13",
        "hover": "#1d1018",
        "border": BORDER_MAGENTA,
        "accent": MAGENTA,
    },

    "green": {
        "bg": "#0c1713",
        "hover": "#0f2019",
        "border": "#1b4a39",
        "accent": GREEN,
    },

    "warning": {
        "bg": "#17130a",
        "hover": "#211a0c",
        "border": "#4c3b17",
        "accent": YELLOW,
    },

    "danger": {
        "bg": "#170c10",
        "hover": "#211015",
        "border": "#4c1d2a",
        "accent": RED,
    },
}


# ============================================================================
# 31. ICON / SYMBOL COLORS
# ============================================================================

ICON_COLORS = {
    "default": TEXT_SECONDARY,
    "active": CYAN,
    "cyan": CYAN,
    "purple": PURPLE,
    "magenta": MAGENTA,
    "green": GREEN,
    "yellow": YELLOW,
    "red": RED,
    "muted": MUTED,
}


# ============================================================================
# 32. DIVIDER SYSTEM
# ============================================================================

DIVIDER = "#18232b"

DIVIDER_SOFT = "#121b21"

DIVIDER_STRONG = "#263640"


# ============================================================================
# 33. TOOLTIP SYSTEM
# ============================================================================

TOOLTIP_PADDING_X = 10

TOOLTIP_PADDING_Y = 7

TOOLTIP_RADIUS = 8

TOOLTIP_BORDER = BORDER_STRONG

TOOLTIP_TEXT = TEXT_PRIMARY


# ============================================================================
# 34. WINDOW CONFIGURATION
# ============================================================================

DEFAULT_WINDOW_WIDTH = 1280

DEFAULT_WINDOW_HEIGHT = 760

MIN_WINDOW_WIDTH = 980

MIN_WINDOW_HEIGHT = 620

WINDOW_BG = APP_BG


# ============================================================================
# 35. RESPONSIVE BREAKPOINTS
# ============================================================================

BREAKPOINT_SMALL = 1000

BREAKPOINT_MEDIUM = 1180

BREAKPOINT_LARGE = 1380

BREAKPOINT_XL = 1600


# ============================================================================
# 36. PERFORMANCE CONFIGURATION
# ============================================================================

# Sengaja tidak terlalu agresif.
# Tkinter pada perangkat low-end lebih stabil dengan jumlah frame
# yang terbatas.

MAX_ANIMATION_FPS = 60

LOW_SPEC_ANIMATION_FPS = 30

ANIMATION_CPU_FRIENDLY = True

USE_HEAVY_BLUR = False

USE_REAL_TIME_SHADOWS = False

USE_EXTERNAL_RENDERER = False


# ============================================================================
# 37. EFFECT CONFIGURATION
# ============================================================================

ENABLE_GLOW = True

ENABLE_HOVER_ANIMATION = True

ENABLE_PAGE_TRANSITION = True

ENABLE_FADE = True

ENABLE_SCAN_EFFECT = True

ENABLE_BACKGROUND_GRID = False

ENABLE_PARTICLE_EFFECT = False


# Background grid dan particle sengaja default OFF.
# Kita ingin futuristic tanpa membuat laptop AMD A8 / RAM 4GB
# bekerja terlalu keras.


# ============================================================================
# 38. ACCESSIBILITY / READABILITY
# ============================================================================

MIN_TEXT_CONTRAST = 0.45

USE_HIGH_CONTRAST_ACTIVE_STATE = True

USE_TEXT_LABELS_WITH_ICONS = True

AVOID_COLOR_ONLY_STATUS = True


# ============================================================================
# 39. APPLICATION BRANDING
# ============================================================================

BRAND_NAME = "CHOCOBOT"

BRAND_PRODUCT = "GUARDIAN"

BRAND_ENGINE = "CHOCOENGINE"

BRAND_FULL = "CHOCOBOT GUARDIAN"

BRAND_TAGLINE = "LOCAL WINDOWS UTILITY & SECURITY PLATFORM"

BRAND_SHORT_TAGLINE = "LOCAL • PRIVATE • SECURE"


# ============================================================================
# 40. SYSTEM LABELS
# ============================================================================

LOCAL_MODE_LABEL = "LOCAL MODE"

OFFLINE_MODE_LABEL = "OFFLINE"

SECURE_MODE_LABEL = "SECURE"

PROTECTED_LABEL = "PROTECTED"

ACTION_NEEDED_LABEL = "ACTION NEEDED"

READY_LABEL = "SYSTEM READY"


# ============================================================================
# 41. DEBUG / DEVELOPMENT
# ============================================================================

DEBUG_UI = False

SHOW_LAYOUT_GUIDES = False

SHOW_WIDGET_BOUNDS = False

SHOW_ANIMATION_DEBUG = False


# ============================================================================
# 42. COMPATIBILITY ALIASES
# ============================================================================
#
# Bagian ini sengaja ada supaya kode lama tetap bisa menggunakan nama
# konstanta terdahulu.
#

FONT_TITLE_LEGACY = "Segoe UI 23 bold"

FONT_SUBTITLE_LEGACY = "Segoe UI 10"

FONT_SIDEBAR_ITEM_LEGACY = "Segoe UI 9"

FONT_SIDEBAR_SECTION_LEGACY = "Segoe UI 7 bold"

FONT_CARD_TITLE_LEGACY = "Segoe UI 10 bold"

FONT_CARD_DESC_LEGACY = "Segoe UI 9"

FONT_BRAND_LEGACY = "Segoe UI 17 bold"

FONT_BRAND_SUB_LEGACY = "Segoe UI 7 bold"

FONT_STATUS_TITLE_LEGACY = "Segoe UI 7 bold"

FONT_STATUS_VALUE_LEGACY = "Segoe UI 15 bold"

FONT_ENTRY_LEGACY = "Segoe UI 10"


# ============================================================================
# 43. SAFE COLOR LOOKUP
# ============================================================================

def get_page_accent(page_key: str) -> str:
    """
    Mengambil accent color berdasarkan page key.

    Jika page tidak dikenal, gunakan CYAN.
    """
    if not page_key:
        return CYAN

    return PAGE_ACCENTS.get(
        str(page_key).upper(),
        CYAN,
    )


def get_status_color(status: str) -> str:
    """
    Mengambil warna status.

    Contoh:
        get_status_color("protected")
        get_status_color("warning")
        get_status_color("error")
    """
    if not status:
        return MUTED

    return STATUS_COLORS.get(
        str(status).lower(),
        MUTED,
    )


def get_card_style(
    style: str = "default",
) -> dict:
    """
    Mengambil konfigurasi card.

    Return selalu dictionary baru sehingga caller
    tidak mengubah CARD_STYLES secara tidak sengaja.
    """
    key = str(style or "default").lower()

    source = CARD_STYLES.get(
        key,
        CARD_STYLES["default"],
    )

    return dict(source)


def get_button_style(
    style: str = "secondary",
) -> dict:
    """
    Mengambil konfigurasi button.
    """
    key = str(style or "secondary").lower()

    source = BUTTON_STYLES.get(
        key,
        BUTTON_STYLES["secondary"],
    )

    return dict(source)


# ============================================================================
# 44. DESIGN TOKENS
# ============================================================================

DESIGN_TOKENS = {
    "colors": {
        "background": APP_BG,
        "panel": PANEL,
        "panel_2": PANEL_2,
        "panel_3": PANEL_3,
        "text": TEXT,
        "muted": MUTED,
        "cyan": CYAN,
        "purple": PURPLE,
        "magenta": MAGENTA,
        "green": GREEN,
        "yellow": YELLOW,
        "red": RED,
    },

    "radius": {
        "xs": RADIUS_XS,
        "sm": RADIUS_SM,
        "md": RADIUS_MD,
        "lg": RADIUS_LG,
        "xl": RADIUS_XL,
        "xxl": RADIUS_XXL,
    },

    "spacing": {
        "content_x": CONTENT_PAD_X,
        "content_top": CONTENT_PAD_TOP,
        "content_bottom": CONTENT_PAD_BOTTOM,
        "card_x": CARD_PAD_X,
        "card_y": CARD_PAD_Y,
        "nav_x": NAV_PAD_X,
        "nav_y": NAV_PAD_Y,
    },

    "animation": {
        "frame_ms": ANIMATION_FRAME_MS,
        "hover_ms": HOVER_ANIMATION_MS,
        "page_ms": PAGE_TRANSITION_MS,
        "fade_in_ms": FADE_IN_MS,
        "fade_out_ms": FADE_OUT_MS,
    },
}


# ============================================================================
# 45. END OF DESIGN SYSTEM
# ============================================================================

__all__ = [
    # Core colors
    "APP_BG",
    "APP_BG_2",
    "APP_BG_3",
    "SIDEBAR_BG",
    "HEADER_BG",
    "PANEL",
    "PANEL_2",
    "PANEL_3",
    "PANEL_DARK",
    "ENTRY_BG",

    # Borders
    "BORDER",
    "BORDER_SOFT",
    "BORDER_STRONG",
    "BORDER_ACTIVE",

    # Text
    "TEXT",
    "TEXT_PRIMARY",
    "TEXT_SECONDARY",
    "TEXT_TERTIARY",
    "MUTED",
    "MUTED_2",
    "DISABLED",
    "WHITE",

    # Accents
    "CYAN",
    "CYAN_BRIGHT",
    "CYAN_SOFT",
    "CYAN_DIM",
    "CYAN_DARK",

    "PURPLE",
    "PURPLE_BRIGHT",
    "PURPLE_SOFT",
    "PURPLE_DIM",
    "PURPLE_DARK",

    "MAGENTA",
    "MAGENTA_BRIGHT",
    "MAGENTA_SOFT",
    "MAGENTA_DIM",
    "MAGENTA_DARK",

    # Semantic
    "GREEN",
    "YELLOW",
    "RED",
    "ORANGE",

    # Interaction
    "ACTIVE_NAV_BG",
    "BUTTON_HOVER_BG",
    "HOVER_GRADIENT_START",
    "HOVER_GRADIENT_END",

    # Fonts
    "FONT_FAMILY",
    "FONT_HERO",
    "FONT_TITLE",
    "FONT_TITLE_SMALL",
    "FONT_SUBTITLE",
    "FONT_BRAND",
    "FONT_BRAND_SUB",
    "FONT_SIDEBAR_ITEM",
    "FONT_SIDEBAR_SECTION",
    "FONT_CARD_TITLE",
    "FONT_CARD_DESC",
    "FONT_STATUS_TITLE",
    "FONT_STATUS_VALUE",
    "FONT_ENTRY",
    "FONT_BUTTON",

    # Layout
    "SIDEBAR_WIDTH",
    "HEADER_HEIGHT",
    "CONTENT_PAD_X",
    "CONTENT_PAD_TOP",
    "CONTENT_PAD_BOTTOM",
    "CARD_PAD_X",
    "CARD_PAD_Y",
    "NAV_PAD_X",
    "NAV_PAD_Y",

    # Radius
    "RADIUS_XS",
    "RADIUS_SM",
    "RADIUS_MD",
    "RADIUS_LG",
    "RADIUS_XL",
    "RADIUS_XXL",

    # Animation
    "ANIMATION_FRAME_MS",
    "HOVER_ANIMATION_MS",
    "HOVER_TRANSITION_STEPS",
    "HOVER_LIFT_PX",
    "HOVER_GLOW_ALPHA",
    "PAGE_TRANSITION_MS",
    "ANIMATION_SMOOTH_MS",

    # Navigation
    "NAV_SECTIONS",
    "PAGES",

    # Helpers
    "get_page_accent",
    "get_status_color",
    "get_card_style",
    "get_button_style",

    # Tokens
    "DESIGN_TOKENS",
]
