from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Tuple
from typing import List

from board import *


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class Facing(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Explorer:

    def __init__(self, board: Board, messages=True):
        self.actions_taken: int = 0
        self.facing: Facing = Facing.NORTH
        self.location: List[int, int] = [0, 0]
        self.is_dead: bool = False
        self.board: Board = deepcopy(board)
        self.display_messages: bool = messages
        self.arrows: int = board.wumpus_count
        self.has_gold: bool = False

    def get_adjacent_cells(self) -> List[List[int]]:
        x = self.location[0]
        y = self.location[1]
        adjacent_cells = []

        if x > 0:
            adjacent_cells.append([x - 1, y])
        if x < self.board.size - 1:
            adjacent_cells.append([x + 1, y])
        if y > 0:
            adjacent_cells.append([x, y - 1])
        if y < self.board.size - 1:
            adjacent_cells.append([x, y + 1])
        return adjacent_cells

    def turn(self, direction: Direction) -> None:
        self.actions_taken += 1
        if direction == Direction.RIGHT:
            if self.facing == Facing.NORTH:
                self.facing = Facing.EAST
            elif self.facing == Facing.EAST:
                self.facing = Facing.SOUTH
            elif self.facing == Facing.SOUTH:
                self.facing = Facing.WEST
            elif self.facing == Facing.WEST:
                self.facing = Facing.NORTH

        elif direction == Direction.LEFT:
            if self.facing == Facing.NORTH:
                self.facing = Facing.WEST
            elif self.facing == Facing.WEST:
                self.facing = Facing.SOUTH
            elif self.facing == Facing.SOUTH:
                self.facing = Facing.EAST
            elif self.facing == Facing.EAST:
                self.facing = Facing.NORTH

        return

    # TODO: DOES NOT ACCOUNT FOR BUMPING OBSTACLE IN BOARD, ONLY EDGES
    def walk(self) -> bool:
        self.actions_taken += 1
        hit_something: bool = False
        target_cell: List[int] = deepcopy(self.location)

        if self.facing == Facing.NORTH:
            target_cell[1] += 1
        elif self.facing == Facing.EAST:
            target_cell[0] += 1
        elif self.facing == Facing.SOUTH:
            target_cell[1] -= 1
        elif self.facing == Facing.WEST:
            target_cell[0] -= 1

        if target_cell[0] < 0 \
            or target_cell[1] < 0 \
               or target_cell[0] > self.board.size - 1 \
               or target_cell[0] > self.board.size - 1 \
               or target_cell[1] > self.board.size - 1 \
                or self.board.grid[target_cell[0]][target_cell[1]][CellContent.OBSTACLE]:
            hit_something = True

        if hit_something:
            if self.display_messages:
                print("You have bumped into something.")
        else:
            self.location = target_cell

        x = self.location[0]
        y = self.location[1]

        if self.board.grid[x][y][CellContent.WUMPUS]:
            if self.display_messages:
                print("You have been eaten by a wumpus.")
            self.die()
        elif self.board.grid[x][y][CellContent.PIT]:
            if self.display_messages:
                print("You have fallen into a pit.")
            self.die()
        elif self.board.grid[x][y][CellContent.GOLD]:
            if self.display_messages:
                print("You have found gold!")
            self.escape()
        else:
            return True
        return False

    def shoot(self) -> bool:
        if self.arrows == 0:
            if self.display_messages:
                print("Your quiver is empty.")
            return False
        else:
            if self.display_messages:
                print("You have", self.arrows, "arrows left.")
        x = self.location[0]
        y = self.location[1]
        targets = []
        if self.facing == Facing.NORTH:
            for i in range(y + 1, self.board.size, 1):
                targets.append([x, i])
        elif self.facing == Facing.EAST:
            for i in range(x + 1, self.board.size, 1):
                targets.append([i, y])
        elif self.facing == Facing.SOUTH:
            for i in range(y - 1, -1, -1):
                targets.append([x, i])
        elif self.facing == Facing.WEST:
            for i in range(x - 1, -1, -1):
                targets.append([i, y])

        if self.display_messages:
            print("Targets are", targets)
        for target in targets:
            if self.board.grid[target[0]][target[1]][CellContent.WUMPUS]:
                self.board.kill_wumpus(target)
                if self.display_messages:
                    print("A scream rings out through the darkness!")
                return True
        if self.display_messages:
            print("The arrow disappears into the darkness.")
        return False

    def observe(self):
        sensations = self.board.get_observations(self.location)
        if self.display_messages:
            if sensations[Sensation.STENCH]:
                print("A terrible stench fills your nostrils.")
            if sensations[Sensation.BREEZE]:
                print("A breeze ruffles your hair.")
            if sensations[Sensation.GLIMMER]:
                print("You see a glimmer in the darkness.")
        return sensations

    def die(self) -> None:
        self.is_dead = True
        return

    def escape(self) -> None:
        self.has_gold = True
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
                    string += "_|"
            rows.append(string)
        rows.reverse()
        for row in rows:
            print(row)

    @abstractmethod
    def act(self) -> bool:
        raise NotImplementedError

    # TODO: IMPLEMENT PATHFINDING. GOTO COORDS (X, Y), THROUGH SAFE THINGS IF POSSIBLE... Wouldn't this defeat the purpose of using a KB? I guess Im confused as to what this method would be doing
    def path(self, coords):
        self.location = coords
        return
