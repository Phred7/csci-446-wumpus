from typing import List

from explorer import *
from knowledge_base import *


class RationalExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)
        self.safe_cells: List[List[int, int]] = []
        self.safe_cells.append(self.location)
        self.frontier: List[Tuple[int, int]]
        self.knowledge_base: KnowledgeBase = KnowledgeBase()
        self.init_knowledge_base()

    #TODO: IMPLEMENT ADDING OBSTACLE INFO
    def walk(self) -> bool:
        bumped: bool = super().walk()
        return bumped

    def act(self) -> bool:
        return Explorer.act(self)



    def update_knowledge_base(self):
        sensations = self.observe()
        adjacent_cells = self.get_adjacent_cells()

        pit_sentences: List[Sentence] = []
        if sensations[Sensation.BREEZE]:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("pit", "p", literals=cell, negated=False))
        else:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("pit", "p", literals=cell, negated=True))

        pit_clause: Clause = Clause(pit_sentences)
        self.knowledge_base.append(pit_clause)

        wumpus_sentences: List[Sentence] = []
        if sensations[Sensation.STENCH]:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("wumpus", "w", literals=cell, negated=False))
        else:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("wumpus", "w", literals=cell, negated=True))

        wumpus_clause: Clause = Clause(wumpus_sentences)
        self.knowledge_base.append(wumpus_clause)

        gold_sentences: List[Sentence] = []
        if sensations[Sensation.GLIMMER]:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("gold", "g", literals=cell, negated=False))
        else:
            for cell in adjacent_cells:
                pit_sentences.append(Sentence("gold", "g", literals=cell, negated=True))

        gold_clause: Clause = Clause(gold_sentences)
        self.knowledge_base.append(gold_clause)


        return

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
