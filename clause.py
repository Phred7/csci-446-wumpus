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

