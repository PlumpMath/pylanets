from pylanets.highlevel.resources import *


def build_component(comp):
    c = Expense()
    c = c.add(Megacredits(comp['cost']))
    c = c.add(Duranium(comp['duranium']))
    c = c.add(Tritanium(comp['tritanium']))
    c = c.add(Molybdenum(comp['molybdenum']))
    return Goal('Build {}'.format(comp['name']), c)


class Goal(object):
    def __init__(self, name, cost):
        self.name = name
        self._cost = cost
        self.subgoals = []

    @property
    def cost(self):
        e = self._cost
        for g in self.subgoals:
            e = e.add(g.cost)
        return e
