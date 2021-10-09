import numpy

import board
from typing import List

from explorer import *


class VisitState(Enum):
    UNKNOWN = 0
    VISITED = 1
    SAFE_FRONTIER = 2
    DANGEROUS_FRONTIER = 3


class ReactiveExplorer(Explorer):

    def __init__(self, _board: Board):
        super().__init__(_board)
        self.visit_map = numpy.full((_board.size, _board.size), 0)
        self.age = 0
        super().__init__(_board, False)

    def act(self) -> None:
        x = self.location[0]
        y = self.location[1]

        if self.board.grid[x, y][CellValue.GOLD]:
            self.has_gold = True
            return

        if self.age > 10000 or self.board.grid[x, y][CellValue.WUMPUS] or self.board.grid[x, y][CellValue.PIT]:
            self.die()
            return
        self.age += 1

        self.visit_map[x][y] = VisitState.VISITED
        adjacent_cells = []

        if x > 0:
            adjacent_cells.append([x - 1, y])
        if x < self.board.size - 1:
            adjacent_cells.append([x + 1, y])
        if y > 0:
            adjacent_cells.append([x, y - 1])
        if y < self.board.size - 1:
            adjacent_cells.append([x, y + 1])

        sensations = self.observe()

        for i, j in adjacent_cells:
            if not self.visit_map[i, j] == VisitState.VISITED \
                    and not self.visit_map[i, j] == VisitState.SAFE_FRONTIER:
                if sensations[Sensation.STENCH] or sensations[Sensation.BREEZE]:
                    self.visit_map[i, j] = VisitState.DANGEROUS_FRONTIER
                else:
                    self.visit_map[i, j] = VisitState.SAFE_FRONTIER

        for i in range(len(self.visit_map)):
            for j in range(len(self.visit_map)):
                if self.visit_map[i, j] == VisitState.SAFE_FRONTIER:
                    self.path([i, j])
                    return
        for i in range(len(self.visit_map)):
            for j in range(len(self.visit_map)):
                if self.visit_map[i, j] == VisitState.DANGEROUS_FRONTIER:
                    self.path([i, j])
                    return

    def disp(self):
        rows = []
        for i in range(self.board.size):
            string = "|"
            for j in range(self.board.size):
                if i == self.location[1] and j == self.location[0]:
                    if self.facing == Facing.NORTH:
                        string += "^|"
                    elif self.facing == Facing.EAST:
                        string += ">|"
                    elif self.facing == Facing.SOUTH:
                        string += "v|"
                    elif self.facing == Facing.WEST:
                        string += "<|"
                else:
                    state = self.visit_map[j, i]
                    if state == VisitState.VISITED:
                        string += "V|"
                    elif state == VisitState.SAFE_FRONTIER:
                        string += "F|"
                    elif state == VisitState.DANGEROUS_FRONTIER:
                        string += "D|"
                    elif state == VisitState.UNKNOWN:
                        string += "_|"
            rows.append(string)
        rows.reverse()
        for row in rows:
            print(row)
