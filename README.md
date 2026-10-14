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
