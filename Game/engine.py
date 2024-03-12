from utils import *
from game_environment import *
from agent import *
import time

class Engine:
    def __init__(self, game_env, agent, max_iters = 1000):
        self.game_env = game_env
        self.agent = agent
        self.max_iters = max_iters
        self.iters = 0

    def simulate(self):
        self.update()
        
        while self.iters < self.max_iters:
            next_action = self.agent.next_action()
            
            print(next_action)

            self.apply_action(next_action)
            
            print("Position: ", self.agent.get_position())
            print("Orientation: ", self.agent.get_orientation())
            print("Energy: ", self.agent.get_energy())
            print("Vision: ", self.agent.vision)

            self.iters += 1
            
            time.sleep(1)

            self.update()
            
    def apply_action(self, next_action):
        match self.is_valid(next_action):
            case Validation.EMPTY_CELL:
                # Terminate the simulation
                print("The agent fell into the void!")
                pass
            case Validation.WALL_CELL:
                print("The agent crashed into a wall!")
                return
            case Validation.NO_ENERGY:
                # Terminate the simulation
                print("The agent ran out of energy!")
                pass
            case Validation.VALID:
                # Update the agent's energy
                row_before, column_before = self.agent.get_position()
                cost = get_cost(next_action, self.game_env.game_map.get_cell_type(row_before, column_before), self.agent.get_bikini(), self.agent.get_shoes())
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

    def update(self):
        # Update the agent's vision
        self.agent.set_vision(self.game_env.game_map.get_vision(self.agent.row, self.agent.column, self.agent.orientation))
        
        # Update the agent's map
        self.game_env.game_map.update_agent_map(self.agent.row, self.agent.column, self.agent.orientation)

        # Update the stats
        return

    def is_valid(self, action):
        # Check if the agent has enough energy to move
        row, column = self.agent.get_position()
        current_cell_type = self.game_env.game_map.get_cell_type(row, column)
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
    
    
env = GameEnv()
engine = Engine(env, Agent(5, 5, Direction.UP, env.game_map.get_vision(5, 5, Direction.UP)))
engine.simulate()