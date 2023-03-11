"""
Implementation of a maze environment,
which is also a Markov decision process.
"""
import enum
from assignment_1.mdp import MDP

# class MazeAction(enum.Enum):
#     """
#     Actions that can taken in a Maze.
#     """
#     MOVE_UP = enum.auto()
#     MOVE_DOWN = enum.auto()
#     MOVE_LEFT = enum.auto()
#     MOVE_RIGHT = enum.auto()


class Maze(MDP):
    """
    The Maze is represented as a two-dimensional array, with squares of varying colors that offer different rewards. The types of squares include:

    White squares represented by '-'.
    Green squares represented by 'G'.
    Brown squares represented by 'B'.
    Walls represented by 'W'.
    """

    def __init__(self, grid, reward_mapping, start, discount_factor):
        self.grid = grid
        self.reward_mapping = reward_mapping
        self.start = start
        self.width = len(grid)
        self.height = len(grid[0])

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        # Initialize obj
        super().__init__({}, possible_actions, discount_factor)

        for x in range(self.width):
            for y in range(self.height):
                if grid[x][y] != 'W':
                    state = (x, y)
                    actions_to_next_state = self.generate_next_state_map(
                        state, possible_actions)
                    self.states[state] = actions_to_next_state

    def generate_next_state_map(self, state, actions):
        next_states = {}
        x, y = state
        for action in actions:
            if action == 'UP':
                next_state = (x, y - 1)
            elif action == 'DOWN':
                next_state = (x, y + 1)
            elif action == 'LEFT':
                next_state = (x - 1, y)
            elif action == 'RIGHT':
                next_state = (x + 1, y)

            if next_state in self.states:
                reward = self.reward_mapping[next_state]
            else:
                reward = self.reward_mapping[state]
            next_states[action] = [(next_state, reward)]
        return next_states

    def transition_model(self, state, action, next_state) -> float:
        """
        params
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state
        - next_state (tuple): intended x, y position (may be invalid)
        return:
        probability which ranges from 0 to 1, inclusive (float)
        """
        # if state and action not present, should throw and error
        next_state_probability_map = self.states[state][action]
        return next_state_probability_map.get(next_state, 0)['probability']

    def reward_function(self, state):
        """
        params:
        - state (tuple): x, y position
        return: reward value (float)
        """
        colour = self.grid[state[0]][state[1]]
        return self.reward_mapping[colour]

    def get_next_states(self, state, action):
        """
        params:
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state
        return: {
            intended_next_state (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.8 (float)
            },
            unintended_next_state_1 (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.1 (float)
            },
            unintended_next_state_2 (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.1 (float)
            },
        }
        """
        if action == 'UP':

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state
            else:
                actual_above_state = state  # invalid state -> remain same spot

            left_state = (state[0] - 1, state[1])

            if left_state in self.states:
                actual_left_state = left_state
            else:
                actual_left_state = state  # invalid state -> remain same spot

            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state
            else:
                actual_right_state = state  # invalid state -> remain same spot

            next_states = {
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.8,
                },
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                },
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                },
            }

        elif action == 'DOWN':

            below_state = (state[0], state[1] + 1)

            if below_state in self.states:
                actual_below_state = below_state
            else:
                actual_below_state = state  # invalid state -> remain same spot

            left_state = (state[0] - 1, state[1])

            if left_state in self.states:
                actual_left_state = left_state
            else:
                actual_left_state = state  # invalid state -> remain same spot

            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state
            else:
                actual_right_state = state  # invalid state -> remain same spot

            next_states = {
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.8,
                },
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                },
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                },
            }

        elif action == 'LEFT':

            left_state = (state[0] - 1, state[1])

            if left_state in self.states:
                actual_left_state = left_state
            else:
                actual_left_state = state  # invalid state -> remain same spot

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state
            else:
                actual_above_state = state  # invalid state -> remain same spot

            below_state = (state[0], state[1] + 1)

            if below_state in self.states:
                actual_below_state = below_state
            else:
                actual_below_state = state  # invalid state -> remain same spot

            next_states = {
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                },
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                },
            }

        else:  # action is 'RIGHT'
            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state
            else:
                actual_right_state = state  # invalid state -> remain same spot

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state
            else:
                actual_above_state = state  # invalid state -> remain same spot

            below_state = (state[0], state[1] + 1)

            if below_state in self.states:
                actual_below_state = below_state
            else:
                actual_below_state = state  # invalid state -> remain same spot

            next_states = {
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                },
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                },
            }

        return next_states
