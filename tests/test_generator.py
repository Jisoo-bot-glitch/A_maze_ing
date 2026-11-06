"""Tests for the maze generator"""

from mazegen import MazeError, MazeGenerator
from mazegen.constants import N, E, S, W, STEP

# sizes to test: small ones, without 42 and with 42
SIZES = [(3, 2), (5, 5), (8, 6), (9, 7), (20, 15), (31, 21)]


def make_maze(width: int, height: int, perfect: bool,
              seed: int) -> MazeGenerator:
    """Make a maze with entry in the top left and exit in the bottom right"""
    gen = MazeGenerator(width, height, (0, 0), (width - 1, height - 1),
                        perfect, seed)
    gen.generate()
    return gen


def count_open_walls(grid: list[list[int]]) -> int:
    """Count open walls inside the maze, I look only at E and S"""
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x + 1 < len(grid[0]) and grid[y][x] & E == 0:
                count += 1
            if y + 1 < len(grid) and grid[y][x] & S == 0:
                count += 1
    return count


def is_maze_error(width: int, height: int, entry: tuple[int, int],
                  exit_p: tuple[int, int]) -> bool:
    """Return True if these parameters give a MazeError"""
    try:
        gen = MazeGenerator(width, height, entry, exit_p)
        gen.generate()
    except MazeError:
        return True
    return False


def test_walls() -> None:
    """Neighbours have the same wall and the border is closed"""
    for width, height in SIZES:
        for perfect in [True, False]:
            for seed in range(10):
                grid = make_maze(width, height, perfect, seed).grid
                for y in range(height):
                    for x in range(width):
                        # my east wall is the west wall of my neighbour
                        if x + 1 < width:
                            assert (grid[y][x] & E != 0) == \
                                (grid[y][x + 1] & W != 0)
                        # my south wall is the north wall of my neighbour
                        if y + 1 < height:
                            assert (grid[y][x] & S != 0) == \
                                (grid[y + 1][x] & N != 0)
                for x in range(width):
                    assert grid[0][x] & N
                    assert grid[height - 1][x] & S
                for y in range(height):
                    assert grid[y][0] & W
                    assert grid[y][width - 1] & E


def test_perfect() -> None:
    """Perfect maze has no loop, so open walls = cells - 1"""
    for width, height in SIZES:
        for seed in range(10):
            gen = make_maze(width, height, True, seed)
            cells = width * height - len(gen.pattern_cells)
            assert count_open_walls(gen.grid) == cells - 1


def test_pacman() -> None:
    """Pac-Man maze has at least 2 loops"""
    for width, height in SIZES:
        for seed in range(10):
            gen = make_maze(width, height, False, seed)
            cells = width * height - len(gen.pattern_cells)
            loops = count_open_walls(gen.grid) - cells + 1
            assert loops >= 2


def test_seed() -> None:
    """Same seed gives the same maze, other seed gives another one"""
    first = make_maze(20, 15, True, 42).grid
    second = make_maze(20, 15, True, 42).grid
    other = make_maze(20, 15, True, 43).grid
    assert first == second
    assert first != other


def test_path() -> None:
    """The path goes through open walls from entry to exit"""
    letters = {'N': N, 'E': E, 'S': S, 'W': W}
    for perfect in [True, False]:
        gen = make_maze(20, 15, perfect, 7)
        grid = gen.grid
        x, y = gen.entry
        for letter in gen.solution_directions():
            direction = letters[letter]
            assert grid[y][x] & direction == 0
            dx, dy = STEP[direction]
            x = x + dx
            y = y + dy
        assert (x, y) == gen.exit
        cells = gen.solve()
        assert cells[0] == gen.entry
        assert cells[-1] == gen.exit


def test_pattern() -> None:
    """42 is drawn from 9x7, its cells are closed (0xF)"""
    small = make_maze(8, 6, True, 1)
    assert small.pattern_drawn is False
    assert len(small.pattern_cells) == 0
    big = make_maze(20, 15, True, 1)
    assert big.pattern_drawn is True
    assert len(big.pattern_cells) == 20
    for x, y in big.pattern_cells:
        assert big.grid[y][x] == 0xF


def test_errors() -> None:
    """Bad parameters give MazeError"""
    assert is_maze_error(1, 5, (0, 0), (0, 4))      # too small
    assert is_maze_error(5, 5, (0, 0), (0, 0))      # entry == exit
    assert is_maze_error(5, 5, (0, 0), (5, 0))      # exit outside
    assert is_maze_error(20, 15, (0, 0), (7, 5))    # exit on the 42
    assert is_maze_error(2, 2, (0, 0), (1, 1)) is False


def test_pacman_too_small() -> None:
    """2x2 is too small for 2 loops in Pac-Man mode"""
    try:
        make_maze(2, 2, False, 1)
    except MazeError:
        return
    assert False, 'no MazeError for 2x2 Pac-Man'
