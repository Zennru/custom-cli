"""
parser.py — Parsing dan tokenisasi input pengguna.

Mendukung:
- Command biasa
- I/O Redirection (>, >>)
- Pipe (|)
- Validasi syntax sederhana
"""

import shlex


def parse_input(user_input):

    stripped = user_input.strip()

    if not stripped:
        return None

    try:
        tokens = shlex.split(stripped)
    except ValueError:
        return {
            "type": "error",
            "message": "Syntax Error: kutip tidak ditutup."
        }

    if not tokens:
        return None

    # ===========================
    # PIPE
    # ===========================
    if "|" in tokens:

        if tokens.count("|") > 1:
            return {
                "type": "error",
                "message": "Multiple pipe belum didukung."
            }

        index = tokens.index("|")

        left = tokens[:index]
        right = tokens[index + 1:]

        if not left:
            return {
                "type":"error",
                "message":"Command sebelum | tidak boleh kosong."
            }

        if not right:
            return {
                "type":"error",
                "message":"Command setelah | tidak boleh kosong."
            }

        return {
            "type":"pipe",

            "left":{
                "command":left[0],
                "args":left[1:]
            },

            "right":{
                "command":right[0],
                "args":right[1:]
            }
        }

    # ===========================
    # REDIRECTION >>
    # ===========================
    if ">>" in tokens:

        if tokens.count(">>") > 1:
            return {
                "type":"error",
                "message":"Terlalu banyak operator >>."
            }

        index = tokens.index(">>")

        command = tokens[:index]
        output = tokens[index+1:]

        if not command:
            return {
                "type":"error",
                "message":"Command sebelum >> kosong."
            }

        if len(output)!=1:
            return {
                "type":"error",
                "message":"Nama file tujuan tidak valid."
            }

        return{

            "type":"redirect",

            "command":command[0],

            "args":command[1:],

            "operator":">>",

            "file":output[0]

        }

    # ===========================
    # REDIRECTION >
    # ===========================
    if ">" in tokens:

        if tokens.count(">")>1:
            return{
                "type":"error",
                "message":"Terlalu banyak operator >."
            }

        index=tokens.index(">")

        command=tokens[:index]

        output=tokens[index+1:]

        if not command:
            return{
                "type":"error",
                "message":"Command sebelum > kosong."
            }

        if len(output)!=1:
            return{
                "type":"error",
                "message":"Nama file tujuan tidak valid."
            }

        return{

            "type":"redirect",

            "command":command[0],

            "args":command[1:],

            "operator":">",

            "file":output[0]

        }

    # ===========================
    # INPUT REDIRECTION <
    # ===========================
    if "<" in tokens:

        if tokens.count("<") > 1:
            return {
                "type": "error",
                "message": "Terlalu banyak operator <."
            }

        index = tokens.index("<")

        command = tokens[:index]
        input_file = tokens[index + 1:]

        if not command:
            return {
                "type": "error",
                "message": "Command sebelum < kosong."
            }

        if len(input_file) != 1:
            return {
                "type": "error",
                "message": "Nama file sumber tidak valid."
            }

        return {
            "type": "input_redirect",
            "command": command[0],
            "args": command[1:],
            "file": input_file[0]
        }

    # ===========================
    # COMMAND BIASA
    # ===========================

    return{

        "type":"normal",

        "command":tokens[0],

        "args":tokens[1:]

    }