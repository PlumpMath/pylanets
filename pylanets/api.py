import getpass
import os
import os.path
import requests

from collections import (UserDict, UserList)

from pylanets import baseobjects

BASE_URL = 'http://api.planets.nu'
API_KEY_FILE = os.path.join(os.environ['HOME'], '.planets.key')


class Filterable(UserList):
    def __init__(self, owner_id, data):
        UserList.__init__(self, data)
        self._owner_id = owner_id

    def by_player(self, player):
        return [_ for _ in self.data if 'ownerid' in _ and _['ownerid'] == player['raceid']]

    def owned(self):
        return [_ for _ in self.data if 'ownerid' in _ and _['ownerid'] == self._owner_id]


class GameTurn(UserDict):
    def __init__(self, owner_player, data):
        UserDict.__init__(self, data)
        self.owner = owner_player
        self.obj_map = {'planets':   baseobjects.Planet,
                        'starbases': baseobjects.Starbase,
                        'ships':     baseobjects.Ship,
                        'engines':   baseobjects.Engine}

    def __getitem__(self, key):
        if key in self.data and isinstance(self.data[key], list):
            if key in self.obj_map:
                _dat = [self.obj_map[key](self, _) for _ in self.data[key]]
            else:
                _dat = self.data[key]
            return Filterable(self.owner['id'], _dat)
        else:
            return UserDict.__getitem__(self, key)

    def find_component(self, cname, cid):
        try:
            return [_ for _ in self.data[cname] if _['id'] == cid][0]
        except IndexError:
            return None


class PlanetsApi(object):
    def __init__(self):
        self._key = self._obtain_api_key()
        self._player_data = self.player_data()
        self._id  = self._player_data['account']['id']

    def player_data(self):
        return self._get('/account/load', {'apikey': self._key})

    def active_games(self):
        return [_['game'] for _ in self._get('/account/activegames', {'accountid': self._id})['games']]

    def load_turn(self, gameid, turn=None):
        dat = {'gameid': gameid, 'apikey': self._key}
        if turn is not None:
            dat['turn'] = turn
        turn_data = self._get('/game/loadturn', dat)['rst']
        for p in turn_data['players']:
            if p['username'] == self._player_data['account']['username']:
                owner = p
                break
        return GameTurn(owner, turn_data)

    def _get(self, sfx, args):
        rsp = requests.get(BASE_URL+sfx, params=args)
        rsp.raise_for_status()
        try:
            return rsp.json()
        except ValueError as e:
            print('Error parsing response: {}\nRaw:\n-----------\n{}\n------------'.format(e, rsp.text))
            raise

    def _post(self, sfx, args):
        rsp = requests.post(BASE_URL+sfx, data=args)
        rsp.raise_for_status()
        try:
            return rsp.json()
        except ValueError as e:
            print('Error parsing response: {}\nRaw:\n-----------\n{}\n------------'.format(e, rsp.text))
            raise

    def _login(self, user, pword):
        raw = self._post('/account/login', {'username': user, 'password': pword})
        if raw['success']:
            return raw['apikey']
        else:
            raise Exception(raw['error'])

    def _obtain_api_key(self):
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE, 'rb') as keyfile:
                return keyfile.read().strip()
        else:
            # prompt for user/password
            print('No key file found: {}'.format(API_KEY_FILE))
            print('\nFetching new key')
            user = raw_input('\tusername: ')
            pwrd = getpass.getpass('\tpassword: ')

            key = self._login(user, pwrd)
            with open(API_KEY_FILE, 'wb') as keyfile:
                keyfile.write(key.strip())
            return key
