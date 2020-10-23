class Cursor:
    """
    A cursor that will be present on the sudoku
    board. Will be present at a tuple position
    where the elements indicate the column index
    and row index
    """

    def __init__(self):
        self.active = False
        self.blink = True
        self.pos = (0, 0)
        self.blink_timer = 0
        self.event_dict = {
            'tab': self.next_field,
            's-tab': self.previous_field,
            'up': self.up_field,
            'down': self.down_field,
            'left': self.left_field,
            'right': self.right_field,
        }

    def select(self, sudoku_board, mouse_pos):
        """
        activates/sets the cursor to the tile at the
        mouse position
        """
        column = mouse_pos[0]
        row = mouse_pos[1]
        tile = sudoku_board.board[row][column]
        if not tile.fixed:
            self.blink = True
            self.blink_time = 0
            self.pos = (column, row)
            self.active = True

    def deselect(self):
        """
        only reason why this is here is for
        the sake of completion
        """
        self.active = False

    # moving the cursor around
    def get_event(self, event, sudoku_board):
        if event in self.event_dict:
            self.blink = True
            self.blink_time = 0
            self.event_dict[event](sudoku_board)

    def next_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            column += 1
            if column == 9:
                column = 0
                row = (row + 1) % 9
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break

    def previous_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            column -= 1
            if column == -1:
                column = 8
                row = (row - 1) % 9
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break

    def up_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            row -= 1
            if row == -1:
                row = 8
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break

    def down_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            row += 1
            if row == 9:
                row = 0
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break

    def left_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            column -= 1
            if column == -1:
                column = 8
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break

    def right_field(self, sudoku_board):
        column = self.pos[0]
        row = self.pos[1]

        while True:
            column += 1
            if column == 9:
                column = 0
            tile = sudoku_board.board[row][column]
            if not tile.fixed:
                self.pos = tile.grid_pos
                break
