"""The state machine class and the generic state class

Every state will inherit from the _State class
The state machine processes the states and their transitions

"""

import pygame
from data import constants as c


class _State:

    def __init__(self):
        self.possible_state_events = []
        self.done = False

    def process_event(self):
        pass
        # if event in self.possible_events:
        #     return event

    def enter_state(self):
        """Perform any init duties before resuming state"""
        pass

    def exit_state(self):
        """Perform any cleanup duties before pausing state"""
        pass

    def draw(self, screen):
        """handles drawing the screen"""
        pass

    def update(self):
        """
        handles updating the state
        returns state text if changing states
        """
        pass

    def fadein(self, screen):
        fadein_surf = pygame.Surface(c.SCREEN_SIZE).convert()
        fadein_surf.fill(c.BLACK)
        for alpha in range(255):
            self.draw()
            fadein_surf.set_alpha(255 - alpha)
            screen.blit(fadein_surf, (0, 0))
            pygame.display.update()

    def fadeout(self, screen):
        self.update()
        fadeout_surf = pygame.Surface(c.SCREEN_SIZE).convert()
        fadeout_surf.fill(c.BLACK)
        for alpha in range(255):
            self.draw()
            fadeout_surf.set_alpha(alpha)
            screen.blit(fadeout_surf, (0, 0))
            pygame.display.update()


class StateMachine:

    def __init__(self, state_dict: dict, inital_state: str):
        """start with a default state"""
        self.state_dict = state_dict
        self.state = self.state_dict[inital_state]
        self.done = False

    def init_pygame(self):
        """starts pygame"""
        # TODO startup pygame

    def on_event(self, event):
        if event in self.state_dict:
            self.state.exit_state()
            self.state = self.state_dict[event]
            self.state.enter_state()

    def main_loop(self):
        while not self.done:
            self.on_event(self.state.process_event())
            self.state.update()
            self.state.draw()
            pygame.display.update()
            self.state.clock.tick(c.FPS)
