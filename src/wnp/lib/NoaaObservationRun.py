#!/usr/bin/env -S python -u

import faulthandler
#import traceback
import sys 
import json
from collections import OrderedDict

#####
# 3rd party library for caching 
#   https://github.com/tkem/cachetools/
#   https://pypi.org/project/cachetools/
from cachetools import TTLCache, cachedmethod

#####
# NOAA library to access weather data
# pip install noaa_sdk
from noaa_sdk import NOAA

sys.path.append("..")

if __name__ != "__main__":
    from config import DEFAULT_DEGREES_UNITS


class NoaaObservationRun():
    def __init__(self):
        self.n = NOAA()
        self.setFileName()
        self.cache=TTLCache(maxsize=100, ttl=900)

    @cachedmethod(lambda self: self.cache)
    def singleshot(self, pzip, country='US'):
        observation = {}
        observations = self.n.get_observations(pzip, country)
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
                        print(f"{keys}: {values}")
                        timestamp = values.split("T")[-1]
                        hour = timestamp.split(":")[0]
                        minute = timestamp.split(":")[1]
                        if int(hour) == 0:
                            hour = 24
                        timestamp = f"{int(hour)-5}{minute}"
                        stuff[keys] = timestamp
            break

        return stuff

    @cachedmethod(lambda self: self.cache)
    def singleshotRaw(self, pzip, country='US'):
        observation = {}
        observations = self.n.get_observations(pzip, country)
        stuff = {}
        for observation in observations:
            #print(json.dumps(observation, indent=4))
            stuff = observation
            break

        # print(f"{json.dumps(stuff, indent=4)}")

        return stuff

    def setFileName(self, filename='data.json'):
        """
        setter for file name managed by this class
        """
        self.filename = filename

    def getAndSaveSingleShot(self, pzip, country='US'):
        """
        acquire a singleshot data, and save it to a file.
        """
        data = self.singleshot(pzip, country)

        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def getAndSaveSingleShotRaw(self, pzip, country='US'):
        """
        acquire a singleshot data, and save it to a file.
        """
        data = self.singleshotRaw(pzip, country)

        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def getAndSaveFordaysRaw(self, pzip, country='US', samples=10, timestamp=False, live=True):
        """
        acquire fordaysRaw data and save it to a file.
        """
        data = self.fordaysRaw(pzip, country='US')

        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=4)

    @cachedmethod(lambda self: self.cache)
    def fordaysRaw(self, pzip, country='US', samples=10, timestamp=False, live=True):
        i = 1 
        observation = {}
        if live:
            observations = self.n.get_observations(pzip, country)
        else:
            with open(self.file2load, 'r') as file:
                observations = json.load(file)
            print(f"{json.dumps(observations, indent=3)}")

        for item in observations:
            tmp = {i : item}
            observation.update(tmp)
            # print(json.dumps(observation, indent=4))
            #break
            i += 1
        # print(json.dumps(observation, indent=4))
        return observation

    @cachedmethod(lambda self: self.cache)
    def fordays(self, pzip, country='US', samples=10, timestamp=False, live=True):
        observation = {}
        print(f"Processing zipcode: {pzip}, country: {country}")
        if live:
            observations = self.n.get_observations(pzip, country)
        else:
            with open(self.file2load, 'r') as file:
                observations = json.load(file)
            print(f"{json.dumps(observations, indent=3)}")
        stuff = {}
        tags = ['timestamp', 'temperature', 'dewpoint', 'relativeHumidity', 'barometricPressure']
        i = 0
        container = OrderedDict()
        for observation in observations:
            #print(json.dumps(observation, indent=4))
            i += 1

            tmptimestamp = observation['timestamp'].split("T")[-1]
            hour = tmptimestamp.split(":")[0]
            minute = tmptimestamp.split(":")[1]
            if int(hour) == 0:
                hour = 24
            tmpdate = observation['timestamp'].split("T")[0]
            #tmpdate = int(''.join(tmpdate.split('-')))
            tmptimestamp = f"{tmpdate}-{(int(hour)-5)%24}{minute}"

            if timestamp:
                container[tmptimestamp] = {}
                container[tmptimestamp]['timestamp'] = tmptimestamp
                try:
                    if DEFAULT_DEGREES_UNITS == 'C' and observation['temperature']['unitCode'][-1] == 'F':
                        container[tmptimestamp]['temperature'] = (float(observation['temperature']['value'])-32)*5/9
                    elif DEFAULT_DEGREES_UNITS == 'F' and observation['temperature']['unitCode'][-1] == 'C':
                        container[tmptimestamp]['temperature'] = float(observation['temperature']['value'])*9/5 + 32
                    else:
                        container[tmptimestamp]['temperature'] = float(observation['temperature']['value'])
                except TypeError as err:
                    container[tmptimestamp]['temperature'] = 0

                try:
                    if DEFAULT_DEGREES_UNITS == 'C' and observation['dewpoint']['unitCode'][-1] == 'F':
                        container[tmptimestamp]['dewpoint'] = (float(observation['dewpoint']['value'])-32)*5/9
                    elif DEFAULT_DEGREES_UNITS == 'F' and observation['dewpoint']['unitCode'][-1] =='C':
                        container[tmptimestamp]['dewpoint'] = float(observation['dewpoint']['value'])*9/5 + 32
                    else:
                        container[tmptimestamp]['dewpoint'] = float(observation['dewpoint']['value'])
                except TypeError as err:
                    container[tmptimestamp]['dewpoint'] = 0

                try:
                    container[tmptimestamp]['relativeHumidity'] = float(observation['relativeHumidity']['value'])
                except TypeError as err:
                    container[tmptimestamp]['relativeHumidity'] = 0

                try:
                    container[tmptimestamp]['barometricPressure'] = float(observation['barometricPressure']['value'])
                except TypeError as err:
                    container[tmptimestamp]['barometricPressure'] = 0

            else:
                container[i] = {}
                container[i]['timestamp'] = tmptimestamp

                try:
                    if DEFAULT_DEGREES_UNITS == 'C' and observation['temperature']['unitCode'][-1] == 'F':
                        container[i]['temperature'] = (float(observation['temperature']['value'])-32)*5/9
                    elif DEFAULT_DEGREES_UNITS == 'F' and observation['temperature']['unitCode'][-1] == 'C':
                        container[i]['temperature'] = float(observation['temperature']['value'])*9/5 + 32
                    else:
                        container[i]['temperature'] = float(observation['temperature']['value'])
                except TypeError as err:
                    if i <= 1:
                        container[i]['temperature'] = 0
                    else:
                        container[i]['temperature'] = container[i-1]['temperature']

                try:
                    if DEFAULT_DEGREES_UNITS == 'C' and observation['dewpoint']['unitCode'][-1] == 'F':
                        container[i]['dewpoint'] = (float(observation['dewpoint']['value'])-32)*5/9
                    elif DEFAULT_DEGREES_UNITS == 'F' and observation['dewpoint']['unitCode'][-1] =='C':
                        container[i]['dewpoint'] = float(observation['dewpoint']['value'])*9/5 + 32
                    else:
                        container[i]['dewpoint'] = float(observation['dewpoint']['value'])
                except TypeError as err:
                    if i <= 1:
                        container[i]['dewpoint'] = 0
                    else:
                        container[i]['dewpoint'] = container[i-1]['dewpoint']

                try:
                    container[i]['relativeHumidity'] = float(observation['relativeHumidity']['value'])
                except TypeError as err:
                    if i <= 1:
                        container[i]['relativeHumidity'] = 0
                    else:
                        container[i]['relativeHumidity'] = container[i-1]['relativeHumidity']

                try:
                    container[i]['barometricPressure'] = float(observation['barometricPressure']['value'])
                except TypeError as err:
                    if i <= 1:
                        container[i]['barometricPressure'] = 0
                    else:
                        container[i]['barometricPressure'] = container[i-1]['barometricPressure']

            if int(i) == int(samples):
                break
        #print(f"{json.dumps(container, indent=4)}")

        return container


