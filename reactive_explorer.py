from typing import List

from explorer import *


class ReactiveExplorer(Explorer):

    def __init__(self, board: Board):
        super().__init__(board)

    def act(self) -> bool:
        return Explorer.act(self)
    