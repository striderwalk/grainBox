import json

import numpy as np


with open("./assets/types.json") as file:
    GRAIN_DATA = json.load(file)

    for key, value in GRAIN_DATA.items():
        GRAIN_DATA[key] = (value[0], np.array(value[1]), value[2])

GRAINS = GRAIN_DATA.keys()
