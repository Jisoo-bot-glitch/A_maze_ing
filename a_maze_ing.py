import sys
from app import parse_file, build_config, ConfigError, output_maze, display
from mazegen import MazeGenerator, MazeError


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)
    try:
        config = build_config(parse_file(sys.argv[1]))
        generator = MazeGenerator(config.width, config.height, config.entry,
                                  config.exit, config.perfect, config.seed)
        maze = generator.generate()
        if not generator.pattern_drawn:
            print("Warning: 42 pattern failed - maze is too small", file=sys.stderr)
        path = generator.solution_directions()
        pattern = generator.pattern_cells
        output_maze(config.output_file, maze, config.entry, config.exit, path)
        display(maze, config.entry, config.exit, path, pattern)
    except (ConfigError, MazeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
