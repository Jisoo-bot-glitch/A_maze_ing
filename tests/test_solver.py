"""Tests for mazegen.solver"""
from mazegen.solver import solver

MAZE = [[11, 9, 3, 11, 13, 5, 3],
        [8, 6, 12, 0, 5, 1, 6],
        [14, 9, 5, 6, 9, 2, 11],
        [13, 6, 9, 5, 2, 12, 6],
        [9, 1, 6, 13, 4, 5, 3],
        [10, 12, 5, 1, 3, 11, 10],
        [12, 5, 7, 12, 12, 6, 14]]
PATH = 'ESEEESWSWWSWSEES'


def test_known_maze() -> None:
    """The example maze gives the expected shortest path."""
    assert solver(MAZE, (1, 0), (3, 6)) == PATH


def test_exit_unreachable() -> None:
    """Two closed cells: no path, empty string."""
    assert solver([[15, 15]], (0, 0), (1, 0)) == ''


def test_entry_is_exit() -> None:
    """Already at the exit: empty path."""
    assert solver(MAZE, (1, 0), (1, 0)) == ''
