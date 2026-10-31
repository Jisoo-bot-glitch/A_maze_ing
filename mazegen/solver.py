""" TEMPORARY placeholder for Jisoo"""

from collections import deque

from .constants import DIRECTIONS, LETTER, STEP

Cell = tuple[int, int]


def bfs(grid: list[list[int]], start: Cell) -> dict[Cell, Cell | None]:
    """Return parent for every cell reachable from start."""
    height, width = len(grid), len(grid[0])
    parent: dict[Cell, Cell | None] = {start: None}
    queue: deque[Cell] = deque([start])
    while queue:
        x, y = queue.popleft()
        for d in DIRECTIONS:
            if grid[y][x] & d:
                continue
            dx, dy = STEP[d]
            nxt = (x + dx, y + dy)
            if 0 <= nxt[0] < width and 0 <= nxt[1] < height \
                    and nxt not in parent:
                parent[nxt] = (x, y)
                queue.append(nxt)
    return parent


def shortest_path(
    grid: list[list[int]], entry: Cell, exit: Cell
) -> list[Cell]:
    """Return the cells from entry to exit, or [] if exit is unreachable"""
    parent = bfs(grid, entry)
    if exit not in parent:
        return []
    path: list[Cell] = []
    cell: Cell | None = exit
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    return path


def path_to_directions(path: list[Cell]) -> str:
    """Turn a list of neighbour cells into N/E/S/W letters"""
    letters: list[str] = []
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        for d in DIRECTIONS:
            if STEP[d] == (x2 - x1, y2 - y1):
                letters.append(LETTER[d])
    return "".join(letters)
