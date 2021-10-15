from random import randint
from random import random
import numpy as np
from enums import *

class Board:

    def __init__(self, size: int = 5, ) -> None:
        self.grid = np.zeros([size, size, len(CellContent)],
                             dtype=bool)  # TODO: WALKER I USED num_dimensions BUT THE TYPE WAS WRONG
        self.size = size
        self.wumpus_count: int = 0
        pass

    # TODO: guarantee safe path
    def generate_board(self, wumpus_probability: float = 0.1, pit_probability: float = 0.1, obstacle_probability: float = 0.1) -> None:
        gold_x: int = 0
        gold_y: int = 0

        while gold_x == 0 and gold_y == 0:
            gold_x = randint(0, self.size - 1)
            gold_y = randint(0, self.size - 1)
        self.grid[gold_x][gold_y][CellContent.GOLD] = True

        for i in range(self.size):
            for j in range(self.size):
                if random() < wumpus_probability and not self.grid[i][j][CellContent.GOLD] and not (i == 0 and j == 0):
                    self.grid[i][j][CellContent.WUMPUS] = True
                    self.wumpus_count += 1

        for i in range(self.size):
            for j in range(self.size):
                if random() < pit_probability and not self.grid[i][j][CellContent.WUMPUS] \
                        and not self.grid[i][j][CellContent.GOLD] \
                        and not (i == 0 and j == 0):
                    self.grid[i][j][CellContent.PIT] = True

        for i in range(self.size):
            for j in range(self.size):
                if random() < pit_probability and not self.grid[i][j][CellContent.WUMPUS] \
                        and not self.grid[i][j][CellContent.GOLD] \
                        and not self.grid[i][j][CellContent.PIT] \
                        and not (i == 0 and j == 0):
                    self.grid[i][j][CellContent.OBSTACLE] = True

        return

    def kill_wumpus(self, coords) -> None:
        self.grid[coords[0]][coords[1]][CellContent.OBSTACLE] = True
        return

    def insert_wumpus(self, coords):
        self.grid[coords[0]][coords[1]][CellContent.WUMPUS] = True
        self.wumpus_count += 1

    def disp(self):
        rows = []
        for i in range(self.size):
            string = "|"
            for j in range(self.size):
                if self.grid[j][i][CellContent.GOLD]:
                    string += "G|"
                elif self.grid[j][i][CellContent.WUMPUS]:
                    string += "W|"
                elif self.grid[j][i][CellContent.PIT]:
                    string += "P|"
                elif self.grid[j][i][CellContent.OBSTACLE]:
                    string += "O|"
                else:
                    string += "_|"
            rows.append(string)
        rows.reverse()
        for row in rows:
            print(row)
