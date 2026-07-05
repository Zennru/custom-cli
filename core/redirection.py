"""
redirection.py

Implementasi I/O Redirection (>, >> dan <)

Linux/macOS:
    fork()
    dup2()
    execvp()

Windows:
    subprocess.Popen(stdout=file) / subprocess.Popen(stdin=file)
"""

import os
import subprocess

from utils.colors import error_text


def execute_redirect(command, args, operator, filename):
    """
    Jalankan command dengan output diarahkan ke file.

    Args:
        command : Nama command
        args : List argumen
        operator : > atau >>
        filename : Nama file tujuan
    """

    tokens = [command] + args

    # ===========================
    # Tentukan mode file
    # ===========================

    mode = "w"

    if operator == ">>":
        mode = "a"

    # ===========================
    # POSIX
    # ===========================

    if hasattr(os, "fork"):

        try:

            pid = os.fork()

            if pid == 0:

                try:

                    fd = os.open(
                        filename,
                        os.O_CREAT | os.O_WRONLY |
                        (os.O_APPEND if mode == "a" else os.O_TRUNC),
                        0o644
                    )

                    os.dup2(fd, 1)

                    os.close(fd)

                    os.execvp(command, tokens)

                except Exception as e:
                    print(error_text(f"Redirect Error: {e}"))
                    os._exit(1)

            else:

                os.waitpid(pid, 0)

        except Exception as e:
            print(error_text(f"Fork Error: {e}"))

        return

    # ===========================
    # WINDOWS
    # ===========================

    try:

        with open(filename, mode, encoding="utf-8") as outfile:

            process = subprocess.Popen(

                tokens,

                stdout=outfile,

                stderr=subprocess.STDOUT,

                stdin=None,

                shell=True,

                cwd=os.getcwd()

            )

            process.wait()

    except Exception as e:

        print(error_text(f"Redirect Error: {e}"))


def execute_input_redirect(command, args, filename):
    """
    Jalankan command dengan input dibaca dari file.

    Contoh: sort < data.txt
    File data.txt akan menjadi stdin untuk perintah sort.

    Args:
        command  : Nama command
        args     : List argumen
        filename : Nama file sumber input
    """

    tokens = [command] + args

    # ===========================
    # Validasi file ada
    # ===========================

    if not os.path.exists(filename):
        print(error_text(f"  ✗ Input Redirect Error: file tidak ditemukan: '{filename}'"))
        return

    if not os.path.isfile(filename):
        print(error_text(f"  ✗ Input Redirect Error: bukan file: '{filename}'"))
        return

    # ===========================
    # POSIX
    # ===========================

    if hasattr(os, "fork"):

        try:

            pid = os.fork()

            if pid == 0:

                try:

                    fd = os.open(filename, os.O_RDONLY)

                    os.dup2(fd, 0)  # Redirect stdin (fd 0)

                    os.close(fd)

                    os.execvp(command, tokens)

                except Exception as e:
                    print(error_text(f"Input Redirect Error: {e}"))
                    os._exit(1)

            else:

                os.waitpid(pid, 0)

        except Exception as e:
            print(error_text(f"Fork Error: {e}"))

        return

    # ===========================
    # WINDOWS
    # ===========================

    try:

        with open(filename, "r", encoding="utf-8") as infile:

            process = subprocess.Popen(

                tokens,

                stdin=infile,

                stdout=None,

                stderr=None,

                shell=True,

                cwd=os.getcwd()

            )

            process.wait()

    except Exception as e:

        print(error_text(f"Input Redirect Error: {e}"))