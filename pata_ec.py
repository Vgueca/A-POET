from Game.engine import Engine
import numpy as np

def compute_novelty(child, all_niches, lower, upper, k, pata_ec_batch_size):
    pata_ec = compute_pata_ec(child, all_niches, lower, upper, pata_ec_batch_size)

    distances = []

    for niche in all_niches:
        distances.append(np.linalg.norm(pata_ec - niche.pata_ec_ranks))

    top_k = np.argsort(np.array(distances))[:k]                           # Sort the distances and store the indices of the k smallest distances
    novelty_score = np.mean([distances[i] for i in top_k])      # Compute the novelty score as the mean of the k smallest distances

    return novelty_score

def cap_score(score, lower, upper):
        if score < lower:
            return lower
        
        if score > upper:
            return upper

        return score

def compute_ranks(x):
    values = np.array(x)

    assert values.ndim == 1

    # Encontrar los valores únicos y sus índices
    unique_values, _ = np.unique(x, return_inverse=True)

    # Crear un diccionario para mapear valores únicos a rangos
    unique_to_rank = {val: rank for rank, val in enumerate(unique_values)}

    # Crear un array de rangos usando el diccionario
    ranks = np.array([unique_to_rank[val] for val in x], dtype=float)

    return ranks

def compute_pata_ec(env, all_niches, lower, upper, pata_ec_batch_size):
    raw_scores = []

    for niche in all_niches:
        score = cap_score(Engine(env, niche.model, niche.args.max_simulation_iters, niche.args.gui).simulate(pata_ec_batch_size, train = False)[0], lower, upper)
        raw_scores.append(score)
    
    env_pata_ec = compute_ranks(raw_scores)             # Sort the clipped pataec scores in descending order and store the indices
    if len(env_pata_ec) > 1:
        env_pata_ec /= float(len(env_pata_ec) - 1)      # Normalize the indices
        env_pata_ec -= 0.5                              # Center the indices

    return env_pata_ec

def update_all_niches_pata_ec(all_niches):
    for niche in all_niches:
        niche.update_pata_ec_ranks(all_niches)