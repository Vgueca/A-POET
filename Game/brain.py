import random

class Brain:
    def __init__(self, model):
        self.model = model
        
    def get_action(self, state):
        self.prev_state = state

        self.last_action = self.model.get_action(state)
        
        return self.last_action
    
    def train(self, new_state):
        reward = self.compute_reward(new_state)

        self.model.train(self.prev_state, self.last_action, reward, new_state)

    def compute_reward(self, new_state):
        if new_state.agent_alive:
            return new_state.compute_percentage_map() - self.prev_state.compute_percentage_map() # + 0.1 * (new_state.agent_energy - self.prev_state.agent_energy) / new_state.agent_max_energy
    
        return -100 # if the agent is dead, we give a negative reward