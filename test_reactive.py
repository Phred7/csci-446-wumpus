import reactive_explorer
import board

def testReactiveExplorer():
    numCaves = 1000
    boardSizes = [3, 5, 10, 15, 20, 25]
    b = board.Board(5)
    b.generate_board()
    b.disp()
    print()
    ex = reactive_explorer.ReactiveExplorer(b)
    while not ex.is_dead and not ex.has_gold:
        ex.act()
        ex.disp()
        print()

    print(ex.history)

    # for boardSize in boardSizes:
    #     numGold = 0
    #     numDeaths = 0
    #     for i in range(numCaves):
    #         b = board.Board(boardSize)
    #         b.generate_board()
    #         e = reactive_explorer.ReactiveExplorer(b)
    #         while not e.is_dead and not e.has_gold:
    #             e.act()
    #         if e.is_dead:
    #             numDeaths += 1
    #         if e.has_gold:
    #             numGold += 1
    #     print("Board size:                 " + str(boardSize) + "x" + str(boardSize))
    #     print("Number of runs:             ", numCaves)
    #     print("Number of times gold found: ", numGold)
    #     print("Number of times died:       ", numDeaths)
    #     print("Success rate:               ", numGold / numCaves)
    #     print()

testReactiveExplorer()
