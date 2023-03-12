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

    # def get_neighbours(self, direction):
        # # store three possible neighbor coordinates
        # coordinates = [None] * 3

        # # Offset Rule
        # offset = [
        #     [[0, -1], [-1, 0], [+1, 0]],
        #     [[0, +1], [+1, 0], [-1, 0]],
        #     [[-1, 0], [0, +1], [0, -1]],
        #     [[+1, 0], [0, -1], [0, +1]]
        # ]

        # try:
        #     # Up
        #     coordinates[0] = Coordinates(
        #         self.col + offset[direction][0][0], self.row + offset[direction][0][1])
        # except ValueError:
        #     coordinates[0] = self

        # try:
        #     # Left
        #     coordinates[1] = Coordinates(
        #         self.col + offset[direction][1][0], self.row + offset[direction][1][1])
        # except ValueError:
        #     coordinates[1] = self

        # try:
        #     # Right
        #     coordinates[2] = Coordinates(
        #         self.col + offset[direction][2][0], self.row + offset[direction][2][1])
        # except ValueError:
        #     coordinates[2] = self

        # return coordinates
    # def get_neighbours(self, direction):  # CHECKME
    #     '''
    #     Get the next 3 possible coordinates with respect to the provided direction.
    #     Returns a list with intended position and to the left and right of original position.
    #     '''
    #     # store three possible neighbor coordinates
    #     coordinates = [None] * 3

    #     if direction == 0:  # Up
    #         if self.row - 1 >= 0 and self.row - 1 < ROWS:
    #             coordinates[0] = Coordinates(self.col, self.row - 1)
    #         else:
    #             coordinates[0] = self

    #         if self.col - 1 >= 0 and self.col - 1 < COLS:
    #             coordinates[1] = Coordinates(self.col - 1, self.row)
    #         else:
    #             coordinates[1] = self

    #         if self.col + 1 >= 0 and self.col + 1 < ROWS:
    #             coordinates[2] = Coordinates(self.col + 1, self.row)
    #         else:
    #             coordinates[2] = self

    #     elif direction == 1:  # Down
    #         if self.row + 1 >= 0 and self.row + 1 < ROWS:
    #             coordinates[0] = Coordinates(self.col, self.row + 1)
    #         if self.col + 1 >= 0 and self.col + 1 < COLS:
    #             coordinates[1] = Coordinates(self.col + 1, self.row)
    #         if self.col - 1 >= 0 and self.col - 1 < COLS:
    #             coordinates[2] = Coordinates(self.col - 1, self.row)
    #     elif direction == 2:  # Left
    #         if self.col - 1 >= 0 and self.col - 1 < COLS:
    #             coordinates[0] = Coordinates(self.col - 1, self.row)
    #         if self.row + 1 >= 0 and self.row + 1 < ROWS:
    #             coordinates[1] = Coordinates(self.col, self.row + 1)
    #         if self.row - 1 >= 0 and self.row - 1 < ROWS:
    #             coordinates[2] = Coordinates(self.col, self.row - 1)
    #     elif direction == 3:  # Right
    #         if self.col + 1 >= 0 and self.col + 1 < COLS:
    #             coordinates[0] = Coordinates(self.col + 1, self.row)
    #         if self.row - 1 >= 0 and self.row - 1 < ROWS:
    #             coordinates[1] = Coordinates(self.col, self.row - 1)
    #         if self.row + 1 >= 0 and self.row + 1 < ROWS:
    #             coordinates[2] = Coordinates(self.col, self.row + 1)
    #     print('coords, ', coordinates)
    #     return coordinates

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
