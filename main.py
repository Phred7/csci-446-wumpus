from knowledge_base import *
from clause import *
from sentence import *
from board import *
from rational_explorer import *

if __name__ == '__main__':
    # Example Resolution:
    knowledge_base: KnowledgeBase = KnowledgeBase()

    sentence: Sentence = Sentence("p", "p", variables=["x"], negated=True)
    sentence_2: Sentence = Sentence("q", "q", variables=["x"])
    clause: Clause = Clause([sentence, sentence_2])
    sentence_3: Sentence = Sentence("p", "p", variables=["x"])
    clause_2: Clause = Clause([sentence_3])
    knowledge_base.set_rules([clause, clause_2])

    print(knowledge_base)
    print("resolving...")
    knowledge_base.resolution()
    print(knowledge_base)

    # Example Rational:
    # board: Board = Board(size=5)
    # board.generate_board()
    # rational: RationalExplorer = RationalExplorer(board)
    # print(rational.knowledge_base)
    # print(f"{rational.board.__class__.__name__}:\n{rational.board}")

    # Example KB:
    # kb: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    # sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negated=True)
    # sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negated=True)
    # clause: Clause = Clause([sentence, sentence_2])
    # clause_2: Clause = Clause([sentence_3])
    # kb.set_rules([clause, clause_2])
    # print("\n\n" + str(kb))
