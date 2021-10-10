from clause import *
from sentence import *


class KnowledgeBase:

    def __init__(self) -> None:
        self.kb: List[Clause] = []
        self.clauses: int = 0
        self.string: str = ""
        self.kb_init: bool = False

    def __str__(self) -> str:  # TODO anytime a KB is modified self.string MUST be set to ""
        if self.string == "":
            string = f"{self.__class__.__name__}:\n"
            for clause in self.kb:
                string += f"{str(clause)}\n"
            self.string = string
        return self.string

    def set_rules(self, rules: List[Clause]) -> None:
        if self.kb_init is True:
            raise IOError("Knowledge Base can only be initialized once. Call append() to add more clauses to this KB.")
        for rule in rules:
            rule.set_kb_id(self.clauses)
            rule.set_rule()
            self.kb.append(rule)
            self.clauses += 1
        self.kb_init = True

    def append(self, item: Clause) -> None:
        if self.kb_init is False:
            raise IOError("Knowledge Base has not been initialized. Call set_rules() to initialize this KB.")
        item.set_kb_id(self.clauses)
        self.string = ""
        self.clauses += 1
        self.kb.append(item)
        self.infer()

    def remove_clause(self, clause_kb_id: int) -> None:
        self.kb.remove(self.get_clause(clause_kb_id))
        self.string = ""
        for i in range(clause_kb_id, len(self.kb)):
            current_id: int = self.kb[i].get_kb_id()
            self.kb[i].set_kb_id(current_id-1)

    def get_clause(self, clause_kb_id: int) -> Clause:
        return self.kb[clause_kb_id]

    def infer(self) -> None:
        pass

    # def resolution(self) -> None:
    #     last_clause: Clause = self.kb[-1]
    #     for clause in self.kb:
    #         if len(last_clause.sentences) == 1 and len(clause.sentences) == 2:  # last clause of the form: p(x)
    #             if clause.sentences[0].negated ^ clause.sentences[1].negated:
    #                 negated_sentence: Sentence = clause.sentences[0] if clause.sentences[0].negated else clause.sentences[1]
    #                 sentence: Sentence = clause.sentences[0] if clause.sentences[1].negated else clause.sentences[1]
    #                 last_sentence: Sentence = last_clause.sentences[0]
    #                 if negated_sentence.name == last_sentence.name:
    #                     if (last_sentence.variables == negated_sentence.variables == sentence.variables) and (last_sentence.literals == negated_sentence.literals == sentence.literals):
    #                         # here the clauses are of the form: ~p(x) | q(x) and p(x)
    #                         new_sentence: Sentence = Sentence(name=deepcopy(negated_sentence.name), identifier=deepcopy(negated_sentence.name), variables=deepcopy(negated_sentence.variables), literals=deepcopy(negated_sentence.literals))
    #                         new_clause: Clause = Clause([new_sentence])
    #                         self.kb.append(new_clause)
    #         elif (len(last_clause.sentences) == 2) and ():  # last clause of the form: p(x) | q(x)
    #             if len(clause.sentences) == 1:  # current clause of the form p(x)
    #                 pass

    def resolution(self) -> None:
        last_clause: Clause = self.kb[-1]
        for clause in self.kb:
            if last_clause == clause:
                break
            if (len(last_clause) == 1 and len(clause) == 2) or len(last_clause) == 2 and len(clause) == 1:
                long_clause: Clause = clause if len(clause) == 2 else last_clause
                short_clause: Clause = clause if len(clause) == 1 else last_clause
                if long_clause.sentences[0].negated ^ long_clause.sentences[1].negated:  # this tests to see if both clauses are defined in scope
                    negated_sentence: Sentence = long_clause.sentences[0] if long_clause.sentences[0].negated else long_clause.sentences[1]
                    sentence: Sentence = long_clause.sentences[0] if long_clause.sentences[1].negated else long_clause.sentences[1]
                    short_sentence: Sentence = short_clause.sentences[0]
                    if negated_sentence.name == short_sentence.name:
                        if (short_sentence.variables == negated_sentence.variables == sentence.variables) and (short_sentence.literals == negated_sentence.literals == sentence.literals):
                            # here the clauses are of the form: ~p(x) | q(x), p(x)
                            new_sentence: Sentence = Sentence(name=deepcopy(sentence.name),
                                                              identifier=deepcopy(sentence.name),
                                                              variables=deepcopy(sentence.variables),
                                                              literals=deepcopy(sentence.literals))
                            new_clause: Clause = Clause([new_sentence])
                            self.remove_clause(short_clause.get_kb_id())
                            self.remove_clause(long_clause.get_kb_id())
                            self.append(new_clause)
                            pass

    @staticmethod
    def unify(x, y, sub_str: str) -> str:
        """
        Essentially want to replace variables in a Sentence with a literal from another Sentence to create an new Fact.
        :return:
        """
        if sub_str == "failure":
            return ""

        return ""

    @staticmethod
    def unify_variable(expression, variable: str, sub_str: str) -> str:
        value = None
        if f"{variable}/{value}" in sub_str:
            KnowledgeBase.unify(value, expression, sub_str)
        elif f"{expression}/{value}" in sub_str:
            KnowledgeBase.unify(variable, value, sub_str)
        elif KnowledgeBase.occur_check(variable, expression):
            return "failure"
        else:
            return sub_str + f" {variable}/{expression}"

    @staticmethod
    def occur_check(variable, expression) -> bool:
        if str(variable) in str(expression):
            return True
        return False
