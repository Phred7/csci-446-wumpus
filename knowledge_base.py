from clause import *
from sentence import *


class KnowledgeBase:

    def __init__(self) -> None:
        self.kb: List[Clause] = []
        self.string: str = ""
        pass

    def set_rules(self, rules: List[Clause]):
        for rule in rules:
            self.kb.append(rule)

    def infer(self) -> None:
        pass

    def append(self, item: Clause) -> None:
        self.kb.append(item)
        self.infer()

    def __str__(self) -> str:  # TODO anytime a KB is modified self.string MUST be set to ""
        if self.string == "":
            string = f"{self.__class__.__name__}:\n"
            for clause in self.kb:
                string += f"{str(clause)}\n"
            self.string = string
        return self.string
