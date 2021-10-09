from knowledge_base import *
from clause import *
from sentence import *

if __name__ == '__main__':
    kb: KnowledgeBase = KnowledgeBase()
    sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negation=True)
    sentence_3: Sentence = Sentence("wumpus", "w", literals=[0, 0], negation=True)
    clause: Clause = Clause([sentence, sentence_2])
    clause_2: Clause = Clause([sentence_3])
    kb.set_rules([clause, clause_2])
    print("\n\n" + str(kb))
