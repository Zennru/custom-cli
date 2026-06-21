"""
cli.py — Entry point utama untuk JenShell.

Jalankan shell dengan: python cli.py
"""

import os
import sys

# Setup encoding UTF-8 untuk Windows agar Unicode characters bisa tampil
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from core.repl import run

if __name__ == "__main__":
    run()