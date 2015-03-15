from builtins import type

class State(object):
    def run(self, sm):
        assert 0, 'run not implemented'
    def next(self, input):
        assert 0, 'next not implemented'
    def __eq__(self, other):
        if self.__class__ == type or other.__class__ == type:
            raise Exception('You must use instantiated state classes')
        return self.__class__ == other.__class__
    def __ne__(self, other):
        return not self.__eq__(other)

class TerminateState(State):
    def run(self):
        return self

class StateMachine(object):
    def __init__(self, initial):
        self.current = initial
        self.start()

    def start(self):
        while self.current != TerminateState():
            self.current = self.current.run(self)
