"""
cd.py — Implementasi perintah built-in `cd` (Tahap 3).

Mengubah direktori aktif shell. Mendukung:
- cd            → pindah ke home directory
- cd ~          → pindah ke home directory
- cd <path>     → pindah ke path yang diberikan
- cd -          → pindah ke direktori sebelumnya (OLDPWD)
"""

import os

from utils.colors import error_text, success_text, info_text

# Menyimpan direktori sebelumnya untuk fitur `cd -`
_previous_directory = None


def execute(args):
    """
    Jalankan perintah cd.

    Args:
        args: List argumen setelah 'cd'.
              - Kosong → pindah ke home directory
              - ['-'] → pindah ke direktori sebelumnya
              - ['<path>'] → pindah ke path tersebut

    Returns:
        None
    """
    global _previous_directory

    # Simpan direktori saat ini sebelum berpindah
    current_dir = os.getcwd()

    # Tentukan target direktori
    if not args or args[0] == "~":
        # cd atau cd ~ → home directory
        target = os.path.expanduser("~")

    elif args[0] == "-":
        # cd - → kembali ke direktori sebelumnya
        if _previous_directory is None:
            print(error_text("cd: OLDPWD belum diatur"))
            return
        target = _previous_directory
        # Tampilkan direktori tujuan saat menggunakan cd -
        print(info_text(target))

    else:
        # cd <path> → path yang diberikan
        target = os.path.expanduser(args[0])

    # Coba berpindah direktori
    try:
        os.chdir(target)
        _previous_directory = current_dir

    except FileNotFoundError:
        print(error_text(f"cd: direktori tidak ditemukan: '{args[0] if args else '~'}'"))

    except NotADirectoryError:
        print(error_text(f"cd: bukan sebuah direktori: '{args[0]}'"))

    except PermissionError:
        print(error_text(f"cd: izin ditolak: '{args[0]}'"))

    except Exception as e:
        print(error_text(f"cd: error: {e}"))
