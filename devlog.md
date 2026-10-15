# 10-14-2026 3:02pm

<!--
TODO: Write this entry in your own words before committing. Some things to cover:
- What the project is: three programs (driver, logger, encryption) talking over pipes.
- How you plan to structure it: Python subprocess.Popen with stdin/stdout pipes.
- What you set up this session: the skeleton files and what is still a stub.
- Anything you are still thinking through (e.g. how history selection should
  work, how to keep passwords out of the log, how to avoid pipe deadlocks).
- What you plan to do next session.
Delete this comment once the entry is written.
-->

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
