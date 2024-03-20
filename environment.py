import random
import numpy as np
from math import *
import Game.gamemap
from Game.utils import CellType

class Environment:
    env_ids = 1  # Class variable to count child names
                 # The first one, hand-picked, must be 0
    
    max_rows = 50
    max_cols = 50

    # Inicializar un reproductor que mínimo tenga un tipo de casilla
    def __init__(self, name, id = None, rows = 10, cols = 10,
                 agent_row = 5, agent_col = 5, agent_orientation = 0,
                 relative_freqs = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],       # 0. Empty | 1. Wall | 2. Stone | 3. Sand | 4. Water | 5. Grass | 6. Mud | 7. Bikini | 8. Shoes | 9. Charge
                 seed = 3):
        if id is None:
            print("ERROR: Environment ID not provided") # RAISE ERROR
            exit(1)

        self.name = name
        self.rows = rows
        self.cols = cols

        # agent's start parameters
        self.agent_row = agent_row
        self.agent_col = agent_col
        self.agent_orientation = agent_orientation

        self.relative_freqs = relative_freqs
        
        if id == 0:
            random.seed(seed)

        self.seed = seed

        self.game_map = self.generate_game_map()    # Maybe we should delete the game map when the environment is not active

    def mutate(self, args):
        child_id = Environment.env_ids    # If we use parallelism, we must use a lock to avoid problems
        Environment.env_ids += 1

        name = self.name + "_" + str(child_id)

        rows = self.rows
        cols = self.cols

        agent_row = self.agent_row
        agent_col = self.agent_col
        agent_orientation = self.agent_orientation
        
        freqs = self.relative_freqs

        seed = self.seed

        # MUTATE ROWS
        rows = rows + random.randint(-args.max_rows_change, args.max_rows_change + 1)
        if rows > Environment.max_rows:
            rows = Environment.max_rows
        if rows < 1:
            rows = 1

        # MUTATE COLS
        cols = cols + random.randint(-args.max_cols_change, args.max_cols_change + 1)
        if cols > Environment.max_cols:
            cols = Environment.max_cols
        if cols < 1:
            cols = 1

        # MUTATE AGENT
        agent_row = agent_row + random.randint(-args.max_agent_row_change, args.max_agent_row_change + 1)
        if agent_row < 0:
            agent_row = 0
        elif agent_row >= rows:
            agent_row = rows - 1
        agent_col = agent_col + random.randint(-args.max_agent_col_change, args.max_agent_col_change + 1)
        if agent_col < 0:
            agent_col = 0
        elif agent_col >= cols:
            agent_col = cols - 1
        agent_orientation = random.randint(0, 3)

        # MUTATE FREQS
        n_cells = rows * cols
        freq_step = 1/n_cells
        max_change = round(args.max_percentage_freq_change * n_cells)

        for i in range(len(freqs)):
            freqs[i] += random.randint(-max_change, max_change) * freq_step
            if freqs[i] < 0:
                freqs[i] = 0
            elif freqs[i] > 1:
                freqs[i] = 1
    
        freqs = normalize_vector(freqs)

        # Creating child
        child = Environment(
            name=name,
            id=child_id,
            rows=rows,
            cols=cols,
            agent_row=agent_row,
            agent_col=agent_col,
            agent_orientation=agent_orientation,
            relative_freqs=freqs, 
            seed=seed
            )

        return child
    
    def generate_game_map(self):
        cell_types = self.get_cell_types_number()
        
        map = self.put_cell_types_into_vector(cell_types)

        agent_index = self.agent_row * self.cols + self.agent_col
        random.shuffle(map)

        if map[agent_index] == CellType.EMPTY or map[agent_index] == CellType.WALL:     # If the agent is in an empty or wall cell, we swap it with a non-empty and non-wall cell
            indexes_map_not_empty_not_wall = [i for i in range(len(map)) if map[i] != CellType.EMPTY and map[i] != CellType.WALL]
            random_index = random.choice(indexes_map_not_empty_not_wall)

            aux = map[agent_index]
            map[agent_index] = map[random_index]
            map[random_index] = aux

        # Vector into matrix
        return vector_into_matrix(map, self.rows, self.cols)
        
    # Method to get the number of cells of each type
    def get_cell_types_number(self):
        n_cells = self.rows * self.cols

        # Obtaining absolute frequencies (could be not interger)
        freqs = [freq_rel*n_cells for freq_rel in self.relative_freqs]

        # Getting the whole part of absolute freqs.
        cells = []
        for i in range(len(freqs)):
            whole_part = floor(freqs[i])
            cells.append(whole_part)
            freqs[i] -= whole_part
        
        # Adding the rest cell types with the decimal part probability distribution. 
        freqs = normalize_vector(freqs)

        rest = n_cells - sum(cells)
        for _ in range(rest):
            addition = 0.0
            prob = random.random()
            for j in range(len(freqs)):
                addition += freqs[j]            # revisar eficiencia de codigo
                if j+1 == len(freqs):           # Solving random > addition decimal part
                    addition = 1.0
                if prob <= addition:
                    cells[j] += 1
                    break

        # Check number of cells
        if sum(cells) != n_cells:
            # RAISE ERROR
            print("RAISE EXCEPTION: Problema dimension")
            exit(1)
        
        return cells
    
    # Method to put cell types (consecutively) in a vector
    def put_cell_types_into_vector(self, cell_types):
        map = []
        for i in range(len(cell_types)):
            for _ in range(cell_types[i]):
                map.append(CellType(i))

        return map

    def __key(self):
        return (self.rows, self.cols, self.agent_row, self.agent_col, self.agent_orientation, self.relative_freqs, self.seed)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Environment):
            return self.__key() == other.__key()
        return NotImplemented    

# ------------------------------------- ADDITIONAL FUNCTIONS -------------------------------------

# Normalize relatives frequencies to [0-1] interval
def normalize_vector(vector):
    total = sum(vector)
    if total == 0:
        return vector
    return [value / total for value in vector]

# Transform a Vector into a Matrix
def vector_into_matrix(vector, nRows, nCols):
    if nRows * nCols != len(vector):
        # RAISE ERROR
        print("ERROR: VECTOR TO MATRIX WITH DIFFERENT SIZES")
        exit(1)
    
    matrix = []
    count = 0
    for i in range(nRows):
        new_row = []
        for j in range(nCols):
            new_row.append(vector[count])
            count += 1
        matrix.append(new_row)
    
    return matrix


