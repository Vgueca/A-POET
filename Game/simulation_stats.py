class SimulationStats:
    def __init__(self):
        self.actions = []
        self.map_percentage = []
        self.energy = []
        self.rewards = []
    
    def update(self, agent, state):
        self.actions.append(agent.brain.last_action)
        self.map_percentage.append(state.compute_percentage_map())
        self.energy.append(agent.get_energy())
        self.rewards.append(agent.get_reward(state))

    def compute_average_energy_consumition(self):
        return sum([self.energy[i] - self.energy[i-1] for i in range(0, len(self.energy))]) / len(self.energy)
    
    def compute_average_map_percentage(self):
        return sum([self.map_percentage[i] - self.map_percentage[i-1] for i in range(0, len(self.map_percentage))]) / len(self.map_percentage)
        
    def compute_percentage_actions(self):
        
        # we can use the count method of the list to count the number of times an action was used
        idle = self.actions.count(0)
        forward = self.actions.count(1)
        turn_left = self.actions.count(2)
        turn_right = self.actions.count(3)
        
        # we can use the len method of the list to get the total number of actions
        total = len(self.actions)
        
        # we can use the format method to print the percentage of each action
        print("Percentage of IDLE action: ", idle/total)
        print("Percentage of FORWARD action: ", forward/total)
        print("Percentage of TURN_LEFT action: ", turn_left/total)
        print("Percentage of TURN_RIGHT action: ", turn_right/total)   
    
    def print_summary(self):
        print("Percentage of map discovered: ", self.map_percentage[-1])
        print("Average energy consumed: ", self.compute_average_energy_consumition())
        print("Percentage of each action: ", self.compute_percentage_actions())
        print("Final score: ", sum(self.rewards))