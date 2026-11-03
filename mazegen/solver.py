from collections import deque
from .constants import N, E, S, W


def solver(maze: list[list[int]],
           entry: tuple[int, int],
           exit_p: tuple[int, int]) -> str:
    """Find the shortest path from entry to exit with BFS.

    Explores the maze breadth-first from the entry. Each queued cell
    carries the path taken to reach it, so the first time the exit is
    reached, its path is the shortest one.

    Args:
        maze: Grid of cells accessed as maze[y][x]. Each cell is an int
            from 0 to 15 whose bits encode closed walls
            (N=1, E=2, S=4, W=8).
        entry: Entry coordinates as (x, y).
        exit_p: Exit coordinates as (x, y).

    Returns:
        The shortest path as a string of 'N', 'E', 'S', 'W' letters.
        Returns an empty string if the exit cannot be reached.
    """
    x, y = entry
    q: deque[tuple[tuple[int, int], str]] = deque()
    visited: set[tuple[int, int]] = set()
    q.append(((x, y), ""))
    visited.add((x, y))
    while q:
        (x, y), path = q.popleft()
        if (x, y) == exit_p:
            return (path)
        if (not (maze[y][x] & E)
                and x + 1 < len(maze[0])
                and (x + 1, y) not in visited):
            visited.add((x + 1, y))
            q.append(((x + 1, y), path + "E"))
        if (not (maze[y][x] & S)
                and y + 1 < len(maze)
                and (x, y + 1) not in visited):
            visited.add((x, y + 1))
            q.append(((x, y + 1), path + "S"))
        if (not (maze[y][x] & W)
                and x - 1 >= 0
                and (x - 1, y) not in visited):
            visited.add((x - 1, y))
            q.append(((x - 1, y), path + "W"))
        if (not (maze[y][x] & N)
                and y - 1 >= 0
                and (x, y - 1) not in visited):
            visited.add((x, y - 1))
            q.append(((x, y - 1), path + "N"))
    return ""
