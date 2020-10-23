""" Manages the tiles within a sudoku board

Takes an optional list of lists and converts the values
to Tile objects.

Some example sudoku boards:

blank
[[0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

easy
[[0,0,0, 0,9,0, 0,0,4],
 [0,7,8, 6,0,0, 3,9,0],
 [3,9,4, 8,7,0, 5,0,2],
 [0,0,0, 0,5,0, 0,7,0],
 [2,0,0, 7,0,4, 0,0,9],
 [0,4,0, 0,1,0, 0,0,0],
 [9,0,1, 0,3,7, 6,4,8],
 [0,3,6, 0,0,8, 9,5,0],
 [8,0,0, 0,6,0, 0,0,0]]

hard
[[0,0,0, 7,0,2, 0,0,6],
 [0,0,0, 0,8,0, 2,7,0],
 [0,5,7, 0,0,6, 0,0,0],
 [4,0,0, 1,0,0, 0,5,0],
 [0,8,0, 0,0,0, 0,1,0],
 [0,9,0, 0,0,4, 0,0,3],
 [0,0,0, 4,0,0, 3,9,0],
 [0,1,4, 0,3,0, 0,0,0],
 [7,0,0, 5,0,1, 0,0,0]]

"""

from .tile import Tile

BLANK_BOARD = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

EASY_BOARD = [[0, 0, 0, 0, 9, 0, 0, 0, 4],
              [0, 7, 8, 6, 0, 0, 3, 9, 0],
              [3, 9, 4, 8, 7, 0, 5, 0, 2],
              [0, 0, 0, 0, 5, 0, 0, 7, 0],
              [2, 0, 0, 7, 0, 4, 0, 0, 9],
              [0, 4, 0, 0, 1, 0, 0, 0, 0],
              [9, 0, 1, 0, 3, 7, 6, 4, 8],
              [0, 3, 6, 0, 0, 8, 9, 5, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 0]]

TEST_BOARD = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]


class SudokuBoard:

    def __init__(self, board_list: list = TEST_BOARD):
        self.board = []
        self.create_board(board_list)

    def create_board(self, board_list):
        for row_num, row in enumerate(board_list):
            row_list = []
            for column_num, val in enumerate(row):
                row_list.append(Tile(val, (column_num, row_num), val != 0))
            self.board.append(row_list)

    def print_board(self):
        """prints the board to console (for testing)"""
        for row in self.board:
            for tile in row:
                # print(tile.grid_pos, end='')
                print(tile.return_printed_tile(), end='')
            print()

    def pencil_number(self, value: int, pos: tuple):
        row = pos[1]
        column = pos[0]
        tile = self.board[row][column]
        if len(tile.penciled_values) < 3 and not tile.fixed:
            tile.penciled_values.append(value)
            return True
        return False

    def unpencil_number(self, pos: tuple):
        row = pos[1]
        column = pos[0]
        tile = self.board[row][column]
        if len(tile.penciled_values) > 0 and not tile.fixed:
            tile.penciled_values.pop()
            return True
        return False

    def place_number(self, pos: tuple):
        """
        attempts to replace the Tile's value at
        the given (column, row)
        returns True if successful, False if not
        """
        row = pos[1]
        column = pos[0]
        tile = self.board[row][column]
        if not tile.fixed and len(tile.penciled_values) > 0:
            tile.value = tile.penciled_values[0]
            # self.check_tile_validity(tile)
            return True
        return False

    def remove_number(self, pos: tuple):
        """
        removes the number at the given
        (column, row) and replaces it with 0
        returns True if successful, False if not
        """
        row = pos[1]
        column = pos[0]
        tile = self.board[row][column]
        if not tile.fixed:
            tile.value = 0
            return True
        return False

    def check_tile_validity(self,  tile: Tile):
        """
        checks whether the current Tile violates
        any rules and changes the Tile's `valid`
        attribute accordingly
        """
        row = tile.row
        column = tile.column

        if tile.value == 0:
            tile.set_invalid()
            return False

        # check the row
        for comparison_tile in self.board[row]:
            if comparison_tile.grid_pos != tile.grid_pos:
                if comparison_tile.value == tile.value:
                    tile.set_invalid()
                    return False

        # check the column
        for board_row in self.board:
            if board_row[column].grid_pos != tile.grid_pos:
                if board_row[column].value == tile.value:
                    tile.set_invalid()
                    return False

        # check the square
        square_index = self.get_square_index(tile.grid_pos)
        for comparison_tile in self.get_square_list(square_index):
            if comparison_tile.grid_pos != tile.grid_pos:
                if comparison_tile.value == tile.value:
                    tile.set_invalid()
                    return False
        tile.set_valid()
        return True

    def refresh_tile_validity(self):
        for row in self.board:
            for tile in row:
                if tile.value != 0:
                    self.check_tile_validity(tile)

    def get_square_list(self, index: int):
        """
        returns a list of Tile objects that are contained
        within a 3x3 square on the board at the parameter
        index (index = 0 represents the topleft square)
        """
        temp_list = []
        for board_row in self.board:
            for tile in board_row:
                if self.get_square_index(tile.grid_pos) == index:
                    temp_list.append(tile)
        return temp_list

    def get_square_index(self, pos: tuple):
        """
        takes a tuple of (column, row) and returns what
        the index number is of the associated 3x3 square
        """
        column = pos[0]
        row = pos[1]
        return column // 3 + 3 * (row // 3)

    def is_won(self):
        """
        returns True if the current sudoku
        board is finished and no tile violates
        any sudoku rules
        returns False otherwise
        """
        for board_row in self.board:
            for tile in board_row:
                if tile.value == 0:
                    return False
                if not tile.valid:
                    return False
        return True


if __name__ == "__main__":
    sb = SudokuBoard(EASY_BOARD)
    sb.print_board()
    print()
    sb.print_board()

    for i in range(5):
        user_row = int(input('Enter row: '))
        user_col = int(input('Enter column: '))
        user_val = int(input('Enter the value: '))

        sb.place_number(user_val, (user_col, user_row))
        print("-"*60)
        sb.print_board()

    print(sb.is_won())
