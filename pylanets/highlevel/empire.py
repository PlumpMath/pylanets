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
                'ground':    {'mc':         0,
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

            rsrc['ground']['neutronium'] += p['groundneutronium']
            rsrc['ground']['duranium'] += p['groundduranium']
            rsrc['ground']['tritanium'] += p['groundtritanium']
            rsrc['ground']['molybdenum'] += p['groundmolybdenum']

        rsrc['total']['mc'] = rsrc['available']['mc']
        rsrc['total']['supplies'] = rsrc['available']['supplies']
        rsrc['total']['neutronium'] = rsrc['available']['neutronium']+rsrc['ground']['neutronium']
        rsrc['total']['duranium'] = rsrc['available']['duranium']+rsrc['ground']['duranium']
        rsrc['total']['tritanium'] = rsrc['available']['tritanium']+rsrc['ground']['tritanium']
        rsrc['total']['molybdenum'] = rsrc['available']['molybdenum']+rsrc['ground']['molybdenum']

        return rsrc

    def hulls(self):
        active = self._turn['player']['activehulls'].split(',')
        return sorted([_ for _ in self._turn['hulls'] if str(_['id']) in active], key=lambda x:x['techlevel'])
