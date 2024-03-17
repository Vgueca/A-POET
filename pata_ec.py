from Game.engine import Engine
from environment import Environment
from niche import Niche
from Models.RL_model import Model
import numpy as np

def compute_novelty(child, all_niches, lower, upper, k):
    pata_ec = compute_pata_ec(child, all_niches, lower, upper)

    distances = []

    for niche in all_niches:
        distances.append(np.linalg.norm(pata_ec - niche.pata_ec))

    top_k = np.argsort(distances)[:k]                           # Sort the distances and store the indices of the k smallest distances
    novelty_score = np.mean([distances[i] for i in top_k])      # Compute the novelty score as the mean of the k smallest distances

    return novelty_score

def cap_score(score, lower, upper):
        if score < lower:
            return lower
        
        if score > upper:
            return upper

        return score

def compute_pata_ec(env, all_niches, lower, upper):
    raw_scores = []

    for niche in all_niches:
        score = cap_score(Engine(env, niche.model).simulate(train = False), lower, upper)
        raw_scores.append(score)
    
    env_pata_ec = np.argsort(-raw_scores)     # Sort the clipped pataec scores in descending order and store the indices
    env_pata_ec /= len(env_pata_ec) - 1       # Normalize the indices
    env_pata_ec -= 0.5                        # Center the indices

    return env_pata_ec

def update_all_niches_pata_ec(all_niches):
    for niche in all_niches:
        niche.update_pata_ec_ranks()