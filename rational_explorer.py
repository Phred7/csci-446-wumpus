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
        # Ex Rule:
        # w(x, y) | ~w(y, z)
        sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
        sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negated=True)
        clause: Clause = Clause([sentence, sentence_2])

        # Ex Fact:
        # ~w(0, 0)
        sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negated=True)
        clause_2: Clause = Clause([sentence_3])

        self.knowledge_base.set_rules([clause, clause_2])
