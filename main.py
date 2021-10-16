import threading
from threading import Thread

import rational_explorer
from knowledge_base import *
from clause import *
from sentence import *
from board import *
from rational_explorer import *
from datetime import datetime

def explore(explorer: RationalExplorer) -> int:
    """
    Used to run this explorer on it's board.
    :return:
    """

    return 0


if __name__ == '__main__':
    # Threading:
    # board_sizes: List[int] = [5, 10, 15, 20, 25]
    #
    # for size in board_sizes:
    #     threads: List[Thread] = []
    #     thread_count: int = 25
    #     for i in range(0, thread_count):
    #         board: Board = Board(size)
    #         rational: RationalExplorer = RationalExplorer(deepcopy(board))
    #         threads.append(threading.Thread(target=explore, args=(deepcopy(rational),),
    #                                         name=f"rational_explorer_thread{i}"))
    #     for thread in threads:
    #         thread.start()
    #     print(f"Threads 0-{thread_count - 1} started")
    #     for thread in threads:
    #         Thread.join(thread)
    #         #Thread._
    #     print(f"Threads 0-{thread_count - 1} joined")

    # Example Unification:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("foo", "f", variables=["x+1"])
    # clause: Clause = Clause([sentence])
    # sentence_2: Sentence = Sentence("foo", "f", literals=[0])
    # clause_2: Clause = Clause([sentence_2])
    # knowledge_base.set_rules([clause, clause_2])
    # print(knowledge_base)
    # print(f"unified: {knowledge_base.unify(knowledge_base.get_clause(0), knowledge_base.get_clause(1))}\n")

    # Example Unification 2:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    # sentence: Sentence = Sentence("foo", "f", variables=["x", "y"])
    # clause: Clause = Clause([sentence])
    # sentence_2: Sentence = Sentence("foo", "f", literals=[1, 2])
    # clause_2: Clause = Clause([sentence_2])
    # knowledge_base.set_rules([clause, clause_2])
    # print(f"unified: {knowledge_base.unify(knowledge_base.get_clause(0), knowledge_base.get_clause(1))}\n")
    # print(knowledge_base)

    # Example Resolution:
    # knowledge_base: KnowledgeBase = KnowledgeBase()
    #
    # sentence: Sentence = Sentence("p", "p", variables=["x"], negated=True)
    # sentence_2: Sentence = Sentence("q", "q", variables=["x"])
    # clause: Clause = Clause([sentence, sentence_2])
    # sentence_3: Sentence = Sentence("p", "p", variables=["x"])
    # clause_2: Clause = Clause([sentence_3])
    # knowledge_base.set_rules([clause, clause_2])
    #
    # print(knowledge_base)
    # print("resolving...")
    # knowledge_base.resolution()
    # print(knowledge_base)

    # # board generation verification
    # board: Board = Board(size=5)
    # board.generate_board()
    # print(board)


    # Example Rational:
    # board: Board = Board(size=5)
    # board.generate_board()
    # print(board)
    # print()
    # rational: RationalExplorer = RationalExplorer(board)
    # # print(f"initial KB:\n{rational.knowledge_base}")
    # while (not rational.is_dead) and (not rational.has_gold):
    #     rational.act()
    #     print(rational)
    #     print()
    # if rational.has_gold:
    #     print("Found gold")
    # else:
    #     print("Big Dead")
    # print(rational)
    # print(rational.board)
    # print("Exiting")

    # More rigorous rational testbed:
    numCaves = 30
    boardSizes = [5, 10, 15, 20, 25]
    for boardSize in boardSizes:
        numGold = 0
        numDeaths = 0
        numWump = 0
        numPit = 0
        numOld = 0
        for i in range(numCaves):
            start = datetime.now()
            b = Board(boardSize)
            b.generate_board()
            e = rational_explorer.RationalExplorer(b)
            while not e.is_dead and not e.has_gold:
                e.act()
            if e.is_dead:
                numDeaths += 1
            if e.has_gold:
                numGold += 1

            x = e.location[0]
            y = e.location[1]

            if e.board.grid[x][y][CellContent.WUMPUS]:
                numWump += 1
            if e.board.grid[x][y][CellContent.PIT]:
                numPit += 1
            if e.max_age <= e.actions_taken:
                numOld += 1

            end = datetime.now()

            print("Finished cave", i, "in", end - start, "      " + ("X" if e.is_dead else "G"))
        print("Board size:                  " + str(boardSize) + "x" + str(boardSize))
        print("Number of runs:             ", numCaves)
        print("Number of times gold found: ", numGold)
        print("Number of times died:       ", numDeaths)
        print("Success rate:               ", numGold / numCaves)
        print("Deaths from old age:        ", numOld / numCaves)
        print("Deaths from pit:            ", numPit / numCaves)
        print("Deaths from wumpus:         ", numWump / numCaves)
        print()


    # rational.knowledge_base.append(Clause([Sentence('stench', 's', literals=[0, 1], negated=False)]))
    # rational.knowledge_base.infer()
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.resolution()
    # print(print("kb after", rational.knowledge_base))

    # print(f"{rational.board.__class__.__name__}:\n{rational.board}")
    # print(rational.knowledge_base)
    # rules: List[Clause] = rational.knowledge_base.get_rules()
    # sentence: Sentence = rational.knowledge_base.kb[-1].sentences[0]
    # for rule in rules:
    #     if rule.sentences[0].name == sentence.name:
    #         theta: str = KnowledgeBase.unify(sentence, rule.sentences[0])
    #         if theta != "failure":
    #             #print(f"theta: {theta}")
    #             sentences: List[Sentence] = []
    #             for i in range(1, len(rule)):
    #                 args: List[str] = []
    #                 for arg in rule.sentences[i].variables:
    #                     beta: List[str] = theta.split(' ')
    #                     beta = beta[:-1]
    #                     #print(f"beta: {beta}")
    #                     for substring in beta:
    #                         #print(f"substring: {substring}")
    #                         substring = substring.strip('{').strip('}')
    #                         val: str = substring[:substring.index("/")]
    #                         var: str = substring[substring.index("/")+1:]
    #                         #print(f"val: {val}\nvar: {var}")
    #                         if var in arg:
    #                             new_arg: str = arg.replace(var, val)
    #                             args.append(new_arg)
    #                 sentences.append(Sentence(rule.sentences[1].name, rule.sentences[1].identifier, variables=args))
    #             rational.knowledge_base.append(Clause(sentences))
    # print(rational.knowledge_base)
    #
    # #resolution example 1
    # #print(rational.knowledge_base)
    # rules: List[Clause] = rational.knowledge_base.get_rules()
    # #conclusion = Clause([Sentence('stench', 'w', literals=[2, 2], negated=True)])
    # #print("before c", conclusion)
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[1, 0], negated=True)]))
    # print("kb ",rational.knowledge_base)
    # # conclusion = conclusion.negate()
    # # print("c", conclusion)
    # kb: List[Clause] = rational.knowledge_base.get_facts()
    # #conclusion = kb[1]
    # #print('conclusion ',conclusion)
    # for fact in kb:
    #     # print()
    #     # print("c ", clause)
    #     # print()
    #     if len(fact) != 1:
    #         #print("in")
    #         conclusion = fact
    #         for clause in kb:
    #             #print("s ",sentence)
    #             # x
    #             copy_clause = deepcopy(clause)
    #             copy_clause.negate()
    #             for stm in conclusion.sentences:
    #                 # print("clause2 ", clause)
    #                 # print("stm", stm)
    #                 #print("before negate", clause)
    #                 #print("after negate", str(clause))
    #                 if copy_clause.negated and copy_clause.sentences[0].negated:
    #                     copy_clause.sentences[0].negate()
    #                     copy_clause.negate()
    #                     #print("after negate2", str(clause))
    #                 print("comparison", stm, "==", copy_clause)
    #                 if str(stm) == str(copy_clause):
    #                     #print("comparison", stm, "==", clause)
    #                     conclusion.remove(stm)
    #                     #conclusion.negate()
    #                     conclusion.string = ""
    #                     rational.knowledge_base.string = ""
    #                     print("conc ", conclusion)
    #
    # print("kb after",rational.knowledge_base)
    #                 # negated_sentence = "~" + str(clause.sentences[0])
    #                 # print("comparison", stm, "==", negated_sentence)
    #                 # #print("negated",negated_sentence[:negated_sentence.index("(")-1:])
    #                 # if negated_sentence[:negated_sentence.index("(")-1:] == "~~":
    #                 #     #print("in")
    #                 #     negated_sentence = negated_sentence.replace("~", "")
    #                 # print("comparison2", stm, "==", negated_sentence)
    #                 # if str(stm) == str(negated_sentence):
    #                 #     pass
    #                         #conclusion.remove(stm)
    #         #if conclusion contradicts sentence

    # #print(f"{rational.board.__class__.__name__}:\n{rational.board}")
    # #print(rational.knowledge_base)
    # rules: List[Clause] = rational.knowledge_base.get_rules()
    # sentence: Sentence = rational.knowledge_base.kb[-1].sentences[0]
    # for rule in rules:
    #     if rule.sentences[0].name == sentence.name:
    #         theta: str = KnowledgeBase.unify(sentence, rule.sentences[0])
    #         if theta != "failure":
    #             #print(f"theta: {theta}")
    #             sentences: List[Sentence] = []
    #             for i in range(1, len(rule)):
    #                 args: List[str] = []
    #                 for arg in rule.sentences[i].variables:
    #                     beta: List[str] = theta.split(' ')
    #                     beta = beta[:-1]
    #                     #print(f"beta: {beta}")
    #                     for substring in beta:
    #                         #print(f"substring: {substring}")
    #                         substring = substring.strip('{').strip('}')
    #                         val: str = substring[:substring.index("/")]
    #                         var: str = substring[substring.index("/")+1:]
    #                         #print(f"val: {val}\nvar: {var}")
    #                         if var in arg:
    #                             new_arg: str = arg.replace(var, val)
    #                             args.append(new_arg)
    #                 sentences.append(Sentence(rule.sentences[1].name, rule.sentences[1].identifier, variables=args))
    #             rational.knowledge_base.append(Clause(sentences))
    # print(rational.knowledge_base)
    #
    # #resolution example 1
    # #print(rational.knowledge_base)
    # rules: List[Clause] = rational.knowledge_base.get_rules()
    # #conclusion = Clause([Sentence('stench', 'w', literals=[2, 2], negated=True)])
    # #print("before c", conclusion)
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('wumpus', 'w', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('pit', 'p', literals=[1, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 0], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[0, 1], negated=True)]))
    # rational.knowledge_base.append(Clause([Sentence('gold', 'g', literals=[1, 0], negated=True)]))
    # print("kb ",rational.knowledge_base)
    # # conclusion = conclusion.negate()
    # # print("c", conclusion)
    # kb: List[Clause] = rational.knowledge_base.get_facts()
    # #conclusion = kb[1]
    # #print('conclusion ',conclusion)
    # for fact in kb:
    #     # print()
    #     # print("c ", clause)
    #     # print()
    #     if len(fact) != 1:
    #         #print("in")
    #         conclusion = fact
    #         for clause in kb:
    #             #print("s ",sentence)
    #             # x
    #             copy_clause = deepcopy(clause)
    #             copy_clause.negate()
    #             for stm in conclusion.sentences:
    #                 # print("clause2 ", clause)
    #                 # print("stm", stm)
    #                 #print("before negate", clause)
    #                 #print("after negate", str(clause))
    #                 if copy_clause.negated and copy_clause.sentences[0].negated:
    #                     copy_clause.sentences[0].negate()
    #                     copy_clause.negate()
    #                     #print("after negate2", str(clause))
    #                 print("comparison", stm, "==", copy_clause)
    #                 if str(stm) == str(copy_clause):
    #                     #print("comparison", stm, "==", clause)
    #                     conclusion.sentences.remove(stm)
    #                     #conclusion.negate()
    #                     conclusion.string = ""
    #                     rational.knowledge_base.string = ""
    #                     print("conc ", conclusion)
    #
    # print("kb after",rational.knowledge_base)


                    # negated_sentence = "~" + str(clause.sentences[0])
                    # print("comparison", stm, "==", negated_sentence)
                    # #print("negated",negated_sentence[:negated_sentence.index("(")-1:])
                    # if negated_sentence[:negated_sentence.index("(")-1:] == "~~":
                    #     #print("in")
                    #     negated_sentence = negated_sentence.replace("~", "")
                    # print("comparison2", stm, "==", negated_sentence)
                    # if str(stm) == str(negated_sentence):
                    #     pass
                            #conclusion.remove(stm)
            #if conclusion contradicts sentence





    # Example KB:
    # kb: KnowledgeBase = KnowledgeBase()
    #
    # sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    # sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negated=True)
    # clause: Clause = Clause([sentence, sentence_2])
    # kb.set_rules([clause])
    #
    # sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negated=True)
    # sentence_4: Sentence = Sentence("test", "t", variables=["10-1", "20+3"])
    # clause_2: Clause = Clause([sentence_3])
    # clause_3: Clause = Clause([sentence_4])
    # kb.append(clause_2)
    # kb.append(clause_3)
    # print("\n\n" + str(kb))
    #
    # query: Sentence = Sentence("test", "t", variables=["10", "256"])
    # print(f"Query: {kb.query(query)}")

