#!/usr/bin/env python3
"""Driver: interactive front end for the encryption program.

Usage: python3 driver.py <logfile>

Starts two child processes connected by pipes:
    logger.py <logfile>   receives log lines on its standard input
    encryption.py         receives commands, replies with RESULT/ERROR lines
Then prompts the user for commands until "quit".
"""

import os
import sys
from subprocess import Popen, PIPE

# Directory containing this script, so the child programs are found no matter
# which directory the driver is run from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Strings entered for encrypt/decrypt and their results, for this run only.
# Passwords are never stored here.
history = []

logger = None
encryptor = None


def start_process(script, args=()):
    """Start a Python program as a child process with piped stdin/stdout."""
    # sys.executable is the interpreter running this script, so the children
    # run under the same Python (plain 'python' may not exist on every system).
    path = os.path.join(SCRIPT_DIR, script)
    return Popen([sys.executable, path, *args], stdin=PIPE, stdout=PIPE, encoding="utf8")


def send_log(action, message):
    """Send one log line to the logger process."""
    logger.stdin.write(f"{action} {message}\n")
    logger.stdin.flush()


def send_encryptor(command, arg=""):
    """Send one command to the encryption program and return its response line."""
    line = f"{command} {arg}" if arg else command
    encryptor.stdin.write(line + "\n")
    encryptor.stdin.flush()
    return encryptor.stdout.readline().rstrip("\n")


def log_response(response):
    """Log a response from the encryption program, e.g. "RESULT OIWWC".

    The first word (RESULT or ERROR) becomes the log action and the rest
    becomes the message, so the logger records it the same way it was sent.
    """
    parts = response.split(" ", 1)
    send_log(parts[0], parts[1] if len(parts) > 1 else "")


# ---------------------------------------------------------------- helpers

def print_menu():
    print()
    print("Commands:")
    print("  password  - set the password")
    print("  encrypt   - encrypt a string")
    print("  decrypt   - decrypt a string")
    print("  history   - show the history")
    print("  quit      - exit")


def prompt_letters(prompt):
    """Ask for a string containing only letters and return it in uppercase."""
    # TODO: Keep asking (or return None) until the input is letters only.
    #       "Hello World!" must be rejected with an error message.
    #       Hint: str.isalpha()
    #       Input is case-insensitive, so return the value .upper().
    return input(prompt).upper()


def choose_from_history():
    """Let the user pick a string from history.

    Returns the chosen string, or None if the user wants to enter a new string.
    """
    # TODO: If history is empty, tell the user and return None.
    #       Otherwise print a numbered list, e.g.
    #           1. HELLO
    #           2. OIWWC
    #           0. Enter a new string instead
    #       and return the selected item (or None for 0).
    #       Handle input that isn't a valid number.
    return None


def get_input_string(prompt):
    """Ask whether to use history or a new string, then return the string.

    Returns (string, is_new) so callers know whether to add it to history.
    """
    # TODO: Ask "Use history? (y/n)". If yes, call choose_from_history();
    #       if that returns None, fall through to entering a new string.
    #       A new string comes from prompt_letters(prompt).
    return prompt_letters(prompt), True


# ---------------------------------------------------------------- commands

def cmd_password():
    # TODO: Get a string with get_input_string("Enter password: ").
    #       Send it with send_encryptor("PASS", password).
    #       Do NOT add the password to history.
    #       Log the command and the result, but never the password itself.
    print("password: not implemented yet")


def cmd_encrypt():
    # TODO: Get a string with get_input_string("Enter string to encrypt: ").
    #       If it is new, add it to history.
    #       Send ENCRYPT, print the result, and add the result to history.
    #       Log the command and the result (RESULT or ERROR).
    print("encrypt: not implemented yet")


def cmd_decrypt():
    # TODO: Same as cmd_encrypt, but with DECRYPT.
    print("decrypt: not implemented yet")


def cmd_history():
    # TODO: Print every entry in history (numbered), or a message if empty.
    print("history: not implemented yet")


def cmd_quit():
    """Tell both child processes to quit and wait for them to exit."""
    # Log the exit first: once the logger gets QUIT it stops reading.
    send_log("EXIT", "Driver exiting.")
    encryptor.stdin.write("QUIT\n")
    encryptor.stdin.flush()
    logger.stdin.write("QUIT\n")
    logger.stdin.flush()
    encryptor.wait()
    logger.wait()


COMMANDS = {
    "password": cmd_password,
    "encrypt": cmd_encrypt,
    "decrypt": cmd_decrypt,
    "history": cmd_history,
}


def main():
    global logger, encryptor

    if len(sys.argv) != 2:
        print("Usage: python3 driver.py <logfile>", file=sys.stderr)
        sys.exit(1)

    log_path = sys.argv[1]
    logger = start_process("logger.py", [log_path])
    encryptor = start_process("encryption.py")

    send_log("START", "Driver started.")

    while True:
        print_menu()
        try:
            command = input("> ").strip().lower()
        except EOFError:
            # Treat end of input (Ctrl-D) as quit so the children are cleaned up.
            command = "quit"

        # Ignore an empty line instead of logging it as a command.
        if not command:
            continue

        send_log("CMD", command)

        if command == "quit":
            cmd_quit()
            break

        handler = COMMANDS.get(command)
        if handler is None:
            print(f"Unknown command: {command}")
            send_log("ERROR", f"Unknown command {command}")
        else:
            handler()


if __name__ == "__main__":
    main()
