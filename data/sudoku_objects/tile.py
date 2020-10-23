class Tile:
    """
    :param grid_pos: the column and row position in a grid
    :type grid_pos: tuple (column, row)
    :param value: the value of the sudoku tile
    :type value: int
    :param fixed: whether the tile's value can be changed
    :type fixed: bool
    """

    def __init__(self, value: int, grid_pos: tuple, fixed: bool = False):
        """constructor method"""
        self.value = value
        self.penciled_values = []
        self.grid_pos = grid_pos
        self.column = self.grid_pos[0]
        self.row = self.grid_pos[1]
        self.fixed = fixed
        self.valid = True

    def return_printed_tile(self):
        if self.value == 0:
            return '   '
        if not self.valid:
            return f'!{self.value}!'
        else:
            return f' {self.value} '

    def set_invalid(self):
        if not self.fixed:
            self.valid = False

    def set_valid(self):
        if not self.fixed:
            self.valid = True

    def __str__(self):
        if self.value == 0:
            return ' '
        else:
            return str(self.value)
