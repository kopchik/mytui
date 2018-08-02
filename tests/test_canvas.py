import pytest

from mytui.canvas import Canvas
from .conftest import multiline


def test_clear():
    canvas = Canvas(5, 1)
    canvas.clear()
    assert "     " == canvas.as_string()
    canvas.clear(ch='X')
    assert "XXXXX" == canvas.as_string()


def test_print_basic():
    canvas = Canvas(5, 1)
    canvas.print("test")
    assert "test " == canvas.as_string()


def test_print_multiline():
    canvas = Canvas(5, 4)
    canvas.print("\ntest\ntest")
    expected = multiline(
        "     ",
        "test ",
        "test ",
        "     ")
    assert expected == canvas.as_string()


def test_size_params():
    wrong_sizes = [(0, 1), (1, 0), (-1, 10), (0, 0)]
    for size_x, size_y in wrong_sizes:
        with pytest.raises(Exception, match='size too small'):
            Canvas(0, -1)


def test_print_overflow():
    canvas = Canvas(1, 1)
    canvas.print('x'*100)
    assert 'x' == canvas.as_string()
