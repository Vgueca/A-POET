import numpy as np
from argparse import ArgumentParser
from copy import deepcopy

from Game.game_environment import GameEnv
from Game.agent import Agent
from Game.engine import Engine
from Game.utils import *

from environment import *
from Models.RL_model import *


def master(args):
    
    '''env = GameEnv(args)
    engine = Engine(env, Agent(args.agent_row, args.agent_col, args.agent_orientation, env.game_map.get_vision(args.agent_row, args.agent_col, args.agent_orientation)))
    engine.simulate()'''

    envs = []
    models = []
    scores = []
    pata_ec_scores = {}
    max_score_last_5 = []

    initial_env = Environment(id = 0)
    inital_model = Model(args)

    envs.append(initial_env)
    models.append(inital_model)
    scores[0] = []
    max_score_last_5[0] = []

    step = 0
    while step < args.max_steps:
        # Simulate every niche. Here the agents must train
        for index, (env, model) in enumerate(zip(envs, models)):
            score = Engine(env, model).simulate()
            
            if len(scores[index]) == 5:
                if max_score_last_5[index] == scores[index][0]:         # If the best score is going to be removed:
                    max_score_last_5[index] = max(scores[index][1:])    #   Recalculate the max score
                
                scores[index].pop(0)    # Remove the first score
            
            scores[index].append(score)
            pata_ec_scores[(index, index)] = score

            if score > max_score_last_5[index]:     # Update the max score
                max_score_last_5[index] = score

        step += 1

        if step % args.steps_before_transfer == 0:      # Attempt transfer
            for index_env, env in enumerate(envs):
                for index_model, model in enumerate(models):
                    if index_model == index_env:
                        continue

                    d_score = Engine(env, model).simulate(train=False)

                    pata_ec_scores[(index_env, index_model)] = d_score

                    if d_score > max_score_last_5[index_env]:           # Passes the direct transfer test
                        ft_score = Engine(env, deepcopy(model)).simulate(train=True)  # Should we use here a copy of the model (it is modified otherwise)?
                        if ft_score > max_score_last_5[index_env]:      # Passes the fine-tuning transfer test

                            # Transfer the model
                            scores[index_env] = [d_score, ft_score]
                            max_score_last_5[index_env] = max(d_score, ft_score)
                            models[index_env] = model

                            # Store the new pataec score
                            pata_ec_scores[(index_env, index_model)] = ft_score
        
        if step % args.steps_before_mutate == 0:
            minimal_criterion_for_reproduce() and reproduce()
            check_novelty_mutated_envs()

        


def main():
    parser = ArgumentParser()
    parser.add_argument("--rows", type=int, default=10)
    parser.add_argument("--cols", type=int, default=10)
    '''parser.add_argument("--agent_row", type=int, default=5)
    parser.add_argument("--agent_col", type=int, default=5)
    parser.add_argument("--agent_orientation", type=int, default=0)'''
    parser.add_argument("--max_simulation_iters", type=int, default=1000)
    parser.add_argument("--gui", type=bool, default=False)
    parser.add_argument("--max_steps", type=int, default=1000)
    parser.add_argument("--steps_before_transfer", type=int, default=25)
    parser.add_argument("--steps_before_mutate", type=int, default=100)
    parser.add_argument("--seed", type=int, default=3)
    args = parser.parse_args()
    
    master(args)
    

if __name__ == "__main__":
    main()