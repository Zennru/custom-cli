"""
executor.py — Forking & Eksekusi Perintah Eksternal (Tahap 4).

Modul ini bertanggung jawab menjalankan perintah bawaan OS (seperti
dir, mkdir, echo, cls, dll.) dengan mekanisme fork + exec:

1. Membentuk command line dari command + arguments
2. Membuat child process menggunakan subprocess.Popen (fork)
3. Child process di-overlay dengan program baru (exec)
4. Parent process menunggu hingga child process selesai (wait)

Di balik layar, subprocess.Popen menggunakan:
- Unix/Linux : fork() + execvp()
- Windows    : CreateProcess()
"""

import os
import subprocess

from utils.colors import error_text, warning_text, info_text, DIM, RESET, BOLD, YELLOW


def execute_external(command, args):
    """
    Jalankan perintah eksternal OS sebagai child process.

    Mekanisme:
        1. Parent process (JenShell) membuat child process via Popen
        2. Child process menjalankan perintah yang diminta (exec)
        3. Parent process menunggu child process selesai (wait)
        4. Jika exit code != 0, tampilkan informasi error

    Args:
        command: Nama perintah eksternal (string), misalnya 'dir', 'echo'.
        args: List argumen untuk perintah tersebut.

    Returns:
        int: Exit code dari child process, atau -1 jika gagal.
    """
    # Gabungkan command + arguments menjadi list untuk Popen
    cmd_list = [command] + args

    try:
        # ─── Fork: Buat child process ────────────────────────────
        # subprocess.Popen secara internal melakukan:
        #   - fork()    → duplikasi proses (membuat child process)
        #   - execvp()  → overlay child process dengan program baru
        #
        # stdin/stdout/stderr di-inherit agar output tampil langsung
        # di terminal dan program interaktif tetap bisa berjalan.
        child_process = subprocess.Popen(
            cmd_list,
            stdin=None,      # inherit dari parent (terminal)
            stdout=None,     # inherit dari parent (terminal)
            stderr=None,     # inherit dari parent (terminal)
            cwd=os.getcwd(), # gunakan direktori aktif shell
            shell=True,      # gunakan shell OS untuk resolusi perintah
        )

        # ─── Wait: Parent menunggu child selesai ─────────────────
        # Parent process (JenShell) menunggu hingga child process
        # selesai dieksekusi sebelum kembali ke REPL loop.
        exit_code = child_process.wait()

        # Tampilkan info jika child process keluar dengan error
        if exit_code != 0:
            print(
                f"  {DIM}[Proses selesai dengan exit code: "
                f"{BOLD}{YELLOW}{exit_code}{RESET}{DIM}]{RESET}"
            )

        return exit_code

    except FileNotFoundError:
        # Perintah tidak ditemukan di PATH sistem
        print(
            error_text(f"  ✗ Perintah tidak ditemukan: '{command}'")
            + f"\n  {DIM}Pastikan perintah tersedia di PATH sistem.{RESET}"
        )
        return -1

    except PermissionError:
        # Tidak punya izin untuk menjalankan perintah
        print(error_text(f"  ✗ Izin ditolak untuk menjalankan: '{command}'"))
        return -1

    except OSError as e:
        # Error OS lainnya (misalnya file corrupt, resource limit, dll.)
        print(error_text(f"  ✗ Error OS saat menjalankan '{command}': {e}"))
        return -1

    except Exception as e:
        # Error tak terduga
        print(error_text(f"  ✗ Error tak terduga: {e}"))
        return -1
