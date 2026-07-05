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

def build_command(command, args):
    """
    Membentuk list command yang akan dijalankan.

    Contoh:
        command = "echo"
        args = ["Halo"]

    Hasil:
        ["echo", "Halo"]
    """
    return [command] + args


def execute_external(command, args):
    """
    Jalankan perintah eksternal OS sebagai child process.

    Mekanisme:
        - Di Unix/Linux: Menggunakan os.fork() + os.execvp() asli untuk duplikasi
          dan overlay proses sesuai prinsip teori Sistem Operasi.
        - Di Windows: Menggunakan subprocess.Popen (fallback) agar program
          tetap dapat diuji secara lokal di Windows native.

    Args:
        command: Nama perintah eksternal (string), misalnya 'dir', 'echo'.
        args: List argumen untuk perintah tersebut.

    Returns:
        int: Exit code dari child process, atau -1 jika gagal.
    """
    tokens = build_command(command, args)

    # ─── 1. Implementasi POSIX (Linux/macOS): Fork & Exec Asli ─────────
    if hasattr(os, "fork"):
        try:
            pid = os.fork()

            if pid == 0:
                # ─── CHILD PROCESS ───
                try:
                    os.execvp(command, tokens)
                except FileNotFoundError:
                    import sys
                    print(error_text(f"  ✗ JenShell: command not found: '{command}'"))
                    sys.exit(1)
                except PermissionError:
                    import sys
                    print(error_text(f"  ✗ JenShell: Permission denied: '{command}'"))
                    sys.exit(1)
                except Exception as e:
                    import sys
                    print(error_text(f"  ✗ JenShell: Execution error: {e}"))
                    sys.exit(1)
            else:
                # ─── PARENT PROCESS ───
                _, status = os.waitpid(pid, 0)
                
                # Ekstrak exit code dari status waitpid
                if os.WIFEXITED(status):
                    exit_code = os.WEXITSTATUS(status)
                    if exit_code != 0:
                        print(
                            f"  {DIM}[Proses selesai dengan exit code: "
                            f"{BOLD}{YELLOW}{exit_code}{RESET}{DIM}]{RESET}"
                        )
                    return exit_code
                return -1

        except Exception as e:
            print(error_text(f"  ✗ Fork error: {e}"))
            return -1

    # ─── 2. Fallback Windows Native: Subprocess ────────────────────────
    else:
        try:
            child_process = subprocess.Popen(
                tokens,
                stdin=None,      # inherit dari parent (terminal)
                stdout=None,     # inherit dari parent (terminal)
                stderr=None,     # inherit dari parent (terminal)
                cwd=os.getcwd(), # gunakan direktori aktif shell
                shell=True,      # gunakan shell OS untuk resolusi perintah
            )

            exit_code = child_process.wait()

            if exit_code != 0:
                print(
                    f"  {DIM}[Proses selesai dengan exit code: "
                    f"{BOLD}{YELLOW}{exit_code}{RESET}{DIM}]{RESET}"
                )

            return exit_code

        except FileNotFoundError:
            print(
                error_text(f"  ✗ Perintah tidak ditemukan: '{command}'")
                + f"\n  {DIM}Pastikan perintah tersedia di PATH sistem.{RESET}"
            )
            return -1

        except PermissionError:
            print(error_text(f"  ✗ Izin ditolak untuk menjalankan: '{command}'"))
            return -1

        except OSError as e:
            print(error_text(f"  ✗ Error OS saat menjalankan '{command}': {e}"))
            return -1

        except Exception as e:
            print(error_text(f"  ✗ Error tak terduga: {e}"))
            return -1

