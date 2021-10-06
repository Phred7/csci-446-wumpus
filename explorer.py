from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple


class Direction(Enum):
    NORTH: int = 0
    EAST: int = 1
    SOUTH: int = 2
    WEST: int = 3


class Explorer(ABC):

    def __init__(self, arrows: int = 0, location=None, facing: int = Direction.EAST):
        if location is None:
            self.location = [()]
        else:
            self.location: Tuple[int, int] = location
        self.facing: int = facing
        self.arrows: int = arrows
        self.score: int = 0

    def turn(self, direction: Direction) -> bool:
        raise NotImplementedError

    def walk(self) -> bool:
        raise NotImplementedError

    def shoot(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def act(self) -> bool:
        raise NotImplementedError
