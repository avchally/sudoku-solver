# import pygame as pg
from .state_machine import _State


class InputScreen(_State):

    def __init__(self):
        _State.__init__(self)
        self.possible_events = ['']  # TODO determine possible events
        self.next_event = None
