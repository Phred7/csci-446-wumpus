from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List
from typing import Tuple

from board import *


class Explorer:

    def __init__(self, board: Board, messages=False):
        self.actions_taken: int = 0
        self.facing: Facing = Facing.NORTH
        self.location: List[int, int] = [0, 0]
        self.is_dead: bool = False
        self.board: Board = deepcopy(board)
        self.display_messages: bool = messages
        self.arrows: int = board.wumpus_count
        self.has_gold: bool = False
        self.generate_graph()
        return

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
    def act(self) -> None:
        raise NotImplementedError

    # METHODS USED FOR PATHFINDING THRU GRAPH REPRESENTING BOARD

    @abstractmethod
    def get_unsafe_cells(self) -> List[List[int]]:
        raise NotImplementedError

    # this method returns a list of vertices, 4 for each cell, which correspond to a cell and a facing.
    # it also returns an adjacency matrix of strings.
    def generate_graph(self) -> None:
        # generate list of vertices
        V: List[Tuple[List[int], Facing]] = []
        for i in range(self.board.size):
            for j in range(self.board.size):
                for k in Facing:
                    V.append(([i, j], k))

        # generate list of edges. string representation: all edges have the same weight, 'l', 'r', 'w' indicate
        # movement options, 'n' represents 'there is no edge between these two'
        # dictionary where key is tuple of origin -> destination, value is movement option

        E = {}

        for v_1 in V:
            for v_2 in V:
                key = (v_1, v_2)

                # quality of life for easy access to x, y and facing
                x_1 = v_1[0][0]
                y_1 = v_1[0][1]
                x_2 = v_2[0][0]
                y_2 = v_2[0][1]
                f_1 = v_1[1]
                f_2 = v_2[1]

                # two vertices are in the same cell
                if v_1[0] == v_2[0]:
                    if (f_1 == Facing.NORTH and f_2 == Facing.EAST) \
                            or (f_1 == Facing.EAST and f_2 == Facing.SOUTH) \
                            or (f_1 == Facing.SOUTH and f_2 == Facing.WEST) \
                            or (f_1 == Facing.WEST and f_2 == Facing.NORTH):

                        E[key] = 'r'

                    elif (f_1 == Facing.NORTH and f_2 == Facing.WEST) \
                            or (f_1 == Facing.WEST and f_2 == Facing.SOUTH) \
                            or (f_1 == Facing.SOUTH and f_2 == Facing.EAST) \
                            or (f_1 == Facing.EAST and f_2 == Facing.NORTH):

                        E[key] = 'l'

                    else:
                        E[key] = 'n'

                # if v_1 is to the left of v_2
                elif (x_1 == x_2 - 1) and (y_1 == y_2) and (f_1 == Facing.EAST) and (f_2 == Facing.EAST):
                    E[key] = 'w'

                # if v_1 is to the right of v_2
                elif (x_1 == x_2 + 1) and (y_1 == y_2) and (f_1 == Facing.WEST) and (f_2 == Facing.WEST):
                    E[key] = 'w'

                # if v_1 is above v_2
                elif (x_1 == x_2) and (y_1 == y_2 + 1) and (f_1 == Facing.SOUTH) and (f_2 == Facing.SOUTH):
                    E[key] = 'w'

                # if v_1 is below v_2
                elif (x_1 == x_2) and (y_1 == y_2 - 1) and (f_1 == Facing.NORTH) and (f_2 == Facing.NORTH):
                    E[key] = 'w'

                # no relation between v_1 and v_2
                else:
                    E[key] = 'n'

        self.G = (V, E)
        return

    # some pathfinding algorithm, idk
    def path(self, coords: List[int]) -> List[str]:
        V, E = self.G
        goals: List[Tuple[List[int], Facing]] = []
        for facing in Facing:
            goals.append((coords, facing))



        self.location = coords

        return

    def depth_first_search(self, coords: List[int]) -> List[str]:
