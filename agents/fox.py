from mesa import Agent
import uuid


class Fox(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = 2
        self.health = 4

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def attack(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates.pop(
            cellmates.index(self)
        )
        if len(cellmates) >= 1:
            for cellmate in cellmates:
                if cellmate.species == 1 and self.health > cellmate.health:
                    self.health += 2
                    self.model.agents_to_remove.append(cellmate)

    def reproduce(self):
        if self.health > 5:
            agent = Fox(uuid.uuid4(), self.model)
            self.model.agents_to_add.append(agent)

    def step(self):
        self.move()
        self.attack()
        self.reproduce()
        self.health -= 1
        if self.health == 0:
            self.model.agents_to_remove.append(self)
