from copy import deepcopy

from sentence import *


class Clause:
    """
    Representation of a Clause in a KnowledgeBase
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

    def __str__(self) -> str:
        """
        Creates the string representation of this Clause.
        This method is memoized. Ie. Clause stores a copy of the value returned from this method.
        If this Clause is not altered when called this method will simply return that string rather than generate the
        same string again.
        :return: str representation of this Clause.
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

    def __len__(self) -> int:
        """
        Gets the length of this Clause.
        :return: int representation of the length of this Clause.
        """
        return self.sentences.__len__()

    def set_kb_id(self, _id: int) -> None:
        """
        Sets the KnowledgeBase Identifier for this Clause. Corresponds to this Clause's index in KnowledgeBase().kb
        :param _id: int to set this Clause's kb_id to.
        :return: None.
        """
        self.kb_id = _id

    def get_kb_id(self) -> int:
        """
        Gets the KnowledgeBase Identifier for this Clause. Corresponds to this Clause's index in KnowledgeBase().kb
        :return: int representing the kb_id for this Clause.
        """
        return self.kb_id

    def set_rule(self) -> None:
        """
        Sets this Clause as a rule clause.
        :return: None.
        """
        self.rule = True

    def negate(self) -> None:
        """
        Negates this Clause.
        Ie. ~w(x,y) | w(z,y) | w(x,zz).negate() = ~(~w(x,y) | w(z,y) | w(x,zz))
        :return: None.
        """
        self.negated = False if self.negated else True
        self.string = ""

    def remove(self, item: Sentence) -> None:
        """
        Removes a Sentence from this Clause. Does not check the length of this Clause so it could be an empty Clause.
        :param item: Sentence to remove from this Clause.
        :return: None.
        """
        self.sentences.remove(item)
        self.string = ""



