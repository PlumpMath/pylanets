from UserDict import UserDict


class BaseObject(object, UserDict):
    def __init__(self, turn, data):
        UserDict.__init__(self, data)
        self._turn = turn
        self._fmt_str = None
        if 'ownerid' in self.data:
            self.data['owner'] = self._turn.player_by_id(self.data['ownerid'])

    def __str__(self):
        return self._fmtstr.format(self.data)


class Planet(BaseObject):
    def __init__(self, *args):
        super(Planet, self).__init__(*args)
        if self.data['owner'] is not None:
            self.data['owner_name'] = self.data['owner']['username']
        else:
            self.data['owner_name'] = 'unowned'

        self._fmtstr = 'Planet({0[id]}) [{0[owner_name]}] : {0[name]}, P[{0[clans]}/{0[nativeclans]}], M[{0[totalneutronium]}/{0[totalduranium]}/{0[totaltritanium]}/{0[totalmolybdenum]}]'

        # for some reason these are often 0 in the server data
        self.data['totalneutronium'] = self.data['neutronium'] + self.data['groundneutronium']
        self.data['totalduranium'] = self.data['duranium'] + self.data['groundduranium']
        self.data['totaltritanium'] = self.data['tritanium'] + self.data['groundtritanium']
        self.data['totalmolybdenum'] = self.data['molybdenum'] + self.data['groundmolybdenum']


class Starbase(BaseObject):
    def __init__(self, *args):
        super(Starbase, self).__init__(*args)
        # search for planet we orbit
        p = self._turn.find_component('planets', self.data['planetid'])
        if p is not None:
            self.data['planet'] = p
            self.data['planet_name'] = p['name']
        else:
            raise Exception('Starbase {} orbiting unfindable planet {}'.format(self.data['id'], self.data['planetid']))

        # assign owner by who owns our planet
        self.data['owner'] = self._turn.find_component('players', p['ownerid'])
        self.data['ownerid'] = p['ownerid']
        if self.data['owner'] is not None:
            self.data['owner_name'] = self.data['owner']['username']
        else:
            self.data['ownerid'] = 'unowned'

        self._fmtstr = 'Starbase({0[id]}) [{0[owner_name]}] : {0[planet_name]}, T[{0[hulltechlevel]}/{0[enginetechlevel]}/{0[beamtechlevel]}/{0[torptechlevel]}]'


class Ship(BaseObject):
    def __init__(self, *args):
        super(Ship, self).__init__(*args)
        if self.data['owner'] is not None:
            self.data['owner_name'] = self.data['owner']['username']
        else:
            self.data['owner_name'] = 'unowned'

        # find our hull info
        self.data['hull'] = self._turn.find_component('hulls', self.data['hullid'])
        if self.data['hull'] is not None:
            self.data['hull_name'] = self.data['hull']['name']
        else:
            raise Exception('Ship {} uses unfindable hull {}'.format(self.data['id'], self.data['hullid']))

        # find our engine info
        self.data['engine'] = self._turn.find_component('engines', self.data['engineid'])
        if self.data['engine'] is not None:
            self.data['enginetech'] = self.data['engine']['techlevel']
        else:
            self.data['enginetech'] = '-'

        # find our beam info
        self.data['beam'] = self._turn.find_component('beams', self.data['beamid'])
        if self.data['beam'] is not None:
            self.data['beamtech'] = self.data['beam']['techlevel']
        else:
            self.data['beamtech'] = '-'

        # find our torp info
        self.data['torp'] = self._turn.find_component('torpedos', self.data['torpedoid'])
        if self.data['torp'] is not None:
            self.data['torptech'] = self.data['torp']['techlevel']
        else:
            self.data['torptech'] = '-'

        if self.data['name'].lower() == self.data['hull_name'].lower():
            self.data['name'] = ''

        self._fmtstr = 'Ship({0[id]}) [{0[owner_name]}] : {0[hull_name]}, E{0[enginetech]}/B{0[beamtech]}/T{0[torptech]} "{0[name]}"'
