"""
repl.py — REPL (Read-Evaluate-Print Loop) utama untuk JenShell (Tahap 1).

Modul ini menjalankan loop utama shell:
1. Tampilkan welcome banner saat pertama kali
2. Tampilkan prompt
3. Baca input pengguna
4. Parse input menjadi command dan arguments
5. Dispatch ke built-in command atau tampilkan info
6. Ulangi hingga pengguna mengetik 'exit'
"""

import os
import sys
import getpass
import platform
from datetime import datetime


def _setup_encoding():
    """Konfigurasi encoding UTF-8 untuk stdout/stderr di Windows."""
    if os.name == "nt":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

from core.prompt import get_prompt
from core.parser import parse_input
from commands.builtin import is_builtin, execute_builtin
from utils.colors import (
    BOLD, RESET, DIM,
    CYAN, GREEN, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_BLUE,
    YELLOW, BRIGHT_YELLOW, MAGENTA, BRIGHT_MAGENTA,
    error_text, warning_text, info_text
)


# ─── Versi Shell ─────────────────────────────────────────────────────
SHELL_VERSION = "1.0.0"
SHELL_NAME = "JenShell"


def _show_banner():
    """Tampilkan welcome banner saat shell pertama kali dijalankan."""
    username = getpass.getuser()
    now = datetime.now().strftime("%d %B %Y, %H:%M")
    os_info = f"{platform.system()} {platform.release()}"

    banner = f"""
{BOLD}{BRIGHT_CYAN}  ╔══════════════════════════════════════════════╗{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}     {BOLD}{BRIGHT_GREEN}🐚 {SHELL_NAME} v{SHELL_VERSION}{RESET}                      {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}     {DIM}Custom CLI Shell - Kelompok 7{RESET}          {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ╠══════════════════════════════════════════════╣{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}  {DIM}User   :{RESET} {BOLD}{BRIGHT_GREEN}{username:<30}{RESET}     {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}  {DIM}OS     :{RESET} {YELLOW}{os_info:<30}{RESET}     {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}  {DIM}Waktu  :{RESET} {MAGENTA}{now:<30}{RESET}     {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ╠══════════════════════════════════════════════╣{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}  {DIM}Ketik{RESET} {BOLD}{BRIGHT_GREEN}help{RESET} {DIM}untuk melihat daftar perintah{RESET}  {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ║{RESET}  {DIM}Ketik{RESET} {BOLD}{BRIGHT_GREEN}exit{RESET} {DIM}untuk keluar dari shell{RESET}      {BOLD}{BRIGHT_CYAN}║{RESET}
{BOLD}{BRIGHT_CYAN}  ╚══════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def _exit_shell():
    """Tampilkan pesan farewell saat keluar dari shell."""
    print()
    print(f"  {BOLD}{BRIGHT_CYAN}✦{RESET} {DIM}Leaving {SHELL_NAME}. See you later!{RESET} {BOLD}{BRIGHT_GREEN}👋{RESET}")
    print()


def run():
    """
    Jalankan REPL loop utama JenShell.

    Flow:
        1. Tampilkan banner
        2. Loop: prompt → input → parse → dispatch → ulangi
        3. Berhenti saat user mengetik 'exit' atau EOF
    """
    # Setup encoding UTF-8 untuk Windows
    _setup_encoding()

    # Aktifkan ANSI support di Windows jika perlu
    if os.name == "nt":
        os.system("")  # Trick untuk enable ANSI escape codes di Windows cmd

    # Tampilkan welcome banner
    _show_banner()

    # ─── Main REPL Loop ─────────────────────────────────────────────
    while True:
        try:
            # Tampilkan prompt dan baca input
            user_input = input(get_prompt())

            # Parse input
            command, arguments = parse_input(user_input)

            # Input kosong → skip
            if command is None:
                continue

            # Perintah exit → keluar
            if command == "exit":
                _exit_shell()
                break

            # Cek apakah built-in command
            if is_builtin(command):
                execute_builtin(command, arguments)
                continue

            # Perintah tidak dikenal (akan ditangani di tahap selanjutnya)
            print(
                error_text(f"  ✗ Perintah tidak ditemukan: '{command}'")
                + f"\n  {DIM}Ketik {BOLD}help{RESET}{DIM} untuk melihat daftar perintah yang tersedia.{RESET}"
            )

        except KeyboardInterrupt:
            # Ctrl+C → baris baru, lanjutkan
            print(f"\n{DIM}  (Tekan Ctrl+C sekali lagi atau ketik 'exit' untuk keluar){RESET}")
            continue

        except EOFError:
            # Ctrl+D / EOF → keluar
            _exit_shell()
            break

        except Exception as e:
            # Tangkap error tak terduga
            print(error_text(f"  ✗ Error tak terduga: {e}"))
            continue
