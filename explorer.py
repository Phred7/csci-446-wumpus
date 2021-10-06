from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple


class Direction(Enum):
    NORTH: int = 0
    EAST: int = 1
    SOUTH: int = 2
    WEST: int = 3


class Explorer(ABC):

    def turn(self, direction: Direction) -> bool:
        pass

    def walk(self) -> bool:
        pass

    def shoot(self) -> bool:
        pass

    @abstractmethod
    def act(self) -> bool:
        raise NotImplementedError
