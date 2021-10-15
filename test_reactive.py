from enums import *
import reactive_explorer
import board
from datetime import *

def testReactiveExplorer():



    # b = board.Board(6)
    # b.generate_board()
    #
    #
    # b.disp()
    # print()
    #
    # ex = reactive_explorer.ReactiveExplorer(b)
    # while not ex.is_dead and not ex.has_gold:
    #     ex.act()
    #     print(ex.actions_taken)
    #     print()
    # if ex.has_gold:
    #     print("won")
    # else:
    #     print("lost")
    #
    # print(ex.history)

    numCaves = 30
    boardSizes = [5, 10, 15, 20, 25]
    for boardSize in boardSizes:
        numGold = 0
        numDeaths = 0
        numWump = 0
        numPit = 0
        numOld = 0
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

            x = e.location[0]
            y = e.location[1]

            if e.board.grid[x][y][CellContent.WUMPUS]:
                numWump += 1
            if e.board.grid[x][y][CellContent.PIT]:
                numPit += 1
            if e.max_age <= e.actions_taken:
                numOld += 1


            end = datetime.now()

            print("Finished cave", i, "in", end - start, "      " + ("X" if e.is_dead else "G"))
        print("Board size:                  " + str(boardSize) + "x" + str(boardSize))
        print("Number of runs:             ", numCaves)
        print("Number of times gold found: ", numGold)
        print("Number of times died:       ", numDeaths)
        print("Success rate:               ", numGold / numCaves)
        print("Deaths from old age:        ", numOld / numCaves)
        print("Deaths from pit:            ", numPit / numCaves)
        print("Deaths from wumpus:         ", numWump / numCaves)
        print()

testReactiveExplorer()
