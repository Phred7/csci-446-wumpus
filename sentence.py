from copy import deepcopy
from typing import List


class Sentence:

    def __init__(self, name: str, identifier: str, *, variables: List[str] = None, literals: List[int] = None,
                 negation: bool = False) -> None:
        self.name: str = name
        self.identifier: str = identifier
        self.literals = List[int] if literals is None else literals
        self.variables: List[str] = [] if variables is None else variables
        self.vars: bool = True if self.variables is not None else False
        self.negation: bool = negation
        self.string: str = ""

    def __str__(self) -> str:  # TODO anytime a sentence is modified self.string MUST be set to ""
        if self.string == "":
            string: str = f"{'~' if self.negation else ''}{self.identifier}("
            arguments = self.variables if self.vars else self.literals
            for arg in arguments:
                string += str(arg)
                if arguments.index(arg) != len(arguments)-1:
                    string += ", "
            string += ")"
            self.string = deepcopy(string)
        return self.string

