'''
Fox-Rabbit Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Fox Rabbit Predation model.
    http://ccl.northwestern.edu/netlogo/models/FoxRabbitPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from mesa_simulation.agents.rabbit import Rabbit
from mesa_simulation.agents.fox import Fox
from mesa_simulation.agents.grass_patch import GrassPatch
from mesa_simulation.schedule import RandomActivationByBreed


class FoxRabbit(Model):
    '''
    Fox-Rabbit Predation Model
    '''

    height = 20
    width = 20

    initial_rabbits = 100
    initial_foxes = 50

    rabbit_reproduce = 0.04
    fox_reproduce = 0.05

    fox_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    rabbit_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating fox and rabbit (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_rabbits=100, initial_foxes=50,
                 rabbit_reproduce=0.04, fox_reproduce=0.05,
                 fox_gain_from_food=20,
                 grass=False, grass_regrowth_time=30, rabbit_gain_from_food=4):
        '''
        Create a new Fox-Rabbit model with the given parameters.

        Args:
            initial_rabbits: Number of rabbits to start with
            initial_foxes: Number of foxes to start with
            rabbit_reproduce: Probability of each rabbit reproducing each step
            fox_reproduce: Probability of each fox reproducing each step
            fox_gain_from_food: Energy a fox gains from eating a rabbit
            grass: Whether to have the rabbit eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            rabbit_gain_from_food: Energy rabbit gain from grass, if enabled.
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_rabbit = initial_rabbits
        self.initial_foxes = initial_foxes
        self.rabbit_reproduce = rabbit_reproduce
        self.fox_reproduce = fox_reproduce
        self.fox_gain_from_food = fox_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.rabbit_gain_from_food = rabbit_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Foxes": lambda m: m.schedule.get_breed_count(Fox),
             "Rabbits": lambda m: m.schedule.get_breed_count(Rabbit)})

        # Create rabbits:
        for i in range(self.initial_rabbit):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.rabbit_gain_from_food)
            rabbit = Rabbit(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(rabbit, (x, y))
            self.schedule.add(rabbit)

        # Create foxes
        for i in range(self.initial_foxes):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.fox_gain_from_food)
            fox = Fox(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(fox, (x, y))
            self.schedule.add(fox)

        # Create grass patches
        if self.grass:
            for agent, (x, y) in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self,
                                   fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Fox),
                   self.schedule.get_breed_count(Rabbit)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number foxes: ',
                  self.schedule.get_breed_count(Fox))
            print('Initial number rabbits: ',
                  self.schedule.get_breed_count(Rabbit))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number foxes: ',
                  self.schedule.get_breed_count(Fox))
            print('Final number rabbits: ',
                  self.schedule.get_breed_count(Rabbit))
