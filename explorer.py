from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List
from typing import Tuple

from board import *


# Abstract class representing an explorer. Has methods and attributes used by both rational and reactive explorer.
# An explorer is initialized with the board it lives on. It also has quality-of-life output messages for debugging,
# which are disabled by default.

class Explorer:

    # Initializes variables for explorer class.
    def __init__(self, board: Board, messages=False):
        self.max_age = 100
        self.actions_taken: int = 0
        self.facing: Facing = Facing.NORTH
        self.location: List[int, int] = [0, 0]
        self.is_dead: bool = False
        self.board: Board = deepcopy(board)
        self.display_messages: bool = messages
        self.arrows: int = board.wumpus_count
        self.has_gold: bool = False
        self.generate_graph()
        self.safe_cells: List[List[int, int]] = []
        self.safe_cells.append(self.location)
        self.history = [self.location]
        return

    # Gets a list of cells adjacent to the explorer, i.e. if explorer is in (x, y) returns (x+1, y), (x-1, y), etc.
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

    # Turns the explorer. The explorer has an enumerated attribute called facing,
    # which corresponds to a cardinal direction.
    # This method takes an enumerated value, called Direction, corresponding to left or right.
    # This method has no return, and changes the facing of the explorer.
    def turn(self, direction: Direction) -> None:
        self.history.append('t')
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

    # This method moves the explorer across the board. When called, there are two possibilities:
    # 1) The explorer moves one cell in the direction it is facing. Returns true in this case.
    # 2) The explorer attempts to walk off the board or into an obstacle. Returns false in this case.
    # This method also resolves the result of walking: if the explorer walks into a cell with a wumpus or pit,
    # the explorer dies. If the explorer walks into a cell with gold, the explorer grabs the gold.
    def walk(self) -> bool:
        self.history.append('w')
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
                or target_cell[1] > self.board.size - 1 \
                or self.board.grid[target_cell[0]][target_cell[1]][CellContent.OBSTACLE]:
            hit_something = True

        if hit_something:
            if self.display_messages:
                print("You have bumped into something.")
            return False
        else:
            self.location = target_cell

        self.history.append(self.location)

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

    # This method shoots an arrow in the direction the explorer is facing. The arrow movse in one direction through
    # cells until it hits the edge of the board, an obstacle, or a wumpus. If the arrow hits a wumpus, the wumpus
    # screams and dies. In this case the method returns True. Otherwise the method returns False.
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

    # This method gains observations about adjacent cells. If any adjacent cell contains a wumpus, pit, or gold,
    # then the explorer will observe a stench, breeze, or glimmer. These values are enumerated as Sensation.
    # Returns a list of booleans; Sensation values correspond to the index of the boolean representing whether that
    # Sensation was observed.
    def observe(self) -> List[bool]:
        adjacent_cells = self.get_adjacent_cells()

        sensations: List[bool] = list(np.full(len(Sensation), False))
        for adj in adjacent_cells:
            x = adj[0]
            y = adj[1]
            if self.board.grid[x][y][CellContent.WUMPUS]:
                sensations[Sensation.STENCH] = True
            if self.board.grid[x][y][CellContent.PIT]:
                sensations[Sensation.BREEZE] = True
            if self.board.grid[x][y][CellContent.GOLD]:
                sensations[Sensation.GLIMMER] = True

        if self.display_messages:
            if sensations[Sensation.STENCH]:
                print("A terrible stench fills your nostrils.")
            if sensations[Sensation.BREEZE]:
                print("A breeze ruffles your hair.")
            if sensations[Sensation.GLIMMER]:
                print("You see a glimmer in the darkness.")

        return sensations

    # This method kills the explorer. A dead explorer cannot act.
    def die(self) -> None:
        self.is_dead = True
        return

    # This method picks up the gold. An explorer with gold cannot act.
    def escape(self) -> None:
        self.has_gold = True
        return

    # This method displays the board and the explorer's position and facing. Does not display any value for any
    # cell except the explorer's location.
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

    # Abstract method implemented by child classes. This is the core method of the Explorer class, and how it chooses
    # what to do at any given time.
    @abstractmethod
    def act(self) -> None:
        raise NotImplementedError

    # All following methods are used for pathfinding through the board.

    # This method creates a directed graph corresponding to the explorer's movement about the board.
    # It creates a list of vertices, 4 for each cell, which correspond to a cell and a facing.
    # For example, the cell (1, 1) would correspond to four vertices:
    # - (1, 1) North
    # - (1, 1) East
    # - (1, 1) South
    # - (1, 1) West
    # It also creates an adjacency matrix of strings representing what movements link the vertices.
    # For example, (1, 1) North is connected to (1, 1) West by turning left, (1, 1) East by turning right, and
    # (1, 2) North by walking.
    def generate_graph(self) -> None:
        # generate list of vertices
        V: List[Tuple[Tuple[int], Facing]] = []
        for i in range(self.board.size):
            for j in range(self.board.size):
                for k in Facing:
                    V.append(((i, j), k))

        # generate list of edges. string representation: all edges have the same weight, 'l', 'r', 'w' indicate
        # movement options, 'n' represents 'there is no edge between these two'
        # dictionary where key is tuple of origin -> destination, value is movement option

        E = {}

        for v_1 in V:
            for v_2 in V:
                key: Tuple[Tuple[Tuple[int], Facing], Tuple[Tuple[int], Facing]] = (v_1, v_2)
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

        self.G = (V, E)
        return

    # TODO description
    def path(self, target: Tuple[int]) -> List[str]:
        V, E = self.G

        # we path to the node representing facing north in the target cell, then remove any excess turns
        path = self.breadth_first_search((target, Facing.NORTH), E)
        if len(path) == 0:
            return path
        while path[-1] != 'w':
            path = path[:-1]
        return path

    # This method implements breadth first search through the graph representing the board.
    # It takes as input a target cell. It then executes a breadth first search beginning at the explorer's current
    # location and ending at the target location, building a list of predecessor vertices for each vertex.
    # The search only allows movement through cells that are known to be safe or into the target cell.
    # Upon finding a predecessor vertex for the target, a list consisting of 'w', 'l', and 'r' strings
    # corresponding to walking and turning actions is assembled and returned.
    # By default, this method searches for a path to the northward facing in the target cell, but eliminates excess
    # turning actions at the end of the path before returning it.
    def breadth_first_search(self, target: Tuple[Tuple[int], Facing], E) -> List[str]:
        predecessors = {}

        s = (tuple(self.location), self.facing)

        queue = []
        queue.append(s)

        safe_cells_with_facings: List[Tuple[Tuple[int], Facing]] = []
        for cell in self.safe_cells:
            for facing in Facing:
                safe_cells_with_facings.append((tuple(cell), facing))

        while queue:
            s = queue.pop(0)

            if s == target:
                path = []
                step = s
                while step != (tuple(self.location), self.facing):
                    path.append(E[(predecessors[step], step)])
                    step = predecessors[step]
                path.reverse()
                return path
            for edge in E.keys():
                if edge[0] == s \
                        and edge[1] not in predecessors.keys() \
                        and edge[1] != (tuple(self.location), self.facing) \
                        and (edge[1] in safe_cells_with_facings or edge[1][0] == target[0]):
                    predecessors[edge[1]] = s
                    queue.append(edge[1])
        self.disp()
        self.board.disp()
        print(target[0])
        raise IOError("Unable to find a path.")
        pass
