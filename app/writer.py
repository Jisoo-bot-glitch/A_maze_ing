def output_maze(
        file: str,
        maze: list[list[int]],
        entry: tuple[int, int],
        exit_p: tuple[int, int],
        path: str) -> None:
    """Write the maze and its solution to a file in hex format.

    Args:
        file: Name of the output file. It is created if it does not exist,
              and overwritten if it already exists.
        maze: Grid of cells accessed as maze[y][x]. Each cell is an int
              from 0 to 15 whose bits encode closed walls (N=1, E=2, S=4, W=8).
        entry: Entry coordinates as (x, y).
        exit_p: Exit coordinates as (x, y).
        path: Shortest path from entry to exit, as a string of
             'N', 'E', 'S', 'W' letters.
    Raises:
        OSError: If the file cannot be opened or written (e.g. the folder
                 does not exist, the name is a directory,
                 or permission is denied).
    """
    digits = "0123456789ABCDEF"
    row = []
    for floor in maze:
        for cell in floor:
            row.append(digits[cell])
        row.append("\n")
    result = "".join(row)
    with open(file, "w") as f:
        f.write(result)
        f.write("\n")
        res = ','.join(str(val) for val in entry)
        f.write(res)
        f.write("\n")
        res_p = ','.join(str(val) for val in exit_p)
        f.write(res_p)
        f.write("\n")
        f.write(path)
        f.write("\n")


if __name__ == "__main__":
    maze = [[9, 5],
            [12, 13]]
    entry = (0, 0)
    exit_p = (19, 14)
    path = "SWESENSWSSENEEENNESSSEES"
    output_maze("output_maze.txt", maze, entry, exit_p, path)
