from typing import List

from explorer import *
from knowledge_base import *


class RationalExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)
        self.safe_cells: List[Tuple[int, int]] = []
        self.safe_cells.append(self.location)
        self.frontier: List[Tuple[int, int]]
        self.knowledge_base: KnowledgeBase = KnowledgeBase()
        self.init_knowledge_base()

    def act(self) -> bool:
        return Explorer.act(self)

    def observe(self) -> None:
        """
        Listens to senses and generates facts about the world from those senses.
        Ex. at a location with no smell generates the fact: ~w(a,b) where a and b are the current x and y location of this explorer
        :return:
        """
        pass

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
        rule4: Clause = Clause(r4_s1, r4_s2)

        self.knowledge_base.set_rules([rule1, rule2, rule3, rule4])
