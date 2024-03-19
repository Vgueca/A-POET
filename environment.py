import random
import numpy as np
from math import *
import Game.gamemap
from Game.utils import CellType

class Environment:
    env_ids = 1  # Class variable to count child names
                 # The first one, hand-picked,  must be 0
    
    max_rows = 50
    max_cols = 50

    # Inicializar un reproductor que mínimo tenga un tipo de casilla
    def __init__(self, id = None, rows = 10, cols = 10,
                 agent_row = 5, agent_col = 5, agent_orientation = 0,
                 relative_freqs = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],       # 0. Empty | 1. Wall | 2. Stone | 3. Sand | 4. Water | 5. Grass | 6. Mud | 7. Bikini | 8. Shoes | 9. Charge
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

        self.relative_freqs = relative_freqs
        
        if id == 0:
            random.seed(seed)

        self.seed = seed

        self.game_map = self.generate_game_map()    # Maybe we should delete the game map when the environment is not active

    def mutate(self):
        child_id = Environment.count_ids    # If we use parallelism, we must use a lock to avoid problems
        Environment.count_ids += 1

        rows = self.rows
        cols = self.cols

        agent_row = self.agent_row
        agent_col = self.agent_col
        agent_orientation = self.agent_orientation
        
        freqs = self.relative_freqs

        seed = self.seed

        # MUTATE ROWS
        rows = rows + random.randint(-10, 10)
        if rows > Environment.max_rows:
            rows = Environment.max_rows
        if rows < 1:
            rows = 1

        # MUTATE COLS
        cols = cols + random.randint(-10, 10)
        if cols > Environment.max_cols:
            cols = Environment.max_cols
        if cols < 1:
            cols = 1

        # MUTATE AGENT
        agent_row = random.randint(0, rows)
        agent_col = random.randint(0, cols)
        agent_orientation = random.randint(0, 3)

        # MUTATE FREQS
        n_cells = rows * cols
        freq_step = 1/n_cells
        max_change = round(0.1 * n_cells)

        for i in range(len(freqs)):
            freqs[i] += random.randint(-max_change, max_change) * freq_step
    
        freqs = normalize_vector(freqs)

        # Creating child
        child = Environment(
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
    
    def get_game_map(self):
        return self.game_map
    
    def generate_game_map(self):
        cell_types = self.get_cell_types_number()
        
        map = self.put_cell_types_into_vector(cell_types=cell_types)

        agent_index = self.agent_row * self.cols + self.agent_col
        random.shuffle(map)
        while (map[agent_index] == CellType.EMPTY or map[agent_index] == CellType.WALL):
            random.shuffle(map)

        # Vector into matrix
        return vector_into_matrix(map, self.rows, self.cols)
        
    # Method to get the number of cells of each type
    def get_cell_types_number(self):
        n_cells = self.rows * self.cols

        # Obtaining absolute frequencies (could be not interger)
        freqs = self.relative_freqs * n_cells

        # Getting the whole part of absolute freqs.
        cells = []
        for i in range(len(freqs)):
            whole_part = floor(freqs[i])
            cells.append(whole_part)
            freqs[i] -= whole_part
        
        # Adding the rest cell types with the decimal part probability distribution. 
        freqs = normalize_vector(freqs)

        rest = n_cells - sum(cells)
        for i in range (rest):
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
            for j in range(cell_types[i]):
                map.append(Game.CellType(i))

        return map

    # Equal operator
    def __eq__(self, __value: object) -> bool:
        return self.rows == __value.rows \
            and self.cols == __value.cols \
            and self.agent_row == __value.agent_row \
            and self.agent_col == __value.agent_col \
            and self.agent_orientation == __value.agent_orientation \
            and self.relative_freqs == __value.relative_freqs \
            and self.seed == __value.seed  
    

# ------------------------------------- ADDITIONAL FUNCTIONS -------------------------------------

# Normalize relatives frequencies to [0-1] interval
def normalize_vector(vector):
    total = sum(vector)
    if total == 0: 
        # RAISE ERROR
        print("ERROR: NONE CELL TYPE FOR THE MAP!")
        exit(1)
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


