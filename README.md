*This activity has been created as part of the 42 curriculum by efatin, jisobaek.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, builds a maze, writes it to a file using a hexadecimal wall encoding,
and draws it in the terminal with colors.

Two kinds of mazes can be generated:

- **Perfect maze** (`PERFECT=True`): exactly one path between any two cells,
  no loops at all.
- **Pac-Man board** (`PERFECT=False`, the default in the subject): every cell
  is reachable, the four corners and the centre are open, there are at least
  two independent loops, dead-ends are removed when possible, and there is
  never an open 3x3 area.

In both modes, a visible **"42"** is drawn in the middle of the maze with
fully closed cells (if the maze is big enough), and the shortest path from
the entry to the exit is computed with a BFS.

The maze generation logic lives in a standalone, reusable package called
`mazegen`, which can be built as a wheel and installed with `pip`.

## Instructions

### Requirements

- Python 3.10 or later
- `make`

### Installation

It is recommended to use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

`make install` installs `flake8`, `mypy` and `build`.

### Run

```bash
python3 a_maze_ing.py config.txt
```

or simply:

```bash
make        # same as make run
make run
```

`config.txt` is the default configuration file. Any other file name can be
given as the only argument.

### Makefile rules

| Rule | Description |
| --- | --- |
| `make install` | Install the development tools (flake8, mypy, build) |
| `make run` | Run the program with `config.txt` |
| `make debug` | Run the program with the Python debugger (`pdb`) |
| `make clean` | Remove `__pycache__`, `.mypy_cache` and `.DS_Store` files |
| `make lint` | Run `flake8` and `mypy` with the flags required by the subject |
| `make lint-strict` | Run `flake8` and `mypy --strict` |

### Interactive menu

After the maze is drawn, a menu is shown:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Quit
```

- **1. Re-generate**: builds a new maze with a new random seed, rewrites the
  output file, and redraws it.
- **2. Show/Hide path**: toggles the shortest path on the screen.
- **3. Rotate colors**: cycles through several wall colors.
- **4. Quit**: exits the program. `Ctrl+C` and `Ctrl+D` also exit cleanly.

Colors on screen: entry in yellow, exit in cyan, shortest path in green,
"42" pattern in light gray.

## Configuration file

One `KEY=VALUE` pair per line. Lines starting with `#` are comments, and
empty lines are ignored.

```
# A-Maze-ing default configuration

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
SEED=42
```

| Key | Mandatory | Description | Rules |
| --- | --- | --- | --- |
| `WIDTH` | yes | Number of cells per row | Integer from 1 to 200 |
| `HEIGHT` | yes | Number of rows | Integer from 1 to 200 |
| `ENTRY` | yes | Entry cell as `x,y` | Two integers, inside the maze |
| `EXIT` | yes | Exit cell as `x,y` | Two integers, inside the maze, different from `ENTRY` |
| `OUTPUT_FILE` | yes | Name of the output file | Not empty. Created, or overwritten if it exists |
| `PERFECT` | yes | Perfect maze or Pac-Man board | `True` or `False` (any case) |
| `SEED` | no | Random seed | Any integer. If missing, a different maze is built on every run |

Other rules:

- Spaces around `=` are allowed (`WIDTH = 20`).
- Keys are not case-sensitive (`width=20` is read as `WIDTH=20`).
- A line without `=`, with more than one `=`, an unknown key or a duplicated
  key is an error.
- Coordinates are always `(x, y)`: `x` is the column, `y` is the row, and
  `(0, 0)` is the top-left cell.

Every error stops the program with a clear message on stderr and exit
status 1. The program never crashes with a traceback.

Some limits come from the generator itself:

- The "42" pattern needs a maze of at least 9x7. On smaller mazes it is
  skipped and a warning is printed.
- `ENTRY` and `EXIT` cannot be on a "42" cell.
- The Pac-Man mode needs enough room to create two loops; on very small
  mazes it reports an error.

## Output file format

Each cell is written as one hexadecimal digit. Each bit is a closed wall:

| Bit | Value | Direction |
| --- | --- | --- |
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

Cells are written row by row, one row per line. After an empty line come
the entry coordinates, the exit coordinates, and the shortest path as
`N`, `E`, `S`, `W` letters. Every line ends with `\n`.

```
9515391539551795151151153
EBABAE812853C1412BA812812
...

0,0
19,14
SWSESWSESWSSSEESEEENEESES...
```

## Maze generation algorithm

### Perfect maze: iterative DFS (recursive backtracker)

1. Every cell starts with its four walls closed.
2. The "42" cells are marked in the middle and stay closed.
3. Starting from the entry, a DFS with an explicit stack picks a random
   unvisited neighbour, opens the wall between the two cells, and moves to
   it. When a cell has no unvisited neighbour, the DFS goes back
   (pops the stack).

A wall is only opened when entering a cell for the first time, so no loop
can ever be created, and every cell is visited. The result is a spanning
tree of the grid: a perfect maze.

### Pac-Man mode

Starting from the perfect maze:

1. **Braiding**: in each dead-end, one more wall is opened.
2. **Key cells**: the four corners and the centre get at least two exits.
3. **Loops**: more walls are opened until there are at least two
   independent loops. The number of loops is
   `open inner walls - cells + 1` (0 for a perfect maze).
4. A wall is never opened if it would create an open 3x3 area.

### Self-check

At the end, the generator checks its own maze and raises `MazeError` if
something is wrong: coherent walls between neighbours, closed outer border,
every cell reachable from the entry, the right number of loops, and no open
3x3 area.

### Shortest path: BFS

