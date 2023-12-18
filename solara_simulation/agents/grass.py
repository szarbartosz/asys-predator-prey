from mesa import Agent


class Grass(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = 0
        self.health = 1
