import random
from Game.state import *
from copy import deepcopy

class Brain:
    def __init__(self, model):
        self.model = model
        self.last_action = None
        self.prev_state = None
        
    def get_action(self, state):
        self.prev_state = deepcopy(state)

        self.last_action = self.model.get_action(state)
        
        return self.last_action
    
    def train(self, new_state):
        reward = self.compute_reward(new_state)

        if self.prev_state is None or self.last_action is None:
            print("Error: prev_state or last_action are None")
            exit(1)

        self.model.train(self.prev_state, self.last_action, reward, new_state)

    def compute_reward(self, new_state):
        # if new_state.agent_alive:
            return compute_percentage_map(new_state.agent_map) - compute_percentage_map(self.prev_state.agent_map) # + 0.1 * (new_state.agent_energy - self.prev_state.agent_energy) / new_state.agent_max_energy
    
        # return -1 # if the agent is dead, we give a negative reward