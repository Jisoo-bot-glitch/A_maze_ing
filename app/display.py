NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
RESET = "\033[0m"
ENTRY_COLOR = "\033[43m"
EXIT_COLOR = "\033[46m"
PATH_COLOR = "\033[42m"
WALL_COLOR = "\033[45m"
PATTERN_COLOR = "\033[47m"


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
        path: str,
        pattern: frozenset[tuple[int, int]],
        wall_color: str = WALL_COLOR) -> None:
    """Print the maze in the terminal, highlighting entry, exit, path
    and the 42 pattern.

    Args:
        maze: Grid of cells accessed as maze[y][x]. Each cell is an int
            from 0 to 15 whose bits encode closed walls
            (N=1, E=2, S=4, W=8).
        entry: Entry coordinates as (x, y).
        exit_p: Exit coordinates as (x, y).
        path: Shortest path from entry to exit, as a string of
            'N', 'E', 'S', 'W' letters. An empty string hides the path.
        pattern: Cells of the 42 pattern, drawn in their own color.
        wall_color: ANSI color code used for the walls.
    """
    cells = path_cells(entry, path)
    for y, floor in enumerate(maze):
        top = []
        mid = []
        for x, cell in enumerate(floor):
            if cell & NORTH:
                top.append(wall_color + "    " + RESET)
            else:
                top.append(wall_color + " " + RESET + "   ")
            if cell & WEST:
                wall = wall_color + " " + RESET
            else:
                wall = " "
            if (x, y) == entry:
                inside = ENTRY_COLOR + "   " + RESET
            elif (x, y) == exit_p:
                inside = EXIT_COLOR + "   " + RESET
            elif (x, y) in cells:
                inside = PATH_COLOR + "   " + RESET
            elif (x, y) in pattern:
                inside = PATTERN_COLOR + "   " + RESET
            else:
                inside = "   "
            mid.append(wall + inside)
        top.append(wall_color + " " + RESET)
        if floor[-1] & EAST:
            mid.append(wall_color + " " + RESET)
        top_line = ''.join(top)
        print(top_line)
        mid_line = ''.join(mid)
        print(mid_line)
    bottom = []
    for end in maze[-1]:
        if end & SOUTH:
            bottom.append(wall_color + "    " + RESET)
        else:
            bottom.append(wall_color + " " + RESET + "   ")
    bottom.append(wall_color + " " + RESET)
    bottom_line = ''.join(bottom)
    print(bottom_line)
