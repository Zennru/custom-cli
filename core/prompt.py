"""
prompt.py — Membangun prompt shell yang informatif dan menarik.

Menampilkan prompt dua baris dengan informasi:
- Username sistem
- Direktori aktif (dengan shortcut ~ untuk home directory)
- Warna ANSI untuk membedakan elemen prompt
"""

import os
import getpass

from utils.colors import (
    BOLD, RESET, DIM,
    CYAN, GREEN, BRIGHT_BLUE, BRIGHT_CYAN, BRIGHT_GREEN, YELLOW
)


def _get_username():
    """Ambil username pengguna saat ini."""
    try:
        return getpass.getuser()
    except Exception:
        return "user"


def _shorten_path(path):
    """
    Singkat path dengan mengganti home directory menjadi ~.

    Contoh:
        /home/bahtiar/Documents → ~/Documents
        C:\\Users\\Bahtiar\\Documents → ~/Documents
    """
    home = os.path.expanduser("~")
    if path == home:
        return "~"
    if path.startswith(home):
        return "~" + path[len(home):].replace("\\", "/")
    return path.replace("\\", "/")


def get_prompt():
    """
    Bangun string prompt dua baris untuk shell.

    Format:
        ┌─[username@JenShell]─[~/path/to/dir]
        └─▶

    Returns:
        String prompt lengkap dengan ANSI color codes.
    """
    username = _get_username()
    cwd = _shorten_path(os.getcwd())

    # Baris 1: info user dan direktori
    line1 = (
        f"{DIM}┌─{RESET}"
        f"{BOLD}{GREEN}[{BRIGHT_GREEN}{username}"
        f"{GREEN}@{BRIGHT_CYAN}JenShell{GREEN}]{RESET}"
        f"{DIM}─{RESET}"
        f"{BOLD}{BRIGHT_BLUE}[{YELLOW}{cwd}{BRIGHT_BLUE}]{RESET}"
    )

    # Baris 2: input arrow
    line2 = f"{DIM}└─{RESET}{BOLD}{CYAN}▶{RESET} "

    return f"{line1}\n{line2}"
