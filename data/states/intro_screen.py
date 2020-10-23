"""
presents the user with an informative title screen
"""

import sys
import pygame
from data.state_machine import _State
from data import constants as c
import time


class IntroScreen(_State):

    def __init__(self):
        # state-related
        _State.__init__(self)
        self.possible_state_events = ['INPUT_BOARD', 'GAME']
        self.next_event = None

        # main init
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH,
                                               c.SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku")

        self.load_surfaces()
        self.load_fonts()
        self.load_buttons()
        self.clock = pygame.time.Clock()

        self.count = 0

    def enter_state(self):
        self.fadein(self.screen)

    def exit_state(self):
        self.fadeout(self.screen)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return 'GAME'

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:

    def update(self):
        pass

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_buttons()

    def draw_background(self):
        bg_rect = self.bg_surf.get_rect(topleft=(0, 0))
        self.screen.blit(self.bg_surf, bg_rect)

    def draw_title(self):
        title_surf = self.title_font.render('Sudoku', c.FONT_AA, c.TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(c.SCREEN_WIDTH/2,
                                                 c.SCREEN_HEIGHT/3))
        self.screen.blit(title_surf, title_rect)

    def draw_buttons(self):
        self.screen.blit(self.play_text_surf, self.play_text_rect)
        if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.play_button_surf, self.play_button_rect)

    def load_fonts(self):
        self.title_font = pygame.font.Font(c.FONT_PATH, 90)
        self.button_font = pygame.font.Font(c.FONT_PATH, 50)

    def load_surfaces(self):
        # background
        self.bg_surf = pygame.image.load(c.INTRO_BACKGROUND)
        self.bg_surf = pygame.transform.scale(self.bg_surf,
                                              (c.SCREEN_WIDTH,
                                               c.SCREEN_HEIGHT))
        # button
        self.button_surf = pygame.image.load(c.BUTTON_IMAGE).convert_alpha()
    
    def load_buttons(self):
        self.play_text_surf = self.button_font.render('Play', c.FONT_AA,
                                                      c.TEXT_COLOR)
        self.play_text_rect = self.play_text_surf.get_rect(center=(c.SCREEN_WIDTH/2,
                                                           c.SCREEN_HEIGHT/2))
        self.play_button_surf = pygame.transform.scale(self.button_surf,
                                                  (self.play_text_rect.width + 30,
                                                   self.play_text_rect.height + 10))
        self.play_button_rect = self.play_button_surf.get_rect(center=self.play_text_rect.center)
