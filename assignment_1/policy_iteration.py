from cells import Cells
from coords import Coordinates
from config import *
from maze import Maze
from csv_generator import CSV


# define K constant value
k = 4


def policy_iteration(maze: Maze):  # CHECK ME
    """Policy Iteration Algorithm Implementation"""
    i = 1
    csv_file = CSV("policy_iteration", maze)

    print("Original Maze:")
    maze.print_maze()
    csv_file.add_utilities(maze)

    while True:
        print(f"Iteration {i}:")

        # Policy Evaluation
        policy_evaluation(maze, k)

        # Policy Improvement
        improved = False
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue

                if policy_improvement(curr_cell, maze):
                    improved = True

        maze.print_maze()
        csv_file.add_utilities(maze)

        if not improved:
            break

        i += 1

    csv_file.write_csv()


def policy_evaluation(maze: Maze, k: int):
    """Policy Evaluation Algorithm Implementation"""
    for _ in range(k):
        for c in range(COLS):
            for r in range(ROWS):
                curr_cell = maze.get_cell(Coordinates(c, r))

                if curr_cell.get_cell_type() == Cells.Type.WALL:
                    continue

                # Set the utilities of each state using Bellman update and current policy
                neighbours = maze.get_neighbours_of_cell_current_policy(
                    curr_cell)
                up = P_UP * neighbours[0].get_utility()
                left = P_LEFT * neighbours[1].get_utility()
                right = P_RIGHT * neighbours[2].get_utility()

                reward = curr_cell.get_reward(curr_cell.cell_type)

                utility = reward + DISCOUNT_FACTOR * (up + left + right)
                curr_cell.set_utility(utility)


def policy_improvement(curr_cell: Cells, maze: Maze):
    """Policy Improvement Algorithm Implementation"""

    # Calculate the maximum estimated utilities based on surrounding neighbors
    max_utility = [0.0] * 4
    for direction in range(Coordinates.TOTAL_DIRECTIONS):
        neighbours = maze.get_neighbours_of_cell_direction(
            curr_cell, direction)
        up = P_UP * neighbours[0].get_utility()
        left = P_LEFT * neighbours[1].get_utility()
        right = P_RIGHT * neighbours[2].get_utility()

        # max_utility.append(up + left + right)
        max_utility[direction] = up + left + right  # CHECKME

    max_direction = max_utility.index(max(max_utility))

    # Calculate the utility of a state using current policy
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
    maze = Maze("original")
    policy_iteration(maze)
