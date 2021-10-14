from enums import *
import reactive_explorer
import board
from datetime import *

def testReactiveExplorer():
    numCaves = 100
    #boardSizes = [5, 10, 15, 20, 25]
    boardSizes = [25]
    # b = board.Board(5)
    # b.generate_board()
    # b.grid[0][1][CellContent.OBSTACLE] = True
    # b.grid[0][2][CellContent.GOLD] = True
    # b.disp()
    # print()
    # ex = reactive_explorer.ReactiveExplorer(b)
    # while not ex.is_dead and not ex.has_gold:
    #     ex.act()
    #     print()
    # if ex.has_gold:
    #     print("won")
    # else:
    #     print("lost")

    # print(ex.history)

    for boardSize in boardSizes:
        numGold = 0
        numDeaths = 0
        for i in range(numCaves):
            start = datetime.now()
            b = board.Board(boardSize)
            b.generate_board()
            e = reactive_explorer.ReactiveExplorer(b)
            while not e.is_dead and not e.has_gold:
                e.act()
            if e.is_dead:
                numDeaths += 1
            if e.has_gold:
                numGold += 1
            end = datetime.now()

            print("Finished cave", i, "in", end - start)
        print("Board size:                  " + str(boardSize) + "x" + str(boardSize))
        print("Number of runs:             ", numCaves)
        print("Number of times gold found: ", numGold)
        print("Number of times died:       ", numDeaths)
        print("Success rate:               ", numGold / numCaves)
        print()

testReactiveExplorer()
