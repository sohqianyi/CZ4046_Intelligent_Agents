from coords import Coordinates
from policy import Policy
from config import *

import enum


class Cells(Coordinates):

    # CHECKME
    class Type(enum.Enum):
        WHITE = enum.auto()
        BROWN = enum.auto()
        WALL = enum.auto()
        GREEN = enum.auto()

    def __init__(self, coordinate: Coordinates):
        super().__init__(coordinate.get_col(), coordinate.get_row())
        self.utility = 0
        self.policy = Policy.UP
        self.cell_type = Cells.Type.WHITE

    def get_utility(self):
        return self.utility

    def set_utility(self, utility):
        self.utility = utility

    def get_policy(self) -> Policy:  # CHECKME
        return self.policy

    def set_policy(self, val):
        if val == 0:
            self.policy = Policy.UP
        elif val == 1:
            self.policy = Policy.DOWN
        elif val == 2:
            self.policy = Policy.LEFT
        elif val == 3:
            self.policy = Policy.RIGHT

    def get_cell_type(self) -> Type:
        return self.cell_type

    def get_reward(self, cell_type):
        if cell_type == Cells.Type.WHITE:
            return WHITE_REWARD
        elif cell_type == Cells.Type.GREEN:
            return GREEN_REWARD
        elif cell_type == Cells.Type.BROWN:
            return BROWN_REWARD
        elif cell_type == Cells.Type.WALL:
            return WALL_REWARD
        else:
            return 0

    def set_cell_type(self, cell_type):
        if cell_type == 'W':
            self.cell_type = Cells.Type.WHITE
            self.set_utility(WHITE_REWARD)
        elif cell_type == 'G':
            self.cell_type = Cells.Type.GREEN
            self.set_utility(GREEN_REWARD)
        elif cell_type == 'B':
            self.cell_type = Cells.Type.BROWN
            self.set_utility(BROWN_REWARD)
        elif cell_type == '#':
            self.cell_type = Cells.Type.WALL
            self.set_utility(WALL_REWARD)
