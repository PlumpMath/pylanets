import bz2
import os.path
import pickle

from pylanets.api import PlanetsApi

class Game:
    def __init__(self, name, cachedir='/tmp', reload=False):
        all_games = PlanetsApi().active_games()
        meta = None
        for g in all_games:
            if name == g['name']:
                meta = g
        if meta is None:
            raise Exception('Game {} not found'.format(name))
        
        cache_path = os.path.join(cachedir, str(meta['id']))
        all_data = {'planets': [], 'ships': []}

        for turn_num in range(meta['turn']):
            print('Fetching {0}:{1} turn {2}'.format(meta['id'], meta['name'], turn_num))
            turn_data = PlanetsApi().load_turn(meta['id'], turn_num)
            for _ in turn_data['planets']:
                _['turn'] = turn_num
            all_data['planets'].extend(turn_data['planets'])
            for _ in turn_data['ships']:
                _['turn'] = turn_num
            all_data['ships'].extend(turn_data['ships'])
            break

        self._write_file(os.path.join(cache_path, 'planets.bz2'), all_data['planets'])
        return self._write_file(os.path.join(cache_path, 'ships.bz2'), all_data['ships'])

    def _load_file(self, file_path):
        if os.path.exists(file_path):
            with bz2.open(file_path, 'rb') as infile:
                pass

    def _write_file(self, file_path, data):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        dd = {}
        for entry in data:
            idx = str(entry['turn'])+'-'+str(entry['id'])
            dd[idx] = entry
        dframe = pd.DataFrame(dd)

        with bz2.open(data_path, 'wb') as outfile:
            pickle.dump(dframe, outfile)
        return dframe