The solver explores the maze breadth-first from the entry with a queue
(`collections.deque`). Each queued cell carries the path taken to reach it
as a string of letters, so the first time the exit is reached, its path is
the shortest one. Visited cells are kept in a `set`.

### Why these algorithms

- **DFS** is simple to implement and to explain, it guarantees a perfect
  maze, and it gives long winding corridors that look like a real maze.
  The iterative version (with a stack) avoids Python's recursion limit on
  big mazes. Using our own `random.Random(seed)` makes every maze
  reproducible from its seed.
- **Braiding** a perfect maze is a direct way to reach the Pac-Man rules:
  removing dead-ends naturally creates loops.
- **BFS** always finds a shortest path in a maze where every step has the
  same cost.

## Reusable code: the `mazegen` package

The whole maze generation (generator, solver, constants and errors) is in
the `mazegen` package and does not depend on the rest of the project.

### Build and install

```bash
python3 -m pip install build
python3 -m build
pip install mazegen-1.0.0-py3-none-any.whl
```

The wheel file `mazegen-1.0.0-py3-none-any.whl` is also available at the
root of the repository.

### Basic example

```python
from mazegen import MazeGenerator, MazeError

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42,
)
grid = generator.generate()          # grid[y][x], one int 0..15 per cell
path = generator.solution_directions()   # for example "SSEESW..."
```

### Custom parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `width`, `height` | `int` | | Size of the maze (at least 2x2) |
| `entry`, `exit` | `tuple[int, int]` | | Cells as `(x, y)` |
| `perfect` | `bool` | `True` | Perfect maze or Pac-Man board |
| `seed` | `int` or `None` | `None` | Same seed gives the same maze. `None` picks a random seed |

### Accessing the result

| Attribute / method | Returns |
| --- | --- |
| `generate()` | Builds the maze and returns the grid |
| `grid` | Copy of the grid, `grid[y][x]`, bits N=1, E=2, S=4, W=8 |
| `has_wall(x, y, direction)` | `True` if that wall is closed |
| `solution_directions()` | Shortest path as `N`/`E`/`S`/`W` letters |
| `solve()` | Shortest path as a list of `(x, y)` cells, entry included |
| `pattern_cells` | Cells of the "42" pattern |
| `pattern_drawn` | `False` if the maze was too small for the "42" |
| `seed` | Seed that was used |

Invalid parameters, or a maze that fails its self-check, raise `MazeError`.

## Team and project management

### Roles

| Member | Role |
| --- | --- |
| **efatin** | `mazegen` package: grid model, "42" pattern, perfect maze (DFS), Pac-Man mode, self-validation, constants, `MazeError`, packaging (`pyproject.toml`, wheel), `LICENSE.md`. Integration tests on many mazes, and speed improvements of the solver (`deque` and `set`). |
| **jisobaek** | Application side: config parser and validation (`ConfigError`), output file writer, terminal display (colors, path, "42"), BFS solver, main program and interactive menu, `Makefile`, default config. |

Both: shared interfaces, code reviews through pull requests, README,
defense preparation.

### Planning and how it evolved

The first plan was about 17 days:

1. Agree on the shared interfaces (grid as `grid[y][x]`, coordinates as
   `(x, y)`, wall bits, path as letters).
2. Work in parallel: generator on one side, config, writer, display and
   solver on the other side.
3. Integrate, test with `maze_analyzer.py`, write the README.

How it evolved:

- The writer and the display were done first, so the generator could be
  checked with `maze_analyzer.py` and seen on screen early.
- The solver was first written as a temporary placeholder inside the
  package to test the generator, then replaced by the final BFS solver.
  The generator was updated to call it.
- The interactive menu was moved from `display.py` to `a_maze_ing.py`, so
  that `display.py` only draws and the main program controls the flow.
- One week was slower than planned because of illness, so the integration
  and the menu were done at the end.

<!-- TODO: check the dates and adjust this section together. -->

### What worked well

- Clear ownership: each file had one owner, written in a shared tracker.
- Agreeing early on the grid format and on `(x, y)` coordinates made the
  parts fit together with very few changes.
- Reviewing each other's code found real bugs on both sides (for example
  a wrong bounds check in the config, and a slow list-based queue in the
  solver).
- `maze_analyzer.py` and a test on hundreds of mazes gave confidence in the
  generator and the solver.

### What could be improved

- Agree on the generator's public API even earlier, before writing code
  that depends on it.
- Always merge through a pull request after the other member's review, and
  ask before changing a file owned by the other member.
- Update the tracker together with every commit.

### Tools

- Git and GitHub (branches, pull requests, code review)
- A shared `TRACKER.md` for tasks, owners and status
- `flake8` and `mypy`
- `maze_analyzer.py` (given with the subject) and a custom tester
- `pdb` for debugging
- Python virtual environments (`venv`)

## Resources

- [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) (Wikipedia)
- [Maze generation: recursive backtracking](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking) (Jamis Buck)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) (Wikipedia)
- [collections.deque](https://docs.python.org/3/library/collections.html#collections.deque) (Python documentation)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html) (Python documentation)
- [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code) (Wikipedia)
- [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/)
- [Packaging Python projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [MIT License](https://choosealicense.com/licenses/mit/)

### Use of AI

- **jisobaek** used Claude as a tutor: explanations of bit operations,
  BFS, Python syntax (lists, dicts, `enumerate`, exceptions), Git, pull
  requests and Makefiles, and review of the code written by hand. The
  algorithm and the code of the config parser, writer, display, solver
  and main program were written by jisobaek, step by step. AI helped
  write some docstrings and draft this README.

<!-- TODO (efatin): describe how you used AI, if you did. -->

## License

This project is under the MIT License. See [LICENSE.md](LICENSE.md).
