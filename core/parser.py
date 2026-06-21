"""
parser.py — Parsing dan tokenisasi input pengguna (Tahap 2).

Memecah string input menjadi command dan arguments menggunakan
shlex.split() agar mendukung argumen berquote.
"""

import shlex


def parse_input(user_input):
    """
    Parse string input menjadi command dan arguments.

    Menggunakan shlex.split() untuk tokenisasi yang mendukung:
    - Argumen dengan spasi dalam tanda kutip: cd "My Documents"
    - Escape characters
    - Multiple spasi antar argumen diabaikan

    Args:
        user_input: String mentah dari input pengguna.

    Returns:
        Tuple (command, arguments):
            - command (str atau None): Nama perintah, atau None jika input kosong.
            - arguments (list): Daftar argumen setelah perintah.

    Contoh:
        parse_input('cd "My Folder"')  →  ('cd', ['My Folder'])
        parse_input('pwd')             →  ('pwd', [])
        parse_input('')                →  (None, [])
    """
    # Bersihkan whitespace di awal/akhir
    stripped = user_input.strip()

    # Input kosong
    if not stripped:
        return None, []

    try:
        # Tokenisasi menggunakan shlex (mendukung quote)
        tokens = shlex.split(stripped)
    except ValueError:
        # Jika ada quote yang tidak tertutup, fallback ke split biasa
        tokens = stripped.split()

    if not tokens:
        return None, []

    command = tokens[0]
    arguments = tokens[1:]

    return command, arguments
