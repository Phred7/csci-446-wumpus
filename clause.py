from copy import deepcopy

from sentence import *


class Clause:
    """
    Operators
        Negation:       ~
        Or:             |
    """

    def __init__(self, arguments: List[Sentence], negated: bool = False, *, operator: str = "|"):
        self.operator: str = operator
        self.negation: bool = negated
        self.sentences: List[Sentence] = arguments
        self.string: str = ""

    def __str__(self) -> str:  # TODO anytime a clause is modified self.string MUST be set to ""
        """
        Implements memoization to decrease time taken to generate strings for Clauses.
        :return:
        """
        if self.string != "":
            string: str = ""
            for arg in self.sentences:
                string += f"{str(arg)}"
                if self.sentences.index(arg) != len(self.sentences) - 1:
                    string += f" {self.operator} "
            self.string = deepcopy(string)
        return self.string
