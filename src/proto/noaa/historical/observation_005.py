#!/usr/bin/env -S python -u

import json
from noaa_sdk import NOAA
import faulthandler
import traceback

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
            # :print(json.dumps(observation, indent=4))
            break
        return observation

    def basic_vals(self, pzip, country, printErr=False):
        
        observation = self.singleshot(pzip, country)    

        relativeHumidity = {}
        barometricPressure = {}
        dewpoint = {}
        temperature = {}

        items = [relativeHumidity, barometricPressure, dewpoint, temperature]

        for key, value in observation.items():
            if key == "relativeHumidity":
                try:
                    relativeHumidity = value
                except TypeError as err:
                    if printErr:
                        print(traceback.format_exc())
                        print(str(err))
            elif key == "barometricPressure":
                try:
                    barometricPressure = value
                    if barometricPressure:
                        barometricPressure['value'] = str(float(barometricPressure['value'])/100)
                    else:
                        barometricPressure = None
                        # print(json.dumps(value, indent=4))
                except TypeError as err:
                    if printErr:
                        print(traceback.format_exc())
                        print(str(err))
            elif key == "dewpoint":
                try:
                    dewpoint = value
                except TypeError as err:
                    if printErr:
                        print(traceback.format_exc())
                        print(str(err))
            elif key == "temperature":
                try:
                    temperature = value
                    if temperature:
                        temperature['value'] = str(round(int(temperature['value'])*9/5+32))
                    else:
                        temperature = None
                except TypeError as err:
                    if printErr:
                        print(traceback.format_exc())
                        print(str(err))
            else:
                continue


        print(f"temperature: {temperature['value']}")
        try:
            print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
        except TypeErr as err:
            if printErr:
                print(traceback.format_exc())
                print(str(err))
        
        print(f"relative humidity: {relativeHumidity['value']}")
        print(f"dewpoint: {dewpoint['value']}")


if __name__ == "__main__":

    import argparse
    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()


    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="00000", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    args = parser.parse_args()

    njob = noaa_job()

    # njob.basic_vals('39503', 'US')
    njob.basic_vals(args.zipcode, args.country)

