from copy import deepcopy
from typing import List


class Sentence:
    """
    Representation of a Sentence in a Clause.
    """

    def __init__(self, name: str, identifier: str, *, variables: List[str] = None, literals: List[int] = None,
                 negated: bool = False) -> None:
        self.name: str = name
        self.identifier: str = identifier
        self.literals: List[int] = [] if literals is None else literals
        self.variables: List[str] = [] if variables is None else variables

        translated_variables = []
        for variable in self.variables:
            if type(variable) != str:
                variable = str(variable)
            translated_variables.append(variable)
        self.variables = translated_variables

        self.arguments: List[str] = deepcopy(self.literals) if self.variables == [] else deepcopy(self.variables)
        self.vars: bool = True if len(self.variables) != 0 else False
        self.verbose: bool = False
        self.negated: bool = negated
        self.string: str = ""

    def __str__(self) -> str:
        """
        Creates the string representation of this Sentence.
        This method is memoized. Ie. Sentence stores a copy of the value returned from this method. If this Sentence is
        not altered this method will simply return that string rather than generate the same string again.
        :return: str representation of this Sentence.
        """
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
        """
        Negates this Sentence.
        Ie. ~w(x,y).negate() = w(x,y)
        :return: None.
        """
        self.negated = False if self.negated else True
        self.string = ""

