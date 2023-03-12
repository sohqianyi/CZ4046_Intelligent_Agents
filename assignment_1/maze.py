import os

from cells import Cells
from coords import Coordinates
from config import *
# from policy import Policy

from typing import List


class Maze:
    def __init__(self, file=None):
        self.col = COLS
        self.row = ROWS
        self.cells = [[Cells((i, j)) for j in range(self.row)]
                      for i in range(self.col)]

        if file is not None:
            self.import_maze(file)

    def get_cell(self, coordinate: Coordinates) -> Cells:
        col, row = coordinate.get_col(), coordinate.get_row()
        return self.cells[col][row]

    def get_neighbours_of_cell_current_policy(self, curr_cell: Cells) -> List[Cells]:

        curr_policy = curr_cell.get_policy()
        curr_direction = curr_policy.get_direction()
        neighbour_coords = curr_cell.get_neighbours(curr_direction)

        neighbour_cells = [None] * 3
        for i, coord in enumerate(neighbour_coords):
            neighbour_cell = self.get_cell(coord)

            if neighbour_cell.get_cell_type() == Cells.Type.WALL:
                neighbour_coords[i] = curr_cell

            neighbour_cells[i] = self.get_cell(neighbour_coords[i])

        return neighbour_cells

    def get_neighbours_of_cell_direction(self, curr_cell: Cells, direction) -> List[Cells]:
        neighbour_coords = curr_cell.get_neighbours(direction)

        neighbour_cells = []
        for coord in neighbour_coords:
            neighbour_cell = self.get_cell(coord)

            if neighbour_cell.get_cell_type() == Cells.Type.WALL:
                coord = curr_cell

            neighbour_cells.append(self.get_cell(coord))

        return neighbour_cells

    def print_maze(self):
        for r in range(self.row):
            for c in range(self.col):
                curr_cell = self.cells[c][r]

                if curr_cell.get_cell_type() != Cells.Type.WALL:
                    utility = curr_cell.get_utility()
                    cell_type = curr_cell.get_cell_type()
                    policy = curr_cell.get_policy().get_symbol()

                    print(f"| {cell_type} {utility:>7.3f} {policy}",
                          end="")
                else:
                    print("|" + " " * 21, end="")

            print("|")

        print()

    def import_maze(self, file):
        try:
            file_path = os.path.join(os.path.dirname(
                __file__), "maze", file + ".txt")

            with open(file_path, "r") as f:
                for r in range(self.row):
                    row = f.readline().strip()
                    row = row.replace(" ", "")  # remove all white spaces
                    for c in range(self.col):
                        cell_type = row[c]
                        self.cells[c][r].set_cell_type(cell_type)
        except Exception as e:
            print(e)
