import random

"""
Creation of maze environment according to Assingment 1.pdf
Legend:
'G' : Green Square
'W' : Wall
'-' : White Square
'B' : Brown Square
"""
map = [
    ['G', 'W', 'G', '-', '-', 'G'],
    ['-', 'B', '-', 'G', 'W', 'B'],
    ['-', '-', 'B', '-', 'G', '-'],
    ['-', '-', '-', 'B', '-', 'G'],
    ['-', 'W', 'W', 'W', 'B', '-'],
    ['-', '-', '-', '-', '-', '-'],
]

# mapping of squares to rewards
reward_mapping = {
    '-': -0.04,  # White square
    'G': 1.0,  # Green square
    'B': -1.0,  # Brown square
}


start = {'x': 3, 'y': 2}  # 'Start' position: 4th row, 3rd column

discount_factor = 0.99

# for value iteration utilities to match reference utilities (approximately)
ref_discount_factor = 0.95
ref_max_error = 1.4

# for value iteration
max_error = 20

# for policy iteration
policy_eval = 100

# Based on maze given, ~0.5 (16 out of 36 squares) of the maze is not white space.
# Among non-white spaces (16 squares), roughly
# ~1/3 are walls (5 walls),
# ~1/3 are brown squares (5 brown),
# ~1/3 are green squares (6 green)
# Therefore, try to generate maze with roughly same distribution.


def generator(grid_length: int):
    """
    Generates a maze as a square grid that has size of (grid_length x grid_length).
    params:
    - grid_length (int): length of the grid
    return:
    - 2D array (list of list): [
        [' ', ..., ' '],
        ...,
        [' ', ..., ' '],
    ]
    """
    random.seed()
    grid = []

    for row in range(grid_length):
        grid.append([])

        for _ in range(grid_length):  # _ is column; column value not used
            colour_number = random.random()

            if colour_number < 0.5 / 3:
                grid[row].append('W')  # wall
            elif colour_number < 0.5 * 2 / 3:
                grid[row].append('B')  # brown
            elif colour_number < 0.5:
                grid[row].append('G')  # green
            else:
                grid[row].append('-')  # white

    return grid
