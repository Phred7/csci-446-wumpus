from typing import Tuple

from explorer import *
from knowledge_base import *

# Implementation of Explorer class which utilizes a knowledge base to make decisions.
class RationalExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)
        self.frontier: List[List[int]] = []
        self.knowledge_base: KnowledgeBase = KnowledgeBase()
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
        if self.actions_taken > 100:
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
        queue: List[Tuple[List[int], float]]  = []
        for cell in self.frontier:
            queue.append((cell, self.assign_danger_value(cell)))
        queue.sort(key = lambda x : x[1], reverse=True)



        target = tuple(queue.pop()[0])
        print("Target is", target)
        path = self.path(target)

        for step in path:
            if step == 'w':
                self.walk()
            elif step == 'l':
                self.turn(Direction.LEFT)
            elif step == 'r':
                self.turn(Direction.RIGHT)

        #print("Ending action.")
        return

    # Modified implementation of parent class's walk method.
    # Calls parent class's walk method, then if the walk was unsuccessful, adds a bump sensation to the knowledege base.
    # Otherwise, adds a lack of bump sensation to the knowledge base.
    def walk(self) -> bool:
        bumped: bool = super().walk()
        target_cell: List[int] = deepcopy(self.location)

        if self.facing == Facing.NORTH:
            target_cell[1] += 1
        elif self.facing == Facing.EAST:
            target_cell[0] += 1
        elif self.facing == Facing.SOUTH:
            target_cell[1] -= 1
        elif self.facing == Facing.WEST:
            target_cell[0] -= 1
        bump_clause: Clause = Clause([Sentence("bump", "bu", literals=target_cell, negated=False)]) \
            if bumped \
            else Clause([Sentence("bump", "bu", literals=target_cell, negated=True)])
        self.knowledge_base.append(bump_clause)
        return bumped

    # Calls parent class's observe method, then adds sensations or lack thereof to the knowledge base.
    def update_knowledge_base(self) -> None:
        sensations: List[bool] = self.observe()

        # bleh ternary statements

        stench_sentence: Sentence = Sentence('stench', 's', literals = self.location, negated=False) \
            if sensations[Sensation.STENCH] \
            else Sentence('stench', 's', literals = self.location, negated=True)

        breeze_sentence: Sentence = Sentence('breeze', 'b', literals=self.location, negated=False) \
            if sensations[Sensation.BREEZE] \
            else Sentence('breeze', 'b', literals=self.location, negated=True)

        glimmer_sentence: Sentence =  Sentence('glimmer', 'gl', literals = self.location, negated=False) \
            if sensations[Sensation.GLIMMER] \
            else Sentence('glimmer', 'gl', literals = self.location, negated=True)

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


        '''
        Rule 1
        (Smell implies wumpus is in adjacent cell) converted to clause form is
        ~s(x,y) | [w(x+1, y) | w(x-1, y) | w(x, y+1) | w(x, y-1)]
        '''

        r1_s1: Sentence = Sentence("stench", "s", variables = ["x", "y"], negated = True)
        r1_s2: Sentence = Sentence("wumpus", "w", variables = ["x+1", 'y'])
        r1_s3: Sentence = Sentence("wumpus", "w", variables=["x-1", 'y'])
        r1_s4: Sentence = Sentence("wumpus", "w", variables=["x", 'y+1'])
        r1_s5: Sentence = Sentence("wumpus", "w", variables=["x", 'y-1'])
        rule1: Clause = Clause([r1_s1, r1_s2, r1_s3, r1_s4, r1_s5])

        '''
        Rule 2
        (Breeze implies pit in adjacent cell) converted to clause form is
        ~b(x,y) | [p(x+1, y) | p(x-1, y) | p(x, y+1) | p(x, y-1)]
        '''

        r2_s1: Sentence = Sentence("breeze", "b", variables=["x", "y"], negated=True)
        r2_s2: Sentence = Sentence("pit", "p", variables=["x+1", 'y'])
        r2_s3: Sentence = Sentence("pit", "p", variables=["x-1", 'y'])
        r2_s4: Sentence = Sentence("pit", "p", variables=["x", 'y+1'])
        r2_s5: Sentence = Sentence("pit", "p", variables=["x", 'y-1'])
        rule2: Clause = Clause([r2_s1, r2_s2, r2_s3, r2_s4, r2_s5])

        """
        Rule 3
        (glimmer implies gold in adjacent cell) converted to clause form is
        ~gl(x,y) | [g(x+1, y) | g(x-1, y) | g(x, y+1) | g(x, y-1)]
        """

        r3_s1: Sentence = Sentence("glimmer", "gl", variables=["x", "y"], negated=True)
        r3_s2: Sentence = Sentence("gold", "g", variables=["x+1", 'y'])
        r3_s3: Sentence = Sentence("gold", "g", variables=["x-1", 'y'])
        r3_s4: Sentence = Sentence("gold", "g", variables=["x", 'y+1'])
        r3_s5: Sentence = Sentence("gold", "g", variables=["x", 'y-1'])
        rule3: Clause = Clause([r3_s1, r3_s2, r3_s3, r3_s4, r3_s5])

        '''
        Rule 4
        (bump implies obstacle which mean you cant move in that direction anymore) converted to clause form is
        ~bu(x,y) | o(x,y)
        '''

        r4_s1: Sentence = Sentence("bump", "bu", variables = ["x", "y"], negated = True)
        r4_s2: Sentence = Sentence("obstacle", "o", variables = ["x", "y"])
        rule4: Clause = Clause([r4_s1, r4_s2])

        self.knowledge_base.set_rules([rule1, rule2, rule3, rule4])

    # TODO: MAKE GOOD
    def assign_danger_value(self, coords) -> float:
        wumpus_danger: float = 0
        wumpus_safe_sentence: Sentence = Sentence("wumpus", "w", literals=coords, negated=True)
        wumpus_danger_sentence: Sentence = Sentence("wumpus", "w", literals=coords, negated=False)

        for clause in self.knowledge_base.kb:
            for sentence in clause.sentences:
                if str(wumpus_safe_sentence) == str(sentence):
                    wumpus_danger = 0
                    break
                elif str(wumpus_danger_sentence) == str(sentence):
                    wumpus_danger += 1 / len(clause)

        pit_danger: float = 0
        pit_safe_sentence: Sentence = Sentence("pit", "p", literals=coords, negated=True)
        pit_danger_sentence = Sentence("pit", "p", literals=coords, negated=False)

        for clause in self.knowledge_base.kb:
            for sentence in clause.sentences:
                if str(pit_safe_sentence) == str(sentence):
                    pit_danger = 0
                    break
                elif str(pit_danger_sentence) == str(sentence):
                    pit_danger += 1 / len(clause)

        gold_likelihood = 0
        gold_sure_sentence: Sentence = Sentence("gold", "g", literals=coords, negated=False)
        gold_not_there_sentence: Sentence = Sentence("gold", "g", literals=coords, negated=True)

        for clause in self.knowledge_base.kb:
            for sentence in clause.sentences:
                if str(gold_sure_sentence) == str(sentence):
                    gold_likelihood = float('inf')
                    break
                elif str(gold_not_there_sentence) == str(sentence):
                    gold_likelihood += 0

        return wumpus_danger + pit_danger - gold_likelihood

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
        for row in rows:
            print(row)