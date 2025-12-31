#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA

n = NOAA()

observations = n.get_observations('11365','US')

tags = ['timestamp', 'temperature', 'dewpoint', 'relativeHumidity', 'barometricPressure']
for observation in observations:
    #print(json.dumps(observation, indent=4))
    for keys, values in observation.items():
        if keys in tags:
            # print(f"{keys}")
            if isinstance(values, dict):
                print(f"{keys}: {values['value']}")
            if isinstance(values, str) and keys == 'timestamp':
                print(f"{keys}: {values}")
                
    break
