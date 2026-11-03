"""app - command-line side of A-Maze-ing: config, output file and display"""

from .config import parse_file, build_config
from .errors import ConfigError
from .display import display
from .writer import output_maze

__all__ = ['parse_file', 'build_config', 'ConfigError', 'display',
           'output_maze']
