#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA

n = NOAA()
observations = n.get_observations('11365','US')
for observation in observations:
    print(json.dumps(observation, indent=4))
    break
