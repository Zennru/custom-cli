"""
colors.py — Konstanta warna ANSI dan helper formatting untuk terminal.

Menyediakan escape codes warna agar output CLI tampil lebih informatif
dan menarik. Mendukung deteksi otomatis apakah terminal mendukung warna.
"""

import os
import sys

# ─── Deteksi Dukungan Warna ──────────────────────────────────────────
def _supports_color():
    """Cek apakah terminal mendukung ANSI escape codes."""
    # Jika di-pipe ke file, nonaktifkan warna
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    # Windows Terminal & modern terminals mendukung ANSI
    if os.name == "nt":
        return os.environ.get("TERM") or os.environ.get("WT_SESSION") or True
    return True

_COLOR_ENABLED = _supports_color()

# ─── ANSI Escape Codes ──────────────────────────────────────────────
# Style
RESET     = "\033[0m"   if _COLOR_ENABLED else ""
BOLD      = "\033[1m"   if _COLOR_ENABLED else ""
DIM       = "\033[2m"   if _COLOR_ENABLED else ""
UNDERLINE = "\033[4m"   if _COLOR_ENABLED else ""

# Foreground Colors
BLACK     = "\033[30m"  if _COLOR_ENABLED else ""
RED       = "\033[31m"  if _COLOR_ENABLED else ""
GREEN     = "\033[32m"  if _COLOR_ENABLED else ""
YELLOW    = "\033[33m"  if _COLOR_ENABLED else ""
BLUE      = "\033[34m"  if _COLOR_ENABLED else ""
MAGENTA   = "\033[35m"  if _COLOR_ENABLED else ""
CYAN      = "\033[36m"  if _COLOR_ENABLED else ""
WHITE     = "\033[37m"  if _COLOR_ENABLED else ""

# Bright Foreground Colors
BRIGHT_RED     = "\033[91m"  if _COLOR_ENABLED else ""
BRIGHT_GREEN   = "\033[92m"  if _COLOR_ENABLED else ""
BRIGHT_YELLOW  = "\033[93m"  if _COLOR_ENABLED else ""
BRIGHT_BLUE    = "\033[94m"  if _COLOR_ENABLED else ""
BRIGHT_MAGENTA = "\033[95m"  if _COLOR_ENABLED else ""
BRIGHT_CYAN    = "\033[96m"  if _COLOR_ENABLED else ""
BRIGHT_WHITE   = "\033[97m"  if _COLOR_ENABLED else ""


# ─── Helper Functions ────────────────────────────────────────────────
def colorize(text, *styles):
    """
    Membungkus teks dengan kode warna/style ANSI.

    Args:
        text: Teks yang akan diwarnai.
        *styles: Satu atau lebih konstanta warna/style.

    Returns:
        String dengan escape codes ANSI.

    Contoh:
        colorize("Hello", BOLD, GREEN)  →  "\\033[1m\\033[32mHello\\033[0m"
    """
    if not _COLOR_ENABLED:
        return text
    prefix = "".join(styles)
    return f"{prefix}{text}{RESET}"


def error_text(text):
    """Format teks sebagai pesan error (merah + bold)."""
    return colorize(text, BOLD, RED)


def success_text(text):
    """Format teks sebagai pesan sukses (hijau + bold)."""
    return colorize(text, BOLD, GREEN)


def info_text(text):
    """Format teks sebagai informasi (cyan)."""
    return colorize(text, CYAN)


def warning_text(text):
    """Format teks sebagai peringatan (kuning + bold)."""
    return colorize(text, BOLD, YELLOW)
