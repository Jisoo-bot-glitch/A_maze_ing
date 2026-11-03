#! /usr/bin/env python3
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


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
    q = []
    visited = []
    q.append(((x, y), ""))
    visited.append((x, y))
    while q:
        (x, y), path = q.pop(0)
        if (x, y) == exit_p:
            return (path)
        if (not (maze[y][x] & EAST)
                and x + 1 < len(maze[0])
                and (x + 1, y) not in visited):
            visited.append((x + 1, y))
            q.append(((x + 1, y), path + "E"))
        if (not (maze[y][x] & SOUTH)
                and y + 1 < len(maze)
                and (x, y + 1) not in visited):
            visited.append((x, y + 1))
            q.append(((x, y + 1), path + "S"))
        if (not (maze[y][x] & WEST)
                and x - 1 >= 0
                and (x - 1, y) not in visited):
            visited.append((x - 1, y))
            q.append(((x - 1, y), path + "W"))
        if (not (maze[y][x] & NORTH)
                and y - 1 >= 0
                and (x, y - 1) not in visited):
            visited.append((x, y - 1))
            q.append(((x, y - 1), path + "N"))
    return ""


if __name__ == "__main__":
    maze = [[11, 9, 3, 11, 13, 5, 3],
            [8, 6, 12, 0, 5, 1, 6],
            [14, 9, 5, 6, 9, 2, 11],
            [13, 6, 9, 5, 2, 12, 6],
            [9, 1, 6, 13, 4, 5, 3],
            [10, 12, 5, 1, 3, 11, 10],
            [12, 5, 7, 12, 12, 6, 14]]
    path = "ESEEESWSWWSWSEES"
    print(solver(maze, (1, 0), (3, 6)))
