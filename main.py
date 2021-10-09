from knowledge_base import *
from clause import *
from sentence import *

if __name__ == '__main__':
    kb: KnowledgeBase = KnowledgeBase()
    sentence: Sentence = Sentence("wumpus", "w", variables=['x', 'y'])
    sentence_2: Sentence = Sentence("wumpus", "w", variables=['y', 'z'], negation=True)
    clause: Clause = Clause([sentence, sentence_2])
    kb.set_rules([clause])
    print("\n\n" + str(kb))
