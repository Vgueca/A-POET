from utils import *
from model import *

class Agent:
    def __init__(self, posX, posY, orientation, max_rows = 100, max_cols = 100, max_battery = 5000):
        self.posX = posX
        self.posY = posY
        self.orientation = orientation
        self.brain = Brain()
        self.battery = max_battery
        self.max_rows = max_rows
        self.max_cols = max_cols
    
    def next_action(self):
        self.brain.get_action()

    def is_valid(self, action):
        if action == Action.FORWARD:
            return self.posX + 1 < self.max_rows and self.posX - 1 >= 0 and self.posY + 1 < self.max_cols and self.posY - 1 >= 0
        return True
