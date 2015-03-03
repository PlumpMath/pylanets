from pylanets.api import PlanetsApi


class Empire(object):
    def __init__(self, turn=None):
        self._turn = turn

    @classmethod
    def from_game(cls, gameid, turn=None):
        api = PlanetsApi()
        return Empire(api.load_turn(gameid, turn))

    def planets(self):
        return self._turn['planets'].owned()

    def starbases(self):
        return self._turn['starbases'].owned()

    def ships(self):
        return self._turn['ships'].owned()
