from dataclasses import dataclass
from typing import Any
from app.errors import ConfigError
ALLOWED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
                "SEED"]
MUST_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


# @dataclass automatically generates the __init__() method.
@dataclass
class Config:
    """Validated settings read from the config file.

    Attributes:
        width: Number of cells per row.
        height: Number of rows.
        entry: Entry coordinates as (x, y).
        exit: Exit coordinates as (x, y).
        output_file: Name of the file the maze is written to.
        perfect: True for a perfect maze (single path),
            False for a Pac-Man board with loops.
        seed: Random seed for reproducible mazes, or None for a
            different maze on every run.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None


def parse_file(file: str) -> dict[str, Any]:
    """Read a config file into a dict of raw string values.

    Blank lines and lines starting with '#' are ignored. Spaces around
    '=' are allowed, and keys are converted to uppercase.

    Args:
        file: Path of the config file.

    Returns:
        Dict mapping each key to its raw string value.

    Raises:
        OSError: If the file cannot be opened.
        ConfigError: If a line has no '=' or more than one '=', a key
        is unknown or duplicated, or a mandatory key is missing.
    """
    raw_config: dict[str, Any] = {}
    try:
        with open(file, "r", encoding="utf-8") as f:
            raw: str = f.read()
    except UnicodeDecodeError:
        raise ConfigError(f"'{file}' is not a text file")
    lines = raw.splitlines()
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if "" == line:
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"line {number}: missing '=' in '{line}'")
        splitted: list[str] = line.split("=")
        if len(splitted) != 2:
            raise ConfigError(f"line {number} has '=' more than two")
        key, value = splitted
        key = key.strip().upper()
        value = value.strip()
        if key in raw_config:
            raise ConfigError(f"line {number}: key is already mentioned")
        if key not in ALLOWED_KEYS:
            raise ConfigError(f"line {number} has not allowed key in '{line}'")
        raw_config[key] = value
    for must in MUST_KEYS:
        if must not in raw_config:
            raise ConfigError(f"missing mandatory key: {must}")
    return (raw_config)


def positive_int(raw: dict[str, str], key: str) -> int:
    """Convert the value of a key to a strictly positive integer.

    Args:
        raw: Raw config values returned by parse_file.
        key: Key to convert (e.g. "WIDTH").

    Returns:
        The value as an int greater than 0.

    Raises:
        ConfigError: If the value is not an integer or is not positive.
    """
    try:
        number = int(raw[key])
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got '{raw[key]}'")
    if number <= 0:
        raise ConfigError(f"{key} must be positive, got {number}")
    return number


def parse_coord(raw: dict[str, str], key: str,
                width: int, height: int) -> tuple[int, int]:
    """Convert an "x,y" value to coordinates inside the maze.

    Args:
        raw: Raw config values returned by parse_file.
        key: Key to convert (e.g. "ENTRY").
        width: Maze width, used for the bounds check.
        height: Maze height, used for the bounds check.

    Returns:
        The coordinates as (x, y).

    Raises:
        ConfigError: If the value is not two integers separated by a
            comma, or the cell is outside the maze.
    """
    parts = raw[key].split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must be 'x,y', got '{raw[key]}'")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        raise ConfigError(f"{key} must be two integers, got '{raw[key]}'")
    if (not 0 <= x < width and 0 <= y < height):
        raise ConfigError(f"{key} {(x, y)} is outside the maze")
    return (x, y)


def build_config(raw: dict[str, str]) -> Config:
    """Convert and validate raw config values into a Config.

    Args:
        raw: Raw config values returned by parse_file.

    Returns:
        A Config with every value converted to its final type.

    Raises:
        ConfigError: If any value is invalid, or ENTRY equals EXIT.
    """
    width = positive_int(raw, "WIDTH")
    height = positive_int(raw, "HEIGHT")
    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError:
            raise ConfigError(f"SEED must be an integer, got '{raw['SEED']}'")
    else:
        seed = None
    output_file = raw["OUTPUT_FILE"]
    if output_file == "":
        raise ConfigError("OUTPUT_FILE is empty")
    perfect_raw = raw["PERFECT"].lower()
    if perfect_raw == "true":
        perfect = True
    elif perfect_raw == "false":
        perfect = False
    else:
        raise ConfigError(
            f"PERFECT must be True or False, got '{raw['PERFECT']}'")
    entry = parse_coord(raw, "ENTRY", width, height)
    exit_p = parse_coord(raw, "EXIT", width, height)
    if entry == exit_p:
        raise ConfigError(f"ENTRY and EXIT must be different, got {entry}")

    return Config(width=width, height=height, entry=entry, exit=exit_p,
                  output_file=output_file, perfect=perfect, seed=seed)


if __name__ == "__main__":
    print(build_config(parse_file("config.txt")))
