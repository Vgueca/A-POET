from environment import *
from Models.RL_model import *
from Game.engine import Engine
from copy import deepcopy
from collections import namedtuple
NicheStats = namedtuple("NicheStats", ["ID", "Environment", "Agent", "N_iters", "Percentage", "Score", "Max_Last_5_Scores"])

class Niche:
    def __init__(self, id, env, model, args):
        self.id = id
        self.env = env
        self.model = model

        self.score = None
        self.last_scores = []
        self.max_score_last_5 = -np.Infinity

        self.pata_ec_dict = {}       # Dictionary to store the pata_ec scores
        self.pata_ec_ranks = []      # Dictionary to store the pata_ec ranks

        self.mc_lower = args.mc_lower
        self.mc_upper = args.mc_upper
        
        self.stats = NicheStats(ID = id, Environment = env, Agent = model, N_iters = 0, Percentage = 0, Score=self.score, Max_Last_5_Scores=self.max_score_last_5) 

    def simulate(self, train = True):
        self.score = Engine(self.env, self.model).simulate(train)

        if len(self.last_scores) == 5:
            if self.max_score_last_5 == self.last_scores[0]:         # If the best score is going to be removed:
                self.max_score_last_5 = max(self.last_scores[1:])    #   Recalculate the max score
            
            self.last_scores.pop(0)    # Remove the first score
        
        self.last_scores.append(self.score)

        if self.score > self.max_score_last_5:     # Update the max score
            self.max_score_last_5 = self.score

    def attempt_transfer(self, all_niches):
        transfer_was_made = False

        for index, niche in enumerate(all_niches):
            if index == self.id:
                self.pata_ec[index] = self.score
                continue

            d_score = Engine(self.env, niche.model).simulate(train=False)

            self.pata_ec[index] = d_score                   # Update the pata_ec scores

            if d_score > self.max_score_last_5:             # Passes the direct transfer test
                new_model = deepcopy(niche.model)
                ft_score = Engine(self.env, new_model).simulate()
                if ft_score > self.max_score_last_5:        # Passes the fine-tuning transfer test
                    self.model = new_model
                    self.last_scores = [ft_score]
                    self.max_score_last_5 = ft_score
                    self.score = ft_score
                    self.pata_ec[self.id] = ft_score
                    transfer_was_made = True

        if transfer_was_made:
            for niche in all_niches:
                score = Engine(niche.env, self.model).simulate(train=False)
                niche.pata_ec[self.id] = score
    
    def update_pata_ec_ranks(self):
        def cap_score(score):
            if score < self.mc_lower:
                return self.mc_lower
            
            if score > self.mc_upper:
                return self.mc_upper

            return score
        
        raw_scores = []
        for value in self.pata_ec_dict.values():
            raw_scores.append(cap_score(value))
        
        self.pata_ec_ranks = np.argsort(-raw_scores)            # Sort the clipped pataec scores in descending order and store the indices
        self.pata_ec_ranks /= len(self.pata_ec_ranks) - 1   # Normalize the indices
        self.pata_ec_ranks -= 0.5                           # Center the indices