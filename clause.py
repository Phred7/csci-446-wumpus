from copy import deepcopy

from sentence import *


class Clause:
    """
    Negation:       ~
    Or:             |
    """

    def __init__(self, arguments: List[Sentence], *, operator: str = "|") -> None:
        self.operator: str = operator
        self.sentences: List[Sentence] = arguments
        self.negated: bool = False
        self.string: str = ""
        self.kb_id: int = -1
        self.rule: bool = False
        self.new: bool = False

    def __str__(self) -> str:  # TODO anytime a clause is modified self.string MUST be set to ""
        """
        Implements memoization to decrease time taken to generate strings for Clauses.
        :return:
        """
        if self.string == "":
            string: str = ""
            if self.negated:
                string += "~("
            for arg in self.sentences:
                string += f"{str(arg)}"
                if self.sentences.index(arg) != len(self.sentences) - 1:
                    string += f" {self.operator} "
            if self.negated:
                string += ")"
            self.string = deepcopy(string)
        return self.string

    def __len__(self):
        return self.sentences.__len__()

    def set_kb_id(self, _id: int) -> None:
        self.kb_id = _id

    def get_kb_id(self) -> int:
        return self.kb_id

    def set_rule(self) -> None:
        self.rule = True

    def negate(self) -> None:
        self.negated = False if self.negated else True
        self.string = ""

    def remove(self, item: Sentence):
        self.sentences.remove(item)
        self.string = ""



