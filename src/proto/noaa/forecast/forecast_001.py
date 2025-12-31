#!/usr/bin/env -S python -u

import json

from noaa_sdk import NOAA

n = NOAA()
res = n.get_forecasts('11365', 'US')
for i in res:
    print(json.dumps(i, indent=4))


