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

#####
# Load local libraries
sys.path.append("../../..")
from wnp.lib.NoaaObservationRun import NoaaObservationRun
from wnp.config import DEFAULT_DEGREES_UNITS


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.njob = NoaaObservationRun()

        self.lineColor = { 'temperature' : 'blue', 'dewpoint' : 'green', 'relativeHumidity' : 'purple', 'barometricPressure' : 'orange' }

    def graph_item(self, item, pzip, country='US', samples=20, timestamp=False):

        # timestamps, i_s, observations = self.njob.fordays(pzip, country)
        # self.njob.singleshot(pzip, country)
        observations = self.njob.fordays(pzip, country, samples, timestamp)
        # print(item)
        # print(f"{json.dumps(observations)}")

        data = []
        wtime = []
        i = 0
        # wtime.append(i)
        for key, value in observations.items():
            '''
            if timestamp:
                # wtime.append(int(''.join(key.split('-'))))
                # the above won't work -- what needs to be done is to
                # use the 'timestamp' as a label for each of the iterations..
                wtime.append(key)
            else:
                wtime.append(key)
            '''
            wtime.append(i)    
            data.append(value[item])
            #print(f"{key}: {item}: {value[item]}")
            i += 1
            if i == int(samples):
                break
        # print(f"{json.dumps(observations, indent=4)}")

        data.reverse()

        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle(item, color="b", size="30pt")
        self.graphWidget.setLabel('left', item, color=self.lineColor[item], size='14pt')
        self.graphWidget.setLabel('bottom', 'Time', color='green', size='14pt')   

        # pen = pg.mkPen(color=(255, 0, 0))
        pen = pg.mkPen(color=self.lineColor[item])

        self.graphWidget.plot(wtime, data, pen=pen)
        

if __name__ == "__main__":

    import argparse

    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="83402", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    parser.add_argument("-s", "--samples", default='2000', help="number of samples to chart")
    parser.add_argument("-T", "--timestamp", action='store_true', help="timestamp")
    parser.add_argument("-t", "--tag", default='temperature', help="tag to plot - one of ['temperature', 'barometricPressure', 'relativeHumidity', 'dewpoint']")
    args = parser.parse_args()

    #njob = noaa_job()
    #containers = njob.fordays(args.zipcode, args.country, args.samples, args.timestamp)
    # print(f"{json.dumps(containers, indent=4)}")
    # stuff = njob.singleshot(args.zipcode, args.country)
    # print(f"{json.dumps(stuff, indent=4)}")

    app = QApplication(sys.argv)
    main = MainWindow()
    main.graph_item(args.tag, args.zipcode, args.country, args.samples, args.timestamp)
    main.show()
    app.exec()


