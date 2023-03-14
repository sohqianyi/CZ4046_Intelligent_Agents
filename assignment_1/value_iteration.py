from cells import Cells
from coords import Coordinates
from config import *
from maze import Maze
from csv_generator import CSV

# define a constant maximum error value
max_error = 68


def value_iteration(maze: Maze):
    """Value Iteration Algorithm Implementation"""

    termination_condition = max_error * \
        ((1 - DISCOUNT_FACTOR) / DISCOUNT_FACTOR)

    print("No. of Iterations: 0")
    maze.print_policy()
    maze.print_utility()
    csv_file = CSV("value_iteration", maze)
    csv_file.add_utilities(maze)

    # iterative approach with initial values for the utilities and updating them until an equilibrium is reached.
    i = 1
    while True:
        print(f"No. of Iterations: {i}")
        max_utility_change = 0

        # for each state
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue

                # find maximum change in utility
                utility_change = calculate_utility(curr_cell, maze)
                if utility_change > max_utility_change:
                    max_utility_change = utility_change

        i += 1
        print(f"Max Utility Change: {max_utility_change:.3f}")
        maze.print_policy()
        maze.print_utility()

        csv_file.add_utilities(maze)

        # break out of loop if equilibrium is reached
        if max_utility_change < termination_condition:
            csv_file.write_csv()
            break


def calculate_utility(curr_cell: Cells, maze: Maze):
    '''
    This function takes in two arguments:
    - curr_cell: an instance of the Cells class, representing the current cell
    - maze: an instance of the Maze class, representing the maze in which the current cell resides
    '''

    # Initialize a list of utilities for each direction
    utilities = [0.0] * 4

    # Iterate over all possible directions
    for direction in range(Coordinates.TOTAL_DIRECTIONS):
        neighbours = maze.get_neighbours_of_cell_direction(
            curr_cell, direction)

        # Calculate the weighted sum of the utilities of the neighboring cells in each direction
        up = P_UP * neighbours[0].get_utility()
        left = P_LEFT * neighbours[1].get_utility()
        right = P_RIGHT * neighbours[2].get_utility()

        utilities[direction] = up + left + right

    # Find the max utility
    max_utility = 0
    for i in range(1, len(utilities)):
        if utilities[i] > utilities[max_utility]:
            max_utility = i

    # Set new policy for state S
    curr_reward = curr_cell.get_reward(curr_cell.get_cell_type())
    curr_utility = curr_cell.get_utility()
    new_utility = curr_reward + DISCOUNT_FACTOR * utilities[max_utility]
    curr_cell.set_utility(new_utility)
    curr_cell.set_policy(max_utility)

    return abs(curr_utility - new_utility)


if __name__ == '__main__':
    # CHANGEME: Change maze here
    # Choose a template from the maze folder
    maze = Maze("original")
    value_iteration(maze)
