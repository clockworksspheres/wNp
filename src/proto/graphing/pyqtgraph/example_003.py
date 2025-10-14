#!/usr/bin/env -S python -u

import faulthandler

import json
from noaa_sdk import NOAA

from PySide6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
import sys

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

    def fordays(self, pzip, country='US'):
        i = 1
        observation = {}
        observations = self.n.get_observations(pzip, country)
        for item in observations:
            tmp = {i : item}
            observation.update(tmp)
            # print(json.dumps(observation, indent=4))
            #break
            i += 1
        # print(json.dumps(observation, indent=4))
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
                # print(json.dumps(value, indent=4))
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

        # print(f"temperature: {temperature['value']}")
        # print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
        # print(f"relative humidity: {relativeHumidity['value']}")
        # print(f"dewpoint: {dewpoint['value']}")

    def fordays_vals(self, pzip, country):
        
        observation = self.fordays(pzip, country)    

        # print(str(observation))

        # print(json.dumps(observation, indent=4))
        # return

        relativeHumidity = {}
        barometricPressure = {}
        dewpoint = {}
        temperature = {}

        items = [relativeHumidity, barometricPressure, dewpoint, temperature]

        for keys, values in observation.items():
            #print(values)
            relativeHumidity = {}
            barometricPressure = {}
            dewpoint = {}
            temperature = {}

            for key, value in values.items():
                # print(value)
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
                else:
                    continue

            # print(f"temperature: {temperature['value']}")
            # print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
            # print(f"relative humidity: {relativeHumidity['value']}")
            # print(f"dewpoint: {dewpoint['value']}")


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

    def graph_item(self, x, pzip, country='US'):

        observations = self.njob.fordays(pzip)
        # print(x)

        data = []
        wtime = []
        i = 0
        # wtime.append(i)
        for key, value in observations.items():
            # print(f"{x}: {json.dumps(value[x], indent=4)}")
            # break
            if value[x]:
                #temperature = str(round(int(value[x]['value'])*9/5+32)) 
                temperature = round(int(value[x]['value'])*9/5+32)
                data.append(temperature)
                wtime.append(i)            
                print(f"{x}: {i}: {temperature}")
                if i == 4:
                    break
                i += 1
               
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(wtime, data, pen=pen)
        

if __name__ == "__main__":

    import argparse

    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="00000", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    args = parser.parse_args()

    # njob = noaa_job()

    # njob.basic_vals('39503', 'US')
    # njob.fordays_vals(args.zipcode, args.country)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.graph_item('temperature', args.zipcode, args.country)
    main.show()
    app.exec()


