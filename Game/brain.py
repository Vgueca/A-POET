import random

class Brain:
    def __init__(self, model):
        self.model = model
    
    def get_action(self):
        return random.randint(0, 3)