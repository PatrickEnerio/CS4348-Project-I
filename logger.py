#!/usr/bin/env python3
"""Logger: records log messages from standard input into a log file.

Usage: python3 logger.py <logfile>

Each input line is "ACTION message...". The first sequence of non-whitespace
characters is the action, and the rest of the line is the message. Each one is
written as:
    YYYY-MM-DD HH:MM [ACTION] MESSAGE
Input is read until the line "QUIT" is received.
"""

import sys
from datetime import datetime


def parse_message(line):
    """Split a log line into (action, message)."""
    # TODO: The action is the first word (first run of non-whitespace chars).
    #       The message is everything after it (may be empty).
    #       Hint: line.split(maxsplit=1)
    return "TODO", line


def format_entry(action, message):
    """Build one log file line with a 24-hour timestamp."""
    # TODO: Use datetime.now().strftime("%Y-%m-%d %H:%M") for the timestamp.
    #       Format: "YYYY-MM-DD HH:MM [ACTION] MESSAGE"
    #       Example: "2026-09-14 11:32 [START] Logging Started."
    return f"{action} {message}"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 logger.py <logfile>", file=sys.stderr)
        sys.exit(1)

    log_path = sys.argv[1]

    with open(log_path, "a") as log_file:
        for line in sys.stdin:
            line = line.rstrip("\n")

            if line == "QUIT":
                break

            # TODO: Skip blank lines?
            action, message = parse_message(line)
            log_file.write(format_entry(action, message) + "\n")
            # Flush after every entry so the log is up to date even if the
            # driver is killed before sending QUIT.
            log_file.flush()


if __name__ == "__main__":
    main()
