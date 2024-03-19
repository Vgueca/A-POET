from Game.utils import CellType, Direction
from Game.gui import *
import random

class GameMap:
    def __init__(self, rows, cols, initial_agent_position, initial_agent_orientation, map):
        self.rows = rows
        self.cols = cols
        
        self.map = map
        
        self.map_gui = GameGUI(self.map, initial_agent_position, initial_agent_orientation)

        self.agent_map = [[CellType.NOT_VISITED for _ in range(cols)] for _ in range(rows)]

        self.agent_gui = GameGUI(self.agent_map, initial_agent_position, initial_agent_orientation)

    def run(self):
        self.agent_gui.mainloop()
    
    def get_cell_type(self, row, col):
        return self.map[row][col]
    
    def get_vision(self, row, col, orientation):
        vision = []

        match orientation:
            # 0
            case Direction.UP:  
                for i in range(0, 4):
                    for j in range(-i,i+1):
                        if row-i < 0 or col+j < 0 or row-i >= self.rows or col+j >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(self.map[row-i][col+j])
            # 1
            case Direction.RIGHT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row+j < 0 or col+i < 0 or row+j >= self.rows or col+i >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(self.map[row+j][col+i])
            # 2
            case Direction.DOWN:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row+i < 0 or col-j < 0 or row+i >= self.rows or col-j >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(self.map[row+i][col-j])
            # 3
            case Direction.LEFT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row-j < 0 or col-i < 0 or row-j >= self.rows or col-i >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(self.map[row-j][col-i])
        
        return vision
    
    def update_agent_map(self, row, col, orientation):
        match orientation:
            # 0
            case Direction.UP:  
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row-i >= 0 and col+j >= 0 and row-i < self.rows and col+j < self.cols:
                            self.agent_map[row-i][col+j] = self.map[row-i][col+j]
            # 1
            case Direction.RIGHT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row+j >= 0 and col+i >= 0 and row+j < self.rows and col+i < self.cols:
                            self.agent_map[row+j][col+i] = self.map[row+j][col+i]
            # 2
            case Direction.DOWN:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row+i >= 0 and col-j >= 0 and row+i < self.rows and col-j < self.cols:
                            self.agent_map[row+i][col-j] = self.map[row+i][col-j]
            # 3
            case Direction.LEFT:
                for i in range(0,4):
                    for j in range(-i,i+1):
                        if row-j >= 0 and col-i >= 0 and row-j < self.rows and col-i < self.cols:
                            self.agent_map[row-j][col-i] = self.map[row-j][col-i]
        
        self.agent_gui.update_gui(self.agent_map, (row, col), orientation)
        self.map_gui.update_gui(self.map, (row, col), orientation)

    def create_map(self, rows, cols):
        self.initialize_random_map(rows, cols)
        
    def initialize_random_map(self, rows, cols):
        self.map = [[self.get_random_cell_type() for _ in range(cols)] for _ in range(rows)]
        
    def get_random_cell_type(self):
        random_number = random.randint(0, 100)
        
        if random_number < 30:
            return CellType.STONE
        elif random_number < 60:
            return CellType.SAND
        elif random_number < 70:
            return CellType.GRASS
        elif random_number < 80:
            return CellType.WATER
        elif random_number < 90:
            return CellType.WALL
        elif random_number < 92:
            return CellType.BIKINI
        elif random_number < 94:
            return CellType.SHOES
        elif random_number < 96:
            return CellType.MUD
        elif random_number < 98:
            return CellType.CHARGE
        else:
            return CellType.EMPTY
        
    def flatten_map(self):
        return [cell for row in self.agent_map for cell in row]