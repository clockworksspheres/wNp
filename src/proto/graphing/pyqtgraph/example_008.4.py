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
                container[tmptimestamp]['temperature'] = observation['temperature']['value'] 
                container[tmptimestamp]['dewpoint'] = observation['dewpoint']['value']
                container[tmptimestamp]['relativeHumidity'] = observation['relativeHumidity']['value']
                container[tmptimestamp]['barometricPressure'] = observation['barometricPressure']['value']
            else:
                container[i] = {}
                container[i]['timestamp'] = tmptimestamp
                container[i]['temperature'] = observation['temperature']['value'] 
                container[i]['dewpoint'] = observation['dewpoint']['value']
                container[i]['relativeHumidity'] = observation['relativeHumidity']['value']
                container[i]['barometricPressure'] = observation['barometricPressure']['value']
        # print(f"{json.dumps(container, indent=4)}")

        '''





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
            #print(f"{json.dumps(stuff, indent=4)}")
            '''
        # print(f"{json.dumps(container, indent=4)}")
        return container


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.njob = noaa_job()

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
            wtime.append(key)
            # data.append(key[value][x])
            data.append(value[x])
            #print(f"{key}: {x}: {value[x]}")
            i += 1
            if i == int(samples):
                break
        print(f"{json.dumps(observations, indent=4)}")
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
    # print(f"{json.dumps(containers, indent=4)}")
    # stuff = njob.singleshot(args.zipcode, args.country)
    # print(f"{json.dumps(stuff, indent=4)}")

    app = QApplication(sys.argv)
    main = MainWindow()
    main.graph_item(args.tag, args.zipcode, args.country, args.samples, args.timestamp)
    main.show()
    app.exec()


