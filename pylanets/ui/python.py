import sys
from datetime import datetime

from pylanets.api import PlanetsApi
from pylanets.highlevel import Empire
from pylanets.ui import StateMachine, State, TerminateState


def clrscr():
    sys.stderr.write("\x1b[2J\x1b[H")


class LoadGame(State):
    def run(self, sm):
        api = PlanetsApi()
        games = api.active_games()
        selected = self._games_prompt(games)

        sm.empire = None
        if selected is not None:
            try:
                print('\nLoading {}'.format(selected['name']))
                sm.empire = Empire.from_game(selected['id'])
                sm.game_name = selected['name']
            except Exception as e:
                print(e)

        return self.next(sm.empire)

    def next(self, input):
        if input is not None:
            return UI.MainMenu
        else:
            return UI.LoadGame

    def _games_prompt(self, games):
        print('\nSelect an active game to load')
        for i,g in enumerate(games):
            print('{0}) {1[name]} ({1[id]})\n\tTurn: {1[turn]}, Next: {1[timetohost]}, {1[shortdescription]}'.format(i+1, g))
        game_sel = raw_input(' > ').strip()
        try:
            return games[int(game_sel)-1]
        except Exception:
            return None


class MainMenu(State):
    def run(self, sm):
        clrscr()
        print(sm.game_name)
        print(' 1) Show ships')
        print(' 2) Show planets')
        print(' 3) Show starbases')
        sel = raw_input('\n> ').strip()

    def next(self, input):
        return TerminateState


class UI(StateMachine):
    def __init__(self):
        super(UI, self).__init__(UI.LoadGame)


UI.LoadGame = LoadGame()
UI.MainMenu = MainMenu()
