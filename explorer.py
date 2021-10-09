from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Tuple

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
        self.location: Tuple[int, int] = (0, 0)
        self.is_dead: bool = False
        self.board: Board = deepcopy(board)
        self.display_messages: bool = messages
        self.arrows: int = board.wumpus_count
        self.has_gold: bool = False

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
        if self.facing == Facing.NORTH:
            if self.location[1] == self.board.size - 1:
                hit_something = True
            else:
                self.location[1] += 1
        elif self.facing == Facing.EAST:
            if self.location[0] == self.board.size - 1:
                hit_something = True
            else:
                self.location[0] += 1
        elif self.facing == Facing.SOUTH:
            if self.location[1] == 0:
                hit_something = True
            else:
                self.location[1] -= 1
        elif self.facing == Facing.WEST:
            if self.location[0] == 0:
                hit_something = True
            else:
                self.location[0] -= 1
        if hit_something:
            if self.display_messages:
                print("You have bumped into something.")
        elif self.board.grid[self.location[0]][self.location[1]][CellValue.WUMPUS]:
            if self.display_messages:
                print("You have been eaten by a wumpus.")
            self.die()
        elif self.board.grid[self.location[0]][self.location[1]][CellValue.PIT]:
            if self.display_messages:
                print("You have fallen into a pit.")
            self.die()
        elif self.board.grid[self.location[0]][self.location[1]][CellValue.GOLD]:
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
            if self.board.grid[target[0]][target[1]][CellValue.WUMPUS]:
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
