from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Checkbox, Slider

from mesa_simulation.agents.wolf import Wolf
from mesa_simulation.agents.sheep import Sheep
from mesa_simulation.agents.grass_patch import GrassPatch
from mesa_simulation.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal["Shape"] = "mesa_simulation/resources/rabbit.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Wolf:
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


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
                             {"Label": "Sheep", "Color": "#666666"}])

model_params = {"grass": Checkbox('Grass Enabled', True),
                "grass_regrowth_time": Slider('Grass Regrowth Time', 20, 1, 50),
                "initial_sheep": Slider('Initial Sheep Population', 100, 10, 300),
                "sheep_reproduce": Slider('Sheep Reproduction Rate', 0.04, 0.01, 1.0,
                                          0.01),
                "initial_wolves": Slider('Initial Wolf Population', 50, 10, 300),
                "wolf_reproduce": Slider('Wolf Reproduction Rate', 0.05, 0.01, 1.0,
                                         0.01,
                                         description="The rate at which wolf agents reproduce."),
                "wolf_gain_from_food": Slider('Wolf Gain From Food Rate', 20, 1, 50),
                "sheep_gain_from_food": Slider('Sheep Gain From Food', 4, 1, 10)}

server = ModularServer(WolfSheep, [canvas_element, chart_element], "Wolf Sheep Predation", model_params)
server.port = 8522