from PyQt5 import QtWidgets, QtCore, uic
from task1 import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
from random import randint
import sys
import os
from pyqtgraph import PlotWidget, plot

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)

        self.x = list(range(1000))  # 100 time points
        self.y = [randint(0,100) for _ in range(1000)]  # 100 data points


        pen = pg.mkPen(color=(255, 0, 0))
        arr = np.genfromtxt('emg.txt')
        # self.data_line =  self.graphWidget.plot(arr, pen=pen)





        # button = QPushButton("Click me")
        # button.clicked.connect(onbtnclick)
        # data = np.genfromtxt('bio_100Hz.csv', dtype=float, delimiter=',', names=False) 

        # plot data: x, y values
        # self.graphWidget.plot(data)
        self.stop=False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    # def draw_plot(self):
    #     L = [0, 1, 2, 3, 4, 5 ,6]
    #     self.ui.plot = pg.PlotWidget(self.ui.centralwidget)
    #     self.ui.gridLayout.addWidget(self.ui.plot)
    #     self.ui.plot.plot(L)
    # def OpenTxt(self):
    #     f = open("ecg.txt", "r")
    #     pw.plot(f)
    #     win = pg.GraphicsWindow()  # Automatically generates grids with multiple items
        # win.addPlot(data1, row=0, col=0)
        # win.addPlot(data2, row=0, col=1)
        # win.addPlot(data3, row=1, col=0, colspan=2)
        # pg.show(imageData)  # imageData must be a numpy array with 2 to 4 dimensions
    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.    

def main(): 
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()