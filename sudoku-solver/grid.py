class Grid:
    def __init__(self, grid=None):
        if not grid:
            self._grid = [[0] * 9 for i in range(9)]
        else:
            self._grid = grid

    @classmethod
    def from_data(cls, serialized_grid: str):
        """
        Reads a serialized grid of Sudoku with the following format:
        row1row2row3row4row5row6row7row8row9

        An empty cell is represented with the value 0.

        For instance, for the following input:
        001700509573024106800501002700295018009400305652800007465080071000159004908007053

        The first line would be:   ..1 | 7.. | 5.9  (dots represent empty cells)
        The second line would be:  573 | .24 | 1.6
        And so on.

        :param serialized_grid: the grid data in row-order, with all rows concatenated
        """
        if len(serialized_grid) != 9*9:
            raise ValueError('The grid must contain 81 values')

        grid = cls()

        for i, value in enumerate(serialized_grid):
            value = int(value)

            if value < 0 or value > 9:
                raise ValueError('Each cell must contain a value between 0 and 9 inclusive')

            row, column = i // 9, i % 9
            grid.set_number(row, column, value)

        return grid

    def set_number(self, row, column, value):
        self._grid[row][column] = value

    def get_number(self, row, column):
        return self._grid[row][column]

    def __str__(self):
        result = []

        for i, row in enumerate(self._grid):
            if i != 0 and i % 3 == 0:
                result.append('-' * 15)

            line = []
            for j in range(3):
                line.append(''.join([str(cell) if cell != 0 else ' ' for cell in row[j*3:j*3+3]]))

            result.append(' | '.join(line))

        return '\n'.join(result)
