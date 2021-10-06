from enum import Enum

import numpy as np


class CellValue(Enum):
    WUMPUS: int = 0
    PIT: int = 1
    OBSTACLE: int = 2
    GOLD: int = 3
    size: int = 4  # this represents the number of bools in the third dim of the grid


class Board:

    def __init__(self, size: int = 0, ):
        self.grid = np.zeros([size, size, CellValue.size], dtype=bool)
        self.wumpus_count: int = 0
        pass

    def get_scream(self, x: int, y: int) -> bool:
        pass

    def get_scent(self, x: int, y: int) -> bool:
        pass

    def get_glimmer(self, x: int, y: int) -> bool:
        pass

    def get_bump(self, x: int, y: int) -> bool:
        pass

    def wumpusi(self) -> int:
        return self.wumpus_count

    def generate_board(self) -> None:
        pass
