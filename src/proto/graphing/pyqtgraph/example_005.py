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
# load internal libraries
sys.path.append("../../..")
from wnp.lib.NoaaObservationRun import NoaaObservationRun
 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.njob = NoaaObservationRun()
        '''
        temperature = [30,32,34,32,33,31,29,32,35,45]

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, pen=pen)
        '''
        #self.graph_item('temperature')

    def graph_item(self, x, pzip, country='US', samples=20):

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
                if i == int(samples):
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
    parser.add_argument("-z", "--zipcode", default="83221", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    parser.add_argument("-s", "--samples", default='20', help="number of samples to chart")
    parser.add_argument("-t", "--tag", default='temperature', help="tag to plot - one of ['temperature', 'barometricPressure', 'relativeHumidity', 'dewpoint']")
    args = parser.parse_args()

    # njob = noaa_job()

    # njob.basic_vals('39503', 'US')
    # njob.fordays_vals(args.zipcode, args.country)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.graph_item(args.tag, args.zipcode, args.country, args.samples)
    main.show()
    app.exec()


