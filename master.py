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
    scores = [[]]
    pata_ec_scores = [[None]]
    pata_ec_ranks = None
    max_score_last_5 = []

    initial_env = Environment(id = 0)
    inital_model = Model(args)

    envs.append(initial_env)
    models.append(inital_model)
    max_score_last_5[0] = -np.Infinity

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
            pata_ec_scores[index][index] = score

            if score > max_score_last_5[index]:     # Update the max score
                max_score_last_5[index] = score

        step += 1

        if len(models) > 0 and step % args.steps_before_transfer == 0:      # Attempt transfer
            attempt_transfer()
        
        if step % args.steps_before_mutate == 0:
            # minimal_criterion_for_reproduce() and reproduce()
            # check_novelty_mutated_envs()
            update_pata_ec_ranks()
            mutate_envs()

    
    def attempt_transfer():
        for index_env, env in enumerate(envs):
            for index_model, model in enumerate(models):
                if index_model == index_env:
                    continue

                d_score = Engine(env, model).simulate(train=False)

                pata_ec_scores[index_env][index_model] = d_score

                if d_score > max_score_last_5[index_env]:           # Passes the direct transfer test
                    ft_score = Engine(env, deepcopy(model)).simulate(train=True)  # Should we use here a copy of the model (it is modified otherwise)?
                    if ft_score > max_score_last_5[index_env]:      # Passes the fine-tuning transfer test

                        # Transfer the model
                        scores[index_env] = [d_score, ft_score]
                        max_score_last_5[index_env] = max(d_score, ft_score)
                        models[index_env] = model

                        # Store the new pataec score
                        pata_ec_scores[index_env][index_model] = ft_score
        
    def mutate_envs():
        parent_id_list = []
        child_list = []

        for index in len(envs):
            if scores[index] > args.repro_threshold:
                parent_id_list.append(index)
        
        for _ in range(args.max_children_trials):               # This is how POET does it. We can decide if we want to try to generate children only n times, or if we want to keep generating children until we reach the maximum number of children
            parent_id = np.random.choice(parent_id_list)        # This way we can choose the same parent more than once (we have to use replace=False if we don't want this to happen)
            parent = envs[parent_id]
            child = parent.mutate()

            if child not in envs:   # This is not exactly like this. We must compare the encodings not the objects
                child_model = deepcopy(models[parent_id])
                score = Engine(child, child_model).simulate(train = False)
                if score > args.mc_lower and score < args.mc_upper:     # Passes the minimal criterion
                    novelty_score = compute_novelty(child)
                    child_list.append((child, child_model, score, novelty_score))

        child_list = sorted(child_list, key = lambda x: x[3], reverse = True) # Sort the children by novelty score

        admitted = 0
        for child, child_model, child_score, _ in child_list:
            max_score = child_score
            model_max_score = child_model
            for model in models:
                score = Engine(child, model).simulate(train = False)
                if score > max_score:
                    max_score = score
                    model_max_score = model
            
            if max_score > args.mc_lower and max_score < args.mc_upper:     # Passes the minimal criterion
                pata_ec_scores.append([None] * len(models))
                for i in range(len(pata_ec_scores)):
                    pata_ec_scores[i].append(None)
                envs.append(child)
                models.append(model_max_score)
                scores.append([max_score])
                max_score_last_5.append(max_score)
                pata_ec_scores[-1][-1] = max_score
                admitted += 1
                if admitted >= args.max_children:
                    break

        while len(envs) > args.max_num_envs:    # We can do this easier using the del statement
            # Remove the first environment and all its data (if we use unique ids it would be easier to remove the environment and its data)
            envs.pop(0)
            models.pop(0)
            scores.pop(0)
            max_score_last_5.pop(0)
            for key in list(pata_ec_scores.keys()):
                if key[0] == 0:
                    pata_ec_scores.pop(key)
                elif key[1] == 0:
                    pata_ec_scores.pop(key)
                else:
                    key = (key[0] - 1, key[1] - 1)      # I'm not sure if this is the correct way to do it because the keys are modified while iterating over them

    def compute_novelty(child):
        # Compute the novelty of the child
        pass

    def update_pata_ec_ranks():
        def cap_score(score):
            return min(max(score, args.mc_lower), args.mc_upper)
        
        pata_ec_ranks = pata_ec_scores

        # Update the pataec ranks
        
        for i in range(len(envs)):
            for j in range(len(models)):
                if pata_ec_ranks[i][j] is None:
                    pata_ec_ranks[i][j] = cap_score(pata_ec_ranks[i][j])
        
        for env_pata_ec in pata_ec_ranks:
            env_pata_ec = np.argsort(-env_pata_ec)    # Sort the clipped pataec scores in descending order and store the indices
            env_pata_ec /= len(env_pata_ec) - 1       # Normalize the indices
            env_pata_ec -= 0.5                        # Center the indices

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
    parser.add_argument("--repro_threshold", type=int, default=200)     # The minimum score to reproduce (we must adjust this to our needs)
    parser.add_argument("--max_children_trials", type=int, default=8)   # The maximum number of reproduction trials per mutation step
    parser.add_argument("--max_children", type=int, default=1)          # The maximum number of children admitted per mutation step
    parser.add_argument("--max_num_envs", type=int, default=100)        # The maximum number of active environments
    parser.add_argument("--mc_lower", type=int, default=25)             # The minimum score to pass the minimal criterion (we must adjust this to our needs)
    parser.add_argument("--mc_upper", type=int, default=340)            # The maximum score to pass the minimal criterion (we must adjust this to our needs)
    args = parser.parse_args()
    
    master(args)
    

if __name__ == "__main__":
    main()