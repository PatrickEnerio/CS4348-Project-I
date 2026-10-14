#!/usr/bin/env python3
"""Encryption program: Vigenere cipher backend driven over standard input.

Usage: python3 encryption.py

Each input line is "COMMAND argument". Each output line starts with a
response type:
    RESULT <result>   the command succeeded
    ERROR <message>   the command failed

Commands:
    PASS <key>        set the current passkey
    ENCRYPT <text>    encrypt text with the current passkey
    DECRYPT <text>    decrypt text with the current passkey
    QUIT              exit the program

Input is assumed to be uppercase letters only (the driver validates it).
"""

import sys

# The currently set passkey. None until PASS is received.
passkey = None


def respond(kind, message=""):
    """Write one response line and flush it so the driver can read it now."""
    if message:
        print(f"{kind} {message}")
    else:
        print(kind)
    sys.stdout.flush()


def vigenere_encrypt(text, key):
    """Encrypt uppercase text with a Vigenere cipher using key."""
    # TODO: For each letter i in text, shift it forward by the key letter at
    #       position i % len(key) (A=0, B=1, ..., Z=25), wrapping around Z.
    #       Check: key "HELLO", text "HELLO" -> "OIWWC"
    return text


def vigenere_decrypt(text, key):
    """Decrypt uppercase text with a Vigenere cipher using key."""
    # TODO: Same as encrypt, but shift backward instead of forward.
    #       Check: key "HELLO", text "OIWWC" -> "HELLO"
    return text


def handle_pass(arg):
    global passkey
    # TODO: Store arg as the passkey and respond with a bare "RESULT".
    #       Consider what to do if arg is empty.
    respond("ERROR", "Not implemented")


def handle_encrypt(arg):
    # TODO: If no passkey is set -> respond("ERROR", "Password not set").
    #       Otherwise respond("RESULT", vigenere_encrypt(arg, passkey)).
    respond("ERROR", "Not implemented")


def handle_decrypt(arg):
    # TODO: If no passkey is set -> respond("ERROR", "Password not set").
    #       Otherwise respond("RESULT", vigenere_decrypt(arg, passkey)).
    respond("ERROR", "Not implemented")


COMMANDS = {
    "PASS": handle_pass,
    "ENCRYPT": handle_encrypt,
    "DECRYPT": handle_decrypt,
}


def main():
    for line in sys.stdin:
        line = line.rstrip("\n")

        # First word is the command; the rest of the line (after the first
        # space) is the argument.
        parts = line.split(" ", 1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if command == "QUIT":
            break

        handler = COMMANDS.get(command)
        if handler is None:
            # TODO: Decide on the error message for unknown commands.
            respond("ERROR", f"Unknown command {command}")
        else:
            handler(arg)


if __name__ == "__main__":
    main()
