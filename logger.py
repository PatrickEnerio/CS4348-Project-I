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
    # The action is the first run of non-whitespace characters; the message
    # is everything after it and may be empty.
    parts = line.split(maxsplit=1)
    action = parts[0].upper()
    message = parts[1] if len(parts) > 1 else ""
    return action, message


def format_entry(action, message):
    """Build one log file line with a 24-hour timestamp."""
    # Example: "2026-09-14 11:32 [START] Logging Started."
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    # rstrip so an entry with no message has no trailing space.
    return f"{timestamp} [{action}] {message}".rstrip()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 logger.py <logfile>", file=sys.stderr)
        sys.exit(1)

    log_path = sys.argv[1]

    with open(log_path, "a") as log_file:
        for line in sys.stdin:
            line = line.rstrip("\r\n")

            if line == "QUIT":
                break

            # Skip blank lines; they have no action to record.
            if not line.strip():
                continue

            action, message = parse_message(line)
            log_file.write(format_entry(action, message) + "\n")
            # Flush after every entry so the log is up to date even if the
            # driver is killed before sending QUIT.
            log_file.flush()


if __name__ == "__main__":
    main()
