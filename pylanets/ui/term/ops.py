import curses

from .base import (Panel, BasePanelState)
from .util import dialog


class OpsCouncil(BasePanelState):
    def draw(self, sm):
        y = self._hcenter(sm)-3
        x = self._wcenter(sm)-8

        sm.wnd.clear()
        sm.wnd.addstr(y+0,x, 'S', curses.color_pair(1)); sm.wnd.addstr('upply Routes')
        sm.wnd.addstr(y+1,x, 'M', curses.color_pair(1)); sm.wnd.addstr('ission Design')
        sm.wnd.addstr(y+2,x, 'E', curses.color_pair(1)); sm.wnd.addstr('mpire Analysis')
        super(OpsCouncil, self).draw(sm)

    def next(self, input):
        try:
            return {'E': Panel.Ops_EmpireAnalysis}[input.upper()]
        except KeyError:
            pass


class EmpireAnalysis(BasePanelState):
    def draw(self, sm):
        rsrc = sm.empire.resources()
        y,x = (1,1)
        sm.wnd.clear()

        sm.wnd.addstr(y+0,x, 'Neu| {}{} | {}{}'.format('\u2191', rsrc['available']['neutronium'], '\u2193', rsrc['ground']['neutronium']))
        sm.wnd.addstr(y+1,x, 'Dur| {}{} | {}{}'.format('\u2191', rsrc['available']['duranium'], '\u2193', rsrc['ground']['duranium']))
        sm.wnd.addstr(y+2,x, 'Tri| {}{} | {}{}'.format('\u2191', rsrc['available']['tritanium'], '\u2193', rsrc['ground']['tritanium']))
        sm.wnd.addstr(y+3,x, 'Mol| {}{} | {}{}'.format('\u2191', rsrc['available']['molybdenum'], '\u2193', rsrc['ground']['molybdenum']))

        super(EmpireAnalysis, self).draw(sm)


###########################################################
Panel.OpsCouncil = OpsCouncil()
Panel.Ops_EmpireAnalysis = EmpireAnalysis()
