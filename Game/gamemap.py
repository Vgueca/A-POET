from utils import CellType, Direction
from gui import *
import random

class GameMap:
    def __init__(self, rows, cols, initial_agent_position, initial_agent_orientation):
        self.rows = rows
        self.cols = cols
        self.map = self.create_map(rows, cols)

        self.agent_map = [[CellType.EMPTY for _ in range(cols)] for _ in range(rows)]

        self.game_gui = GameGUI(self.agent_map, initial_agent_position, initial_agent_orientation)

        self.game_gui.mainloop()
    
    def get_cell_type(self, row, col):
        return self.map[row][col]
    
    def get_vision(self, row, col, orientation):
        vision = []

        match orientation:
            # 0
            case Direction.UP:  
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row-i < 0 or col+j < 0 or row-i >= self.rows or col+j >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(map[row-i][col+j])
            # 1
            case Direction.RIGHT:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row+j < 0 or col+i < 0 or row+j >= self.rows or col+i >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(map[row+j][col+i])
            # 2
            case Direction.DOWN:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row+i < 0 or col-j < 0 or row+i >= self.rows or col-j >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(map[row+i][col-j])
            # 3
            case Direction.LEFT:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row-j < 0 or col-i < 0 or row-j >= self.rows or col-i >= self.cols:
                            vision.append(CellType.EMPTY)
                        else:
                            vision.append(map[row-j][col-i])
        
        return vision
    
    def update_agent_map(self, row, col, orientation):
        self.agent_map = [[CellType.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

        match orientation:
            # 0
            case Direction.UP:  
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row-i < 0 or col+j < 0 or row-i >= self.rows or col+j >= self.cols:
                            self.agent_map[row-i][col+j] = self.map[row-i][col+j]
            # 1
            case Direction.RIGHT:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row+j < 0 or col+i < 0 or row+j >= self.rows or col+i >= self.cols:
                            self.agent_map[row+j][col+i] = self.map[row+j][col+i]
            # 2
            case Direction.DOWN:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row+i < 0 or col-j < 0 or row+i >= self.rows or col-j >= self.cols:
                            self.agent_map[row+i][col-j] = self.map[row+i][col-j]
            # 3
            case Direction.LEFT:
                for i in range(0, 3):
                    for j in range(-i, i):
                        if row-j < 0 or col-i < 0 or row-j >= self.rows or col-i >= self.cols:
                            self.agent_map[row-j][col-i] = self.map[row-j][col-i]
        
        self.game_gui.update_gui(self.agent_map, self.agent_position, self.agent_orientation)

    def create_map(self, rows, cols):
        self.initialize_random_map(rows, cols)
    
    def initialize_random_map(self, rows, cols):
        map = [[random.randint(0, 10) for _ in range(cols)] for _ in range(rows)]