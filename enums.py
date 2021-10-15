from enum import *

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Facing(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class CellContent(IntEnum):
    WUMPUS: int = 0
    PIT: int = 1
    OBSTACLE: int = 2
    GOLD: int = 3

class Sensation(IntEnum):
    STENCH: int = 0
    BREEZE: int = 1
    GLIMMER: int = 2

class VisitState(IntEnum):
    UNKNOWN = 0
    VISITED = 1
    FRONTIER = 2
    IMPASSABLE = 3