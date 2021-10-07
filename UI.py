from explorer import *
from board import *


class Player:
    def __init__(self):
        self.b = Board()
        self.b.generate_board()
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
            print('d: display board')
            print('q: exit program')
            print('You have', self.e.arrowCount, 'arrows.')
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
        elif result == 'd':
            self.e.disp()
        elif result == 'q':
            return False
        else:
            print("Invalid input.")
        print()

        return True


def main():
    p: Player = Player()
    #p.b.disp()
    while p.prompt():
        continue
    print(p.e.actionsTaken)
    p.b.disp()
main()