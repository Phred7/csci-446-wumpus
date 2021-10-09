import numpy

import board
from explorer import *

class VisitState(IntEnum):
    UNKNOWN = 0
    VISITED = 1
    SAFE_FRONTIER = 2
    DANGEROUS_FRONTIER = 3

class ReactiveExplorer(Explorer):

    def __init__(self, board: Board):
        self.visitMap = numpy.full((board.size, board.size), 0)
        self.age = 0
        super().__init__(board, False)

    def act(self) -> None:
        x = self.location[0]
        y = self.location[1]

        if self.board.grid[x, y][CellValue.GOLD]:
            self.hasGold = True
            return

        if self.age > 10000 or self.board.grid[x, y][CellValue.WUMPUS] or self.board.grid[x, y][CellValue.PIT]:
            self.die()
            return
        self.age += 1

        self.visitMap[x][y] = VisitState.VISITED
        adjacentCells = []

        if x > 0:
            adjacentCells.append([x - 1, y])
        if x < self.board.size - 1:
            adjacentCells.append([x + 1, y])
        if y > 0:
            adjacentCells.append([x, y - 1])
        if y < self.board.size - 1:
            adjacentCells.append([x, y + 1])

        sensations = self.observe()

        for i, j in adjacentCells:
            if not self.visitMap[i, j] == VisitState.VISITED \
                    and not self.visitMap[i, j] == VisitState.SAFE_FRONTIER:
                if sensations[Sensation.STENCH] or sensations[Sensation.BREEZE]:
                    self.visitMap[i, j] = VisitState.DANGEROUS_FRONTIER
                else:
                    self.visitMap[i, j] = VisitState.SAFE_FRONTIER

        for i in range(len(self.visitMap)):
            for j in range(len(self.visitMap)):
                if self.visitMap[i, j] == VisitState.SAFE_FRONTIER:
                    self.path([i, j])
                    return
        for i in range(len(self.visitMap)):
            for j in range(len(self.visitMap)):
                if self.visitMap[i, j] == VisitState.DANGEROUS_FRONTIER:
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
                    state = self.visitMap[j, i]
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




