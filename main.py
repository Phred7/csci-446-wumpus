from knowledge_base import *
from clause import *
from sentence import *
from board import *
from rational_explorer import *

if __name__ == '__main__':
    board: Board = Board(5)
    board.generate_board()
    rational: RationalExplorer = RationalExplorer(board)
    rational.init_knowledge_base()
    print(rational.knowledge_base)
    print(rational.board)

    # Example KB:
    # kb: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    # sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negation=True)
    # sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negation=True)
    # clause: Clause = Clause([sentence, sentence_2])
    # clause_2: Clause = Clause([sentence_3])
    # kb.set_rules([clause, clause_2])
    # print("\n\n" + str(kb))


