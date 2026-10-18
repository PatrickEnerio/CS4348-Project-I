# 10-14-2026 3:02pm

This session I set up the skeleton for all three files.
The driver can already start both children, show the menu, and on quit send QUIT to both and wait for them to exit, so I know the pipes are connected.
I start the children with sys.executable instead of just "python" so they run under the same interpreter as the driver, and I build their paths from the driver's own directory so it works no matter where I run it from.
Everything else is a stub with TODO comments: the logger's parsing, the Vigenère cipher, and all of the driver's menu commands.

There are a few things I am still thinking through.
The driver writes a command to the encryption program and then blocks on readline() waiting for the reply, so the encryption program has to answer every single line, or the driver will hang forever. For the same reason, both children have to flush their output after each line, or the reply could sit in a buffer. I also need to keep passwords out of the log and out of the history, even when the password is picked from the history. I have not decided exactly how the history menu should look yet, other than that it needs a way to back out and type a new string.

Next session I plan to fill in the logger, since it does not depend on anything else and I can test it on its own.

# 10-15-2026 2:50pm

This session I filled in the logger, since it is the one piece that does not depend on anything else and I can test it on its own by piping lines into it with printf. The driver already sends lines in the form "ACTION message", so the logger just has to split each line and write it back out with a timestamp.

For parsing I used line.split(maxsplit=1).
The first word becomes the action, and everything after it, spaces included, stays together as the message. If there is only one word, the message is empty.
I uppercase the action so the log stays consistent no matter how the driver spells it.

The entry format is "YYYY-MM-DD HH:MM [ACTION] MESSAGE" using datetime.now().strftime("%Y-%m-%d %H:%M"), which is 24-hour time. I rstrip the finished line so an action with no message does not leave a trailing space.

I also decided to skip blank lines.
Without that, a blank line would give split() an empty list and parts[0] would crash the logger, which would then break the driver's pipe. I strip "\r\n" instead of only "\n" in case input ever comes in with Windows line endings, so "QUIT\r" still matches. The log file is flushed after every entry so it stays up to date even if the driver dies before sending QUIT.

To test it, I piped in a START line, a blank line, a one-word line, QUIT, and a line after QUIT. The log had the three expected entries, and nothing showed up from the blank line or the line after QUIT. I also ran the driver and typed quit to make sure it still starts and stops both children cleanly.

Next session I plan to write the Vigenère cipher and the command loop in encryption.py.

# 10-15-2026 4:36pm

This session I wrote the Vigenère cipher and the command handlers in encryption.py. A Vigenère cipher shifts each letter of the text by an amount that comes from the key, with A=0, B=1, up to Z=25. Letter i of the text uses key letter i % len(key), so the key repeats if the text is longer than it. Adding the shift and taking % 26 makes it wrap around from Z back to A. Decrypting is the same thing in the other direction, so I wrote one shift() helper that takes a direction of +1 or -1, and encrypt and decrypt each just call it. Because Python's % always gives a non-negative result, shifting backwards past A wraps to Z without any extra checks.

PASS stores the key and replies with a bare RESULT, and ENCRYPT and DECRYPT reply "ERROR Password not set" until a key exists, matching the example in the spec. I decided to reject an empty PASS with an error. With an empty key, len(key) is 0, so i % len(key) would raise a divide-by-zero error and crash the program, which would also break the driver's pipe. When this happens the old key stays set.

I also made sure the program replies to every line, even a blank or unknown one, with "ERROR Unknown command". The driver blocks on readline() after every command it sends, so if the encryption program skipped a line, the driver would wait forever. This is different from the logger, which can safely skip blank lines because the driver never waits on it.Like the logger, I strip "\r\n" so Windows line endings do not end up in the argument.

To test it, I piped commands straight into encryption.py with printf.
The spec's example gave ERROR Password not set, RESULT, and RESULT OIWWC, and decrypting OIWWC gave back HELLO. To check that the key repeats, I used the key KEY on ATTACKATDAWN and got KXRKGIKXBKAL, which I checked by hand, and decrypting it gave back the original. An empty PASS gave an error and the previous key kept working, unknown and blank lines got an ERROR reply, and nothing after QUIT was processed.

Next session I plan to wire logging into the driver: the start and exit of the driver, each command, and the result of each command.

# 10-18-2026 3:10pm

This session I wired logging into the driver. The spec says the start and exit of the driver should be logged, along with each command and its result. The driver now sends "START Driver started." right after it launches the two child processes, and "CMD <command>" for every command the user types. If the command is not one of the menu options, the driver prints an error and also logs "ERROR Unknown command <command>". I decided to skip empty input instead of logging it, since pressing enter by accident is not really a command and would just clutter the log.

The order matters when quitting. The driver logs "EXIT Driver exiting." before it sends QUIT to the logger, because once the logger reads QUIT it stops reading and closes the file. Anything sent after that would be lost. Since the main loop already treats end of input (Ctrl-D) as quit, the EXIT line gets logged in that case too.

I also added a log_response() helper for logging the replies from the encryption program. A reply like "RESULT OIWWC" or "ERROR Password not set" already has the form "ACTION message", so the helper splits off the first word as the action and passes the rest along as the message. Nothing calls it yet, because the password, encrypt, and decrypt commands are still stubs, but they will all use it. This also takes care of keeping passwords out of the log.
The driver logs "CMD password" and then the response, and PASS replies with a bare RESULT, so the password itself never gets sent to the logger.

To test it, I piped "foo", a blank line, "history", and "quit" into the driver and read the log file. It had START, CMD foo, the unknown command error, CMD history, CMD quit, and EXIT, with nothing for the blank line. I also ran it with input that ends without typing quit, to act like Ctrl-D, and EXIT was still logged and both child processes exited.

Next session I plan to implement the password, encrypt, decrypt, and history commands, including the history menu and checking that input contains only letters.
