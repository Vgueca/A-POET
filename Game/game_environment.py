from gamemap import GameMap
from utils import *

class GameEnv:
    def __init__(self):
        self.game_map = GameMap(10, 10, (5, 5), Direction.UP)