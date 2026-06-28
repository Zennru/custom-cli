"""
builtin.py — Registry dan dispatcher untuk perintah built-in shell.

Mengelola daftar perintah built-in yang tersedia dan mendispatch
eksekusi ke modul handler yang sesuai.
"""

from commands import cd, pwd
from utils.colors import error_text, info_text, colorize, BOLD, BRIGHT_CYAN, YELLOW, DIM, RESET, GREEN, BRIGHT_GREEN


# ─── Registry Built-in Commands ─────────────────────────────────────
# Setiap entry: nama_perintah → (fungsi_handler, deskripsi_singkat)
BUILTIN_COMMANDS = {
    "cd":   (cd.execute,   "Mengubah direktori aktif"),
    "pwd":  (pwd.execute,  "Menampilkan jalur direktori aktif saat ini"),
    "help": (None,         "Menampilkan daftar perintah yang tersedia"),
    "exit": (None,         "Keluar dari JenShell"),
}


def is_builtin(command):
    """
    Cek apakah perintah termasuk built-in command.

    Args:
        command: Nama perintah (string).

    Returns:
        True jika perintah ada di registry, False jika tidak.
    """
    return command in BUILTIN_COMMANDS


def execute_builtin(command, args):
    """
    Jalankan built-in command yang sesuai.

    Args:
        command: Nama perintah (string).
        args: List argumen untuk perintah.

    Returns:
        True jika perintah berhasil di-dispatch, False jika tidak ditemukan.
    """
    if command not in BUILTIN_COMMANDS:
        return False

    handler, _ = BUILTIN_COMMANDS[command]

    # help dan exit ditangani khusus di REPL
    if command == "help":
        _show_help()
        return True

    if handler is not None:
        handler(args)

    return True


def _show_help():
    """Tampilkan daftar perintah built-in dan info perintah eksternal."""
    print()
    print(f"  {BOLD}{BRIGHT_CYAN}╔══════════════════════════════════════════════╗{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}  {BOLD}📖 Daftar Perintah JenShell{RESET}               {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}╠══════════════════════════════════════════════╣{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}  {DIM}Built-in Commands:{RESET}                        {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}")

    for cmd_name, (_, description) in BUILTIN_COMMANDS.items():
        cmd_display = f"{BOLD}{BRIGHT_GREEN}{cmd_name:<8}{RESET}"
        desc_display = f"{DIM}{description}{RESET}"
        print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}    {cmd_display}  {desc_display}")

    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}╠══════════════════════════════════════════════╣{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}  {DIM}Perintah Eksternal:{RESET}                       {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}  {DIM}  Perintah OS juga didukung, misalnya:{RESET}    {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}    {BOLD}{YELLOW}dir{RESET}       {DIM}echo{RESET}      {DIM}mkdir{RESET}     {DIM}cls{RESET}      {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}    {DIM}type{RESET}      {DIM}python{RESET}    {DIM}ping{RESET}      {DIM}git{RESET}      {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}    {DIM}(Semua perintah/aplikasi di PATH Anda){RESET}        {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}║{RESET}                                              {BOLD}{BRIGHT_CYAN}║{RESET}")
    print(f"  {BOLD}{BRIGHT_CYAN}╚══════════════════════════════════════════════╝{RESET}")
    print()
