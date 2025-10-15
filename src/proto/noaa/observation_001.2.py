#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA




def doit():

    n = NOAA()

    observations = n.get_observations('11365','US')
    stuff = {}
    tags = ['timestamp', 'temperature', 'dewpoint', 'relativeHumidity', 'barometricPressure']
    for observation in observations:
        #print(json.dumps(observation, indent=4))
        for keys, values in observation.items():
            if keys in tags:
                # print(f"{keys}")
                if isinstance(values, dict):
                    # print(f"{keys}: {values['value']}")
                    stuff[keys] = values['value']
                elif isinstance(values, str) and keys == 'timestamp':
                    # print(f"{keys}: {values}")
                    stuff[keys] = values
        break

    return stuff

stuff = doit()

print(f"{json.dumps(stuff, indent=4)}")

