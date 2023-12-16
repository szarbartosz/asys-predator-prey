from mesa import Agent
import uuid


class Rabbit(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = 1
        self.health = 4

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def eat_grass(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates.pop(
            cellmates.index(self)
        )
        if len(cellmates) >= 1:
            for cellmate in cellmates:
                if cellmate.species == 0:
                    self.health += 2
                    self.model.agents_to_remove.append(cellmate)
                    break

    def reproduce(self):
        if self.health > 4:
            agent = Rabbit(uuid.uuid4(), self.model)
            self.model.agents_to_add.append(agent)

    def step(self):
        self.move()
        self.eat_grass()
        self.reproduce()
        self.health -= 1
        if self.health == 0:
            self.model.agents_to_remove.append(self)
