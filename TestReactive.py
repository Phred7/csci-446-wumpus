import reactive_explorer
import board

def testReactiveExplorer():
    numCaves = 1000
    boardSizes = [3, 5, 10, 15, 20, 25]
    for boardSize in boardSizes:
        numGold = 0
        numDeaths = 0
        for i in range(numCaves):
            b = board.Board(boardSize)
            b.generate_board()
            e = reactive_explorer.ReactiveExplorer(b)
            while not e.isDead and not e.hasGold:
                e.act()
            if e.isDead:
                numDeaths += 1
            if e.hasGold:
                numGold += 1
        print("Board size:                  " + str(boardSize) + "x" + str(boardSize))
        print("Number of runs:             ", numCaves)
        print("Number of times gold found: ", numGold)
        print("Number of times died:       ", numDeaths)
        print("Success rate:               ", numGold / numCaves)
        print()

testReactiveExplorer()
