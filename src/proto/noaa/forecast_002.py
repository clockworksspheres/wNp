#!/usr/bin/env -S python -u

import json

from noaa_sdk import NOAA

n = NOAA()
res = n.get_forecasts('39503', 'US')
for i in res:
    # print(json.dumps(i, indent=4))
    print("{")
    print(f"temperature: {i['temperature']}")
    print(f"dewpoint:{i['dewpoint']['value']}")
    print(f"relativeHumidity :{i['relativeHumidity']['value']}")
    # print(f":{}")
    # print(f":{}")
    print("}")
