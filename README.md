# CS4348 Project 1

An encryption system built from three Python programs that communicate through
pipes using the `subprocess` module.

## Files

| File | Description |
| --- | --- |
| `driver.py` | Interactive front end. Starts the logger and the encryption program as child processes, connects to their standard input and output with pipes, and prompts the user for commands. |
| `logger.py` | Reads log messages from standard input and appends them to the log file as `YYYY-MM-DD HH:MM [ACTION] MESSAGE`. Stops on `QUIT`. |
| `encryption.py` | Vigenère cipher backend. Accepts `PASS`, `ENCRYPT`, `DECRYPT`, and `QUIT` on standard input and replies with `RESULT ...` or `ERROR ...`. |
| `devlog.md` | Development log. |

## Status

| Part | State |
| --- | --- |
| `logger.py` | Done. Parses `ACTION message` lines, timestamps them, skips blank lines, stops on `QUIT`. |
| `encryption.py` | Stub. Vigenère cipher and command handling not written yet. |
| `driver.py` | Partial. Starts and stops both child processes; the menu commands, logging calls, and input validation are still stubs. |

## Requirements

Python 3.6 or newer. Uses only the standard library.

## Running

Run the driver and give it the name of the log file:

```
python3 driver.py log.txt
```

The driver starts the other two programs itself. Commands:

- `password`: set the passkey, either a new string or one picked from the history
- `encrypt`: encrypt a new string or one picked from the history
- `decrypt`: decrypt a new string or one picked from the history
- `history`: show the strings and results from this run
- `quit`: stop the logger and the encryption program, then exit

Input must contain letters only and is case insensitive.

## Testing the programs on their own

```
printf 'START Logging Started.\nQUIT\n' | python3 logger.py log.txt
printf 'PASS HELLO\nENCRYPT HELLO\nQUIT\n' | python3 encryption.py
```

The logger command above appends a line like this to `log.txt`:

```
2026-10-15 14:05 [START] Logging Started.
```

The logger uppercases the action, so `start` and `START` produce the same
entry. Blank lines are skipped, and anything sent after `QUIT` is ignored. A
line with an action and no message is logged as just `YYYY-MM-DD HH:MM [ACTION]`.
