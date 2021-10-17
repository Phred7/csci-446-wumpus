import multiprocessing
import time
from multiprocessing import Process, Queue

from knowledge_base import *
from clause import *
from sentence import *
from board import *
from rational_explorer import *
from datetime import datetime


class MultiProcessExplore:

    def __init__(self):
        # self.board_sizes: List[int] = [5, 10, 15, 20, 25]
        self.board_sizes: List[int] = [10]
        self.lock = multiprocessing.Lock()
        self.queue: Queue = Queue()
        self.num_gold: int = 0
        self.num_deaths: int = 0
        self.num_wumpus: int = 0
        self.num_pit: int = 0
        self.num_old: int = 0
        self.num_caves: int = 10

    def explore(self) -> None:
        for size in self.board_sizes:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Board: {size}")
            self.lock.release()
            for i in range(0, self.num_caves):
                processes.append(multiprocessing.Process(target=self._run_explorer, args=(deepcopy(size), i,),
                                                         name=f"rational_explorer_process_{i}"))
            for process in processes:
                process.start()
            self.lock.acquire()
            print(f"Processes 0-{self.num_caves - 1} started for board size: {size}")
            self.lock.release()
            for process in processes:
                pop = self.queue.get()
                if len(pop) == 5:
                    if pop[0] == 1:
                        self.num_deaths += 1
                    if pop[1] == 1:
                        self.num_gold += 1
                    if pop[2] == 1:
                        self.num_wumpus += 1
                    if pop[3] == 1:
                        self.num_pit += 1
                    if pop[4] == 1:
                        self.num_old += 1
                process.join()
            self.lock.acquire()
            print(f"Processes 0-{self.num_caves - 1} joined for board size: {size}\n")
            print("Board size:                  " + str(size) + "x" + str(size))
            print("Number of runs:             ", self.num_caves)
            print("Number of times gold found: ", self.num_gold)
            print("Number of times died:       ", self.num_deaths)
            print("Success rate:               ", self.num_gold / self.num_caves)
            print("Deaths from old age:        ", self.num_old / self.num_caves)
            print("Deaths from pit:            ", self.num_pit / self.num_caves)
            print("Deaths from wumpus:         ", self.num_wumpus / self.num_caves)
            print("\n\n")
            self.num_gold: int = 0
            self.num_deaths: int = 0
            self.num_wumpus: int = 0
            self.num_pit: int = 0
            self.num_old: int = 0
            self.lock.release()

    def _run_explorer(self, board_size: int, process_number: int) -> None:
        """
        Used to create and run a rationalExplorer on a Board of size board_size.
        :return:
        """
        start_time = datetime.now()
        board: Board = Board(board_size)
        board.generate_board()
        rational_explorer: RationalExplorer = RationalExplorer(board)
        while not rational_explorer.is_dead and not rational_explorer.has_gold:
            rational_explorer.act()
        self.lock.acquire()

        x: int = rational_explorer.location[0]
        y: int = rational_explorer.location[1]

        self.queue.put([
            1 if rational_explorer.is_dead else 0,
            1 if rational_explorer.has_gold else 0,
            1 if rational_explorer.board.grid[x][y][CellContent.WUMPUS] else 0,
            1 if rational_explorer.board.grid[x][y][CellContent.PIT] else 0,
            1 if rational_explorer.max_age <= rational_explorer.actions_taken else 0])
        end_time = datetime.now()

        print("Finished cave", process_number, "in", end_time - start_time,
              "      " + ("X" if rational_explorer.is_dead else "G"))
        self.lock.release()
        return


if __name__ == '__main__':
    # Threading:
    multi_process_explore: MultiProcessExplore = MultiProcessExplore()
    multi_process_explore.explore()

    # Example Unification:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("foo", "f", variables=["x+1"])
    # clause: Clause = Clause([sentence])
    # sentence_2: Sentence = Sentence("foo", "f", literals=[0])
    # clause_2: Clause = Clause([sentence_2])
    # knowledge_base.set_rules([clause, clause_2])
    # print(knowledge_base)
    # print(f"unified: {knowledge_base.unify(knowledge_base.get_clause(0), knowledge_base.get_clause(1))}\n")

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
    # knowledge_base: KnowledgeBase = KnowledgeBase(5)
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

    # # board generation verification
    # board: Board = Board(size=5)
    # board.generate_board()
    # print(board)

    # Example Rational:
    # board: Board = Board(size=5)
    # board.generate_board()
    # print(board)
    # print()
    # rational: RationalExplorer = RationalExplorer(board)
    # # print(f"initial KB:\n{rational.knowledge_base}")
    # while (not rational.is_dead) and (not rational.has_gold):
    #     rational.act()
    #     print(rational)
    #     print()
    # if rational.has_gold:
    #     print("Found gold")
    # else:
    #     print("Big Dead")
    # print(rational)
    # print(rational.board)
    # print("Exiting")

    # More rigorous rational testbed:
    # numCaves = 30
    # boardSizes = [5, 10, 15, 20, 25]
    # for boardSize in boardSizes:
    #     num_gold = 0
    #     num_deaths = 0
    #     num_wump = 0
    #     num_pit = 0
    #     num_old = 0
    #     for i in range(numCaves):
    #         start = datetime.now()
    #         b = Board(boardSize)
    #         b.generate_board()
    #         e = rational_explorer.RationalExplorer(b)
    #         while not e.is_dead and not e.has_gold:
    #             e.act()
    #         if e.is_dead:
    #             num_deaths += 1
    #         if e.has_gold:
    #             num_gold += 1
    #
    #         x = e.location[0]
    #         y = e.location[1]
    #
    #         if e.board.grid[x][y][CellContent.WUMPUS]:
    #             num_wump += 1
    #         if e.board.grid[x][y][CellContent.PIT]:
    #             num_pit += 1
    #         if e.max_age <= e.actions_taken:
    #             num_old += 1
    #
    #         end = datetime.now()
    #
    #         print("Finished cave", i, "in", end - start, "      " + ("X" if e.is_dead else "G"))
    #     print("Board size:                  " + str(boardSize) + "x" + str(boardSize))
    #     print("Number of runs:             ", numCaves)
    #     print("Number of times gold found: ", num_gold)
    #     print("Number of times died:       ", num_deaths)
    #     print("Success rate:               ", num_gold / numCaves)
    #     print("Deaths from old age:        ", num_old / numCaves)
    #     print("Deaths from pit:            ", num_pit / numCaves)
    #     print("Deaths from wumpus:         ", num_wump / numCaves)
    #     print()

    # Example KB:
    # kb: KnowledgeBase = KnowledgeBase()
    #
    # sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    # sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negated=True)
    # clause: Clause = Clause([sentence, sentence_2])
    # kb.set_rules([clause])
    #
    # sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negated=True)
    # sentence_4: Sentence = Sentence("test", "t", variables=["10-1", "20+3"])
    # clause_2: Clause = Clause([sentence_3])
    # clause_3: Clause = Clause([sentence_4])
    # kb.append(clause_2)
    # kb.append(clause_3)
    # print("\n\n" + str(kb))
    #
    # query: Sentence = Sentence("test", "t", variables=["10", "256"])
    # print(f"Query: {kb.query(query)}")
