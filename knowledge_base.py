from clause import *
from sentence import *


class KnowledgeBase:
    """
    Representation of a KnowledgeBase
    """

    def __init__(self, n: int) -> None:
        self.kb: List[Clause] = []
        self.clauses: int = 0
        self.string: str = ""
        self.kb_init: bool = False
        self.new_clauses_are_new: bool = False
        self._n = n

    def __str__(self) -> str:
        """
        Creates the string representation of this KnowledgeBase.
        This method is memoized. Ie. KnowledgeBase stores a copy of the value returned from this method.
        If this KnowledgeBase is not altered when called this method will simply return that string rather than generate the
        same string again.
        :return: str representation of this KnowledgeBase.
        """
        if self.string == "":
            string = f"{self.__class__.__name__}:\n"
            for clause in self.kb:
                if len(clause) == 0:
                    self.remove_clause(clause.kb_id)
                else:
                    string += f"{str(clause)}\n"
            self.string = string
        return self.string

    def set_rules(self, rules: List[Clause]) -> None:
        """
        Sets the rules of this KnowledgeBase.
        :param rules: List of Clauses.
        :return: None.
        """
        if self.kb_init is True:
            raise IOError("Knowledge Base can only be initialized once. Call append() to add more clauses to this KB.")
        for rule in rules:
            rule.set_kb_id(self.clauses)
            rule.set_rule()
            rule.new = False
            self.kb.append(rule)
            self.clauses += 1
        self.kb_init = True

    def append(self, item: Clause) -> None:
        """
        Appends a clause to this KnowledgeBase. This Clause should be a fact rather than a rule.
        :param item: Clause to add to this KnowledgeBase
        :return: None.
        """
        if self.kb_init is False:
            raise IOError("Knowledge Base has not been initialized. Call set_rules() to initialize this KB.")
        item.set_kb_id(self.clauses)
        if self.new_clauses_are_new:
            item.new = True
        self.string = ""
        self.clauses += 1
        self.kb.append(item)

    def query_in(self, query_sentence: Sentence) -> List[Clause]:
        """
        Searches this KnowledgeBase for a Sentence within a Clause. This Sentence must not be the only sentence in
        this Clause. All Clauses with a instance of this Sentence will be returned as a List of Clauses.
        :param query_sentence: Sentence to search this KnowledgeBase for.
        :return: List of Clauses with instances of query sentence.
        """
        clause_list: List[Clause] = []
        for clause in self.kb:
            if not clause.rule:
                for sentence in clause.sentences:
                    if str(query_sentence) in str(sentence) and not str(query_sentence) == str(
                            clause) and query_sentence.negated == sentence.negated:
                        clause_list.append(clause)
        return clause_list

    def query_equal(self, query_sentence: Sentence) -> List[Clause]:
        """
        Searches this KnowledgeBase for a Sentence. This Sentence must be the only Sentence in a Clause.
        All Clauses that match this pattern are returned as a List of Clauses.
        :param query_sentence: Sentence to search this KnowledgeBase for.
        :return: List of Clauses with an instance of query_sentence and patching the pattern.
        """
        clause_list: List[Clause] = []
        for clause in self.kb:
            if not clause.rule:
                if str(query_sentence) == str(clause):
                    clause_list.append(clause)
        return clause_list

    def remove_clause(self, clause_kb_id: int) -> None:
        """
        Removes a Clause from this KnowledgeBase based on the Clause's kb_id. The kb_id of all following Clauses must then be updated.
        :param clause_kb_id: int representing the Clause to remove from this KnowledgeBase.
        :return: None.
        """
        self.kb.remove(self.get_clause(clause_kb_id))
        self.string = ""
        self.clauses -= 1
        for i in range(clause_kb_id, len(self.kb)):
            current_id: int = self.kb[i].get_kb_id()
            self.kb[i].set_kb_id(current_id - 1)

    def remove_sentence(self, clause: Clause, sentence: Sentence) -> None:
        """
        Removes a Sentence from a Clause in this KnowledgeBase. This Sentence sentence must be in this Clause clause to be removed from clause.
        :param clause: Clause to remove sentence from.
        :param sentence: Sentence to remove from clause.
        :return: None.
        """
        self.string = ""
        clause.remove(sentence)
        if len(clause) == 0:
            self.remove_clause(clause.kb_id)

    def get_clause(self, clause_kb_id: int) -> Clause:
        """
        Gets a Clause in this KnowledgeBase based on it's kb_id.
        :param clause_kb_id: int representation of a Clause in this KnowledgeBase.
        :return: Clause with the kb_id clause_kb_id.
        """
        return self.kb[clause_kb_id]

    @property
    def rules(self) -> List[Clause]:
        """
        A property of KnowledgeBase that maintains a List of the Rules of this KnowledgeBase.
        :return: List of Clause in this KnowledgeBase that are rules.
        """
        rules: List[Clause] = []
        for clause in self.kb:
            if clause.rule:
                rules.append(clause)
        return rules

    def facts(self) -> List[Clause]:
        """
        A List of Clauses in this KnowledgeBase that are not rules.
        :return: List of Clauses in this KnowledgeBase that are facts.
        """
        facts: List[Clause] = []
        for clause in self.kb:
            if not clause.rule:
                facts.append(clause)
        return facts

    def new_facts(self) -> List[Clause]:
        """
        A List of Clauses in this KnowledgeBase that are facts and are considered new facts in the KnowledgeBase.
        :return: List of Clauses in this KnowledgeBase that are new facts.
        """
        new_facts: List[Clause] = []
        for clause in self.kb:
            if clause.new:
                new_facts.append(clause)
        return new_facts

    def infer(self) -> None:
        """
        Implements Unification and Resolution to generate new facts from the current facts and rules in this KnowledgeBase.
        :return: None.
        """
        new_facts: List[Clause] = deepcopy(self.new_facts())
        self.new_clauses_are_new = False
        for fact in new_facts:
            self.generate_facts_from_senses(fact)
            fact.new = False
        self.resolution()
        self.new_clauses_are_new = True
        pass

    def resolution(self) -> None:
        kb = self.facts()
        for fact in kb:
            # print()
            # print("c ", clause)
            # print()
            if len(fact) != 1:
                # print("in")
                conclusion = fact
                for clause in self.facts():
                    # print("s ",sentence)
                    # x
                    copy_clause = deepcopy(clause)
                    if len(copy_clause) == 0:
                        self.string = ""
                        continue
                    copy_clause.negate()
                    for stm in conclusion.sentences:
                        # print("clause2 ", clause)
                        # print("stm", stm)
                        # print("before negate", clause)
                        # print("after negate", str(clause))
                        if copy_clause.negated and copy_clause.sentences[0].negated:
                            copy_clause.sentences[0].negate()
                            copy_clause.negate()
                            # print("after negate2", str(clause))
                        # print("comparison", stm, "==", copy_clause)
                        if str(stm) == str(copy_clause):
                            # print("comparison", stm, "==", clause)
                            self.remove_sentence(conclusion, stm)
        pass

    @staticmethod
    def unify(x, y, *, theta: str = "") -> str:
        """
        Direct implementation of Unification.
        Unifies the variables and literals in x and y.
        :param x: An Expression. An Expression can be a Clause, Sentence, a list of variables, literals or functions, or a variable, literal, or function.
        :param y: An Expression.
        :param theta: substitution string thus far. Defaults to the empty string.
        :return: str substitution string that represents how to equal the variables and literals in x and y.
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
        """
        :param expression: An Expression to unify with the Variable variable.
        :param variable: A Variable to unify with the Expression expression.
        :param theta: The current substring calculated through Unification.
        :return: The value of theta, the unification substitution string, updated in this method.
        """
        # if f"{variable}/" in theta:
        #     if type(variable) == int:
        #         variable = str(variable)
        #     beta: str = theta[theta.index(variable) + 2:]
        #     value: str = beta[:beta.index("}")]
        #     return KnowledgeBase.unify(value, expression, theta=theta)
        if f"{expression}/" in theta:
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
        """
        Checks to see if this variable is in this expression.
        :param variable: Variable to check is in an Expression.
        :param expression: An Expression to check if a Variable is in.
        :return: True if variable is in expression. Otherwise False.
        """
        if str(variable) in str(expression):
            return True
        return False

    def generate_facts_from_senses(self, fact: Clause) -> None:
        """
        Method that implements unification to generate new facts from the newest facts in this KnowledgeBase and from this KnowledgeBase's Rules.
        :param fact: A Clause in this KnowledgeBase that is considered new. Checks to see if fact can be unified with any rule in this KnowledgeBase to generate a new Clause that is a fact.
        :return: None.
        """
        rules: List[Clause] = self.rules
        fact_sentence: Sentence = fact.sentences[0]
        for rule in rules:
            if rule.sentences[0].name == fact_sentence.name:
                theta: str = KnowledgeBase.unify(fact_sentence, rule.sentences[0])
                if theta != "failure":
                    sentences: List[Sentence] = []
                    for i in range(1, len(rule)):
                        args: List[str] = []
                        for arg in rule.sentences[i].variables:
                            beta: List[str] = theta.split(' ')
                            beta = beta[:-1]
                            for substring in beta:
                                substring = substring.strip('{').strip('}')
                                val: str = substring[:substring.index("/")]
                                var: str = substring[substring.index("/") + 1:]
                                if var in arg:
                                    new_arg: str = arg.replace(var, val)
                                    args.append(new_arg)
                        sentences.append(Sentence(rule.sentences[1].name, rule.sentences[1].identifier, variables=args))

                    remove: List[int] = []

                    for new_sentence in sentences:
                        new_sentence.string = ""
                        invalid: bool = False
                        str(new_sentence)
                        for arg in new_sentence.arguments:
                            arg = str(eval(arg)) if '-' in arg or '+' in arg else arg
                            if '-' in arg or arg.isdigit():
                                if int(arg) < 0 or int(arg) >= self._n:
                                    invalid = True
                        if invalid:
                            remove.append(sentences.index(new_sentence))
                    remove.reverse()
                    for rem in remove:
                        sentences.pop(rem)
                    if fact_sentence.negated == rule.sentences[0].negated:
                        for sentence in sentences:
                            sentence.negate()
                            self.append(Clause([sentence]))
                    else:
                        self.append(Clause(sentences))
