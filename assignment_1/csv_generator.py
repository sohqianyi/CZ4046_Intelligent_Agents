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
        incoming = []

        for c in range(COLS):
            for r in range(ROWS):
                incoming.append(maze.get_cell(Coordinates(c, r)).get_utility())

        self.data.append(incoming)

    def create_csv(self) -> None:
        CSV.write(self.file + "_bigger_maze", self.headings, self.data)

    @staticmethod
    def write(file: str, headings: List[str], data: List[List[float]]) -> None:
        try:
            filePath = os.path.abspath('')
            with open(os.path.join(filePath, 'csv', file + '.csv'), mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(headings)
                for iteration in data:
                    writer.writerow(iteration)

        except IOError as e:
            print("I/O error occurred: ", e)
