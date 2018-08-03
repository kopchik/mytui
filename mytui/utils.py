import functools
import sys
import termios
import tty

from . import input


def walk_children(node):
    to_visit = node.children.copy()
    for child in to_visit:
        to_visit.extend(child.children)
        yield child


def splitline(line, size):
    """ Chop line into chunks of specified size. """
    result = []
    ptr = 0
    while ptr < len(line):
        chunk = line[ptr:ptr+size]
        result.append(chunk)
        ptr += size
    return result


def mywrapper(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        with t.fullscreen():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            try:
                return f(*args, **kwargs)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN,
                                  old_settings)
    return wrapped


def loop(root, clear=True):
    root.initroot(clear=clear)

    for key in input.myinput():
        # if key == SPECIAL.CTRLC:
        #  os.kill(0, signal.SIGINT)
        #  continue
        if root.cur_focus:
            root.cur_focus.input(key)


@functools.total_ordering
class XY:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return self.__class__(self.x + other.x,
                              self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x,
                              self.y - other.y)

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        return iter([self.x, self.y])

    def __repr__(self):
        cls = self.__class__.__name__
        return "%s(%s, %s)" % (cls, self.x, self.y)
