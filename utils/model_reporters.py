def count_predators(model):
    count = 0
    for agent in model.schedule.agents:
        if agent.species == 2:
            count += 1
    return count


def count_preys(model):
    count = 0
    for agent in model.schedule.agents:
        if agent.species == 1:
            count += 1
    return count
