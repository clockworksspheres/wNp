#!/usr/bin/env -S python -u

import faulthandler
import traceback

import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg

class GraphWindow(QWidget):
    def __init__(self, title, data):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)
        
        # Create PlotWidget
        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
        # Plot data
        self.plot_widget.plot(data, pen='b')
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
        layout = QVBoxLayout(central_widget)
        
        # Create sample data for different graphs
        self.data1 = np.sin(np.linspace(0, 10, 100))
        self.data2 = np.cos(np.linspace(0, 10, 100))
        self.data3 = np.random.random(100)
        self.data4 = np.linspace(0, 5, 100) ** 2
        
        # Create buttons
        button1 = QPushButton("Sine Wave")
        button2 = QPushButton("Cosine Wave")
        button3 = QPushButton("Random Data")
        button4 = QPushButton("Quadratic")
        
        # Connect buttons to functions
        button1.clicked.connect(self.show_graph1)
        button2.clicked.connect(self.show_graph2)
        button3.clicked.connect(self.show_graph3)
        button4.clicked.connect(self.show_graph4)
        
        # Add buttons to layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        
        # Store graph windows to keep reference
        self.graph_windows = []
        
    def show_graph1(self):
        graph = GraphWindow("Sine Wave", self.data1)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph2(self):
        graph = GraphWindow("Cosine Wave", self.data2)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph3(self):
        graph = GraphWindow("Random Data", self.data3)
        graph.show()
        self.graph_windows.append(graph)
        
    def show_graph4(self):
        graph = GraphWindow("Quadratic", self.data4)
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


