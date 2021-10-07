from enum import IntEnum

import numpy as np


class CellValue(IntEnum):
    WUMPUS: int = 0
    PIT: int = 1
    OBSTACLE: int = 2
    GOLD: int = 3
    num_dimensions: int = 4  # this represents the number of bools in the third dim of the grid

class Sensation(IntEnum):
    STENCH: int = 0
    BREEZE: int = 1
    GLIMMER: int = 2

class Board:

    def __init__(self, size: int = 5, ):
        self.grid = np.zeros([size, size, 4], dtype=bool) #TODO: WALKER I USED num_dimensions BUT THE TYPE WAS WRONG
        self.size = size
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

    def generate_board(self) -> None:
        pass

    def kill_wumpus(self, coords) -> None:
        pass

    def insert_wumpus(self, coords):
        self.grid[coords[0]][coords[1]][CellValue.WUMPUS] = True
        self.wumpus_count += 1

    #TODO: IDK HOW TO DO A RETURN SIGNATURE FOR AN ARRAY
    def get_observations(self, coords):
        adjacentCells = []
        x = coords[0]
        y = coords[1]

        if x > 0:
            adjacentCells.append([x - 1, y])
        if y > 0:
            adjacentCells.append([x, y - 1])
        if x < self.size - 1:
            adjacentCells.append([x + 1, y])
        if y < self.size - 1:
            adjacentCells.append([x, y + 1])

        sensations = np.full(len(Sensation), False)
        for adj in adjacentCells:
            if self.grid[adj[0]][adj[1]][CellValue.WUMPUS]:
                sensations[Sensation.STENCH] = True
            if self.grid[adj[0]][adj[1]][CellValue.PIT]:
                sensations[Sensation.BREEZE] = True
            if self.grid[adj[0]][adj[1]][CellValue.GOLD]:
                sensations[Sensation.GLIMMER] = True
        return sensations