from explorer import *


class ReactiveExplorer(Explorer):

    def __init__(self, arrows: int = 0, location=None, facing: int = Direction.EAST):
        if location is None:
            self.location = [()]
        else:
            self.location: Tuple[int, int] = location
        self.facing: int = facing
        self.arrows: int = arrows
        self.score: int = 0

    def act(self) -> bool:
        return Explorer.act(self)
    