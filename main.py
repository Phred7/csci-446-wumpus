import multiprocessing
import time
from multiprocessing import Process, Queue


from rational_explorer import *
from reactive_explorer import *
from datetime import datetime


class MultiProcessExplore:

    def __init__(self):
        self.board_sizes: List[int] = [5, 10, 15, 20, 25]
        # self.board_sizes: List[int] = [5]
        self.lock = multiprocessing.Lock()
        self.queue: Queue = Queue()

        self.output = list(np.full(len(Output), 0))

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
                if len(pop) == len(Output):
                    for i in range(len(pop)):
                        self.output[i] += pop[i]


                process.join()
            self.lock.acquire()
            print(f"Processes 0-{self.num_caves - 1} joined for board size: {size}\n")
            print("Board size:                  " + str(size) + "x" + str(size))
            print("Number of runs:             ", self.num_caves)
            print("Rational: Number of times gold found: ", self.output[Output.RAT_GOLD])
            print("Rational: Number of times died:       ", self.output[Output.RAT_DEATHS])
            print("Rational: Success rate:               ", self.output[Output.RAT_GOLD] / self.num_caves)
            print("Rational: Deaths from old age:        ", self.output[Output.RAT_OLD] / self.num_caves)
            print("Rational: Deaths from pit:            ", self.output[Output.RAT_PIT] / self.num_caves)
            print("Rational: Deaths from wumpus:         ", self.output[Output.RAT_WUMPUS] / self.num_caves)
            print("Rational: Average actions taken:      ", self.output[Output.RAT_ACTIONS] / self.num_caves)
            print()
            print("Reactive: Number of times gold found: ", self.output[Output.REA_GOLD])
            print("Reactive: Number of times died:       ", self.output[Output.REA_DEATHS])
            print("Reactive: Success REAe:               ", self.output[Output.REA_GOLD] / self.num_caves)
            print("Reactive: Deaths from old age:        ", self.output[Output.REA_OLD] / self.num_caves)
            print("Reactive: Deaths from pit:            ", self.output[Output.REA_PIT] / self.num_caves)
            print("Reactive: Deaths from wumpus:         ", self.output[Output.REA_WUMPUS] / self.num_caves)
            print("Reactive: Average actions taken:      ", self.output[Output.REA_ACTIONS] / self.num_caves)

            print("\n\n")
            self.output = list(np.full(len(Output), 0))
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
        reactive_explorer: ReactiveExplorer = ReactiveExplorer(deepcopy(board))
        while not rational_explorer.is_dead and not rational_explorer.has_gold:
            rational_explorer.act()
        while not reactive_explorer.is_dead and not reactive_explorer.has_gold:
            reactive_explorer.act()
        self.lock.acquire()

        x: int = rational_explorer.location[0]
        y: int = rational_explorer.location[1]

        self.queue.put([
            1 if rational_explorer.is_dead else 0,
            1 if rational_explorer.has_gold else 0,
            1 if rational_explorer.board.grid[x][y][CellContent.WUMPUS] else 0,
            1 if rational_explorer.board.grid[x][y][CellContent.PIT] else 0,
            1 if rational_explorer.max_age <= rational_explorer.actions_taken else 0,
            rational_explorer.actions_taken,
            
            1 if reactive_explorer.is_dead else 0,
            1 if reactive_explorer.has_gold else 0,
            1 if reactive_explorer.board.grid[x][y][CellContent.WUMPUS] else 0,
            1 if reactive_explorer.board.grid[x][y][CellContent.PIT] else 0,
            1 if reactive_explorer.max_age <= reactive_explorer.actions_taken else 0,
            reactive_explorer.actions_taken

            ])
        end_time = datetime.now()

        print("Finished cave", process_number, "in", end_time - start_time,
              "      " + ("X" if rational_explorer.is_dead else "G"),
              "/", ("X" if reactive_explorer.is_dead else "G"),
              "      " + str(rational_explorer.actions_taken),
              "/", str(reactive_explorer.actions_taken))
        self.lock.release()
        return


if __name__ == '__main__':
    # Parallelism:
    # multi_process_explore: MultiProcessExplore = MultiProcessExplore()
    # multi_process_explore.explore()
    num_gold = 0
    num_deaths = 0
    num_wump = 0
    num_pit = 0
    num_old = 0
    start = datetime.now()
    b = Board(5)
    b.generate_board()
    e = RationalExplorer(b)
    print(b)
    while not e.is_dead and not e.has_gold:
        print(e)
        e.act()
    if e.is_dead:
        num_deaths += 1
    if e.has_gold:
        num_gold += 1

    x = e.location[0]
    y = e.location[1]

    if e.board.grid[x][y][CellContent.WUMPUS]:
        num_wump += 1
    if e.board.grid[x][y][CellContent.PIT]:
        num_pit += 1
    if e.max_age <= e.actions_taken:
        num_old += 1

    end = datetime.now()
    print(e)


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


