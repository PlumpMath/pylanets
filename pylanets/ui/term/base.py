import curses
import curses.panel

from pylanets.ui import StateMachine, State, TerminateState


class Console():
    def __init__(self, y, x, height, width):
        self.scr = curses.newwin(width,height,y,x)
        self.panel = curses.panel.new_panel(self.scr)
        self.msg_buf = ['','']
        self.counter = 0
        self.draw()

    def log(self, msg):
        if self.msg_buf[0] == '':
            self.msg_buf[0] = msg
        elif self.msg_buf[1] == '':
            self.msg_buf[1] = msg
        else:
            self.msg_buf[0] = self.msg_buf[1]
            self.msg_buf[1] = msg
            self.counter += 1
        self.draw()

    def draw(self):
        self.scr.clear()
        self.scr.addstr(1,1, '{}: {}'.format(self.counter, self.msg_buf[0]))
        self.scr.addstr(2,1, '{}: {}'.format(self.counter+1, self.msg_buf[1]))
        self.scr.border()
        self.scr.refresh()

class BasePanelState(State):
    def __init__(self):
        self.input_fn = None

    def run(self, sm):
        if not hasattr(self, 'last_state'):
            self.last_state = self
        self.console = sm.console
        self.draw(sm)
        self.handle_input(sm)  # calls next

    def draw(self, sm):
        sm.wnd.border()

    def handle_input(self, sm):
        if self.input_fn is not None:
            self.input_fn(sm)
        else:
            sm.wnd.hline(self._height(sm)-3, 1, curses.ACS_HLINE, self._width(sm)-2)
            sm.wnd.addstr(self._height(sm)-2, self._width(sm)-10, '[')
            sm.wnd.addstr('H', curses.color_pair(1))
            sm.wnd.addstr('ome|')
            sm.wnd.addstr('U', curses.color_pair(1))
            sm.wnd.addstr('p]')
            sm.wnd.move(self._height(sm)-2, 1)
            sm.wnd.refresh()
            ch = sm.wnd.getkey()

            # Home/Up handling
            if ch.upper() == 'H':
                sm.state_stack = [Panel.TopLevel]
            elif ch.upper() == 'U':
                sm.state_stack = sm.state_stack[:-1]
                if len(sm.state_stack) == 0:
                    sm.state_stack.append(Panel.TopLevel)

            # panel switch handling
            else:
                if ord(ch) == 9:  # tab
                    ch = str(((sm.next_wnd+1)%4)+1)
                try:
                    n = int(ch)
                    if n > 0 and n < 5:
                        self._clear_input_area(sm)
                        sm.next_wnd = n-1
                        sm.state_stack.append(TerminateState())
                except ValueError:
            # send to child to handle
                    n = self.next(ch)
                    if n is not None:
                        sm.state_stack.append(n)

    def _clear_input_area(self, sm):
        sm.wnd.addstr(self._height(sm)-3,1, '')
        sm.wnd.clrtoeol()
        sm.wnd.addstr(self._height(sm)-2,1, '')
        sm.wnd.clrtoeol()
        sm.wnd.border()
        sm.wnd.refresh()

    def _dim(self, sm):
        return sm.wnd.getmaxyx()

    def _width(self, sm):
        return self._dim(sm)[1]

    def _height(self, sm):
        return self._dim(sm)[0]

    def _wcenter(self, sm):
        return int(self._width(sm)/2)

    def _hcenter(self, sm):
        return int(self._height(sm)/2)


class UI(StateMachine):
    def __init__(self, curses_screen):
        self.console = Console(curses.LINES-4,0, curses.COLS,4)
        self.stdscr = curses_screen
        self.empire = None
        super(UI, self).__init__(UI.LoadGame)


class Panel(StateMachine):
    def __init__(self, empire, x, y, width, height):
        self.empire = empire
        self.wnd = curses.newwin(height, width, y, x)
        self.wnd.border()
        self.panel = curses.panel.new_panel(self.wnd)
        self.next_wnd = 0
        self.state_stack = [Panel.TopLevel]
        self.state_stack[0].draw(self)

    def start(self):
        while len(self.state_stack) > 0:
            state = self.state_stack[-1]
            if state == TerminateState():
                self.state_stack.pop()
                break
            else:
                state.run(self)
        return self.next_wnd
