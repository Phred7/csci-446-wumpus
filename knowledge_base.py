

class KnowledgeBase:

    def set_rules(self, kb):
        """
        key:
        s = smell, w = wumpus, b = breeze, p = pit, gl = glimmer, g = gold,
        bu = bump, o = obstacle, (x,y) is coordinate on the board
        Rules:
        (Smell implies wumpus is in adjacent cell) converted to clause form is
        ~s(x,y) | [w(x+1, y) | w(x-1, y) | w(x, y+1) | w(x, y-1)]
        (Breeze implies pit in adjacent cell) converted to clause form is
        ~b(x,y) | [p(x+1, y) | p(x-1, y) | p(x, y+1) | p(x, y-1)]
        (glimmer implies gold in adjacent cell) converted to clause form is
        ~gl(x,y) | [g(x+1, y) | g(x-1, y) | g(x, y+1) | g(x, y-1)]
        (bump implies obstacle which mean you cant move in that direction anymore) converted to clause form is
        ~bu(x,y) | o(x,y)
        (scream implies wumpus is dead in direction you shot)



        """
        pass

    pass