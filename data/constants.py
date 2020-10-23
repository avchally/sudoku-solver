""" Primarily stores constants related to PyGame

"""

# State-related
ALL_STATES = ['INTRO', 'INPUT_BOARD', 'GAME', 'SOLVING']


# === MAIN GAME === #

MENU_HEIGHT = 60
S_BOARD_WIDTH = 600
S_BOARD_HEIGHT = 600
SCREEN_WIDTH = S_BOARD_WIDTH
SCREEN_HEIGHT = S_BOARD_HEIGHT + MENU_HEIGHT
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

TILE_WIDTH = S_BOARD_WIDTH / 9
TILE_HEIGHT = S_BOARD_HEIGHT / 9
TILE_CENTER_X = TILE_WIDTH / 2
TILE_CENTER_Y = TILE_HEIGHT / 2

CURSOR_WIDTH = int(TILE_WIDTH * 0.5)
CURSOR_HEIGHT = int(TILE_HEIGHT * 0.05)
CURSOR_VERT_OFFSET = 0.69 * TILE_HEIGHT / 2
CURSOR_BLINK_DURATION = 0.5  # in seconds

# Line Constants
THIN_LINE_WIDTH = 1
THICK_LINE_WIDTH = 5
Y_VALUES = [S_BOARD_HEIGHT * (n / 9) for n in range(1, 9)]
X_VALUES = [S_BOARD_WIDTH * (n / 9) for n in range(1, 9)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MENU_COLOR = (186, 186, 187)
BACKGROUND_COLOR = (27, 28, 30)
LINE_COLOR = (186, 186, 187)
TEXT_COLOR = (255, 255, 255)
TEXT_COLOR_FIXED = (130, 130, 130)
TEXT_COLOR_INVALID = (229, 40, 30)
CURSOR_COLOR = TEXT_COLOR

# Font
# FONT_PATH = 'distinct_py_projects\\sudoku_solver\\assets\\OpenSans-Regular.ttf'
FONT_PATH = 'distinct_py_projects\\sudoku_solver\\assets\\MinimalFont5x7.ttf'
FONT_AA = False

# === INTRO SCREEN === #
INTRO_BACKGROUND = 'distinct_py_projects\\sudoku_solver\\assets\\intro_bg.png'
BUTTON_IMAGE = 'distinct_py_projects\\sudoku_solver\\assets\\menu_selector.png'
