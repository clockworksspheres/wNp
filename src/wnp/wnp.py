#!/usr/bin/env -S python -u

import faulthandler
import traceback
import sys 
import json

#####
# Importing 3rd party libraries - must be installed
# separately
#import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
import pyqtgraph as pg

####
# loading local libs
from lib.NoaaObservationRun import NoaaObservationRun
from PainStarDelegate import PainTrackerWidget

class GraphWindow(QWidget):
    def __init__(self, title, x, y=None, xtitle='X', ytitle='Value'):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)
    
        # Create PlotWidget
        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
    
        # Plot data
        if isinstance(x, list)  and isinstance(y, list):
            self.plot_widget.plot(x, y, pen='b')
        else:
            y = x 
            self.plot_widget.plot(y, pen='b')
        self.plot_widget.setTitle(title)
        self.plot_widget.setLabel('left', ytitle)
        self.plot_widget.setLabel('bottom', xtitle)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)
    
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vlayout = QVBoxLayout(central_widget)
        #hOneLayout = QHBoxLayout(central_widget)
        #hTwoLayout = QHBoxLayout(vlayout)

        # Create sample data for different graphs
        # self.data1 = np.sin(np.linspace(0, 10, 100))
        # self.data2 = np.cos(np.linspace(0, 10, 100))
        # self.data3 = np.random.random(100)
        # self.data4 = np.linspace(0, 5, 100) ** 2

        # Create line edit and title
        self.zipLabel = QLabel("Zip Code")
        self.zipLineEdit = QLineEdit()
        self.zipLineEdit.setText(f"83402")

        self.countryLabel = QLabel("Country")
        self.countryLineEdit = QLineEdit()
        self.countryLineEdit.setText(f"US")

        #self.samplesLabel = 

        #hOneLayout.addWidget(self.zipLabel)
        #hOneLayout.addWidget(self.zipLineEdit)

        # Create buttons
        button1 = QPushButton("Temperature")
        button2 = QPushButton("Relative Humidity")
        button3 = QPushButton("Barometric Pressure")
        button4 = QPushButton("Dewpoint")
        button5 = QPushButton("Graph All Four")
        button6 = QPushButton("Pain Survey")

        # Connect buttons to functions
        button1.clicked.connect(self.show_graph1)
        button2.clicked.connect(self.show_graph2)
        button3.clicked.connect(self.show_graph3)
        button4.clicked.connect(self.show_graph4)
        button5.clicked.connect(self.show_graphAll)
        button6.clicked.connect(self.pain_survey)


        # Add buttons to layout
        #vlayout.addWidget(hOneLayout)
        vlayout.addWidget(self.zipLabel)
        vlayout.addWidget(self.zipLineEdit)
        vlayout.addWidget(self.countryLabel)
        vlayout.addWidget(self.countryLineEdit)
        vlayout.addWidget(button1)
        vlayout.addWidget(button2)
        vlayout.addWidget(button3)
        vlayout.addWidget(button4)
        vlayout.addWidget(button5)
        vlayout.addWidget(button6)

        self.setLayout(vlayout)

        # Store graph windows to keep reference
        self.graph_windows = []

        # instanciate an NoaaObservationRun object
        self.njob = NoaaObservationRun()

    def get_live_observations(self, y='temperature', pzip='39503', country='US', samples=40, timestamp=False):
        # pzip = self.zipLineEdit.text()
        # pzip = pzip.strip()
        print(f"Zip Code: {pzip}")

        self.data = []
        self.wtime = []

        try:
            observations = self.njob.fordays(pzip, country='US', samples=2000)

            self.data = []
            self.wtime = []
            i = 0
            # wtime.append(i)
            for key, value in observations.items():
                self.wtime.append(i)
                self.data.append(value[y])
                #print(f"{key}: {item}: {value[item]}")
                i += 1
                #if i == int(samples):
                #    break
            # print(f"{json.dumps(observations, indent=4)}")
        except AttributeError as err:
            print(f"{traceback.format_exc()}")
            print("#####")
            print("Error trying to collect data from the NOAA, either too often or network errors...")
            print("#####")

        self.data.reverse()

        return self.wtime, self.data

    def show_graph1(self):

        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        country = self.countryLineEdit.text()
        country = country.strip

        wtime, data = self.get_live_observations('temperature', pzip, country)

        graph = GraphWindow(f"Temperature: {pzip}", wtime, data, 'Time', 'Temperature')
        graph.show()
        self.graph_windows.append(graph)

    def show_graph2(self):

        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        country = self.countryLineEdit.text()
        country = country.strip

        wtime, data = self.get_live_observations('relativeHumidity', pzip, country)

        graph = GraphWindow(f"Relative Humidity: {pzip}", wtime, data, 'Time', 'Relative Humidity')
        graph.show()
        self.graph_windows.append(graph)

    def show_graph3(self):

        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        country = self.countryLineEdit.text()
        country = country.strip

        wtime, data = self.get_live_observations('barometricPressure', pzip, country)

        graph = GraphWindow(f"Barometric Pressure: {pzip}", wtime, data, 'Time', 'Barometric Pressure')
        graph.show()
        self.graph_windows.append(graph)

    def show_graph4(self):

        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        country = self.countryLineEdit.text()
        country = country.strip

        wtime, data = self.get_live_observations('dewpoint', pzip, country)

        graph = GraphWindow(f"Dewpoint: {pzip}", wtime, data, 'Time', 'Dewpoint')
        graph.show()
        self.graph_windows.append(graph)

    def show_graphAll(self):

        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        country = self.countryLineEdit.text()
        country = country.strip

        wtime, data = self.get_live_observations('temperature', pzip, country)

        graph = GraphWindow(f"Temperature: {pzip}", wtime, data, 'Time', 'Temperature')
        graph.show()
        self.graph_windows.append(graph)

        wtime, data = self.get_live_observations('relativeHumidity', pzip, country)

        graph = GraphWindow(f"Relative Humidity: {pzip}", wtime, data, 'Time', 'Relative Humidity')
        graph.show()
        self.graph_windows.append(graph)

        wtime, data = self.get_live_observations('barometricPressure', pzip, country)

        graph = GraphWindow(f"Barometric Pressure: {pzip}", wtime, data, 'Time', 'Barometric Pressure')
        graph.show()
        self.graph_windows.append(graph)

        wtime, data = self.get_live_observations('dewpoint', pzip, country)

        graph = GraphWindow(f"Dewpoint: {pzip}", wtime, data, 'Time', 'Dewpoint')
        graph.show()
        self.graph_windows.append(graph)

    def pain_survey(self):
        """
        """
        print("\t Attempting to show the pain tracker widget...")
        widget = PainTrackerWidget()
        # widget.resize(900, 900)
        widget.show()
        # widget.raise_()
        # widget.activateWindow()
        self.graph_windows.append(widget)





if __name__ == '__main__':

    import argparse

    #####
    # Enable traceback on segmentation fault...
    faulthandler.enable()

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    # parser.add_argument("-g", "--gui", action="store_true", help="Start the GUI - the default option.  If this option is given, all others will be ignored.")
    parser.add_argument("-z", "--zipcode", default="83402", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    parser.add_argument("-l", "--loadFile", default='', help="raw json data file to load, rather than acquire live data")
    parser.add_argument("-f", "--saveJsonData", default='', help="save raw json data to file")
    parser.add_argument("-o", "--saveOneshotJsonData", default='', help="save oneshot json data to file")
    parser.add_argument("-O", "--saveOneshotRawJsonData", default='', help="save raw oneshot json data to file")
    parser.add_argument("-s", "--samples", default='2000', help="number of samples to chart")
    parser.add_argument("-T", "--timestamp", action='store_true', help="timestamp")
    parser.add_argument("-R", "--raw", action='store_true', help="dump raw observation data to console")
    parser.add_argument("-t", "--tag", default='temperature', help="tag to plot - one of ['temperature', 'barometricPressure', 'relativeHumidity', 'dewpoint']")
    args = parser.parse_args()

    try:
        #####
        # Must make sure environment is set correctly if OS is Linux
        # and the window manager is Wayland.  Must be set before 
        # creating QApplication.  Does not check if X11 is running.
        if sys.platform.lower().startswith("linux"):
            logging.info("Found Linux Checking for Wayland")
            if os.environ.get("WAYLAND_DISPLAY") is not None or \
            os.environ.get("XDG_SESSION_TYPE") == "wayland":
                logging.info("Found Wayland, setting QT_QPA_PLATFORM")
                os.environ["QT_QPA_PLATFORM"] = "xcb"
    except OSError:
        logging.info("Problem checking for and setting environment variable in linux")


    # if len(sys.argv) == 1 or args.gui:
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)

        # Set pyqtgraph to use PySide6
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:

        njob = NoaaObservationRun()

    if args.saveJsonData:
        njob.setFileName(args.saveJsonData)
        containers = njob.getAndSaveFordaysRaw(args.zipcode, args.country, args.samples, args.timestamp)

    elif args.saveOneshotRawJsonData:
        njob.setFileName(args.saveOneshotRawJsonData)
        containers = njob.getAndSaveSingleShotRaw(args.zipcode, args.country)

        print(f"{json.dumps(containers, indent=4)}")

    elif args.saveOneshotJsonData:
        njob.setFileName(args.saveOneshotJsonData)
        containers = njob.getAndSaveSingleShot(args.zipcode, args.country)

        print(f"{json.dumps(containers, indent=4)}")

    elif args.raw:
        containers = njob.fordaysRaw(args.zipcode, args.country, args.samples, args.timestamp)
        print(f"{json.dumps(containers, indent=3)}")
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

