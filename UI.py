from explorer import *
from board import *


class Player:
    def __init__(self):
        self.b = Board()
        wumpusCoords = [[1, 0], [3, 3]]
        for coord in wumpusCoords:
            self.b.insert_wumpus(coord)

        self.b.grid[4][4][CellValue.GOLD] = True
        self.b.grid[2][2][CellValue.PIT] = True

        self.e = Explorer(self.b)

    def prompt(self) -> bool:
        print("At", self.e.location, "facing", self.e.facing)
        self.e.observe()
        print("Enter an action. Enter 'h' to view all actions.")
        result = input().lower()
        if result == 'h':
            print("w: walk")
            print("l: turn left")
            print('r: turn right')
            print('s: shoot arrow')
            print('q: exit program')
        elif result == "w":
            self.e.walk()
            if self.e.isDead:
                return False
            elif self.e.hasGold:
                return False
        elif result == 'l':
            self.e.turn(Direction.LEFT)
        elif result == 'r':
            self.e.turn(Direction.RIGHT)
        elif result == 's':
            self.e.shoot()
        elif result == 'q':
            return False
        else:
            print("Invalid input.")
        print()

        return True


def main():
    p: Player = Player()
    while p.prompt():
        continue
main()