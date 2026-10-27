#! /usr/bin/env python3
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


def path_cells(entry: tuple[int, int],
               path: str) -> list[tuple[int, int]]:
    """Convert a path string into the list of cells it visits.

    Args:
        entry: Entry coordinates as (x, y).
        path: Path from entry to exit, as a string of
            'N', 'E', 'S', 'W' letters.
    Returns:
        List of (x, y) cells visited after the entry, in order.
        The entry itself is not included: the last cell is the exit.
    """
    x, y = entry
    cells = []
    for letter in path:
        if letter == "E":
            x += 1
        elif letter == "S":
            y += 1
        elif letter == "W":
            x -= 1
        elif letter == "N":
            y -= 1
        cells.append((x, y))
    return cells


def display(
        maze: list[list[int]],
        entry: tuple[int, int],
        exit_p: tuple[int, int],
        path: str) -> None:
    """Print the maze in the terminal, highlighting entry, exit and path.

    Args:
        maze: Grid of cells accessed as maze[y][x]. Each cell is an int
            from 0 to 15 whose bits encode closed walls
            (N=1, E=2, S=4, W=8).
        entry: Entry coordinates as (x, y).
        exit_p: Exit coordinates as (x, y).
        path: Shortest path from entry to exit, as a string of
              'N', 'E', 'S', 'W' letters.
    """
    cells = path_cells(entry, path)
    for y, floor in enumerate(maze):
        top = []
        mid = []
        for x, cell in enumerate(floor):
            if cell & NORTH:
                top.append("+---")
            else:
                top.append("+   ")
            if cell & WEST:
                wall = "|"
            else:
                wall = " "
            if (x, y) == entry:
                inside = " S "
            elif (x, y) == exit_p:
                inside = " E "
            elif (x, y) in cells:
                inside = " . "
            else:
                inside = "   "
            mid.append(wall + inside)
        top.append("+")
        if floor[-1] & EAST:
            mid.append("|")
        top_line = ''.join(top)
        print(top_line)
        mid_line = ''.join(mid)
        print(mid_line)
    bottom = []
    for end in maze[-1]:
        if end & SOUTH:
            bottom.append("+---")
        else:
            bottom.append("+   ")
    bottom.append("+")
    bottom_line = ''.join(bottom)
    print(bottom_line)


if __name__ == "__main__":
    maze = [[11, 9, 3, 11, 13, 5, 3],
            [8, 6, 12, 0, 5, 1, 6],
            [14, 9, 5, 6, 9, 2, 11],
            [13, 6, 9, 5, 2, 12, 6],
            [9, 1, 6, 13, 4, 5, 3],
            [10, 12, 5, 1, 3, 11, 10],
            [12, 5, 7, 12, 12, 6, 14]]
    path = "ESEEESWSWWSWSEES"
    display(maze, (1, 0), (3, 6), path)
    print(path_cells((1, 0), "ESEEESWSWWSWSEES"))
