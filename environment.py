import random as r
import numpy as np

class Environment:
    env_ids = 1  # Class variable to count child names
                 # The first one, hand-picked,  must be 0

    # Inicializar un reproductor que mínimo tenga un tipo de casilla
    def __init__(self, id = None, n_cells = 0, dim_rel = 0, 
                 empty = 0, wall = 0, stone = 0, sand = 0, water = 0, grass = 0, mud = 0, bikini = 0, shoes = 0, charge = 0):
        self.name = 'e_' + str(id)
        self.n_cells = n_cells
        self.dim_rel = dim_rel

        self.empty = empty
        self.wall = wall
        self.stone = stone
        self.sand = sand
        self.water = water
        self.grass = grass
        self.mud = mud
        self.bikini = bikini
        self.shoes = shoes
        self.charge = charge

    def mutate(self, categories):
        child_id = Environment.count_ids
        Environment.count_ids += 1

        n_cells = self.n_cells
        dim_rel = self.dim_rel
        empty = self.empty
        wall = self.wall
        stone = self.stone
        sand = self.sand
        water = self.water
        grass = self.grass
        mud = self.mud
        bikini = self.bikini
        shoes = self.shoes
        charge = self.charge

        #están un poco mal planteados los parametros, pensar mejor como codear y programar en consecuencia
        if 'n_cells' in categories:
            n_cells = self.n_cells + r.randint(-10, 10)

        if 'dim_rel' in categories:
            n_cells = self.n_cells + r.randint(-1, 1)

        if 'empty' in categories:
            empty = np.round(self.empty + r.randint(0, 5)/n_cells) #Esta suma es una mierda
            max_empty = 0.5
            if empty > max_empty:
                empty = max_empty

            if empty <= 0.0:
                empty = 0.0

        #continuar con resto


        child = Environment(
            name=child_id,
            )

        return child