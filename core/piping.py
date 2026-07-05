"""
piping.py

Implementasi Pipe (|)

Linux/macOS:
    pipe()
    fork()
    dup2()
    execvp()

Windows:
    subprocess.PIPE
"""

import os
import subprocess

from utils.colors import error_text


def execute_pipe(left, right):
    """
    Jalankan command dengan operator pipe.

    Args:
        left  : {"command": ..., "args": [...]}
        right : {"command": ..., "args": [...]}
    """

    left_tokens = [left["command"]] + left["args"]
    right_tokens = [right["command"]] + right["args"]

    # ==================================================
    # POSIX (Linux/macOS)
    # ==================================================

    if hasattr(os, "pipe") and hasattr(os, "fork"):

        try:

            read_fd, write_fd = os.pipe()

            pid1 = os.fork()

            if pid1 == 0:

                # Child pertama
                os.dup2(write_fd, 1)

                os.close(read_fd)
                os.close(write_fd)

                os.execvp(left["command"], left_tokens)

            pid2 = os.fork()

            if pid2 == 0:

                # Child kedua
                os.dup2(read_fd, 0)

                os.close(read_fd)
                os.close(write_fd)

                os.execvp(right["command"], right_tokens)

            os.close(read_fd)
            os.close(write_fd)

            os.waitpid(pid1, 0)
            os.waitpid(pid2, 0)

        except Exception as e:

            print(error_text(f"Pipe Error: {e}"))

        return

    # ==================================================
    # WINDOWS
    # ==================================================

    try:

        # Bangun command seperti yang diketik di CMD
        left_command = subprocess.list2cmdline(left_tokens)
        right_command = subprocess.list2cmdline(right_tokens)

        full_command = f"{left_command} | {right_command}"

        subprocess.run(
            full_command,
            shell=True,
            cwd=os.getcwd()
        )

    except Exception as e:

        print(error_text(f"Pipe Error: {e}"))