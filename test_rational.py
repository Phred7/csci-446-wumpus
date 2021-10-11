import random

from rational_explorer import *

def TestRational():
    b: Board = Board()
    b.grid[0][1][CellContent.WUMPUS] = True

    ex: RationalExplorer = RationalExplorer(b)
    ex.generate_graph()

    ex.update_knowledge_base()

    print()
    print("Knowledge base after update:")
    for i, clause in enumerate(ex.knowledge_base.kb):
        print(i, clause)



    # sentence1: Sentence = Sentence("wumpus", "w", literals=[0, 1], negated=False)
    # sentence2: Sentence = Sentence("wumpus", "w", literals=[1, 0], negated=False)
    # sentence3: Sentence = Sentence("wumpus", "w", literals=[1, 1], negated=False)
    # sentence4: Sentence = Sentence("gold", 'g', literals = [0, 1], negated=True)
    #
    # ex.knowledge_base.append(Clause([sentence1, sentence2, sentence3, sentence4]))
    #
    # print(ex.assign_danger_value([0, 1]))

TestRational()