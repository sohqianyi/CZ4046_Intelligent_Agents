from config import *


class Coordinates:
    TOTAL_DIRECTIONS = 4
    UP, DOWN, LEFT, RIGHT = range(TOTAL_DIRECTIONS)

    def __init__(self, col: int, row: int):
        if col < 0 or row < 0:
            raise ValueError("Column and row must be positive.")
        elif row > ROWS - 1:
            raise ValueError("Row out of range.")
        elif col > COLS - 1:
            raise ValueError("Column out of range.")
        else:
            self.col = col
            self.row = row

    def get_col(self) -> int:
        return self.col

    def get_row(self) -> int:
        return self.row

    def get_neighbours(self, direction):
        '''
        Get the next 3 possible coordinates with respect to the provided direction.
        Returns a list with intended position and to the left and right of original position.
        '''
        offsets = {
            0: [(0, -1), (-1, 0), (1, 0)],  # Up
            1: [(0, 1), (1, 0), (-1, 0)],  # Down
            2: [(-1, 0), (0, 1), (0, -1)],  # Left
            3: [(1, 0), (0, -1), (0, 1)],  # Right
        }
        # store three possible neighbor coordinates
        coordinates = [None] * 3
        for i, (x, y) in enumerate(offsets[direction]):
            row, col = self.row + y, self.col + x
            if 0 <= row < ROWS and 0 <= col < COLS:
                coordinates[i] = Coordinates(col, row)
            else:
                coordinates[i] = self
        return coordinates
