import enum
import os
import select
import signal
import sys

SPECIAL = enum.Enum('SPECIAL', "ESC BSPACE ENTER CTRLC")
ARROW = enum.Enum('ARROW', "UP DOWN LEFT RIGHT")


def myinput(timeout=None):
    stdin = sys.stdin
    special = False
    while True:
        try:
            r, _, _ = select.select([stdin], [], [], timeout)
            if not r:
                yield None
                continue
            ch = os.read(stdin.fileno(), 1)
        except InterruptedError:  # "[Errno 4] Interrupted system call"
            continue
        ch = ch.decode()
        if ch == '\x1b':
            if special:
                yield SPECIAL.ESC
            else:
                special = True
        elif ch == '[':
            if not special:
                yield ch
        else:
            if special:
                special = False
                if ch == 'A':
                    yield ARROW.UP
                elif ch == 'B':
                    yield ARROW.DOWN
                elif ch == 'C':
                    yield ARROW.RIGHT
                elif ch == 'D':
                    yield ARROW.LEFT
            else:
                if ch == '\x7f':
                    yield SPECIAL.BSPACE
                elif ch == '\x03':
                    os.kill(0, signal.SIGINT)
                    # yield SPECIAL.CTRLC
                elif ch == '\r':
                    # yield SPECIAL.ENTER
                    yield '\n'
                else:
                    yield ch
