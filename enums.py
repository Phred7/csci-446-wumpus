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
    
class Output(IntEnum):
    RAT_DEATHS = 0
    RAT_GOLD = 1
    RAT_WUMPUS = 2
    RAT_PIT = 3
    RAT_OLD = 4
    RAT_ACTIONS = 5
    REA_DEATHS = 6
    REA_GOLD = 7
    REA_WUMPUS = 8
    REA_PIT = 9
    REA_OLD = 10
    REA_ACTIONS = 11