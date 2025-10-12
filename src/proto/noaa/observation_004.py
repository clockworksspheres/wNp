#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA

pzip = '83221'
country = 'US'

class noaa_job():
    def __init__(self):
        self.n = NOAA()

    def singleshot(self, pzip, country='US'):
        observation = {}
        observations = self.n.get_observations(pzip, country)
        for item in observations:
            observation = item
            print(json.dumps(observation, indent=4))
            break
        return observation

    def basic_vals(self, pzip, country):
        
        observation = self.singleshot(pzip, country)    

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
                if barometricPressure:
                    barometricPressure['value'] = str(float(barometricPressure['value'])/100)
                else:
                    barometricPressure = None
                print(json.dumps(value, indent=4))
            elif key == "dewpoint":
                dewpoint = value
            elif key == "temperature":
                temperature = value
                if temperature:
                    temperature['value'] = str(round(int(temperature['value'])*9/5+32))
                else:
                    temperature = None
            else:
                continue


        print(f"temperature: {temperature['value']}")
        print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
        print(f"relative humidity: {relativeHumidity['value']}")
        print(f"dewpoint: {dewpoint['value']}")


njob = noaa_job()

njob.basic_vals('39503', 'US')



    
'''
relativeHumidity
barometricPressure
dewpoint
temperature
'''
