"""颜色和字体配置，支持 light/dark 模式"""

COLORS = {
    "light": {
        "bg": "#F5F5F7",
        "fg": "#1D1D1F",
        "accent": "#FF6B6B",
        "accent_break": "#4ECDC4",
        "button_fg": "#FFFFFF",
        "button_hover": "#E8E8ED",
        "timer_text": "#1D1D1F",
        "progress_bg": "#E5E5EA",
        "progress_fg": "#FF6B6B",
        "titlebar_bg": "#E8E8ED",
        "dot_red": "#FF5F57",
        "dot_yellow": "#FEBC2E",
        "dot_green": "#28C840",
    },
    "dark": {
        "bg": "#1C1C1E",
        "fg": "#F5F5F7",
        "accent": "#FF6B6B",
        "accent_break": "#4ECDC4",
        "button_fg": "#2C2C2E",
        "button_hover": "#3A3A3C",
        "timer_text": "#F5F5F7",
        "progress_bg": "#2C2C2E",
        "progress_fg": "#FF6B6B",
        "titlebar_bg": "#2C2C2E",
        "dot_red": "#FF5F57",
        "dot_yellow": "#FEBC2E",
        "dot_green": "#28C840",
    },
}

FONTS = {
    "timer_display": ("SF Pro Display", 72, "bold"),
    "timer_display_fallback": ("Segoe UI", 72, "bold"),
    "phase_label": ("SF Pro Text", 16),
    "phase_label_fallback": ("Segoe UI", 16),
    "button": ("SF Pro Text", 14),
    "button_fallback": ("Segoe UI", 14),
    "session": ("SF Pro Text", 12),
    "session_fallback": ("Segoe UI", 12),
}

# 番茄钟时长配置（秒）
WORK_DURATION = 25 * 60
SHORT_BREAK_DURATION = 5 * 60
LONG_BREAK_DURATION = 15 * 60
SESSIONS_BEFORE_LONG_BREAK = 4


def get_font(name: str) -> tuple:
    """获取字体配置，tkinter 会自动 fallback"""
    return FONTS[name]
