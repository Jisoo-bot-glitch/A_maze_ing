from typing import Final

N: Final[int] = 1
E: Final[int] = 2
S: Final[int] = 4
W: Final[int] = 8

ALL_WALLS: Final[int] = N | E | S | W
NO_WALLS: Final[int] = 0

DIRECTIONS: Final[tuple[int, ...]] = (N, E, S, W)
STEP: Final[dict[int, tuple[int, int]]] = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}
OPPOSITE: Final[dict[int, int]] = {
    N: S,
    E: W,
    S: N,
    W: E
}
LETTER: Final[dict[int, str]] = {
    N: 'N',
    E: 'E',
    S: 'S',
    W: 'W'
}

PATTERN_42: Final[tuple[str, ...]] = (
    '#.#.###',
    '#.#...#',
    '###.###',
    '..#.#..',
    '..#.###',
)

PATTERN_WIDTH: Final[int] = len(PATTERN_42[0])
PATTERN_HEIGHT: Final[int] = len(PATTERN_42)
PATTERN_MARGIN: Final[int] = 1
MIN_WIDTH_PATTERN: Final[int] = PATTERN_WIDTH + 2 * PATTERN_MARGIN
MIN_HEIGHT_PATTERN: Final[int] = PATTERN_HEIGHT + 2 * PATTERN_MARGIN
CHAR: Final[str] = '#'

# Pac-Man mode lower
