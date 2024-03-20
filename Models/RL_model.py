import numpy as np

class Model:
    def __init__(self, args):
        self.q_values = {}
        self.learning_rate = args.learning_rate
        self.discount_factor = args.discount_factor
        self.epsilon = args.epsilon_greedy

        #self.model = self.build_model()

    def get_action(self, state):
        self.initialize_q_values(state)
        if np.random.rand() < self.epsilon:
            return np.random.choice(4)
        else:
            candidates_q_values = [self.q_values[(state, a)] for a in range(4)]
            return np.argmax(candidates_q_values)

    def train(self, prev_state, action, reward, next_state):
        self.initialize_q_values(prev_state)
        self.initialize_q_values(next_state)
        
        ''' Condition that should never happen
        # if next state is none it means that the agent has reached a terminal state
        if next_state is None:
            self.q_values[(prev_state, action)] += self.learning_rate * (reward - self.q_values[(prev_state, action)])
            return'''
        
        candidates_q_values = [self.q_values[(next_state, a)] for a in range(4)]
        next_q_value = np.max(candidates_q_values)
        
        self.q_values[(prev_state, action)] += self.learning_rate * (reward + self.discount_factor * next_q_value - self.q_values[(prev_state, action)])
        
    # if the q_values are not initialized, we initialize them
    def initialize_q_values(self, state):
        for action in range(4):
            if (state, action) not in self.q_values:
                self.q_values[(state, action)] = 0


