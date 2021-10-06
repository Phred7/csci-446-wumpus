from typing import List

from explorer import *
from knowledge_base import *


class RationalExplorer(Explorer):

    def __init__(self, arrows: int = 0, location=None, facing: int = Direction.EAST):
        if location is None:
            self.location = [()]
        else:
            self.location: Tuple[int, int] = location
        self.facing: int = facing
        self.arrows: int = arrows
        self.score: int = 0
        self.safe_cells: List[Tuple[int, int]] = []
        self.safe_cells.append(self.location)
        self.frontier: List[Tuple[int, int]]
        self.knowledge_base: KnowledgeBase = KnowledgeBase()

    def act(self) -> bool:
        return Explorer.act(self)

    def observe(self) -> None:
        pass
