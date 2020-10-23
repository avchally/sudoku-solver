import math
import sys
import pygame
from data.state_machine import _State
from data.sudoku_objects.sudoku_board import SudokuBoard
from data.sudoku_objects.cursor import Cursor
from data import constants as c


class Game(_State):

    def __init__(self):
        # state-related
        _State.__init__(self)
        self.possible_state_events = ['INTRO']
        self.next_state = None

        # main game init
        pygame.init()  # TODO remove when state machine is implemented
        self.load_base_objects()
        self.clock = pygame.time.Clock()
        self.square_font = pygame.font.Font(c.FONT_PATH,
                                            int(c.TILE_HEIGHT*0.75))
        self.penciled_font = pygame.font.Font(c.FONT_PATH,
                                              int(c.TILE_HEIGHT*0.25))
        self.sb = SudokuBoard()
        self.solving = False
        self.cursor = Cursor()
        self.solver_speed = 5

    def enter_state(self):
        self.fadein(self.screen)

    def exit_state(self):
        self.fadeout(self.screen)

    def process_event(self):
        if not self.solving:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.cursor.get_event('s-tab', self.sb)
                        else:
                            self.cursor.get_event('tab', self.sb)
                    if event.key == pygame.K_RIGHT:
                        self.cursor.get_event('right', self.sb)
                    if event.key == pygame.K_LEFT:
                        self.cursor.get_event('left', self.sb)
                    if event.key == pygame.K_UP:
                        self.cursor.get_event('up', self.sb)
                    if event.key == pygame.K_DOWN:
                        self.cursor.get_event('down', self.sb)
                    if event.key == pygame.K_ESCAPE:
                        self.cursor.deselect()
                    if event.key == pygame.K_DELETE and self.cursor.active:
                        self.sb.remove_number(self.cursor.pos)
                    if event.key == pygame.K_i:
                        return 'INTRO'
                    if event.key == pygame.K_s:
                        self.initiate_solver()
                        self.solving = True
                    for i in range(1, 10):
                        if event.key == 48 + i and self.cursor.active:
                            self.sb.pencil_number(i, self.cursor.pos)
                    if event.key == pygame.K_RETURN and self.cursor.active:
                        self.sb.place_number(self.cursor.pos)
                    if event.key == pygame.K_BACKSPACE and self.cursor.active:
                        self.sb.unpencil_number(self.cursor.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if self.sudoku_rect.collidepoint(mouse_position):
                        new_mouse_pos = self.convert_screen_pos(mouse_position)
                        self.cursor.select(self.sb, new_mouse_pos)

    def initiate_solver(self):
        self.cursor.pos = (0, 0)
        self.cursor.active = True
        self.cursor.next_field(self.sb)

    def increment_solver(self):
        solver_counter = 0
        while self.solving and solver_counter <= self.solver_speed*20 + 1:
            solver_counter += 1
            tile = self.sb.board[self.cursor.pos[1]][self.cursor.pos[0]]
            if tile.value == 10:
                tile.value = 0
                self.cursor.previous_field(self.sb)
                tile = self.sb.board[self.cursor.pos[1]][self.cursor.pos[0]]
                tile.value += 1
            else:
                if self.sb.check_tile_validity(tile):
                    self.cursor.next_field(self.sb)
                    if self.sb.is_won():
                        self.solving = False
                else:
                    tile.value += 1

    def update(self):
        self.update_cursor()
        self.sb.refresh_tile_validity()
        self.increment_solver()

    def draw(self):
        self.draw_background()
        for row in self.sb.board:
            for tile in row:
                self.draw_tile(tile)

        if self.cursor.active and self.cursor.blink:
            self.draw_cursor()

        self.screen.blit(self.sudoku_screen, self.sudoku_rect)

    def draw_tile(self, tile):
        text_x = tile.grid_pos[0] * c.TILE_WIDTH + c.TILE_CENTER_X
        text_y = tile.grid_pos[1] * c.TILE_HEIGHT + c.TILE_CENTER_Y
        pen0_x = text_x - c.TILE_WIDTH/3
        pen0_y = text_y - c.TILE_HEIGHT/3

        if tile.penciled_values != []:
            for i, value in enumerate(tile.penciled_values):
                pen_pos = (pen0_x + i*c.TILE_WIDTH/3, pen0_y)
                pen_surf = self.penciled_font.render(str(value), c.FONT_AA,
                                                     c.TEXT_COLOR)
                pen_rect = pen_surf.get_rect(center=(pen_pos))
                self.sudoku_screen.blit(pen_surf, pen_rect)

        if tile.valid:
            text_surf = self.square_font.render(str(tile), c.FONT_AA, 
                                                c.TEXT_COLOR)
        if tile.fixed:
            text_surf = self.square_font.render(str(tile), c.FONT_AA,
                                                c.TEXT_COLOR_FIXED)
        if not tile.valid:
            text_surf = self.square_font.render(str(tile), c.FONT_AA,
                                                c.TEXT_COLOR_INVALID)

        text_rect = text_surf.get_rect(center=(text_x, text_y))
        self.draw_tile_border(tile, (text_x, text_y))
        self.sudoku_screen.blit(text_surf, text_rect)

    def draw_tile_border(self, tile, center_pos):
        if tile.fixed:
            pass

    def update_cursor(self):
        self.cursor.blink_timer += 1
        if self.cursor.blink_timer / c.FPS >= c.CURSOR_BLINK_DURATION:
            self.cursor.blink = not self.cursor.blink
            self.cursor.blink_timer = 0

    def draw_cursor(self):
        cursor_center_x = self.cursor.pos[0] * c.TILE_WIDTH + c.TILE_CENTER_X
        cursor_center_y = (self.cursor.pos[1] * c.TILE_HEIGHT +
                           c.TILE_CENTER_Y + c.CURSOR_VERT_OFFSET)
        cursor_pos_1 = (cursor_center_x - c.CURSOR_WIDTH / 2, cursor_center_y)
        cursor_pos_2 = (cursor_center_x + c.CURSOR_WIDTH / 2, cursor_center_y)

        pygame.draw.line(self.sudoku_screen, c.CURSOR_COLOR, cursor_pos_1,
                         cursor_pos_2, c.CURSOR_HEIGHT)

    def load_base_objects(self):
        """
        loads the main screen surface, and the main playing
        surface and its rect
        """
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH,
                                               c.SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.sudoku_screen = pygame.Surface((c.S_BOARD_WIDTH,
                                             c.S_BOARD_HEIGHT))
        self.sudoku_rect = self.sudoku_screen.get_rect()
        self.sudoku_rect.bottom = c.S_BOARD_HEIGHT + c.MENU_HEIGHT

    def draw_background(self):
        """
        draws the menu, the background, and the lines
        """
        self.screen.fill(c.MENU_COLOR)
        self.sudoku_screen.fill(c.BACKGROUND_COLOR)

        # print lines
        for x_val in c.X_VALUES:
            point_a = (x_val, 0)
            point_b = (x_val, c.S_BOARD_HEIGHT)
            if int(x_val) % int(c.S_BOARD_HEIGHT / 3) in range(-5, 5):
                # thick lines
                pygame.draw.line(self.sudoku_screen, c.LINE_COLOR,
                                 point_a, point_b, c.THICK_LINE_WIDTH)
            else:  # thin lines
                pygame.draw.line(self.sudoku_screen, c.LINE_COLOR,
                                 point_a, point_b, c.THIN_LINE_WIDTH)
        for y_val in c.Y_VALUES:
            point_a = (0, y_val)
            point_b = (c.S_BOARD_WIDTH, y_val)
            if int(y_val) % int(c.S_BOARD_WIDTH / 3) in range(-5, 5):
                # thick lines
                pygame.draw.line(self.sudoku_screen, c.LINE_COLOR,
                                 point_a, point_b, c.THICK_LINE_WIDTH)
            else:  # thin lines
                pygame.draw.line(self.sudoku_screen, c.LINE_COLOR,
                                 point_a, point_b, c.THIN_LINE_WIDTH)

    def convert_screen_pos(self, pos):
        """
        converts a position on the screen to the
        associated tile index as a tuple
        in the format (column, row)
        """
        column = math.floor(pos[0] / c.S_BOARD_WIDTH * 9)
        row = math.floor((pos[1] - c.MENU_HEIGHT) / c.S_BOARD_HEIGHT * 9)

        return (column, row)
