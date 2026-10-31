"""mazegen - reusable maze generator from the A-Maze-ing project"""

from .errors import MazeError
from .generator import MazeGenerator

__all__ = ['MazeGenerator', 'MazeError']