if __name__ == "__main__":

    import argparse

    sys.path.append("../..")

    # from wnp.lib.config import DEFAULT_DEGREES_UNITS
    from wnp.config import DEFAULT_DEGREES_UNITS
    
    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="83402", help="zipcode to gather data on")
    parser.add_argument("-l", "--loadFile", default='', help="raw json data file to load, rather than acquire live data")
    parser.add_argument("-f", "--saveJsonData", default='', help="save raw json data to file")
    parser.add_argument("-o", "--saveOneshotJsonData", default='', help="save oneshot json data to file")
    parser.add_argument("-O", "--saveOneshotRawJsonData", default='', help="save raw oneshot json data to file")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    parser.add_argument("-s", "--samples", default='2000', help="number of samples to chart")
    parser.add_argument("-T", "--timestamp", action='store_true', help="timestamp")
    parser.add_argument("-R", "--raw", action='store_true', help="dump raw observation data to console")
    parser.add_argument("-t", "--tag", default='temperature', help="tag to plot - one of ['temperature', 'barometricPressure', 'relativeHumidity', 'dewpoint']")
    args = parser.parse_args()

    njob = NoaaObservationRun()

    if args.saveJsonData:
        njob.setFileName(args.saveJsonData)
        containers = njob.getAndSaveFordaysRaw(args.zipcode, args.country, args.samples, args.timestamp)

    if args.saveOneshotRawJsonData:
        njob.setFileName(args.saveOneshotRawJsonData)
        containers = njob.getAndSaveSingleShotRaw(args.zipcode, args.country)

        print(f"{json.dumps(containers, indent=4)}")

    if args.saveOneshotJsonData:
        njob.setFileName(args.saveOneshotJsonData)
        containers = njob.getAndSaveSingleShot(args.zipcode, args.country)

        print(f"{json.dumps(containers, indent=4)}")

    if args.raw:
        containers = njob.fordaysRaw(args.zipcode, args.country, args.samples, args.timestamp)
        # print(f"{json.dumps(containers, indent=3)}")
    else:
        containers = njob.fordays(args.zipcode, args.country, args.samples, args.timestamp)
        print("###############################")
        print("### ForDays Observation run ###")
        print(f"{json.dumps(containers, indent=4)}")
        stuff = njob.singleshot(args.zipcode, args.country)
        print("##################################")
        print("### SingleShot Observation run ###")
        print(f"{json.dumps(stuff, indent=4)}")
        print("##################################")

