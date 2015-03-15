import curses

from .base import (Panel, PanelState)


class FleetCommand(PanelState):
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
            return {}[input.upper()]
        except KeyError:
            return self


###########################################################
Panel.FleetCommand = FleetCommand()
