"""
pwd.py — Implementasi perintah built-in `pwd` (Tahap 3).

Menampilkan jalur direktori aktif (current working directory) saat ini.
"""

import os

from utils.colors import BOLD, BRIGHT_CYAN, RESET


def execute(args):
    """
    Jalankan perintah pwd.

    Menampilkan path absolut dari direktori aktif saat ini.

    Args:
        args: List argumen (diabaikan untuk pwd).

    Returns:
        None
    """
    cwd = os.getcwd()
    print(f"{BOLD}{BRIGHT_CYAN}{cwd}{RESET}")
