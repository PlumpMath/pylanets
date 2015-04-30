from pylanets.highlevel.resources import *


def build_component(comp):
    c = Expense()
    c = c.add(Megacredits(comp['cost']))
    c = c.add(Duranium(comp['duranium']))
    c = c.add(Tritanium(comp['tritanium']))
    c = c.add(Molybdenum(comp['molybdenum']))
    return Goal('Build {}'.format(comp['name']), c)


def build_ship(hull, eng, beams, launchers):
    """ eng, beams, launchers a tuple of the form (comp,count) """
    s = Goal('Build Ship, {}'.format(hull['name']))

    s.add_goal(build_component(hull))
    
    count = eng[1]
    if count is None:
        count = hull['engines']
    for n in range(count):
        s.add_goal(build_component(eng[0]))

    count = beams[1]
    if count is None:
        count = hull['beams']
    for n in range(count):
        s.add_goal(build_component(beams[0]))

    count = launchers[1]
    if count is None:
        count = hull['launchers']
    for n in range(count):
        s.add_goal(build_component(launchers[0]))
    return s


class Goal(object):
    def __init__(self, name, cost=None, goals=None):
        self.name = name
        self._cost = cost or Expense()
        if goals is None:
            self.subgoals = []
        else:
            self.subgoals = goals

    def add_goal(self, goal):
        self.subgoals.append(goal)

    @property
    def cost(self):
        e = self._cost
        for g in self.subgoals:
            e = e.add(g.cost)
        return e

    def __repr__(self):
        return '{}, {}'.format(self.name, self.cost)
