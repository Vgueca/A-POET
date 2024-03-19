import random

class Brain:
    def __init__(self, model):
        self.model = model
        
    def get_action(self, state):
        self.prev_state = state

        self.last_action = random.randint(0, 3)
        
        return self.last_action
    
    def train(self, new_state):
        reward = self.compute_reward(new_state)

        self.model.train(self.prev_state, self.last_action, reward)

    def compute_reward(self, state):
        # TODO compute the reward based on the state
        pass