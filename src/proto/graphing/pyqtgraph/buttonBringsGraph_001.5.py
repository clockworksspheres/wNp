#!/usr/bin/env -S python -u

import faulthandler
import traceback
import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
import pyqtgraph as pg

####
# loading local libs
sys.path.append("../../..")
from wnp.lib.NoaaObservationRun import NoaaObservationRun


class GraphWindow(QWidget):
    def __init__(self, title, x, y=None):
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
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'X')

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
        self.data1 = np.sin(np.linspace(0, 10, 100))
        self.data2 = np.cos(np.linspace(0, 10, 100))
        self.data3 = np.random.random(100)
        self.data4 = np.linspace(0, 5, 100) ** 2
        
        # Create line edit and title
        self.zipLabel = QLabel("Zip Code")
        self.zipLineEdit = QLineEdit()
        self.zipLabel.setText(f"Zip Code")
        self.zipLineEdit.setText(f"83402")

        #self.samplesLabel = 

        #hOneLayout.addWidget(self.zipLabel)
        #hOneLayout.addWidget(self.zipLineEdit)

        # Create buttons
        button1 = QPushButton("Temperature")
        button2 = QPushButton("Relative Humidity")
        button3 = QPushButton("Barometric Pressure")
        button4 = QPushButton("Dewpoint")
        
        # Connect buttons to functions
        button1.clicked.connect(self.show_graph1)
        button2.clicked.connect(self.show_graph2)
        button3.clicked.connect(self.show_graph3)
        button4.clicked.connect(self.show_graph4)
        
        # Add buttons to layout
        #vlayout.addWidget(hOneLayout)
        vlayout.addWidget(self.zipLabel)
        vlayout.addWidget(self.zipLineEdit)
        vlayout.addWidget(button1)
        vlayout.addWidget(button2)
        vlayout.addWidget(button3)
        vlayout.addWidget(button4)

        self.setLayout(vlayout)
        
        # Store graph windows to keep reference
        self.graph_windows = []

    def get_live_observations(self, y='temperature', pzip='39503', country='US', samples=40, timestamp=False):
        pzip = self.zipLineEdit.text()
        pzip = pzip.strip()
        print(f"Zip Code: {pzip}")
        
        njob = NoaaObservationRun()
        observations = njob.fordays(pzip, country='US', samples=2000)

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

        self.data.reverse()

        return self.wtime, self.data
 
    def show_graph1(self):

        wtime, data = self.get_live_observations('temperature', '39503')        

        graph = GraphWindow("Temperature", wtime, data)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph2(self):

        wtime, data = self.get_live_observations('relativeHumidity', '39503')        

        graph = GraphWindow("Relative Humidity", wtime, data)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph3(self):

        wtime, data = self.get_live_observations('barometricPressure', '39503')
        
        graph = GraphWindow("Barometric Pressure", wtime, data)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph4(self):

        wtime, data = self.get_live_observations('dewpoint', '39503')

        graph = GraphWindow("Dewpoint", wtime, data)
        graph.show()
        self.graph_windows.append(graph)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set pyqtgraph to use PySide6
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


