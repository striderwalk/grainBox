import json

import numpy as np

# dict to map the names to their corresponding types
# a dict of the types to their corresponding data

GRAINS = dict()

GRAIN_DATA = dict()

with open("./assets/types.json") as file:
    data = json.load(file)

    type_id = 0
    for key, value in data.items():

        GRAIN_DATA[type_id] = value
        GRAIN_DATA[type_id]["movement"] = np.array(GRAIN_DATA[type_id]["movement"])

        GRAINS[key] = type_id
        type_id += 1
GRAIN_TO_NAME = {value: key for key, value in GRAINS.items()}
