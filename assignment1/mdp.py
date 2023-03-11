class MDP:
    """
    Superclass representing a Markov Decision Process (MDP) represents a decision-making problem in which the outcomes
    are partly random and partly under the control of a decision-maker. It consists of a set of
    states, a set of actions, a transition model, and a reward function. The MDP has the Markov
    property, which means that the likelihood of future states only depends on the current state
    and action, not on the sequence of past states and actions.
    """

    def __init__(self, states, actions, discount_factor):
        """
        Initialize the MDP with the given set of states, actions, and discount factor.
        """
        self.states = states
        self.actions = actions
        self.discount_factor = discount_factor

    def transition_model(self, state, action, next_state):
        """
        Return the probability of transitioning from the current state to the next state
        given the action taken.
        """
        pass

    def reward_function(self, state):
        """
        Return the reward obtained at the given state.
        """
        pass

    def get_next_states(self, state, action):
        """
        Return the possible next states given the current state and action.
        """
        pass
