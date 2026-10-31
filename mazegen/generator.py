import random

from .constants import (
    ALL_WALLS,
    DIRECTIONS,
    E,
    MAX_OPEN_AREA,
    MIN_HEIGHT_FOR_PATTERN,
    MIN_LOOPS,
    MIN_WIDTH_FOR_PATTERN,
    N,
    OPPOSITE,
    PATTERN_42,
    PATTERN_CHAR,
    STEP,
    S,
    W,
)
from .errors import MazeError
from .solver import bfs, path_to_directions, shortest_path

# A cell position (x, y) = (column, row)
Cell = tuple[int, int]

MIN_SIZE = 2

SEED_RANGE = 2 ** 32

# Generate a perfect maze or a Pac-Man-ready board.
class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Cell,
        exit: Cell,
        perfect: bool = True,
        seed: int | None = None,
    ) -> None:
        if not _is_int(width) or not _is_int(height):
            raise MazeError('width and height must be integers')
        if width < MIN_SIZE or height < MIN_SIZE:
            raise MazeError(
                f'maze must be at least {MIN_SIZE}x{MIN_SIZE}, '
                f'got {width}x{height}'
            )
        self._width = width
        self._height = height
        self._entry = self._checked_cell(entry, 'entry')
        self._exit = self._checked_cell(exit, 'exit')
        if self._entry == self._exit:
            raise MazeError('entry and exit must be different cells')
        if seed is not None and not _is_int(seed):
            raise MazeError('seed must be an integer')
        self._perfect = bool(perfect)
        self._seed = (
            seed if seed is not None else random.randrange(SEED_RANGE)
        )
        self._rng = random.Random(self._seed)
        self._grid: list[list[int]] = []
        self._pattern: set[Cell] = set()
        self._pattern_drawn = False

    # Public API
    def generate(self) -> list[list[int]]:
        self._rng = random.Random(self._seed)
        self._grid = [
            [ALL_WALLS] * self._width for _ in range(self._height)
        ]
        self._place_pattern()
        self._carve_perfect()
        if not self._perfect:
            self._braid()
            self._open_key_cells()
            self._ensure_loops()
        self._validate()
        return self.grid

    @property
    def grid(self) -> list[list[int]]:
        self._require_generated()
        return [row[:] for row in self._grid]

    # Number of columns
    @property
    def width(self) -> int:
        return self._width

    # Number of rows
    @property
    def height(self) -> int:
        return self._height

    # Entry cell (x, y)
    @property
    def entry(self) -> Cell:
        return self._entry

    # Exit cell (x, y)
    @property
    def exit(self) -> Cell:
        return self._exit

    # True for a perfect maze, False for Pac-Man mode
    @property
    def perfect(self) -> bool:
        return self._perfect

    # The seed actually used (given, or drawn when None)
    @property
    def seed(self) -> int:
        return self._seed

    # Cells of the 42 pattern (empty when it did not fit)
    @property
    def pattern_cells(self) -> frozenset[Cell]:
        return frozenset(self._pattern)

    # False when the maze is too small for the 42 pattern
    @property
    def pattern_drawn(self) -> bool:
        return self._pattern_drawn

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        self._require_generated()
        if not self._inside(x, y):
            raise MazeError(f'cell ({x}, {y}) is outside the maze')
        return bool(self._grid[y][x] & direction)

    # Find a path from entry to exit
    def solve(self) -> list[Cell]:
        self._require_generated()
        path = shortest_path(self._grid, self._entry, self._exit)
        if not path:
            raise MazeError('exit is not reachable from entry')
        return path

    def solution_directions(self) -> str:
        return path_to_directions(self.solve())

    # Grid helpers
    def _checked_cell(self, cell: Cell, name: str) -> Cell:
        if (
            not isinstance(cell, tuple)
            or len(cell) != 2
            or not all(_is_int(v) for v in cell)
        ):
            raise MazeError(f'{name} must be a pair of integers (x, y)')
        if not self._inside(cell[0], cell[1]):
            raise MazeError(
                f'{name} {cell} is outside the {self._width}x'
                f'{self._height} maze'
            )
        return cell

    def _require_generated(self) -> None:
        if not self._grid:
            raise MazeError('maze not generated yet: call generate()')

    def _inside(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height

    def _neighbour(self, x: int, y: int, d: int) -> Cell:
        dx, dy = STEP[d]
        return x + dx, y + dy

    def _remove_wall(self, x: int, y: int, d: int) -> None:
        nx, ny = self._neighbour(x, y, d)
        self._grid[y][x] &= ~d
        self._grid[ny][nx] &= ~OPPOSITE[d]

    def _add_wall(self, x: int, y: int, d: int) -> None:
        nx, ny = self._neighbour(x, y, d)
        self._grid[y][x] |= d
        self._grid[ny][nx] |= OPPOSITE[d]

    def _open_sides(self, x: int, y: int) -> int:
        return sum(1 for d in DIRECTIONS if not self._grid[y][x] & d)

    def _is_free(self, x: int, y: int) -> bool:
        return self._inside(x, y) and (x, y) not in self._pattern

    def _closed_free_sides(self, x: int, y: int) -> list[int]:
        return [
            d for d in DIRECTIONS
            if self._grid[y][x] & d
            and self._is_free(*self._neighbour(x, y, d))
        ]

    # 42 pattern
    def _place_pattern(self) -> None:
        self._pattern = set()
        self._pattern_drawn = (
            self._width >= MIN_WIDTH_FOR_PATTERN
            and self._height >= MIN_HEIGHT_FOR_PATTERN
        )
        if not self._pattern_drawn:
            return
        ox = self._width // 2 - len(PATTERN_42[0]) // 2
        oy = self._height // 2 - len(PATTERN_42) // 2
        for row, line in enumerate(PATTERN_42):
            for col, char in enumerate(line):
                if char == PATTERN_CHAR:
                    self._pattern.add((ox + col, oy + row))
        for name, cell in (('entry', self._entry), ('exit', self._exit)):
            if cell in self._pattern:
                raise MazeError(
                    f'{name} {cell} is on the 42 pattern, choose '
                    'another cell'
                )

    # Perfect maze: iterative randomized depth-first search
    def _carve_perfect(self) -> None:
        visited: set[Cell] = set(self._pattern)
        stack: list[Cell] = [self._entry]
        visited.add(self._entry)
        while stack:
            x, y = stack[-1]
            free: list[int] = []
            for d in DIRECTIONS:
                nxt = self._neighbour(x, y, d)
                if self._inside(*nxt) and nxt not in visited:
                    free.append(d)
            if not free:
                stack.pop()
                continue
            d = self._rng.choice(free)
            self._remove_wall(x, y, d)
            nxt = self._neighbour(x, y, d)
            visited.add(nxt)
            stack.append(nxt)

    # Pac-Man mode
    def _braid(self) -> None:
        dead_ends = [
            (x, y)
            for y in range(self._height)
            for x in range(self._width)
            if self._is_free(x, y) and self._open_sides(x, y) == 1
        ]
        self._rng.shuffle(dead_ends)
        for x, y in dead_ends:
            if self._open_sides(x, y) != 1:
                continue
            sides = self._closed_free_sides(x, y)
            self._rng.shuffle(sides)
            sides.sort(
                key=lambda d: self._open_sides(*self._neighbour(x, y, d))
                != 1
            )
            for d in sides:
                if self._try_open(x, y, d):
                    break

    def _open_key_cells(self) -> None:
        w, h = self._width, self._height
        key_cells = [
            (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
            (w // 2, h // 2),
        ]
        for x, y in key_cells:
            if not self._is_free(x, y) or self._open_sides(x, y) >= 2:
                continue
            sides = self._closed_free_sides(x, y)
            self._rng.shuffle(sides)
            for d in sides:
                if self._try_open(x, y, d):
                    break

    def _ensure_loops(self) -> None:
        if self._count_loops() >= MIN_LOOPS:
            return
        walls = [
            (x, y, d)
            for y in range(self._height)
            for x in range(self._width)
            for d in (E, S)
            if self._is_free(x, y) and d in self._closed_free_sides(x, y)
        ]
        self._rng.shuffle(walls)
        for x, y, d in walls:
            if self._try_open(x, y, d) and \
                    self._count_loops() >= MIN_LOOPS:
                return
        raise MazeError(
            f'{self._width}x{self._height} is too small for the Pac-Man '
            f'mode ({MIN_LOOPS} independent loops needed)'
        )

    def _try_open(self, x: int, y: int, d: int) -> bool:
        self._remove_wall(x, y, d)
        if self._has_open_area((x, y), self._neighbour(x, y, d)):
            self._add_wall(x, y, d)
            return False
        return True

    def _has_open_area(self, a: Cell, b: Cell) -> bool:
        size = MAX_OPEN_AREA
        x_lo = max(0, max(a[0], b[0]) - size + 1)
        x_hi = min(min(a[0], b[0]), self._width - size)
        y_lo = max(0, max(a[1], b[1]) - size + 1)
        y_hi = min(min(a[1], b[1]), self._height - size)
        for wy in range(y_lo, y_hi + 1):
            for wx in range(x_lo, x_hi + 1):
                if self._window_open(wx, wy):
                    return True
        return False

    def _window_open(self, wx: int, wy: int) -> bool:
        size = MAX_OPEN_AREA
        for y in range(wy, wy + size):
            for x in range(wx, wx + size):
                cell = self._grid[y][x]
                if x < wx + size - 1 and cell & E:
                    return False
                if y < wy + size - 1 and cell & S:
                    return False
        return True

    def _count_open_walls(self) -> int:
        count = 0
        for y in range(self._height):
            for x in range(self._width):
                if x + 1 < self._width and not self._grid[y][x] & E:
                    count += 1
                if y + 1 < self._height and not self._grid[y][x] & S:
                    count += 1
        return count

    def _count_loops(self) -> int:
        cells = self._width * self._height - len(self._pattern)
        return self._count_open_walls() - cells + 1

    # Self-check
    def _validate(self) -> None:
        self._check_coherence()
        self._check_border()
        self._check_connected()
        loops = self._count_loops()
        if self._perfect and loops != 0:
            raise MazeError(f'perfect maze has {loops} loop(s)')
        if not self._perfect:
            if loops < MIN_LOOPS:
                raise MazeError(f'only {loops} loop(s), {MIN_LOOPS} needed')
            self._check_no_open_area()

    def _check_coherence(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                for d in (E, S):
                    nx, ny = self._neighbour(x, y, d)
                    if not self._inside(nx, ny):
                        continue
                    if bool(self._grid[y][x] & d) != \
                            bool(self._grid[ny][nx] & OPPOSITE[d]):
                        raise MazeError(
                            f'incoherent wall between ({x}, {y}) and '
                            f'({nx}, {ny})'
                        )

    def _check_border(self) -> None:
        for x in range(self._width):
            if not self._grid[0][x] & N or \
                    not self._grid[self._height - 1][x] & S:
                raise MazeError(f'border open in column {x}')
        for y in range(self._height):
            if not self._grid[y][0] & W or \
                    not self._grid[y][self._width - 1] & E:
                raise MazeError(f'border open in row {y}')

    def _check_connected(self) -> None:
        reached = bfs(self._grid, self._entry)
        expected = self._width * self._height - len(self._pattern)
        if len(reached) != expected:
            raise MazeError(
                f'{expected - len(reached)} cell(s) unreachable from entry'
            )

    def _check_no_open_area(self) -> None:
        size = MAX_OPEN_AREA
        for wy in range(self._height - size + 1):
            for wx in range(self._width - size + 1):
                if self._window_open(wx, wy):
                    raise MazeError(
                        f'open {size}x{size} area at ({wx}, {wy})'
                    )


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)
