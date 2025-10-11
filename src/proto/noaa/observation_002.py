#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA

zip = '39503'
country = 'US'

n = NOAA()
observation = {}
observations = n.get_observations(zip, country)
for item in observations:
    observation = item
    print(json.dumps(observation, indent=4))
    break

relativeHumidity = {}
barometricPressure = {}
dewpoint = {}
temperature = {}

items = [relativeHumidity, barometricPressure, dewpoint, temperature]

for key, value in observation.items():
    if key == "relativeHumidity":
        relativeHumidity = value
    elif key == "barometricPressure":
        barometricPressure = value
    elif key == "dewpoint":
        dewpoint = value
    elif key == "temperature":
        temperature = value
    else:
        continue

print(f"temperature: {temperature['value']}")
print(f"barometric pressure: {barometricPressure['value']}")
print(f"relative humidity: {relativeHumidity['value']}")
print(f"dewpoint: {dewpoint['value']}")


zip = '83221'

n = NOAA()
observation = {}
observations = n.get_observations(zip, country)
for item in observations:
    observation = item
    print(json.dumps(observation, indent=4))
    break

relativeHumidity = {}
barometricPressure = {}
dewpoint = {}
temperature = {}

for key, value in observation.items():
    if key == "relativeHumidity":
        relativeHumidity = value
    elif key == "barometricPressure":
        barometricPressure = value
        if barometricPressure:
            barometricPressure['value'] = str(float(barometricPressure['value'])/100)
        else:
            barometricPressure = None
        print(json.dumps(value, indent=4))
    elif key == "dewpoint":
        dewpoint = value
    elif key == "temperature":
        temperature = value
    else:
        continue


print(f"temperature: {temperature['value']}")
print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
print(f"relative humidity: {relativeHumidity['value']}")
print(f"dewpoint: {dewpoint['value']}")

    
'''
relativeHumidity
barometricPressure
dewpoint
temperature
'''