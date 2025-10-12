#!/usr/bin/env -S python -u

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


        print(f"temperature: {temperature['value']}")
        print(f"barometric pressure: {float(barometricPressure['value']):.5f}")
        print(f"relative humidity: {relativeHumidity['value']}")
        print(f"dewpoint: {dewpoint['value']}")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, pen=pen)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="00000", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    args = parser.parse_args()

    njob = noaa_job()

    # njob.basic_vals('39503', 'US')
    njob.basic_vals(args.zipcode, args.country)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec()


