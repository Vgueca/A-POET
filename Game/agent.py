from Game.utils import *
from Game.brain import *

class Agent:
    def __init__(self, row, column, orientation, initial_vision, model, max_rows = 50, max_cols = 50, max_energy = 5000):
        self.row = row
        self.column = column
        self.orientation = orientation
        
        self.brain = Brain(model)
        
        self.energy = max_energy
        
        self.max_rows = max_rows
        self.max_cols = max_cols
        
        self.has_bikini = False
        self.has_shoes = False
        
        self.relative_row = 0
        self.relative_column = 0
        self.discovered_map = {}

        self.vision = initial_vision
        self.register_vision()
        
        self.alive = True

    def next_action(self, state):
        # Get the next action from the brain (model)
        return self.brain.get_action(state)
    
    def train_brain(self, new_state):
        self.brain.train(new_state)
    
    def get_score(self, state):
        return self.brain.compute_reward(state)

    def get_position(self):
        return self.row, self.column
    
    def get_orientation(self): 
        return self.orientation
    
    def get_energy(self):
        return self.energy
    
    def get_forward_cell_type(self):
        return self.vision[2]
    
    def get_bikini(self):
        return self.has_bikini
    
    def get_shoes(self):
        return self.has_shoes
    
    def get_memory(self):
        return self.discovered_map

    def is_alive(self):
        return self.alive
    
    def set_position(self, row, column):
        self.row = row
        self.column = column
        
    def set_orientation(self, orientation):
        self.orientation = orientation
        
    def set_energy(self, energy):
        self.energy = energy
        
    def increase_energy(self, energy):
        self.energy += energy
        
    def decrease_energy(self, energy):
        self.energy -= energy
        
    def set_bikini(self, has_bikini):
        self.has_bikini = has_bikini
        
    def set_shoes(self, has_shoes):
        self.has_shoes = has_shoes
    
    def set_vision(self, vision):
        self.vision = [CellType(x) for x in vision]
        self.register_vision()

    def enough_energy(self, action, current_cell_type):
        # Get the cost of the action and check if the agent has enough energy
        cost = get_cost(action, current_cell_type, self.has_bikini, self.has_shoes)
        return self.energy >= cost
    
    def move_forward(self):
        if self.orientation == Direction.UP:
            self.row -= 1
        elif self.orientation == Direction.DOWN:
            self.row += 1
        elif self.orientation == Direction.RIGHT:
            self.column += 1
        elif self.orientation == Direction.LEFT:
            self.column -= 1
        
    def turn_left(self):
        self.orientation = (self.orientation + 3) % 4
    
    def turn_right(self):
        self.orientation = (self.orientation + 1) % 4
            
    def register_vision(self):
        count = 0
        row = self.relative_row
        col = self.relative_column
        
        match self.orientation:
            # 0
            case Direction.UP:  
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map[(row-i, col+j)] = self.vision[count]
                        count += 1
            # 1
            case Direction.RIGHT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map[(row+j, col+i)] = self.vision[count]
                        count += 1
            # 2
            case Direction.DOWN:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map[(row+i, col-j)] = self.vision[count]
                        count += 1
            # 3
            case Direction.LEFT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map[(row-j, col-i)] = self.vision[count]
                        count += 1
                        
            