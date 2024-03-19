from Game.utils import *
from Game.agent import *
from Game.simulation_stats import *
from Game.state import *
import time

class Engine:
    def __init__(self, env, model, max_iters = 1000):
        self.game_map = env.get_game_map()

        initial_agent_vision = self.game_map.get_vision(env.agent_row, env.agent_col, env.agent_orientation)
        self.agent = Agent(env.agent_row, env.agent_col, env.agent_orientation, initial_agent_vision, model, env.rows, env.cols)

        self.max_iters = max_iters
        self.iters = 0
        
        self.stats = SimulationStats()

    def simulate(self, train = True):
        self.update(train)
        
        while self.iters < self.max_iters:
            state = State(self.agent, self.game_map)
            next_action = self.agent.next_action(state)
            
            print(next_action)

            valid = self.apply_action(next_action)

            self.iters += 1

            time.sleep(1)

            self.update(train)

            # if the agent fell into the void or ran out of energy, terminate the simulation
            if valid == Validation.EMPTY_CELL or valid == Validation.NO_ENERGY:
                break
        
        self.stats.print_summary()
        
        # we return just the final score of the simulation
        return self.stats.scores[-1]
            
    def apply_action(self, next_action):
        match self.is_valid(next_action):
            case Validation.EMPTY_CELL:
                # Terminate the simulation
                print("The agent fell into the void!")
                self.agent.alive = False
                return Validation.EMPTY_CELL
            case Validation.WALL_CELL:
                print("The agent crashed into a wall!")
                return Validation.WALL_CELL
            case Validation.NO_ENERGY:
                # Terminate the simulation
                print("The agent ran out of energy!")
                return Validation.NO_ENERGY 
            case Validation.VALID:
                # Update the agent's energy
                row_before, column_before = self.agent.get_position()
                cost = get_cost(next_action, self.game_map.get_cell_type(row_before, column_before), self.agent.get_bikini(), self.agent.get_shoes())
                self.agent.decrease_energy(cost)
                
                if self.agent.get_energy() < 0:
                    # RAISE ERROR
                    print("ERROR: NEGATIVE ENERGY!")
                
                match next_action:
                    case Action.FORWARD:
                        self.agent.move_forward()
                    case Action.TURN_LEFT:
                        self.agent.turn_left()
                    case Action.TURN_RIGHT:
                        self.agent.turn_right()
                
                return Validation.VALID

    def update(self, train):
        if self.agent.is_alive():
            # Update the agent's vision
            self.agent.set_vision(self.game_map.get_vision(self.agent.row, self.agent.column, self.agent.orientation))
            
            # Update the agent's map
            self.game_map.update_agent_map(self.agent.row, self.agent.column, self.agent.orientation)
        
        # Create a new state
        new_state = State(self.agent, self.game_map)
        
        # Update the stats
        self.stats.update(self.agent, new_state)
        
        # Train the agent's brain model
        if train:
            self.agent.train_brain(new_state)

    def is_valid(self, action):
        # Check if the agent has enough energy to move
        row, column = self.agent.get_position()
        current_cell_type = self.game_map.get_cell_type(row, column)
        cost = get_cost(action, current_cell_type, self.agent.get_bikini(), self.agent.get_shoes())

        next_cell_type = self.agent.get_forward_cell_type()

        if cost > self.agent.get_energy():
            return Validation.NO_ENERGY

        if action == Action.FORWARD:
            if next_cell_type == CellType.EMPTY:
                return Validation.EMPTY_CELL
            elif next_cell_type == CellType.WALL:
                return Validation.WALL_CELL
            else:
                return Validation.VALID

        return Validation.VALID
