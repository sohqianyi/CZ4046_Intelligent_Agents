import csv
import os
from cells import Cells
from coords import Coordinates
from config import *
from maze import Maze

from typing import List


class CSV:
    def __init__(self, file: str, maze: Maze):
        self.file = file
        self.headings: List[str] = []
        self.data: List[List[float]] = []

        for c in range(COLS):
            for r in range(ROWS):
                cell = maze.get_cell(Coordinates(c, r))
                if cell.get_cell_type() == Cells.Type.WALL:
                    self.headings.append(f'"Wall: ({c}, {r})"')
                elif cell.get_cell_type() == Cells.Type.GREEN:
                    self.headings.append(f'"Green: ({c}, {r})"')
                elif cell.get_cell_type() == Cells.Type.WHITE:
                    self.headings.append(f'"White: ({c}, {r})"')
                elif cell.get_cell_type() == Cells.Type.BROWN:
                    self.headings.append(f'"Brown: ({c}, {r})"')

    def add_utilities(self, maze: Maze) -> None:
        utility = []

        for c in range(COLS):
            for r in range(ROWS):
                utility.append(maze.get_cell(Coordinates(c, r)).get_utility())

        self.data.append(utility)

    def write_csv(self) -> None:
        try:
            path = os.path.abspath('')
            results_path = os.path.join(
                path, 'results', self.file + '_complex.csv')

            with open(results_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(self.headings)
                for iteration in self.data:
                    writer.writerow(iteration)

            print('CSV generated at:', results_path)

        except IOError as e:
            print("I/O error occurred: ", e)
