from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Checkbox, Slider

from mesa_simulation.agents.fox import Fox
from mesa_simulation.agents.rabbit import Rabbit
from mesa_simulation.agents.grass_patch import GrassPatch
from mesa_simulation.model import FoxRabbit


def fox_rabbit_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Rabbit:
        portrayal["Shape"] = "mesa_simulation/resources/rabbit.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = "mesa_simulation/resources/fox.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(fox_rabbit_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Foxes", "Color": "#AA0000"},
                             {"Label": "Rabbits", "Color": "#666666"}])

model_params = {"grass": Checkbox('Grass Enabled', True),
                "grass_regrowth_time": Slider('Grass Regrowth Time', 20, 1, 50),
                "initial_rabbits": Slider('Initial Rabbit Population', 100, 10, 300),
                "rabbit_reproduce": Slider('Rabbit Reproduction Rate', 0.04, 0.01, 1.0,
                                          0.01),
                "initial_foxes": Slider('Initial Fox Population', 50, 10, 300),
                "fox_reproduce": Slider('Fox Reproduction Rate', 0.05, 0.01, 1.0,
                                         0.01,
                                         description="The rate at which fox agents reproduce."),
                "fox_gain_from_food": Slider('Fox Gain From Food Rate', 20, 1, 50),
                "rabbit_gain_from_food": Slider('Rabbit Gain From Food', 4, 1, 10)}

server = ModularServer(FoxRabbit, [canvas_element, chart_element], "Fox Rabbit Predation", model_params)
server.port = 8522
