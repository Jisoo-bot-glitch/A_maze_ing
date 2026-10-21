from dataclasses import dataclass
from typing import Any

@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool

def parse_file():
    raw_config: dict[str, Any] = {}
    file = open("config.txt")
    raw: str = file.read()
    lines = raw.splitlines()
    print(lines)
    for word in lines:
        if "=" in word:
            splitted: list[str] = word.split("=")
            if len(splitted) != 2:
                raise Exception("Invalid config file.")
    

if __name__ == "__main__":
    parse_file()
