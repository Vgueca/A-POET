from utils import *

class Engine:
    def __init__(self, game_env, agent, max_iters=1000):
        self.game_map = game_env.game_map
        self.agent = agent
        self.max_iters = max_iters
        self.iters = 0
    
    def simulate(self):
        while self.iters < self.max_iters:
            next_action = self.agent.next_action()

            self.apply_action(next_action)

            self.iters += 1

            if self.agent.posX == self.game_map.goalX and self.agent.posY == self.game_map.goalY:
                return True
            
        return False
    
    def apply_action(self, next_action):
        if self.agent.is_valid(next_action):
            match next_action:
                case Action.IDLE:
                    pass
                case Action.FORWARD:
                    self.agent.move_forward()
                case Action.TURN_LEFT:
                    self.agent.turn_left()
                case Action.TURN_RIGHT:
                    self.agent.turn_right()
                case _:
                    pass