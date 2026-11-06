"""A-Maze-ing: generate a maze from a config file and show it.

Usage:
    python3 a_maze_ing.py <config_file>

Reads the config file, builds the maze with mazegen, writes it to the
output file in hex format and draws it in the terminal.
"""
import sys
from app import (
    parse_file,
    build_config,
    Config,
    ConfigError,
    output_maze,
    display
)
from mazegen import MazeGenerator, MazeError


def build_maze(config: Config, seed: int | None
               ) -> tuple[list[list[int]], str, frozenset[tuple[int, int]]]:
    generator = MazeGenerator(config.width,
                              config.height,
                              config.entry,
                              config.exit,
                              config.perfect,
                              seed)
    maze = generator.generate()
    if not generator.pattern_drawn:
        print("Warning: 42 pattern failed - maze size", file=sys.stderr)
    path = generator.solution_directions()
    pattern = generator.pattern_cells
    output_maze(config.output_file, maze, config.entry, config.exit, path)
    return maze, path, pattern


def main() -> None:
    """Run the program from the command line.

    Steps: read the config, generate the maze, print a warning if the
    42 pattern does not fit, find the shortest path, write the output
    file, then draw the maze and show the interactive menu.

    Menu:
        1. Re-generate: build a new maze with a random seed, then
           rewrite the output file and redraw it.
        2. Show/Hide the shortest path.
        3. Rotate the wall color.
        4. Quit (Ctrl+C and Ctrl+D also quit cleanly).

    Exits with status 1 and a message on stderr if the arguments are
    wrong, or if a ConfigError, MazeError or OSError happens.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)
    try:
        config = build_config(parse_file(sys.argv[1]))
        maze, path, pattern = build_maze(config, config.seed)
        show_path = True
        wall_colors = ["\033[45m", "\033[44m", "\033[41m"]
        color_index = 0
        print("\033[2J\033[H", end="")
        display(maze,
                config.entry,
                config.exit,
                path,
                pattern,
                wall_colors[color_index])
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            try:
                choice = input("Choice? (1-4): ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if choice == "1":
                maze, path, pattern = build_maze(config, None)
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                color_index = (color_index + 1) % len(wall_colors)
            elif choice == "4":
                break
            else:
                print("Invalid choice")
                continue
            if show_path:
                shown_path = path
            else:
                shown_path = ""
            print("\033[2J\033[H", end="")
            display(maze,
                    config.entry,
                    config.exit,
                    shown_path,
                    pattern,
                    wall_colors[color_index])
    except (ConfigError, MazeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
