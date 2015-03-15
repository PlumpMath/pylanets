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

    def resources(self):
        """ available - above ground or on ships
            total     - available + unmined """
        rsrc = {'available': {'mc':         0,
                              'supplies':   0,
                              'neutronium': 0,
                              'duranium':   0,
                              'tritanium':  0,
                              'molybdenum': 0},
                'total':     {'neutronium': 0,
                              'duranium':   0,
                              'tritanium':  0,
                              'molybdenum': 0}}
        # ships
        for s in self.ships():
            rsrc['available']['mc'] += s['megacredits']
            rsrc['available']['supplies'] += s['supplies']
            rsrc['available']['neutronium'] += s['neutronium']
            rsrc['available']['duranium'] += s['duranium']
            rsrc['available']['tritanium'] += s['tritanium']
            rsrc['available']['molybdenum'] += s['molybdenum']
        # planets
        for p in self.planets():
            rsrc['available']['mc'] += p['megacredits']
            rsrc['available']['supplies'] += p['supplies']
            rsrc['available']['neutronium'] += p['neutronium']
            rsrc['available']['duranium'] += p['duranium']
            rsrc['available']['tritanium'] += p['tritanium']
            rsrc['available']['molybdenum'] += p['molybdenum']

            rsrc['total']['neutronium'] += p['groundneutronium']
            rsrc['total']['duranium'] += p['groundduranium']
            rsrc['total']['tritanium'] += p['groundtritanium']
            rsrc['total']['molybdenum'] += p['groundmolybdenum']

        rsrc['total']['mc'] = rsrc['available']['mc']
        rsrc['total']['supplies'] = rsrc['available']['supplies']
        rsrc['total']['neutronium'] += rsrc['available']['neutronium']
        rsrc['total']['duranium'] += rsrc['available']['duranium']
        rsrc['total']['tritanium'] += rsrc['available']['tritanium']
        rsrc['total']['molybdenum'] += rsrc['available']['molybdenum']

        return rsrc
