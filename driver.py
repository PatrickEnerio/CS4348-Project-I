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
    while True:
        s = input(prompt).strip()
        # isalpha() is False for "", spaces, digits, and punctuation, so
        # "Hello World!" and an empty entry are both rejected.
        if s.isalpha():
            # The encryption program expects uppercase, and this makes input
            # case-insensitive: "Hello" and "hello" give the same result.
            return s.upper()
        print("Error: input must contain only letters.")


def print_history():
    for i, item in enumerate(history, start=1):
        print(f"  {i}. {item}")


def choose_from_history():
    """Let the user pick a string from history.

    Returns the chosen string, or None if the user wants to enter a new string.
    """
    if not history:
        print("History is empty.")
        return None

    print_history()
    print("  0. Enter a new string instead")
    while True:
        choice = input("Select a number: ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(history):
            n = int(choice)
            return history[n - 1] if n > 0 else None
        print(f"Error: enter a number from 0 to {len(history)}.")


def get_input_string(prompt):
    """Ask whether to use history or a new string, then return the string.

    Returns (string, is_new) so callers know whether to add it to history.
    """
    while True:
        answer = input("Use history? (y/n): ").strip().lower()
        if answer in ("y", "n"):
            break
        print("Error: enter y or n.")

    if answer == "y":
        chosen = choose_from_history()
        if chosen is not None:
            return chosen, False
    return prompt_letters(prompt), True


# ---------------------------------------------------------------- commands

def cmd_password():
    # The password is never added to history, and only the encryptor's reply
    # is logged. PASS replies with a bare RESULT, so the password stays out
    # of the log even when it was picked from history.
    password, _ = get_input_string("Enter password: ")
    response = send_encryptor("PASS", password)
    log_response(response)
    kind, _, message = response.partition(" ")
    if kind == "RESULT":
        print("Password set.")
    else:
        print(f"Error: {message}")


def run_cipher(command, prompt):
    """Shared body of encrypt and decrypt: command is "ENCRYPT" or "DECRYPT"."""
    text, is_new = get_input_string(prompt)
    if is_new:
        history.append(text)

    response = send_encryptor(command, text)
    log_response(response)
    kind, _, result = response.partition(" ")
    if kind == "RESULT":
        print(f"Result: {result}")
        history.append(result)
    else:
        # e.g. "Password not set". Errors aren't results, so not saved.
        print(f"Error: {result}")


def cmd_encrypt():
    run_cipher("ENCRYPT", "Enter string to encrypt: ")


def cmd_decrypt():
    run_cipher("DECRYPT", "Enter string to decrypt: ")


def cmd_history():
    if not history:
        print("History is empty.")
    else:
        print_history()


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
            try:
                handler()
            except EOFError:
                # Input ended in the middle of a prompt: quit cleanly instead
                # of crashing and leaving the children running.
                print()
                cmd_quit()
                break


if __name__ == "__main__":
    main()
