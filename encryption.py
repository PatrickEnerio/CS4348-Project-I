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


def shift(text, key, direction):
    """Shift each letter of text by the matching key letter.

    Letter i uses key letter i % len(key) (A=0, B=1, ..., Z=25), so the key
    repeats when the text is longer. direction is +1 to encrypt, -1 to decrypt.
    The % 26 wraps past Z back to A (or past A back to Z).
    """
    result = []
    for i, c in enumerate(text):
        k = ord(key[i % len(key)]) - ord("A")
        result.append(chr((ord(c) - ord("A") + direction * k) % 26 + ord("A")))
    return "".join(result)


def vigenere_encrypt(text, key):
    """Encrypt uppercase text with a Vigenere cipher using key."""
    return shift(text, key, 1)


def vigenere_decrypt(text, key):
    """Decrypt uppercase text with a Vigenere cipher using key."""
    return shift(text, key, -1)


def handle_pass(arg):
    global passkey
    # An empty key would make i % len(key) divide by zero, so reject it.
    if not arg:
        respond("ERROR", "Password is empty")
        return
    passkey = arg
    respond("RESULT")


def handle_encrypt(arg):
    if passkey is None:
        respond("ERROR", "Password not set")
    else:
        respond("RESULT", vigenere_encrypt(arg, passkey))


def handle_decrypt(arg):
    if passkey is None:
        respond("ERROR", "Password not set")
    else:
        respond("RESULT", vigenere_decrypt(arg, passkey))


COMMANDS = {
    "PASS": handle_pass,
    "ENCRYPT": handle_encrypt,
    "DECRYPT": handle_decrypt,
}


def main():
    for line in sys.stdin:
        # Strip "\r" too, so Windows line endings don't end up in the argument.
        line = line.rstrip("\r\n")

        # First word is the command; the rest of the line (after the first
        # space) is the argument.
        parts = line.split(" ", 1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if command == "QUIT":
            break

        handler = COMMANDS.get(command)
        if handler is None:
            # Always reply, even to a blank line. The driver waits on
            # readline() after every command, so no reply would hang it.
            respond("ERROR", f"Unknown command {command}")
        else:
            handler(arg)


if __name__ == "__main__":
    main()
