from random import randint
from random import random
from typing import List

import numpy as np
from copy import deepcopy
from enums import *


class Board:

    def __init__(self, size: int = 5, ) -> None:
        self.grid = np.zeros([size, size, len(CellContent)],
                             dtype=bool)
        self.size: int = size
        self.wumpus_count: int = 0

    def generate_board(self, wumpus_probability: float = 0.05, pit_probability: float = 0.05,
                       obstacle_probability: float = 0.05) -> None:
        gold_x: int = 0
        gold_y: int = 0

        while gold_x == 0 and gold_y == 0:
            gold_x = randint(0, self.size - 1)
            gold_y = randint(0, self.size - 1)
        self.grid[gold_x][gold_y][CellContent.GOLD] = True

        for i in range(self.size):
            for j in range(self.size):
                if random() < wumpus_probability and not self.grid[i][j][CellContent.GOLD] and not (i == 0 and j == 0):
                    if self.path_to_gold_exists([i, j], (gold_x, gold_y)):
                        self.grid[i][j][CellContent.WUMPUS] = True
                        self.wumpus_count += 1

        for i in range(self.size):
            for j in range(self.size):
                if random() < pit_probability \
                        and not self.grid[i][j][CellContent.WUMPUS] \
                        and not self.grid[i][j][CellContent.GOLD] \
                        and not (i == 0 and j == 0):
                    if self.path_to_gold_exists([i, j], (gold_x, gold_y)):
                        self.grid[i][j][CellContent.PIT] = True

        for i in range(self.size):
            for j in range(self.size):
                if random() < obstacle_probability \
                        and not self.grid[i][j][CellContent.WUMPUS] \
                        and not self.grid[i][j][CellContent.GOLD] \
                        and not self.grid[i][j][CellContent.PIT] \
                        and not (i == 0 and j == 0):
                    if self.path_to_gold_exists([i, j], (gold_x, gold_y)):
                        self.grid[i][j][CellContent.OBSTACLE] = True

        return

    def kill_wumpus(self, coords) -> None:
        self.grid[coords[0]][coords[1]][CellContent.OBSTACLE] = True
        return

    def insert_wumpus(self, coords):
        self.grid[coords[0]][coords[1]][CellContent.WUMPUS] = True
        self.wumpus_count += 1

    def __str__(self) -> str:
        string: str = ""
        rows: List[str] = self.disp(dunder_str=True)
        for row in rows:
            string += row
            string += "\n"
        return string

    def disp(self, *, dunder_str: bool = False) -> List[str]:
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
        if not dunder_str:
            for row in rows:
                print(row)
        return rows

    def path_to_gold_exists(self, coords, gold_coords) -> bool:
        def dfs(loc, target, marked, edges) -> bool:
            marked.append(loc)
            for v in edges[loc]:
                if v not in marked:
                    if v == target:
                        return True
                    else:
                        if dfs(v, target, marked, edges):
                            return True
            return False

        marked = []
        edges = {}
        grid = deepcopy(self.grid)
        grid[coords[0]][coords[1]][CellContent.WUMPUS] = True

        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                targets = []
                edges[(i, j)] = []
                if not j == len(self.grid) - 1:
                    targets.append((i, j + 1))

                if not j == 0:
                    targets.append((i, j - 1))

                if not i == len(self.grid) - 1:
                    targets.append((i + 1, j))

                if not i == 0:
                    targets.append((i - 1, j))

                for target in targets:

                    if (not grid[target[0]][target[1]][CellContent.WUMPUS]) \
                            and (not grid[target[0]][target[1]][CellContent.PIT]) \
                            and (not grid[target[0]][target[1]][CellContent.OBSTACLE]):
                        edges[(i, j)].append(target)

        return dfs((0, 0), gold_coords, marked, edges)
