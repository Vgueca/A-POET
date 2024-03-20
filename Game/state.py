from Game.utils import CellType

class State:
    def __init__(self, agent, agent_map):
        self.agent_memory = agent.get_memory()
        self.agent_map = agent_map
        self.agent_position = agent.get_position()
        self.agent_orientation = agent.get_orientation()
        self.agent_energy = agent.get_energy()
        self.agent_vision = agent.get_vision()
        self.agent_bikini = agent.get_bikini()
        self.agent_shoes = agent.get_shoes()
        self.agent_alive = agent.is_alive()
        self.agent_max_energy = agent.max_energy
        
    def flatten_state(self): # we are not using it since we have not a neural network as model
        return [self.agent_position[0], self.agent_position[1], self.agent_orientation, self.agent_energy, self.agent_bikini, self.agent_shoes] + self.agent_vision + self.agent_memory #TODO concatenate dictionary with lists???
    
    def __key(self):
        return (self.agent_position, self.agent_orientation, self.agent_energy, tuple(self.agent_vision), self.agent_bikini, self.agent_shoes, tuple(self.agent_memory))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__key() == other.__key()
        return NotImplemented
    
def compute_percentage_map(agent_map):
    flatten_agent_map = [x for row in agent_map for x in row]
    return (len(flatten_agent_map) - flatten_agent_map.count(CellType.NOT_VISITED)) / len(flatten_agent_map)