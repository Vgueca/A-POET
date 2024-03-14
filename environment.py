import random as r
import numpy as np

class Environment:
    env_ids = 1  # Class variable to count child names
                 # The first one, hand-picked,  must be 0

    # Inicializar un reproductor que mínimo tenga un tipo de casilla
    def __init__(self, id = None, rows = 10, cols = 10,
                 agent_row = 5, agent_col = 5, agent_orientation = 0,
                 empty = 0, wall = 0, stone = 0, sand = 0, water = 0, grass = 0, mud = 0, bikini = 0, shoes = 0, charge = 0,
                 seed = 3):
        if id is None:
            print("ERROR: Environment ID not provided") # RAISE ERROR
            exit(1)

        self.name = 'e_' + str(id)
        self.rows = rows
        self.cols = cols

        # agent's start parameters
        self.agent_row = agent_row
        self.agent_col = agent_col
        self.agent_orientation = agent_orientation

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
        self.seed = seed

        self.game_map = self.generate_game_map()

    def mutate(self, categories):
        child_id = Environment.count_ids
        Environment.count_ids += 1

        rows = self.rows
        cols = self.cols

        agent_row = self.agent_row
        agent_col = self.agent_col
        agent_orientation = self.agent_orientation
        
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
        seed = self.seed

        #están un poco mal planteados los parametros, pensar mejor como codear y programar en consecuencia
        if 'rows' in categories:
            rows = self.rows + r.randint(-10, 10)

        if 'cols' in categories:
            cols = self.cols + r.randint(-1, 1)

        if 'empty' in categories:
            empty = np.round(self.empty + r.randint(0, 5)/rows) #Esta suma es una mierda
            max_empty = 0.5
            if empty > max_empty:
                empty = max_empty

            if empty <= 0.0:
                empty = 0.0

        #continuar con resto

        child = Environment(
            id=child_id,
            rows=rows,
            cols=cols,
            agent_row=agent_row,
            agent_col=agent_col,
            agent_orientation=agent_orientation,
            empty=empty,
            wall=wall,
            stone=stone,
            sand=sand,
            water=water,
            grass=grass,
            mud=mud,
            bikini=bikini,
            shoes=shoes,
            charge=charge,
            seed=seed
            )

        return child
    
    def get_game_map(self):
        return self.game_map
    
    def generate_game_map(self):
        pass