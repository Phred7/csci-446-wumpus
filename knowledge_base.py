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

    def query(self, query_sentence: Sentence) -> bool:
        for clause in self.kb:
            if not clause.rule:
                if str(query_sentence) == str(clause):
                    return True
        return False

    def remove_clause(self, clause_kb_id: int) -> None:
        self.kb.remove(self.get_clause(clause_kb_id))
        self.string = ""
        self.clauses -= 1
        for i in range(clause_kb_id, len(self.kb)):
            current_id: int = self.kb[i].get_kb_id()
            self.kb[i].set_kb_id(current_id - 1)

    def get_clause(self, clause_kb_id: int) -> Clause:
        return self.kb[clause_kb_id]

    def get_rules(self) -> List[Clause]:
        rules: List[Clause] = []
        for clause in self.kb:
            if clause.rule:
                rules.append(clause)
        return rules

    def get_facts(self) -> List[Clause]:
        facts: List[Clause] = []
        for clause in self.kb:
            if not clause.rule:
                facts.append(clause)
        return facts

    def infer(self) -> None:
        pass


    def resolution(self) -> bool:
        last_clause: Clause = self.kb[-1]
        resolved: bool = False
        for clause in self.kb:
            if last_clause == clause:
                break
            if (len(last_clause) == 1 and len(clause) == 2) or len(last_clause) == 2 and len(clause) == 1:
                long_clause: Clause = clause if len(clause) == 2 else last_clause
                short_clause: Clause = clause if len(clause) == 1 else last_clause
                if long_clause.sentences[0].negated ^ long_clause.sentences[
                        1].negated:  # this tests to see if both clauses are defined in scope
                    negated_sentence: Sentence = long_clause.sentences[0] if long_clause.sentences[0].negated else \
                        long_clause.sentences[1]
                    sentence: Sentence = long_clause.sentences[0] if long_clause.sentences[1].negated else \
                        long_clause.sentences[1]
                    short_sentence: Sentence = short_clause.sentences[0]
                    if negated_sentence.name == short_sentence.name:
                        if (short_sentence.variables == negated_sentence.variables == sentence.variables) and (
                                short_sentence.literals == negated_sentence.literals == sentence.literals):
                            # here the clauses are of the form: ~p(x, y, z) | q(x, y, z), p(x, y, z)
                            new_sentence: Sentence = Sentence(name=deepcopy(sentence.name),
                                                              identifier=deepcopy(sentence.name),
                                                              variables=deepcopy(sentence.variables),
                                                              literals=deepcopy(sentence.literals))
                            new_clause: Clause = Clause([new_sentence])
                            # self.remove_clause(short_clause.get_kb_id())
                            self.remove_clause(long_clause.get_kb_id())
                            self.append(new_clause)
                            resolved = True
        return resolved if not resolved else self.resolution()  # TODO: may not want recursive feature?

    @staticmethod
    def unify(x, y, *, theta: str = "") -> str:
        """
        Essentially want to replace variables in a Sentence with a literal from another Sentence to create an new Fact.
        :return:
        """
        if theta == "failure":
            return theta
        elif str(x) == str(y):
            return theta
        elif type(x) == str:
            return KnowledgeBase.unify_variable(x, y, theta)
        elif type(y) == str:
            return KnowledgeBase.unify_variable(y, x, theta)
        elif type(x) == Clause and type(y) == Clause:
            x: Clause = x
            y: Clause = y
            return KnowledgeBase.unify(x.sentences, y.sentences, theta=theta)
        elif type(x) == Sentence and type(y) == Sentence:
            x: Sentence = x
            y: Sentence = y
            return KnowledgeBase.unify(x.arguments, y.arguments, theta=theta)
        elif type(x) == list and type(y) == list:
            return KnowledgeBase.unify(x[1:], y[1:], theta=KnowledgeBase.unify(x[0], y[0], theta=theta))
        return "failure"

    @staticmethod
    def unify_variable(expression, variable: str, theta: str) -> str:
        if f"{variable}/" in theta:
            if type(variable) == int:
                variable = str(variable)
            beta: str = theta[theta.index(variable) + 2:]
            value: str = beta[:beta.index("}")]
            return KnowledgeBase.unify(value, expression, theta=theta)
        elif f"{expression}/" in theta:
            beta: str = theta[theta.index(variable) + 2:]
            value: str = beta[:beta.index("}")]
            return KnowledgeBase.unify(variable, value, theta=theta)
        elif KnowledgeBase.occur_check(variable, expression):
            return "failure"
        else:
            expression = expression[:expression.index("+")] if "+" in expression else expression
            expression = expression[:expression.index("-")] if "-" in expression else expression
            expression = expression.strip('')
            return theta + '{' + f"{variable}/{expression}" + '} '

    @staticmethod
    def occur_check(variable, expression) -> bool:
        if str(variable) in str(expression):
            return True
        return False


