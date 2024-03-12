import random
import numpy as np
from argparse import ArgumentParser

from Game.game_environment import GameEnv
from Game.agent import Agent
from Game.engine import Engine
from Game.utils import *


def master(args):
    
    env = GameEnv(args)
    engine = Engine(env, Agent(args.agent_row, args.agent_col, args.agent_orientation, env.game_map.get_vision(args.agent_row, args.agent_col, args.agent_orientation)))
    engine.simulate()



def main():
    parser = ArgumentParser()
    parser.add_argument("--rows", type=int, default=10)
    parser.add_argument("--cols", type=int, default=10)
    parser.add_argument("--agent_row", type=int, default=5)
    parser.add_argument("--agent_col", type=int, default=5)
    parser.add_argument("--agent_orientation", type=int, default=0)
    parser.add_argument("--max_iters", type=int, default=1000)
    args = parser.parse_args()
    
    master(args)
    

if __name__ == "__main__":
    main()