import json

import numpy as np

# dict to map the names to their corresponding types
# a dict of the types to their corresponding data

GRAINS = dict()

GRAIN_DATA = dict()

with open("./assets/types.json") as file:
    data = json.load(file)

    type_name = 0
    for key, value in data.items():
        GRAIN_DATA[type_name] = (value[0], np.array(value[1]), value[2])
        GRAINS[key] = type_name
        type_name += 1
