import curses

from .. import State
from .base import (UI, Panel, PanelState)

class LoadGame(State):
    def run(self, sm):
        api = PlanetsApi()
        games = api.active_games()
        selected = self._games_prompt(games, sm.stdscr)

        sm.empire = None
        if selected is not None:
            try:
                sm.stdscr.addstr('Loading {0[name]}'.format(selected))
                sm.stdscr.refresh()
                sm.empire = Empire.from_game(selected['id'])
                sm.game_name = selected['name']
            except Exception as e:
                print(e)

        return self.next(sm.empire)

    def next(self, input):
        if input is not None:
            return UI.Main
        else:
            return UI.LoadGame

    def _games_prompt(self, games, scr):
        top = 2
        left = 2
        scr.clear()
        scr.border()
        scr.addstr(top, left, 'Select an active game to load')
        game_str1 = '{0}) {1[name]} ({1[id]})'
        game_str2 = 'Turn: {0[turn]}, Next: {0[timetohost]}, {0[shortdescription]}'
        for i,g in enumerate(games):
            scr.addstr(top+2+3*i, left, game_str1.format(i+1, g))
            scr.addstr(top+3+3*i, left+4, game_str2.format(g))
        scr.addstr(top+5+3*i, left, '> ')
        scr.refresh()
        curses.echo()
        game_sel = scr.getstr(2)
        curses.noecho()
        try:
            return games[int(game_sel)-1]
        except Exception:
            return None


class Main(State):
    def run(self, sm):
        buf = 4
        hmid = int((curses.LINES-buf)/2)
        vmid = int(curses.COLS/2)
        sm.stdscr.clear()
        if not hasattr(sm, 'wnd'):
            sm.wnd = []
            sm.wnd.append(Panel(sm.empire, 0, 0, vmid, hmid))
            sm.wnd.append(Panel(sm.empire, vmid, 0, vmid, hmid))
            sm.wnd.append(Panel(sm.empire, 0, hmid, vmid, hmid))
            sm.wnd.append(Panel(sm.empire, vmid, hmid, vmid, hmid))
        curses.panel.update_panels()
        for _ in sm.wnd:
            _.console = sm.console

        next_wnd = 0
        while next_wnd != None:
            next_wnd = sm.wnd[next_wnd].start()
            

class TopLevel(PanelState):
    def draw(self, sm):
        y = self._hcenter(sm)-3
        x = self._wcenter(sm)-10

        sm.wnd.clear()
        sm.wnd.addstr(y+0,x, 'F', curses.color_pair(1)); sm.wnd.addstr('leet Command\n')
        sm.wnd.addstr(y+1,x, 'P', curses.color_pair(1)); sm.wnd.addstr('lanetary Command\n')
        sm.wnd.addstr(y+2,x, 'O', curses.color_pair(1)); sm.wnd.addstr('perations Council\n')
        sm.wnd.addstr(y+3,x, 'I', curses.color_pair(1)); sm.wnd.addstr('ntelligence\n')
        super(TopLevel, self).draw(sm)

    def next(self, input):
        try:
            return {'F': Panel.FleetCommand}[input.upper()]
        except KeyError:
            return self


###########################################################
UI.LoadGame = LoadGame()
UI.Main = Main()

Panel.TopLevel = TopLevel()
