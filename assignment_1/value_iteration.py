from cells import Cells
from coords import Coordinates
from config import *
from maze import Maze
from csv_generator import CSV

max_error = 70


def value_iteration(maze: Maze):
    threshold = max_error * ((1 - DISCOUNT_FACTOR) / DISCOUNT_FACTOR)
    max_utility_change = 0
    i = 1
    csv_file = CSV("ValueIteration", maze)

    print("Original:")
    maze.print()
    csv_file.add_utilities(maze)

    while max_utility_change >= threshold:
        print(f"Iteration: {i}")
        max_utility_change = 0

        # Runs for each State in the Maze
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue

                # Get the max utility change between each iteration
                utility_change = calculate_utility(curr_cell, maze)
                if utility_change > max_utility_change:
                    max_utility_change = utility_change

        i += 1
        print(f"Maximum Utility Change: {max_utility_change:.3f}")
        maze.print()
        csv_file.add_utilities(maze)

    csv_file.create_csv()


def calculate_utility(curr_cell: Cells, maze: Maze):
    utilities = [0.0] * 4

    # Calculating the utilities of each direction policy
    for directions in range(Coordinates.TOTAL_DIRECTIONS):
        neighbours = maze.get_neighbours_of_cell_direction(
            curr_cell, directions)
        up = P_UP * neighbours[0].get_utility()
        left = P_LEFT * neighbours[1].get_utility()
        right = P_RIGHT * neighbours[2].get_utility()

        utilities[directions] = up + left + right

    # Get the max utility out of the 4 directions
    max_utility = 0
    for i in range(1, len(utilities)):  # CHECKME
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
    maze = Maze("bigger_maze")
    value_iteration(maze)
