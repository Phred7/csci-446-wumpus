from typing import List


class Sentence:

    def __init__(self, name: str, identifier: str, *, variables: List[str] = None, literals: List[int] = None):
        self.name: str = name
        self.identifier: str = identifier
        self.literals = [] if literals is None else literals
        self.variables = [] if variables is None else variables
