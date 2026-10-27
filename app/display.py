#! /usr/bin/env python3
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


def display(
        maze: list[list[int]],
        entry: tuple[int, int],
        exit_p: tuple[int, int],
        path: str) -> None:
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
    maze = [[11, 9, 3, 10, 13, 5, 3],
            [8, 6, 12, 0, 5, 1, 6],
            [14, 9, 5, 6, 9, 2, 11],
            [13, 6, 9, 5, 2, 12, 6],
            [9, 1, 6, 13, 4, 5, 3],
            [10, 12, 5, 1, 3, 11, 10],
            [12, 5, 7, 10, 12, 6, 14]]
    path = "ESEEESWSWWSWSEES"
    display(maze, (1, 0), (3, 6), path)
