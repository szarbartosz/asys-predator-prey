from mesa_simulation.random_walk import RandomWalker
from mesa_simulation.agents.rabbit import Rabbit


class Fox(RandomWalker):
    '''
    A fox that walks around, reproduces (asexually) and eats rabbit.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are rabbit present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        rabbit = [obj for obj in this_cell if isinstance(obj, Rabbit)]
        if len(rabbit) > 0:
            rabbit_to_eat = self.random.choice(rabbit)
            self.energy += self.model.fox_gain_from_food

            # Kill the rabbit
            self.model.grid.remove_agent(rabbit_to_eat)
            self.model.schedule.remove(rabbit_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.fox_reproduce:
                # Create a new fox cub
                self.energy /= 2
                cub = Fox(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
