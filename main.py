import threading
from threading import Thread

from knowledge_base import *
from clause import *
from sentence import *
from board import *
from rational_explorer import *


def explore(explorer: RationalExplorer) -> int:
    """
    Used to run this explorer on it's board.
    :return:
    """
    explorer.init_knowledge_base()
    return 0


if __name__ == '__main__':

    board_sizes: List[int] = [5, 10, 15, 20, 25]

    for size in board_sizes:
        threads: List[Thread] = []
        thread_count: int = 25
        for i in range(0, thread_count):
            board: Board = Board(size)
            rational: RationalExplorer = RationalExplorer(deepcopy(board))
            threads.append(threading.Thread(target=explore, args=(deepcopy(rational),),
                                            name=f"rational_explorer_thread{i}"))
        for thread in threads:
            thread.start()
        print(f"Threads 0-{thread_count - 1} started")
        for thread in threads:
            thread.join()
        print(f"Threads 0-{thread_count - 1} joined")

    pass
    # Example Unification:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("foo", "f", variables=["x"])
    # clause: Clause = Clause([sentence])
    # sentence_2: Sentence = Sentence("foo", "f", variables=["a"])
    # clause_2: Clause = Clause([sentence_2])
    # knowledge_base.set_rules([clause, clause_2])
    # print(knowledge_base)
    # print(f"unified: {knowledge_base.unify(knowledge_base.get_clause(0), knowledge_base.get_clause(1))}\n")
    #
    # Example Unification 2:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("foo", "f", variables=["x", "y"])
    # clause: Clause = Clause([sentence])
    # sentence_2: Sentence = Sentence("foo", "f", literals=[1, 2])
    # clause_2: Clause = Clause([sentence_2])
    # knowledge_base.set_rules([clause, clause_2])
    # print(f"unified: {knowledge_base.unify(knowledge_base.get_clause(0), knowledge_base.get_clause(1))}\n")
    # print(knowledge_base)

    # Example Resolution:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    #
    # sentence: Sentence = Sentence("p", "p", variables=["x"], negated=True)
    # sentence_2: Sentence = Sentence("q", "q", variables=["x"])
    # clause: Clause = Clause([sentence, sentence_2])
    # sentence_3: Sentence = Sentence("p", "p", variables=["x"])
    # clause_2: Clause = Clause([sentence_3])
    # knowledge_base.set_rules([clause, clause_2])
    #
    # print(knowledge_base)
    # print("resolving...")
    # knowledge_base.resolution()
    # print(knowledge_base)

    # Example Rational:
    # board: Board = Board(size=5)
    # board.generate_board()
    # rational: RationalExplorer = RationalExplorer(board)
    # print(rational.knowledge_base)
    # print(f"{rational.board.__class__.__name__}:\n{rational.board}")

    #Example KB:
    # kb: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    # sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negated=True)
    # sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negated=True)
    # clause: Clause = Clause([sentence, sentence_2])
    # clause_2: Clause = Clause([sentence_3])
    # kb.set_rules([clause, clause_2])
    # print("\n\n" + str(kb))

