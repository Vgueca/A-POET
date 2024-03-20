import numpy as np
from argparse import ArgumentParser
from copy import deepcopy
from collections import namedtuple

from Game.agent import Agent
from Game.engine import Engine
from Game.utils import *

from environment import *
from Models.RL_model import *

from niche import Niche

from pata_ec import *

# GlobalStats = namedtuple("GlobalStats", ["Enviroment_Size", "Agent_Size", "Number_Transfers", "Number_mutations"])

def master(args):
    active_niches = []
    all_niches = []

    initial_env = Environment(name = "e_0", id = 0, seed = args.seed)
    inital_model = Model(args)

    initial_niche = Niche(0, initial_env, inital_model, args)
    active_niches.append(initial_niche)
    all_niches.append(initial_niche)
    
    #TODO print adequately the global stats for each iteration (via GUI in the future)
    n_mutations = 0
    n_transfers = 0

    step = 0
    while step < args.max_steps:
        # Simulate every niche. Here the agents must train
        for niche in active_niches:
            niche.simulate(args.simulation_batch_size)
            print("Step:", step, "Env:", niche.env.name, "Simulation finished with score:", niche.score)

        step += 1

        if len(active_niches) > 1 and step % args.steps_before_transfer == 0:      # Attempt transfer
            n_transfers += attempt_transfer(all_niches, args.pata_ec_batch_size)
        
        if step % args.steps_before_mutate == 0:
            # minimal_criterion_for_reproduce() and reproduce()
            # check_novelty_mutated_envs()
            update_all_niches_pata_ec(all_niches)
            n_mutations += mutate_envs(active_niches, all_niches, args)
            print("NUM EVS:", len(all_niches))

    
def attempt_transfer(all_niches, pata_ec_batch_size):         # In POET the only attempt the tranfers between the active niches
    n_transfer = 0
    for niche in all_niches:
        transfer_was_made = niche.attempt_transfer(all_niches, pata_ec_batch_size)
        
        if transfer_was_made:
            print("TRANSFER MADE!")
            n_transfers += 1

    return n_transfer

def mutate_envs(active_niches, all_niches, args):
    all_envs = [niche.env for niche in all_niches]
    all_models = [niche.model for niche in all_niches]  # Future possible change: we can use active_niches instead of all_niches

    parent_index_list = []
    child_list = []

    n_mutations = 0

    for index, niche in enumerate(active_niches):     # Future possible change: we can use all_niches instead of active_niches
        if niche.score > args.repro_threshold:
            parent_index_list.append(index)
    
    if len(parent_index_list) == 0:
        return 0

    for _ in range(args.max_children_trials):               # This is how POET does it. We can decide if we want to try to generate children only n times, or if we want to keep generating children until we reach the maximum number of children
        parent_id = np.random.choice(parent_index_list)     # Future possible change: This way we can choose the same parent more than once (we have to use replace=False if we don't want this to happen)
        parent_niche = active_niches[parent_id]
        child_env = parent_niche.env.mutate(args)

        if child_env not in all_envs:
            child_model = deepcopy(parent_niche.model)              # Not necessary because the model is not modified
            # score = Engine(child_env, child_model, args.max_simulation_iters, args.gui).simulate(train = False)
            score = Engine(child_env, child_model, args.max_simulation_iters, True).simulate(args.mc_batch_size, train = False)
            print(f"CHILD SCORE (mean over {args.mc_batch_size}):", score)
            if score > args.mc_lower and score < args.mc_upper:     # Passes the minimal criterion
                novelty_score = compute_novelty(child_env, all_niches, args.mc_lower, args.mc_upper, args.k, args.pata_ec_batch_size)
                child_list.append((child_env, child_model, score, novelty_score))

    child_list = sorted(child_list, key = lambda x: x[3], reverse = True) # Sort the children by novelty score

    print("CHILDREN CANDIDATES:", len(child_list))

    admitted = 0
    for child_env, child_model, child_score, _ in child_list:
        max_score = child_score
        model_max_score = child_model
        for model in all_models:
            score = Engine(child_env, model, args.max_simulation_iters, args.gui).simulate(args.pata_ec_batch_size, train = False)
            if score > max_score:
                max_score = score
                model_max_score = model

        print("MAX SCORE FOR CHILD:", max_score)
        
        if max_score > args.mc_lower and max_score < args.mc_upper:     # Passes the minimal criterion
            new_niche = Niche(len(all_niches), child_env, model_max_score, args)
            all_niches.append(new_niche)
            active_niches.append(new_niche)
            admitted += 1
            n_mutations += 1
            print("CHILD ADMITTED!")
            if admitted >= args.max_children:
                break

    if len(active_niches) > args.max_num_envs:
        active_niches = active_niches[:args.max_num_envs]

    return n_mutations

def main():
    parser = ArgumentParser()
    parser.add_argument("--max_simulation_iters", type=int, default=1000)
    parser.add_argument("--gui", type=bool, default=False)
    parser.add_argument("--max_steps", type=int, default=1000)
    parser.add_argument("--steps_before_transfer", type=int, default=25)
    parser.add_argument("--steps_before_mutate", type=int, default=100)
    parser.add_argument("--seed", type=int, default=3)
    parser.add_argument("--repro_threshold", type=int, default=0.75)    # The minimum score to reproduce (we must adjust this to our needs)
    parser.add_argument("--max_children_trials", type=int, default=8)   # The maximum number of reproduction trials per mutation step
    parser.add_argument("--max_children", type=int, default=1)          # The maximum number of children admitted per mutation step
    parser.add_argument("--max_num_envs", type=int, default=100)        # The maximum number of active environments
    parser.add_argument("--mc_lower", type=int, default=0.25)           # The minimum score to pass the minimal criterion (we must adjust this to our needs)
    parser.add_argument("--mc_upper", type=int, default=0.9)             # The maximum score to pass the minimal criterion (we must adjust this to our needs)
    parser.add_argument("--k", type=int, default=5)                     # The number of neighbors to consider for the novelty score (in POET they use 5)
    parser.add_argument("--learning_rate", type=float, default=0.1)
    parser.add_argument("--discount_factor", type=float, default=0.99)
    parser.add_argument("--epsilon_greedy", type=float, default=0.1)
    parser.add_argument("--simulation_batch_size", type=int, default=10)
    parser.add_argument("--mc_batch_size", type=int, default=5)
    parser.add_argument("--pata_ec_batch_size", type=int, default=5)
    parser.add_argument("--max_rows_change", type=int, default=5)
    parser.add_argument("--max_cols_change", type=int, default=5)
    parser.add_argument("--max_agent_row_change", type=int, default=5)
    parser.add_argument("--max_agent_col_change", type=int, default=5)
    parser.add_argument("--max_percentage_freq_change", type=float, default=0.05)
    args = parser.parse_args()
    
    master(args)
    

if __name__ == "__main__":
    main()