from utils import CellType

class State:
    def __init__(self, agent):
        self.agent_memory = agent.get_memory()
        self.agent_position = agent.get_position()
        self.agent_orientation = agent.get_orientation()
        self.agent_energy = agent.get_energy()
        self.agent_vision = agent.get_vision()
        self.agent_bikini = agent.get_bikini()
        self.agent_shoes = agent.get_shoes()
        self.agent_alive = agent.is_alive()
        
    def flatten_state(self): # we are not using it since we have not a neural network as model
        return [self.agent_position[0], self.agent_position[1], self.agent_orientation, self.agent_energy, self.agent_bikini, self.agent_shoes] + self.agent_vision + self.agent_memory #TODO concatenate dictionary with lists???

    def __eq__(self, other):
        return self.agent_position == other.agent_position and \
            self.agent_orientation == other.agent_orientation and \
            self.agent_energy == other.agent_energy and \
            self.agent_vision == other.agent_vision and \
            self.agent_bikini == other.agent_bikini and \
            self.agent_shoes == other.agent_shoes and \
            self.agent_memory == other.agent_memory
    
    def compute_percentage_map(self):
        return self.agent_memory.values().count(CellType.EMPTY) / len(self.agent_memory)