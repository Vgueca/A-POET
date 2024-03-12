from utils import *
from brain import *

class CoordinatesDictionary:
    # Create a void dictionary to store the relative coordinates and their values
    def __init__(self):
        self.c_dictionary = {}
    
    def add_c(self, x, y, value):
        self.c_dictionary[(x, y)] = value
    
    def get_c(self, key):
        return self.c_dictionary[key]
    
    def remove_c(self, x, y):
        del self.c_dictionary[(x, y)]


class Agent:
    def __init__(self, row, column, orientation, initial_vision, max_rows = 100, max_cols = 100, max_energy = 5000):
        self.row = row
        self.column = column
        self.orientation = orientation
        
        self.brain = Brain()
        
        self.energy = max_energy
        
        self.max_rows = max_rows
        self.max_cols = max_cols
        
        self.has_bikini = False
        self.has_shoes = False
        
        self.relative_row = 0
        self.relative_column = 0
        self.discovered_map = CoordinatesDictionary()

        self.vision = initial_vision
        self.register_vision()

    def next_action(self):
        # Get the next action from the brain (model)
        return self.brain.get_action()

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
                        self.discovered_map.add_c(row-i, col+j, self.vision[count])
                        count += 1
            # 1
            case Direction.RIGHT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map.add_c(row+j, col+i, self.vision[count])
                        count += 1
            # 2
            case Direction.DOWN:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map.add_c(row+i, col-j, self.vision[count])
                        count += 1
            # 3
            case Direction.LEFT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        self.discovered_map.add_c(row-j, col-i, self.vision[count])
                        count += 1
                        
            