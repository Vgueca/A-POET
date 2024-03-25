from environment import *
from Models.RL_model import *
from Game.engine import Engine
from copy import deepcopy
from collections import namedtuple
from pata_ec import compute_ranks
NicheStats = namedtuple("NicheStats", ["ID", "Environment", "Agent", "N_iters", "Percentage", "Score", "Max_Last_5_Scores"])

class Niche:
    def __init__(self, id, env, model, args):
        self.id = id
        self.env = env
        self.model = model

        self.score = 0
        self.last_scores = []
        self.max_score_last_5 = -np.Infinity

        self.pata_ec_dict = {}       # Dictionary to store the pata_ec scores
        self.pata_ec_ranks = []      # List to store the pata_ec ranks

        self.args = args
        
        self.stats = NicheStats(ID = id, Environment = env, Agent = model, N_iters = 0, Percentage = 0, Score=self.score, Max_Last_5_Scores=self.max_score_last_5)

    def simulate(self, batch_size, train = True):
        self.score, best_stats = Engine(self.env, self.model, self.args.max_simulation_iters, self.args.gui).simulate(batch_size, train)

        if len(self.last_scores) == 5:
            if self.max_score_last_5 == self.last_scores[0]:         # If the best score is going to be removed:
                self.max_score_last_5 = max(self.last_scores[1:])    #   Recalculate the max score
            
            self.last_scores.pop(0)    # Remove the first score
        
        self.last_scores.append(self.score)
        self.pata_ec_dict[self.id] = self.score

        if self.score > self.max_score_last_5:     # Update the max score
            self.max_score_last_5 = self.score
        
        return best_stats

    def attempt_transfer(self, all_niches, pata_ec_batch_size):
        transfer_was_made = False

        for niche in all_niches:
            if niche.id == self.id:
                # self.pata_ec_dict[index] = self.score
                continue

            d_score = Engine(self.env, niche.model, self.args.max_simulation_iters, self.args.gui).simulate(pata_ec_batch_size, train = False)[0]

            self.pata_ec_dict[niche.id] = d_score                   # Update the pata_ec scores

            if d_score > self.max_score_last_5:             # Passes the direct transfer test
                new_model = deepcopy(niche.model)
                ft_score = Engine(self.env, new_model, self.args.max_simulation_iters, self.args.gui).simulate(pata_ec_batch_size, train = True)[0]
                if ft_score > self.max_score_last_5:        # Passes the fine-tuning transfer test
                    self.model = new_model
                    self.last_scores = [ft_score]
                    self.max_score_last_5 = ft_score
                    self.score = ft_score
                    self.pata_ec_dict[self.id] = ft_score
                    transfer_was_made = True

        if transfer_was_made:
            for niche in all_niches:
                score = Engine(niche.env, self.model, self.args.max_simulation_iters, self.args.gui).simulate(pata_ec_batch_size, train = False)[0]
                niche.pata_ec_dict[self.id] = score
    
    def update_pata_ec_ranks(self, all_niches):
        def cap_score(score):
            if score < self.args.mc_lower:
                return self.args.mc_lower
            
            if score > self.args.mc_upper:
                return self.args.mc_upper

            return score
        
        raw_scores = []
        for niche in all_niches:
            value = self.pata_ec_dict[niche.id]
            raw_scores.append(cap_score(value))
        
        self.pata_ec_ranks = compute_ranks(raw_scores)                          # Sort the clipped pataec scores in descending order and store the indices
        if len(self.pata_ec_ranks) > 1:
            self.pata_ec_ranks /= float(len(self.pata_ec_ranks) - 1)            # Normalize the indices
            self.pata_ec_ranks -= 0.5                                           # Center the indices