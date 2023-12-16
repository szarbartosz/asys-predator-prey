from fox_rabbit.models.predator_prey import PredatorPreyModel
from mesa.experimental import JupyterViz


def agent_portrayal(agent):
    size = 30
    color = "tab:red"
    if agent.species == 0:
        color = "tab:green"
    elif agent.species == 1:
        color = "tab:blue"
    elif agent.species == 2:
        color = "tab:red"

    return {
        "color": color,
        "size": size
    }


model_params = {
    "predators_no": {
        "type": "SliderInt",
        "value": 200,
        "label": "Number of predators:",
        "min": 10,
        "max": 400,
        "step": 10,
    },
    "preys_no": {
        "type": "SliderInt",
        "value": 400,
        "label": "Number of preys:",
        "min": 10,
        "max": 1000,
        "step": 10,
    },
    "width": 40,
    "height": 40,
}

page = JupyterViz(
    PredatorPreyModel,
    model_params,
    measures=["Predators", "Preys"],
    name="Predator Prey Model",
    agent_portrayal=agent_portrayal,
)
