#!/bin/env python3

from blessings import Terminal

from .utils import XY

_terminal = Terminal()


class Error(Exception):
    pass


class PositionError(Error):
    pass


class Canvas:
    def __init__(self, size_x, size_y):
        if size_x < 1 or size_y < 1:
            err = f"size too small (size_x={size_x}, size_y={size_y})"
            raise Exception(err)

        self.size_x = size_x
        self.size_y = size_y
        self.cur_pos = XY(0, 0)
        self._canvas = bytearray(b' '*self.size_x * self.size_y)

    def clear(self, ch=' '):
        for offset in range(len(self._canvas)):
            self._canvas[offset] = ord(ch)

    def print(self, text, pos=XY(0, 0)):
        offset = pos.x + pos.y * self.size_x
        max_offset = len(self._canvas)
        for ch in text:
            if ch == '\n':
                curr_line = offset // self.size_x
                offset = (curr_line + 1) * self.size_x
                continue
            if offset >= max_offset:
                return
            self._canvas[offset] = ord(ch)
            offset += 1

    def as_string(self):
        lines = [l.decode() for l in self.iter_lines()]
        return "\n".join(lines)

    def iter_lines(self):
        for y in range(self.size_y):
            start = y * self.size_x
            stop = start + self.size_x
            line = self._canvas[start:stop]
            yield line

    def render(self, offset_x=0, offset_y=0, terminal=_terminal):
        # TODO: overflow check?
        # TODO: skipt control chars?
        for y in range(self.size_y):
            for x in range(self.size_x):
                offset = x + y * self.size_x
                print(terminal.move(y+offset_y, x+offset_x), end='')
                print(chr(self._canvas[offset]), end='')
