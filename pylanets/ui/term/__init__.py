import curses
import curses.panel

from .base import (UI)
from . import (main, fleet)

def run_ui():
    curses.wrapper(_start)

def _start(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    UI(stdscr).start()
