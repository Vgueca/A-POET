from Game.gamemap import GameMap
from Game.utils import *

class GameEnv:
    def __init__(self, args):
        self.game_map = GameMap(args.rows, args.cols, (args.agent_row, args.agent_col), args.agent_orientation)