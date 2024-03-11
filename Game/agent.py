from utils import *
from model import *

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
        
        self.vision = initial_vision

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
        return self.vision[0]
    
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
        self.vision = vision

    def enough_energy(self, action, current_cell):
        # Get the cost of the action and check if the agent has enough energy
        cost = get_cost(action, current_cell, self.has_bikini, self.has_shoes)
        return self.energy - cost >= 0
    
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
        if self.orientation == Direction.UP:
            self.orientation = Direction.LEFT
        elif self.orientation == Direction.DOWN:
            self.orientation = Direction.RIGHT
        elif self.orientation == Direction.RIGHT:
            self.orientation = Direction.UP
        elif self.orientation == Direction.LEFT:
            self.orientation = Direction.DOWN
    
    def turn_right(self):
        if self.orientation == Direction.UP:
            self.orientation = Direction.RIGHT
        elif self.orientation == Direction.DOWN:
            self.orientation = Direction.LEFT
        elif self.orientation == Direction.RIGHT:
            self.orientation = Direction.DOWN
        elif self.orientation == Direction.LEFT:
            self.orientation = Direction.UP