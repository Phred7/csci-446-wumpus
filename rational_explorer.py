from typing import List

from explorer import *
from knowledge_base import *


class RationalExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)
        self.safe_cells: List[List[int, int]] = []
        self.safe_cells.append(self.location)
        self.frontier: List[List[int]] = []
        self.knowledge_base: KnowledgeBase = KnowledgeBase()
        self.init_knowledge_base()

    def walk(self) -> bool:
        bumped: bool = super().walk()
        if bumped:
            target_cell: List[int] = deepcopy(self.location)

            if self.facing == Facing.NORTH:
                target_cell[1] += 1
            elif self.facing == Facing.EAST:
                target_cell[0] += 1
            elif self.facing == Facing.SOUTH:
                target_cell[1] -= 1
            elif self.facing == Facing.WEST:
                target_cell[0] -= 1

            obstacle_clause: Clause = Clause([Sentence("obstacle", "o", literals=target_cell, negated=False)])
            self.knowledge_base.append(obstacle_clause)
        return bumped

    def act(self) -> None:
        self.update_knowledge_base()

        # TODO: TRY TO PROVE THINGS ABOUT FRONTIER CELLS? OR JUST DO RESOLUTION AND PROVE EVERYTHING WE CAN
        #self.knowledge_base.resolution()

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

        self.path(queue.pop()[0])

        return

    def update_knowledge_base(self):
        print("updating knowledge base")
        sensations: List[Sensation] = self.observe()
        print("sensations:", sensations)
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

        # TODO: SHOULD THIS BE DELETED? CAN PROBABLY JUST BE IMPLEMENTED IN act()
        # # Introduction of clauses which make the explorer think that there are obstacles as cave walls.
        # wall_sentences: List[Sentence] = []
        # for i in range(self.board.size):
        #     #below
        #     wall_sentences.append(Sentence("obstacle", "o", literals=[i, -1]))
        #     #above
        #     wall_sentences.append(Sentence("obstacle", "o", literals=[i, self.board.size]))
        #     #west
        #     wall_sentences.append(Sentence("obstacle", "o", literals=[-1, i]))
        #     #above
        #     wall_sentences.append(Sentence("obstacle", "o", literals=[self.board.size, i]))
        #
        # for wall_sentence in wall_sentences:
        #     self.knowledge_base.append(Clause([wall_sentence]))
        #
        self.knowledge_base.set_rules([clause, clause_2])

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
                    gold_likelihood += 1 / len(clause)

        return wumpus_danger + pit_danger - gold_likelihood
