from typing import Tuple

from explorer import *
from knowledge_base import *


# Implementation of Explorer class which utilizes a knowledge base to make decisions.
class RationalExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)
        self.max_age = 500
        self.frontier: List[List[int]] = []
        self.knowledge_base: KnowledgeBase = KnowledgeBase(board.size)
        self.init_knowledge_base()

    # Core decision-making and executing method. Does the following:
    # - ages, and if necessary, dies.
    # - exits if explorer is dead or has gold.
    # - makes observations about sensations from adjacent cells.
    # - infers new facts from sensations.
    # - does some bookkeeping:
    # - - marks own location as safe
    # - - removes own location from frontier
    # - - adds new locations to frontier
    # - assigns a danger rating to each cell on the frontier. Cells with definite dangers are infinitely dangerous,
    #   cells with no dangers have zero danger, and cells with known gold have negative infinite danger.
    #   TODO: DESCRIBE DANGER RATING PROCESS (MIGHT CHANGE)
    # - chooses a target cell, which is the cell with lowest danger
    # - finds a path to that cell
    # - executes that path
    # -
    def act(self) -> None:
        if self.actions_taken > self.max_age:
            self.die()

        if self.is_dead or self.has_gold:
            return

        # make observations
        self.update_knowledge_base()

        # observe new facts
        self.knowledge_base.infer()

        # the cell i'm in is safe
        if self.location not in self.safe_cells:
            self.safe_cells.append(self.location)

        # the cell i'm in is not in the frontier
        if self.location in self.frontier:
            self.frontier.remove(self.location)

        # if adjacent cells weren't already in the frontier and aren't visited, add them
        for adjacent_cell in self.get_adjacent_cells():
            if adjacent_cell not in self.safe_cells and adjacent_cell not in self.frontier:
                self.frontier.append(adjacent_cell)

        # assign values to each frontier, create a queue of frontier cells in ascending order of danger
        queue: List[Tuple[List[int], float]] = []
        for cell in self.frontier:
            queue.append((cell, self.assign_danger_value(cell)))
        queue.sort(key=lambda x: x[1], reverse=True)

        target = tuple(queue.pop()[0])

        path = self.path(target)

        for step in path:
            if step == 'w':
                self.walk()
            elif step == 'l':
                self.turn(Direction.LEFT)
            elif step == 'r':
                self.turn(Direction.RIGHT)

        return

    # Modified implementation of parent class's walk method.
    # Calls parent class's walk method, then if the walk was unsuccessful, adds a bump sensation to the knowledege base.
    # Otherwise, adds a lack of bump sensation to the knowledge base.
    def walk(self) -> bool:
        bumped: bool = not super().walk()
        target_cell: List[int] = deepcopy(self.location)

        if self.facing == Facing.NORTH:
            target_cell[1] += 1
        elif self.facing == Facing.EAST:
            target_cell[0] += 1
        elif self.facing == Facing.SOUTH:
            target_cell[1] -= 1
        elif self.facing == Facing.WEST:
            target_cell[0] -= 1

        if bumped:
            self.knowledge_base.append(Clause([Sentence("bump", "bu", literals=target_cell, negated=False)]))

        return bumped

    def shoot(self) -> None:
        heard_scream = super().shoot()
        if heard_scream:
            scream_clause: Clause = Clause([Sentence("scream", "sc", literals=[self.location[0],
                                                                               self.location[1],
                                                                               self.facing],
                                                     negated=False)])
            self.knowledge_base.append(scream_clause)
        else:
            no_scream_clause: Clause = Clause([Sentence("scream", "sc", literals=[self.location[0],
                                                                                  self.location[1],
                                                                                  self.facing],
                                                        negated=True)])
            self.knowledge_base.append(no_scream_clause)
        return

    # Calls parent class's observe method, then adds sensations or lack thereof to the knowledge base.
    def update_knowledge_base(self) -> None:
        sensations: List[bool] = self.observe()

        # bleh ternary statements

        stench_sentence: Sentence = Sentence('stench', 's', literals=self.location, negated=False) \
            if sensations[Sensation.STENCH] \
            else Sentence('stench', 's', literals=self.location, negated=True)

        breeze_sentence: Sentence = Sentence('breeze', 'b', literals=self.location, negated=False) \
            if sensations[Sensation.BREEZE] \
            else Sentence('breeze', 'b', literals=self.location, negated=True)

        glimmer_sentence: Sentence = Sentence('glimmer', 'gl', literals=self.location, negated=False) \
            if sensations[Sensation.GLIMMER] \
            else Sentence('glimmer', 'gl', literals=self.location, negated=True)

        self.knowledge_base.append(Clause([breeze_sentence]))
        self.knowledge_base.append(Clause([stench_sentence]))
        self.knowledge_base.append(Clause([glimmer_sentence]))

        return

    def init_knowledge_base(self) -> None:
        '''
            key:
            s = smell, w = wumpus, b = breeze, p = pit, gl = glimmer, g = gold,
            bu = bump, o = obstacle, (x,y) is coordinate on the board
        '''

        rules: List[Clause] = []
        facts: List[Clause] = []

        '''
        Rule 1
        (Smell implies wumpus is in adjacent cell) converted to clause form is
        ~s(x,y) | [w(x+1, y) | w(x-1, y) | w(x, y+1) | w(x, y-1)
        '''
        rule1: Clause = Clause([Sentence("stench", "s", variables=["x", "y"], negated=True),
                                Sentence("wumpus", "w", variables=["x+1", 'y']),
                                Sentence("wumpus", "w", variables=["x-1", 'y']),
                                Sentence("wumpus", "w", variables=["x", 'y+1']),
                                Sentence("wumpus", "w", variables=["x", 'y-1'])])

        rules.append(rule1)

        '''
        Rule 2
        (Breeze implies pit in adjacent cell) converted to clause form is
        ~b(x,y) | [p(x+1, y) | p(x-1, y) | p(x, y+1) | p(x, y-1)]
        '''
        rule2: Clause = Clause([Sentence("breeze", "b", variables=["x", "y"], negated=True),
                                Sentence("pit", "p", variables=["x+1", 'y']),
                                Sentence("pit", "p", variables=["x-1", 'y']),
                                Sentence("pit", "p", variables=["x", 'y+1']),
                                Sentence("pit", "p", variables=["x", 'y-1'])])

        rules.append(rule2)

        """
        Rule 3
        (glimmer implies gold in adjacent cell) converted to clause form is
        ~gl(x,y) | [g(x+1, y) | g(x-1, y) | g(x, y+1) | g(x, y-1)]
        """

        rule3: Clause = Clause([Sentence("glimmer", "gl", variables=["x", "y"], negated=True),
                                Sentence("gold", "g", variables=["x+1", 'y']),
                                Sentence("gold", "g", variables=["x-1", 'y']),
                                Sentence("gold", "g", variables=["x", 'y+1']),
                                Sentence("gold", "g", variables=["x", 'y-1'])])

        rules.append(rule3)

        '''
        Rule 4
        (bump implies obstacle which mean you cant move in that direction anymore) converted to clause form is
        ~bu(x,y) | o(x,y)
        '''

        rule4: Clause = Clause([Sentence("bump", "bu", variables=["x", "y"], negated=True),
                                Sentence("obstacle", "o", variables=["x", "y"])])

        rules.append(rule4)

        """
        Rule 5
        (wumpus implies no pit)
        ~w(x, y) | ~p(x, y)
        """

        rule5: Clause = Clause([Sentence("wumpus", "w", variables=["x", "y"], negated=True),
                                Sentence("pit", "p", variables=["x", "y"], negated=True)])

        rules.append(rule5)

        """
        Rule 6
        (wumpus implies no gold)
        ~w(x, y) | ~g(x, y)
        """

        rule6: Clause = Clause([Sentence("wumpus", "w", variables=["x", "y"], negated=True),
                                Sentence("gold", "g", variables=["x", "y"], negated=True)])

        rules.append(rule6)

        """
        Rule 7
        (pit implies no wumpus)
        ~p(x, y) | ~w(x, y)
        """

        rule7: Clause = Clause([Sentence("wumpus", "w", variables=["x", "y"], negated=True),
                                Sentence("pit", "p", variables=["x", "y"], negated=True)])

        rules.append(rule7)

        """
        Rule 8
        (pit implies no gold)
        ~p(x, y) | ~g(x, y)
        """
        rule8: Clause = Clause([Sentence("gold", "g", variables=["x", "y"], negated=True),
                                Sentence("pit", "p", variables=["x", "y"], negated=True)])

        rules.append(rule8)

        """
        Rule 9
        (pit implies no obstacle)
        ~p(x, y) | ~o(x, y)
        """

        rule9: Clause = Clause([Sentence("obstacle", "o", variables=["x", "y"], negated=True),
                                Sentence("pit", "p", variables=["x", "y"], negated=True)])

        rules.append(rule9)

        """
        Rule 10
        (gold implies no obstacle)
        ~g(x, y) | ~o(x, y)
        """

        rule10: Clause = Clause([Sentence("obstacle", "o", variables=["x", "y"], negated=True),
                                 Sentence("gold", "g", variables=["x", "y"], negated=True)])

        rules.append(rule10)

        """
        Rule 11
        (no scream north implies no wumpus north)
        sc(x, y, 0) | ~w(x, y+1)
        """
        # TODO: DOES THIS WORK? LITERALS/VARIABLES MIXING??
        rule11: Clause = Clause([Sentence("scream", "sc", variables=["x", "y", "0"], negated=False),
                                 Sentence("wumpus", "w", variables=["x", "y+1"], negated=True)])

        rules.append(rule11)

        """
        Rule 12
        (no scream east implies no wumpus east)
        sc(x, y, 1) | ~w(x+1, y)
        """
        # TODO: DOES THIS WORK? LITERALS/VARIABLES MIXING??
        rule12: Clause = Clause([Sentence("scream", "sc", variables=["x", "y", "1"], negated=False),
                                 Sentence("wumpus", "w", variables=["x+1", "y"], negated=True)])

        rules.append(rule12)

        """
        Rule 13
        (no scream south implies no wumpus south)
        sc(x, y, 2) | ~w(x, y-1)
        """
        # TODO: DOES THIS WORK? LITERALS/VARIABLES MIXING??
        rule13: Clause = Clause([Sentence("scream", "sc", variables=["x", "y", "2"], negated=False),
                                 Sentence("wumpus", "w", variables=["x", "y-1"], negated=True)])

        rules.append(rule13)

        """
        Rule 14
        (no scream east implies no wumpus east)
        sc(x, y, 3) | ~w(x-1, y)
        """
        # TODO: DOES THIS WORK? LITERALS/VARIABLES MIXING??
        rule14: Clause = Clause([Sentence("scream", "sc", variables=["x", "y", "3"], negated=False),
                                 Sentence("wumpus", "w", variables=["x-1", "y"], negated=True)])

        rules.append(rule14)

        """
        Rule 15
        Scream to the north implies wumpus to the north. Depends on how many cells there are.
        These rules are generated algorithmically based on the size of the board.
        Example on a board of size 4, facing north:
        ~sc(x, 0, 0) | w(x, 1) | w(x, 2) | w(x, 3) | w(x, 4)
        ~sc(x, 1, 0) | w(x, 2) | w(x, 3) | w(x, 4)
        ~sc(x, 2, 0) | w(x, 3) | w(x, 4)
        ~sc(x, 3, 0) | w(x, 4)
        """
        for facing in Facing:

            if facing == Facing.NORTH:

                for offset in range(1, self.board.size, 1):
                    possible_targets: List[Sentence] = []
                    facing_sentence: Sentence = Sentence("scream", "sc", variables=["x", offset - 1, "0"], negated=True)
                    possible_targets.append(facing_sentence)
                    for i in range(0, self.board.size - offset, 1):
                        possible_target: Sentence = Sentence("wumpus", "w", variables=["x", offset + i])
                        possible_targets.append(possible_target)
                    target_clause: Clause = Clause(possible_targets)
                    rules.append(target_clause)

            elif facing == Facing.EAST:

                for offset in range(1, self.board.size, 1):
                    possible_targets: List[Sentence] = []
                    facing_sentence: Sentence = Sentence("scream", "sc", variables=[offset - 1, "y", "1"], negated=True)
                    possible_targets.append(facing_sentence)
                    for i in range(0, self.board.size - offset, 1):
                        possible_target: Sentence = Sentence("wumpus", "w", variables=[offset + i, "y"])
                        possible_targets.append(possible_target)
                    target_clause: Clause = Clause(possible_targets)
                    rules.append(target_clause)

            elif facing == Facing.SOUTH:

                for offset in range(1, self.board.size, 1):
                    possible_targets: List[Sentence] = []
                    facing_sentence: Sentence = Sentence("scream", "sc", variables=["x", 4 - (offset - 1), "2"],
                                                         negated=True)
                    possible_targets.append(facing_sentence)
                    for i in range(0, self.board.size - offset, 1):
                        possible_target: Sentence = Sentence("wumpus", "w", variables=["x", 4 - (offset + i)])
                        possible_targets.append(possible_target)
                    target_clause: Clause = Clause(possible_targets)
                    rules.append(target_clause)

            elif facing == Facing.WEST:

                for offset in range(1, self.board.size, 1):
                    possible_targets: List[Sentence] = []
                    facing_sentence: Sentence = Sentence("scream", "sc", variables=[4 - (offset - 1), "y", "3"],
                                                         negated=True)
                    possible_targets.append(facing_sentence)
                    for i in range(0, self.board.size - offset, 1):
                        possible_target: Sentence = Sentence("wumpus", "w", variables=[4 - (offset + i), "y"])
                        possible_targets.append(possible_target)
                    target_clause: Clause = Clause(possible_targets)
                    rules.append(target_clause)

        self.knowledge_base.set_rules(rules)

        """
        Rule 16
        There are no wumpuses, pits, or golds immediately off the board. There are obstacles immediately off the board.
        These facts are useful for generation of facts based off of sensations, allowing the inference engine to
        eliminate some possibilities immediately.
        """
        # content_types = [["wumpus", "w", True], ["pit", "p", True], ["gold", "g", True], ["obstacle", "o", False]]
        # for content_type in content_types:
        #     for i in range(self.board.size):
        #         for j in [-1, self.board.size]:
        #             vertical_clause: Clause = Clause(
        #                 [Sentence(content_type[0], content_type[1], literals=[i, j], negated=content_type[2])])
        #             horizontal_clause: Clause = Clause(
        #                 [Sentence(content_type[0], content_type[1], literals=[j, i], negated=content_type[2])])
        #             self.knowledge_base.append(vertical_clause)
        #             self.knowledge_base.append(horizontal_clause)

        self.knowledge_base.new_clauses_are_new = True

    def assign_danger_value(self, coords) -> float:

        obstacle_clause: Clause = Clause([Sentence("obstacle", 'o', literals=coords, negated=False)])
        for clause in self.knowledge_base.kb:
            if str(clause) == str(obstacle_clause):
                return float('inf')

        wumpus_danger: float = 0
        wumpus_safe_sentence: Sentence = Sentence("wumpus", "w", literals=coords, negated=True)
        wumpus_danger_sentence: Sentence = Sentence("wumpus", "w", literals=coords, negated=False)

        shortest_wumpus_clause_len: float = float('inf')
        for clause in self.knowledge_base.kb:
            if str(clause) == str(wumpus_safe_sentence):
                break
            for sentence in clause.sentences:
                if str(sentence) == str(wumpus_danger_sentence):
                    if len(clause) < shortest_wumpus_clause_len:
                        shortest_wumpus_clause_len = len(clause)

        if shortest_wumpus_clause_len == 1:
            wumpus_danger = float('inf')
        else:
            wumpus_danger = 1 / shortest_wumpus_clause_len

        pit_danger: float = 0
        pit_safe_sentence: Sentence = Sentence("pit", "p", literals=coords, negated=True)
        pit_danger_sentence: Sentence = Sentence("pit", "p", literals=coords, negated=False)

        shortest_pit_clause_len: float = float('inf')
        for clause in self.knowledge_base.kb:
            if str(clause) == str(pit_safe_sentence):
                break
            for sentence in clause.sentences:
                if str(sentence) == str(pit_danger_sentence):
                    if len(clause) < shortest_pit_clause_len:
                        shortest_pit_clause_len = len(clause)

        if shortest_pit_clause_len == 1:
            pit_danger = float('inf')
        else:
            pit_danger = 1 / shortest_pit_clause_len

        gold_danger: float = 0
        gold_safe_sentence: Sentence = Sentence("gold", "g", literals=coords, negated=True)
        gold_danger_sentence: Sentence = Sentence("gold", "g", literals=coords, negated=False)

        shortest_gold_clause_len: float = float('inf')
        for clause in self.knowledge_base.kb:
            if str(clause) == str(gold_safe_sentence):
                break
            for sentence in clause.sentences:
                if str(sentence) == str(gold_danger_sentence):
                    if len(clause) < shortest_gold_clause_len:
                        shortest_gold_clause_len = len(clause)

        if shortest_gold_clause_len == 1:
            gold_danger = float('inf')
        else:
            gold_danger = 1 / shortest_gold_clause_len

        return wumpus_danger + pit_danger - (0.1 * gold_danger)

    def __str__(self) -> str:
        string: str = ""
        rows: List[str] = self.disp(dunder_str=True)
        for row in rows:
            string += row
            string += "\n"
        return string

    def disp(self, *, dunder_str: bool = False) -> List[str]:
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
                    danger = self.assign_danger_value([j, i])
                    if [j, i] in self.safe_cells:
                        string += "S|"
                    elif danger == 0:
                        string += '0|'
                    elif danger > 0:
                        string += 'X|'
                    else:
                        string += '0|'
            rows.append(string)
        rows.reverse()
        if not dunder_str:
            for row in rows:
                print(row)
        return rows
