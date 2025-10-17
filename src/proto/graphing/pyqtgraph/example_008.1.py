#!/usr/bin/env -S python -u

import faulthandler
import traceback
import sys
import json
from collections import OrderedDict

#####
# Graphics libraries
# pip install pyqtgraph
# pip install PySide6
from PySide6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

#####
# NOAA library to access weather data
# pip install noaa_sdk
from noaa_sdk import NOAA


class noaa_job():
    def __init__(self):
        self.n = NOAA()

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

    def fordays(self, pzip, country='US', timestamp=False):
        observation = {}
        observations = self.n.get_observations(pzip, country)
        stuff = {}
        tags = ['timestamp', 'temperature', 'dewpoint', 'relativeHumidity', 'barometricPressure']
        i = 0
        container = {}
        for observation in observations:
            #print(json.dumps(observation, indent=4))
            i += 1
            for keys, values in observation.items():
                if keys in tags:
                    # print(f"{keys}")
                    if isinstance(values, dict):
                        # print(f"{keys}: {values['value']}")
                        stuff[keys] = values['value']
                    elif isinstance(values, str) and keys == 'timestamp':
                        # print(f"{keys}: {values}")
                        tmptimestamp = values.split("T")[-1]
                        hour = tmptimestamp.split(":")[0]
                        minute = tmptimestamp.split(":")[1]
                        if int(hour) == 0:
                            hour = 24
                        tmptimestamp = f"{(int(hour)-5)%24}{minute}"
                        stuff[keys] = tmptimestamp
            if timestamp:
                container[stuff['timestamp']] = stuff
            else:
                container[i] = stuff
        # print(f"{json.dumps(container, indent=4)}")
        return container

    def badfordays(self, pzip, country='US'):
        i = 1
        i_s = []
        timestamps = []
        observation = OrderedDict()
        observations = self.n.get_observations(pzip, country)
        print(f"{json.dumps(observations, indent=4)}")
        return
        tags = ['timestamp', 'temperature', 'relativeHumidity', 'dewpoiont', 'barometricPressure']
        for key, value in json.dump(observations):
            #if item in tags:
            if key in tags:
                tmp = {i : item}
                observation.update(tmp)
                print(json.dumps(observation, indent=4))
                #break
            else:
                break
            if item == 'timestamp':
                i += 1

        print(json.dumps(observation, indent=4))
        return observation


    def basic_vals(self, pzip, country):
        
        observation = self.singleshot(pzip, country)    

        relativeHumidity = {}
        barometricPressure = {}
        timestamp = {}

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
                # print(json.dumps(value, indent=4))
            elif key == "dewpoint":
                dewpoint = value
            elif key == "temperature":
                temperature = value
                if temperature:
                    temperature['value'] = str(round(int(temperature['value'])*9/5+32))
                else:
                    temperature = None
            elif key == 'timestamp':
                tmptimestamp = value.split("T")[-1]
                hour = tmptimestamp.split(":")[0]
                minute = tmptimestamp.split(":")[1]
                tmptimestamp = f"{(int(hour)-5)%24}{minute}"
                timestamp[value] = tmptimestamp
            else:
                continue

        # print(f"temperature: {temperature['value']}")
        # print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
        # print(f"relative humidity: {relativeHumidity['value']}")
        # print(f"dewpoint: {dewpoint['value']}")

    def fordays_vals(self, pzip, country='US'):
        
        observation = self.fordays(pzip, country)    

        # print(str(observation))

        # print(json.dumps(observation, indent=4))
        # return

        relativeHumidity = {}
        barometricPressure = {}
        dewpoint = {}
        temperature = {}

        items = ['relativeHumidity', 'barometricPressure', 'dewpoint', 'temperature', 'timestamp']
        i = 0
        eyes = []
        timestamps = []
        observations = {}
        for keys, values in observation.items():
            #print(values)
            relativeHumidity = {}
            barometricPressure = {}
            dewpoint = {}
            temperature = {}
            i += 1
            timestamps = []
            i_s = []
            # print (f"{json.dumps(values, indent=4)})")
            for key, value in values.items():
                # print(value)
                if key == "relativeHumidity":
                    observations[i] = key
                    relativeHumidity = value
                    observations[i][key] = relativeHumidity
                elif key == "barometricPressure":
                    observations[i] = key
                    barometricPressure = value
                    if barometricPressure:
                        barometricPressure['value'] = float(barometricPressure['value'])/100
                        observations[i][key] = barometricPressure['value']
                    else:
                        barometricPressure = None
                        observations[i][key] = None
                    # print(json.dumps(value, indent=4))
                elif key == "dewpoint":
                    observations[i] = key
                    dewpoint = value
                    observations[i][key] = dewpoint
                elif key == "temperature":
                    observations[i] = {key}
                    temperature = value
                    if temperature:
                        temperature['value'] = round(int(temperature['value'])*9/5+32)
                        observations[i][key] = temperature['value']
                    else:
                        temperature = None
                        observations[i][key] = None
                elif  key == "timestamp":
                    i += 1
                    observations[i] = key
                    timestamp = value.split("T")[-1]
                    hour = timestamp.split(":")[0]
                    minute = timestamp.split(":")[1]
                    timestamp = f"{int(hour)-5}{minute}"
                    timestamps.append(timestamp)
                    i_s.append(i)
                else:
                    continue

            # print(f"temperature: {temperature['value']}")
            # print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
            # print(f"relative humidity: {relativeHumidity['value']}")
            # print(f"dewpoint: {dewpoint['value']}")

            return timestamp, i_s, observations


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.njob = noaa_job()
        '''
        temperature = [30,32,34,32,33,31,29,32,35,45]

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, pen=pen)
        '''
        #self.graph_item('temperature')

    def graph_item(self, x, pzip, country='US', samples=20, timestamp=False):

        # timestamps, i_s, observations = self.njob.fordays(pzip, country)
        # self.njob.singleshot(pzip, country)
        observations = self.njob.fordays(pzip, country)
        # print(x)
        # print(f"{json.dumps(observations)}")

        data = []
        wtime = []
        i = 0
        # wtime.append(i)
        for key, value in observations.items():
            # print(f"{x}: {json.dumps(value[x], indent=4)}")
            # break
            if value[x]:
                '''
                # temperature = round(int(value[x]['value'])*9/5+32)
                if x == 'temperature':
                    temperature = round(int(value[x]['value'])*9/5+32)
                    print(f"temp: {temperature}")
                    data.append(temperature)
                else:
                '''
                thedata = value[x]['value']
                data.append(thedata)
                wtime.append(i)
                # print(f"{x}: {i}: {thedata}")
                if i == int(samples):
                    break
                i += 1
               
        if timestamp:
             wtime = timestamps
        else:
             wtimme = i_s

        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(wtime, data, pen=pen)
        

if __name__ == "__main__":

    import argparse

    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="83221", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    parser.add_argument("-s", "--samples", default='20', help="number of samples to chart")
    parser.add_argument("-T", "--timestamp", action='store_true', help="timestamp")
    parser.add_argument("-t", "--tag", default='temperature', help="tag to plot - one of ['temperature', 'barometricPressure', 'relativeHumidity', 'dewpoint']")
    args = parser.parse_args()

    njob = noaa_job()
    containers = njob.fordays(args.zipcode, args.country, args.timestamp)
    print(f"{json.dumps(containers, indent=4)}")
    #stuff = njob.singleshot(args.zipcode, args.country)
    # print(f"{json.dumps(stuff, indent=4)}")
    # njob.basic_vals('39503', 'US')
    # njob.fordays_vals(args.zipcode, args.country)
    '''
    app = QApplication(sys.argv)
    main = MainWindow()
    main.graph_item(args.tag, args.zipcode, args.country, args.samples, args.timestamp)
    main.show()
    app.exec()
    '''

