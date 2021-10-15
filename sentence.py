from copy import deepcopy
from typing import List


class Sentence:

    def __init__(self, name: str, identifier: str, *, variables: List[str] = None, literals: List[int] = None,
                 negated: bool = False) -> None:
        self.name: str = name
        self.identifier: str = identifier
        self.literals: List[int] = [] if literals is None else literals
        self.variables: List[str] = [] if variables is None else variables
        self.arguments: List[str] = deepcopy(self.literals) if self.variables == [] else deepcopy(self.variables)
        self.vars: bool = True if len(self.variables) != 0 else False
        self.verbose: bool = False
        self.negated: bool = negated
        self.string: str = ""

    def __str__(self) -> str:  # TODO anytime a sentence is modified self.string MUST be set to ""
        if self.string == "" or self.verbose is True:
            string: str = f"{'~' if self.negated else ''}{self.name if self.verbose else self.identifier}("
            arguments = self.variables if self.vars else self.literals
            for i in range(len(arguments)):
                arguments[i] = eval(arguments[i]) if (type(arguments[i]) == str and ("+" in arguments[i] or "-" in arguments[i]) and ("x" not in arguments[i] and "y" not in arguments[i])) else arguments[i]
                string += str(arguments[i])
                if i != len(arguments)-1:
                    string += ", "
            string += ")"
            self.string = deepcopy(string)
        return self.string

    def negate(self) -> None:
        self.negated = False if self.negated else True
        self.string = ""

