from cells import Cells
from coords import Coordinates
from config import *
from maze import Maze
from csv_generator import CSV


# define K constant value
k = 4


def policy_iteration(maze: Maze):
    """Policy Iteration Algorithm Implementation"""

    print("No. of Iterations: 0")
    maze.print_policy()
    maze.print_utility()
    csv_file = CSV("policy_iteration", maze)
    csv_file.add_utilities(maze)
    i = 1

    # repeat until the policy converges
    while True:
        print(f"No. of Iterations: {i}")

        # set a flag to check if the policy has changed during the iteration
        unchanged = True
        # call the policy_evaluation function to estimate the utility values
        policy_evaluation(maze, k)

        # iterate over each cell in the maze to improve the policy
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue
                # call the policy_improvement function to improve the policy for the current cell
                # if the policy has changed, set the flag to False
                if policy_improvement(curr_cell, maze):
                    unchanged = False

        maze.print_policy()
        maze.print_utility()
        csv_file.add_utilities(maze)

        # if the policy has not changed during this iteration, break the loop
        if unchanged:
            break

        i += 1

    csv_file.write_csv()


def policy_evaluation(maze: Maze, k: int):
    '''
    Args:
    - maze (Maze): the maze environment
    - k (int): number of iterations for policy evaluation

    Returns:
    - None
    '''
    for _ in range(k):
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue

                # Calculate the utility of the current state using Bellman update and current policy
                neighbours = maze.get_neighbours_of_cell_current_policy(
                    curr_cell)
                up = P_UP * neighbours[0].get_utility()
                left = P_LEFT * neighbours[1].get_utility()
                right = P_RIGHT * neighbours[2].get_utility()

                reward = curr_cell.get_reward(curr_cell.cell_type)

                utility = reward + DISCOUNT_FACTOR * (up + left + right)
                curr_cell.set_utility(utility)


def policy_improvement(curr_cell: Cells, maze: Maze):
    """
    Given the current state (curr_cell) and the current policy, updates the policy
    if a better policy is found.

    Args:
    - curr_cell: the current cell whose policy is being improved
    - maze: the maze object

    Returns:
    - True if the policy is updated, False otherwise
    """

    max_utility = [0.0] * 4

    # determine the maximum expected utilities from the neighboring cells
    for direction in range(Coordinates.TOTAL_DIRECTIONS):
        neighbours = maze.get_neighbours_of_cell_direction(
            curr_cell, direction)
        up = P_UP * neighbours[0].get_utility()
        left = P_LEFT * neighbours[1].get_utility()
        right = P_RIGHT * neighbours[2].get_utility()

        max_utility[direction] = up + left + right

    # get max utility
    max_direction = max_utility.index(max(max_utility))

    # calculate the utility of a state using current policy
    neighbours = maze.get_neighbours_of_cell_current_policy(curr_cell)
    up = P_UP * neighbours[0].get_utility()
    left = P_LEFT * neighbours[1].get_utility()
    right = P_RIGHT * neighbours[2].get_utility()

    curr_utility = up + left + right

    if max_utility[max_direction] > curr_utility:
        curr_cell.set_policy(max_direction)
        return True
    else:
        return False


if __name__ == '__main__':
    maze = Maze("complex")
    policy_iteration(maze)
