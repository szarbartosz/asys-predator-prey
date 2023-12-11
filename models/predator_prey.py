import mesa
import uuid
import random
from agents.grass import Grass
from agents.rabbit import Rabbit
from agents.fox import Fox
from utils.model_reporters import count_preys, count_predators


class PredatorPreyModel(mesa.Model):
    def __init__(self, predators_no, preys_no, width, height):
        self.predators_no = predators_no
        self.preys_no = preys_no
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.agents = 0
        self.agents_to_remove = []
        self.agents_to_add = []

        for i in range(self.predators_no):
            agent = Rabbit(uuid.uuid4().int, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        for i in range(self.preys_no):
            agent = Fox(uuid.uuid4().int, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.datacollector = mesa.DataCollector(
            model_reporters={"Predators": count_predators, "Preys": count_preys}, agent_reporters={}
        )

    def step(self):
        for i in range(self.grid.width * self.grid.height):
            if random.randint(0, 100) < 2:
                agent = Grass(uuid.uuid4().int, self)
                self.schedule.add(agent)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

        self.datacollector.collect(self)
        self.schedule.step()

        for agent in self.agents_to_add:
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.agents_to_add.remove(agent)

        for agent in list(set(self.agents_to_remove)):
            try:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)
                self.agents_to_remove.remove(agent)
            except Exception as e:
                print(f"Tried to delete the agent with id {e} again")
