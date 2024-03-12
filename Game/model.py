import random

class Brain:
    def __init__(self):
        pass
    
    def get_action(self):
        return random.randint(0, 3)