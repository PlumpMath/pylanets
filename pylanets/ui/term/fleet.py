import curses

from .base import (Panel, BasePanelState)
from .util import dialog
from ...filters import shipfilters


class FleetCommand(BasePanelState):
    def draw(self, sm):
        y = self._hcenter(sm)-3
        x = self._wcenter(sm)-8

        sm.wnd.clear()
        sm.wnd.addstr(y+0,x, 'I', curses.color_pair(1)); sm.wnd.addstr('nventory')
        sm.wnd.addstr(y+1,x, 'S', curses.color_pair(1)); sm.wnd.addstr('hipyard')
        sm.wnd.addstr(y+2,x, 'F', curses.color_pair(1)); sm.wnd.addstr('leet Operations')
        super(FleetCommand, self).draw(sm)

    def next(self, input):
        try:
            return {'I': Panel.Fleet_Inventory}[input.upper()]
        except KeyError:
            return self


class Inventory(BasePanelState):
    def __init__(self):
        super(Inventory, self).__init__()
        self.ship_filter = None

    def draw(self, sm):
        y,x = (1,1)
        sm.wnd.clear()
        # ship list
        for i,shp in enumerate(filter(self.ship_filter, sm.empire.ships())):
            sm.wnd.addstr(y,x, '{0:>3}: {1[name]}\n'.format(i+1,shp))
            y += 1
            if y > self._height(sm)-4:
                break

        # input area
        sm.wnd.addstr(self._height(sm)-2,2, 'F', curses.color_pair(1))
        sm.wnd.addstr('/'); sm.wnd.addstr('S', curses.color_pair(1))

        super(Inventory, self).draw(sm)

    def next(self, input):
        if input.upper() == 'F':
            self.input_fn = self._input_filter

    def _input_filter(self, sm):
        w = dialog('Filter', sm.wnd, 6, 10, [(' R', curses.color_pair(1), 'ole'),
                                             (' H', curses.color_pair(1), 'ull')])
        input = w.getkey()
        del w
        if input.upper() == 'R':
            w = dialog('Filter: Role', sm.wnd, 10, 20,
                    [(' C', curses.color_pair(1), 'ombat Vessel'),
                     ('   Lar', 'g', curses.color_pair(1), 'e Warship'),
                     ('   S', 'm', curses.color_pair(1), 'all Warship'),
                     (' T', curses.color_pair(1), 'ransport'),
                     ('   L', curses.color_pair(1), 'arge Transport'),
                     ('   S', curses.color_pair(1), 'mall Transport'),
                     (' S', 'p', curses.color_pair(1), 'ecial')])
            input = w.getkey()
            try:
                self.ship_filter = {'C': shipfilters.combat,
                                    'G': shipfilters.combat_large,
                                    'M': shipfilters.combat_small,
                                    'T': shipfilters.transport,
                                    'L': shipfilters.transport_large,
                                    'S': shipfilters.transport_small,
                                    'P': shipfilters.special}[input.upper()]
            except KeyError:
                self.ship_filter = None

        self.input_fn = None


###########################################################
Panel.FleetCommand = FleetCommand()
Panel.Fleet_Inventory = Inventory()
