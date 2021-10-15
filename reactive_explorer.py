import numpy

from explorer import *





class ReactiveExplorer(Explorer):

    def __init__(self, _board: Board):
        super().__init__(_board)
        self.visit_map = numpy.full((_board.size, _board.size), 0)
        self.max_age = 500
        super().__init__(_board, False)

    def act(self) -> None:
        x = self.location[0]
        y = self.location[1]

        if self.actions_taken > self.max_age:
            self.die()

        self.visit_map[x][y] = VisitState.VISITED
        self.safe_cells.append(self.location)

        adjacent_cells = self.get_adjacent_cells()

        sensations = self.observe()
        # if sensations[Sensation.STENCH]:
        #     if self.arrows > 0:
        #         scream = self.shoot()
        #         if scream:
        #             if self.facing == Facing.NORTH:
        #                 self.visit_map[self.location[0]][self.location[1] + 1] = VisitState.SAFE_FRONTIER
        #             elif self.facing == Facing.EAST:
        #                 self.visit_map[self.location[0] + 1][self.location[1]] = VisitState.SAFE_FRONTIER
        #             elif self.facing == Facing.SOUTH:
        #                 self.visit_map[self.location[0]][self.location[1] - 1] = VisitState.SAFE_FRONTIER
        #             elif self.facing == Facing.WEST:
        #                 self.visit_map[self.location[0] - 1][self.location[1]] = VisitState.SAFE_FRONTIER



        for i, j in adjacent_cells:
            if not self.visit_map[i, j] == VisitState.VISITED \
                    and not self.visit_map[i, j] == VisitState.SAFE_FRONTIER\
                    and not self.visit_map[i, j] == VisitState.IMPASSABLE:
                if sensations[Sensation.STENCH] or sensations[Sensation.BREEZE]:
                    self.visit_map[i, j] = VisitState.DANGEROUS_FRONTIER
                elif sensations[Sensation.GLIMMER]:
                    self.visit_map[i, j] = VisitState.ATTRACTIVE_FRONTIER
                else:
                    self.visit_map[i, j] = VisitState.SAFE_FRONTIER

        # self.disp()


        target: Tuple[int, int] = None
        for i in range(len(self.visit_map)):
            for j in range(len(self.visit_map)):
                if self.visit_map[i, j] == VisitState.ATTRACTIVE_FRONTIER:
                    if target == None:
                        target = (i, j)

        for i in range(len(self.visit_map)):
            for j in range(len(self.visit_map)):
                if self.visit_map[i, j] == VisitState.SAFE_FRONTIER:
                    if target == None:
                        target = (i, j)

        for i in range(len(self.visit_map)):
            for j in range(len(self.visit_map)):
                if self.visit_map[i, j] == VisitState.DANGEROUS_FRONTIER:
                    if target == None:
                        target = (i, j)
        if target == None:
            self.die()
            return
        path = self.path(target)

        for step in path:
            if step == 'w':
                successfully_walked = self.walk()
                if not successfully_walked:
                    self.visit_map[target[0]][target[1]] = VisitState.IMPASSABLE
            elif step == 'l':
                self.turn(Direction.LEFT)
            elif step == 'r':
                self.turn(Direction.RIGHT)


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
                    elif state == VisitState.IMPASSABLE:
                        string += "I|"
                    elif state == VisitState.ATTRACTIVE_FRONTIER:
                        string += "A|"
            rows.append(string)
        rows.reverse()
        for row in rows:
            print(row)
