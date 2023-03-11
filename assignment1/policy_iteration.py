
from assignment1.mdp import MDP

# reference: policy iteration algorithm,
# as shown in figure 17.7 of Artificial Intelligence: A Modern Approach


def policy_iteration(
    mdp: MDP,
    num_policy_evaluation: int = 1,
    verbose: bool = False
):
    """
    params:
    - mdp (MDP): an MDP with 
        states S, 
        actions A(s), 
        transition model P(s′|s, a), 
        rewards R(s), 
        discount γ
    - num_policy_evaluation (int): number of times to do policy evaluation (k)
    - verbose (bool): determines whether to print information
    return: {
        'utilities': {
            (x, y): utility value (float)
        },
        'optimal_policy': {
            (x, y): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    }
    """
    # U , a vector of utilities for states in S , initially zero
    # π, a policy vector indexed by state, initially random
    utilities, policy = {}, {}

    # for: Plot of utility estimates as a function of the number of iterations
    iteration_utilities = {}

    for state_position in mdp.states:
        utilities[state_position] = 0
        policy[state_position] = 'UP'

        # start with first utility in place since it is updated at end of iteration
        iteration_utilities[state_position] = [0]

    unchanged = False
    num_iterations = 0

    # repeat
    while not unchanged:
        # U ← POLICY-EVALUATION (π, U , mdp)
        utilities, new_iteration_utilities = _policy_evaluation(
            mdp,
            policy,
            utilities,
            num_policy_evaluation,
        )

        policy, unchanged = _policy_improvement(mdp, policy, utilities)

        num_iterations += num_policy_evaluation
        print('unchanged:', unchanged, 'at iteration:', num_iterations)

        if verbose:
            print('iteration:', num_iterations)

        for state_position in mdp.states:
            iteration_utilities[state_position].extend(
                new_iteration_utilities[state_position])

            if verbose:
                print('at', state_position, '-best action:',
                      policy[state_position])

    # algorithm: return π
    #
    # in my implementation, I return the utilities and number of iterations
    # as well, as they will come in useful later
    return {
        'utilities': utilities,
        'optimal_policy': policy,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_utilities,
    }


def _policy_evaluation(
    mdp: MDP,
    policy: dict,
    utilities: dict,
    num_policy_evaluation: int,
):
    """
    Simplified version of Bellman equation.
    params:
    - mdp (MDP): an MDP with 
        states S, 
        actions A(s), 
        transition model P(s′|s, a), 
        rewards R(s), 
        discount γ
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }
    - num_policy_evaluation (int): number of times to do policy evaluation (k)
    return: (
        { (x, y): updated utility value (float) },
        { (x, y): [utility for each iteration (float)] }
    )
    """
    current_utilities, updated_utilities = {}, {}
    new_iteration_utilities = {}

    for state_position in mdp.states:
        # U_i ← U
        current_utilities[state_position] = utilities[state_position]
        new_iteration_utilities[state_position] = []

    # for i in range(k)
    for _ in range(num_policy_evaluation):
        # for each state s in S do
        for state_position in mdp.states:
            reward = mdp.reward_function(state_position)

            # ∑s′P (s'|s, π_i(s)) U_i(s')
            expected_utility = _get_expected_utility(
                mdp,
                state_position,
                policy[state_position],
                current_utilities
            )

            # U_i+1(s) ← R(s) + γ ∑s′P (s'|s, π_i(s)) U_i(s')
            updated_utilities[state_position] = reward + \
                mdp.discount * expected_utility

        # U_i ← U_i+1
        for state_position in mdp.states:
            current_utilities[state_position] = updated_utilities[state_position]
            new_iteration_utilities[state_position].append(
                current_utilities[state_position])

    return (current_utilities, new_iteration_utilities)


def _policy_improvement(
    mdp,
    policy,
    utilities,
):
    """
    params:
    - mdp (MDP): the MDP to solve
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }
    return: (
        updated_policy (dict),
        unchanged (bool),
    )
    """
    updated_policy = {}
    unchanged = True  # unchanged? ← true

    # for each state s in S do
    for state_position in mdp.states:
        # get max a∈A(s) ∑s′ P (s'|s, a) U [s']
        max_expected_utility = float('-inf')
        best_action = None

        action_next_state_map = mdp.states[state_position]

        for action in action_next_state_map:
            expected_utility = _get_expected_utility(
                mdp,
                state_position,
                action,
                utilities
            )

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

        # get ∑s′ P (s'|s, π[s]) U [s']
        utility = _get_expected_utility(
            mdp,
            state_position,
            policy[state_position],
            utilities
        )

        # if max a∈A(s) ∑s′ P (s'|s, a) U [s'] > ∑s′ P (s'|s, π[s]) U [s'] then do
        if max_expected_utility > utility:
            updated_policy[state_position] = best_action
            unchanged = False
        else:
            updated_policy[state_position] = policy[state_position]

    return (updated_policy, unchanged)
