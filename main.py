# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets, QtCore, uic,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *

import pyqtgraph as pg
import numpy as np
from random import randint
import sys
import os
from pyqtgraph import PlotWidget, plot

import csv 
import pandas as pd

#from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window=QtWidgets.QMainWindow()
        self.x1=[]
        self.y1=[]
        self.x2=[]
        self.y2=[]
        self.x3=[]
        self.y3=[]
        self.x4=[]
        self.y4=[]
        self.x5=[]
        self.y5=[]

        self.signal1=[]
        # self.signal2=[]
        # self.signal3=[]
        # self.signal4=[]
        # self.signal5=[]



        self.initGui()
#=====================THE MENUBAR================================
#================================================================
        ExitAction = QtGui.QAction("&Exit", self)
        ExitAction.setShortcut("Ctrl+Q")
        ExitAction.setStatusTip('Leave the App')
        ExitAction.triggered.connect(self.close_application)

        openAction=QtGui.QAction("&New File",self)
        openAction.setShortcut("Ctrl+N")
        openAction.setStatusTip('Open a new file')
        openAction.triggered.connect(self.openFileNameDialog)

        openActions=QtGui.QAction("&Multiple Files",self)
        openActions.setShortcut("Ctrl+M")
        openActions.setStatusTip('Open multiple files')
        openActions.triggered.connect(self.openFileNamesDialog)

        mainMenu = self.menuBar()
        fileMenu= mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(openActions)
        fileMenu.addAction(ExitAction)
        

        editMenu=mainMenu.addMenu('&Edit')
        editMenu.addAction(ExitAction)

        viewMenu=mainMenu.addMenu('&View')
        viewMenu.addAction(ExitAction)
        
        toolsMenu=mainMenu.addMenu('&Tools')
        toolsMenu.addAction(ExitAction)

        helpMenu=mainMenu.addMenu('&Help')
        helpMenu.addAction(ExitAction)

#=====================THE TOOLBAR================================
#================================================================
    def initGui(self):        
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32,32))
        self.addToolBar(toolbar)


#=====================THE ICONS==================================
#================================================================
        AFile = QAction( "Load a new file", self)
        AFile.setIcon(QtGui.QIcon("file.png"))
        AFile.setStatusTip("Load a new file")
        AFile.triggered.connect(self.openFileNameDialog)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(AFile)
        self.index=-1

        toolbar.addSeparator()

        Multiple_Files = QAction( "Open Multiple Files", self)
        Multiple_Files.setIcon(QtGui.QIcon("files.png"))
        Multiple_Files.setStatusTip("Open Multiple Files")
        Multiple_Files.triggered.connect(self.openFileNamesDialog)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(Multiple_Files)

        toolbar.addSeparator()


        # CURSOR = QAction("Your button", self)
        # CURSOR.setIcon(QtGui.QIcon("cursor.png"))
        # CURSOR.setStatusTip("This is your button")
        # CURSOR.triggered.connect(self.onMyToolBarButtonClick)
        # CURSOR.setCheckable(True)
        # toolbar.addAction(CURSOR)        


        # toolbar.addSeparator()
        
        PAUSE = QAction( "Pause the Signal", self)
        PAUSE.setIcon(QtGui.QIcon("pause.png"))
        PAUSE.setStatusTip("Pause the Signal")
        PAUSE.triggered.connect(self.pauseSignal)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(PAUSE)


        toolbar.addSeparator()
        
        PLAY = QAction( "Play the Signal", self)
        PLAY.setIcon(QtGui.QIcon("play.png"))
        PLAY.setStatusTip("Play the Signal")
        PLAY.triggered.connect(self.playSignal)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(PLAY)

        toolbar.addSeparator()
        
        PLAYALL = QAction( "Play all the Signals", self)
        PLAYALL.setIcon(QtGui.QIcon("playMultiple.png"))
        PLAYALL.setStatusTip("Play all the signals")
        PLAYALL.triggered.connect(self.playSignals)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(PLAYALL)

        toolbar.addSeparator()
        
        STOP = QAction( "Stop the Signal", self)
        STOP.setIcon(QtGui.QIcon("stop.png"))
        STOP.setStatusTip("Stop the Signal")
        STOP.triggered.connect(self.stopSignal)
        #Commented but we will choose if we need it or not    
        # PAUSE.setCheckable(True)
        toolbar.addAction(STOP)

        toolbar.addSeparator()

        SignalA = QtGui.QCheckBox('Hide Signal', self)
        SignalA.move(300, 30)
        SignalA.stateChanged.connect(self.HideOrShow)


    def HideOrShow(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.graphicsView.setVisible(False)
        else: 
            self.ui.graphicsView.setVisible(True)


    def contextMenuEvent(self, event):
       
           cmenu = QMenu(self)
           
           newAct = cmenu.addAction("New")
           opnAct = cmenu.addAction("Open")
           quitAct = cmenu.addAction("Quit")
           action = cmenu.exec_(self.mapToGlobal(event.pos()))

           if action == quitAct:
               qApp.quit()
            
           if action == opnAct:
               self.openFileNameDialog()
       

    def onMyToolBarButtonClick(self, s):
        print("click", s)            

    #    self.openFileNamesDialog()

    
    def openFileNameDialog(self):
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                pen = pg.mkPen(color=(255, 0, 0))

                if fileName.endswith('.txt'): 
                    arr = np.genfromtxt(fileName)
                    ii = arr[:,0]
                    jj = arr[:,1]
                    self.x = ii
                    self.y =jj # 100 data points
                    # self.ui.graphicsView.addLegend()
                    # self.ui.graphicsView.plot(ii,jj, pen=pen,name='signal1')
                    # self.signal1.append(self.x)
                    # self.signal1.append(self.y)
                    # self.signal1=[sellf.x,self.y]

                elif  fileName.endswith('.xlsx'): 
                    df = pd.read_excel(fileName,sheet_name = 0,usecols = [0,1],names=['B', 'C'])
                    #self.ui.graphicsView.addLegend()
                    self.x = np.array(df['B'])
                    self.y = np.array(df['C']) 
                    # self.data_line =  self.ui.graphicsView.plot(df['B'],df['C'],name=fileName.getname(),   pen=pen)
                    # self.signal2.append(self.x)
                    # self.signal2.append(self.y)

                elif fileName.endswith('.csv'):
                    df=pd.read_csv(fileName,header=None,usecols=[0,1])
                    self.x=np.array(df[0])
                    self.y=np.array(df[1])
                   
                    # self.signal3.append(self.x)
                    # self.signal3.append(self.y)

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        # file_list=[]
        # root_dir = sys.path[0]
        # path = "/"
        if files:
            for i in range(len(files)):
                if files[i].endswith('.txt'): 
                    arr = np.genfromtxt(files[i])
                    ii = arr[:,0]
                    jj = arr[:,1]
                    
                    if i==0:
                        self.x1= ii
                        self.y1=jj
                        # self.signal1.append(self.x1)
                        # self.signal1.append(self.y1)
                    elif i==1:
                        self.x2=ii
                        self.y2=jj
                        # self.signal2.append(self.x2)
                        # self.signal2.append(self.y2)
                    elif i==2:
                        self.x3=ii
                        self.y3=jj
                        # self.signal3.append(self.x3)
                        # self.signal3.append(self.y3)

                    elif i==3:
                        self.x4=ii
                        self.y4=jj
                        # self.signal4.append(self.x4)
                        # self.signal4.append(self.y4)

                    else :
                        self.x5=ii
                        self.y5=jj
                        # self.signal5.append(self.x5)
                        # self.signal5.append(self.y5)


                elif  files[i].endswith('.xlsx'): 
                    df = pd.read_excel( files[i],sheet_name = 0,usecols = [0,1],names=['B', 'C'])
                    # self.ui.graphicsView.addLegend()
                    if i==0:
                        self.x1 = np.array(df['B'])
                        self.y1=np.array(df['C'])
                        # self.signal1.append(self.x1)
                        # self.signal1.append(self.y1)

                    elif i==1:
                        self.x2=np.array(df['B'])
                        self.y2=np.array(df['C'])
                        # self.signal2.append(self.x2)
                        # self.signal2.append(self.y2)
                    elif i==2:
                        self.x3=np.array(df['B'])
                        self.y3=np.array(df['C'])
                        # self.signal3.append(self.x3)
                        # self.signal3.append(self.y3)
                    elif i==3:
                        self.x4=np.array(df['B'])
                        self.y4=np.array(df['C'])
                        # self.signal4.append(self.x4)
                        # self.signal4.append(self.y4)
                    else:
                        self.x5=np.array(df['B'])
                        self.y5=np.array(df['C'])
                        # self.signal5.append(self.x5)
                        # self.signal5.append(self.y5)
                    #self.ui.graphicsView.plot(df['B'],df['C'],   pen='b')
                    
                elif  files[i].endswith('.csv'):
                    df=pd.read_csv(files[i],header=None,usecols=[0,1])
                    if i==0:
                        self.x1 = np.array(df[0])
                        self.y1=np.array(df[1])
                        # self.signal1.append(self.x1)
                        # self.signal1.append(self.y1)
                    elif i==1:
                        self.x2=np.array(df[0])
                        self.y2=np.array(df[1])
                        # self.signal2.append(self.x2)
                        # self.signal2.append(self.y2)
                    elif i==2:
                        self.x3=np.array(df[0])
                        self.y3=np.array(df[1])
                        # self.signal3.append(self.x3)
                        # self.signal3.append(self.y3)
                    elif i==3:
                        self.x4=np.array(df[0])
                        self.y4=np.array(df[1])
                        # self.signal4.append(self.x4)
                        # self.signal4.append(self.y4)
                    else:
                        self.x5=np.array(df[0])
                        self.y5=np.array(df[1])
                        # self.signal5.append(self.x5)
                        # self.signal5.append(self.y5)
                   
    
    def playSignals(self):
        self.stop=False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data1)
        self.timer.start()

    def playSignal(self):
        self.stop=False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def stopSignal(self):
        self.ui.graphicsView.clear()


    def pauseSignal(self):
        self.stop=True
        self.timer = QtCore.QTimer()

    def update_plot_data(self):       
        self.index+=1
        # # self.ui.graphicsView.addLegend()
        # self.y = self.y[1:]  # Remove the first 
        # self.x = self.x[1:]  # Remove the first 


        self.signal1=self.ui.graphicsView.plot(self.x[:self.index+1], self.y[:self.index+1],pen='b')



    def update_plot_data1(self):       
        self.index+=1
            
        self.ui.graphicsView.plot(self.x1[:self.index+1], self.y1[:self.index+1],pen='b',name='Signal1')
        self.ui.graphicsView.plot(self.x2[:self.index+1], self.y2[:self.index+1],pen='r',name='Signal2')
        self.ui.graphicsView.plot(self.x3[:self.index+1], self.y3[:self.index+1],pen='m',name='Signal3')
        self.ui.graphicsView.plot(self.x4[:self.index+1], self.y4[:self.index+1],pen='k',name='Signal4')
        self.ui.graphicsView.plot(self.x5[:self.index+1], self.y5[:self.index+1],pen='g',name='Signal5')

     

    def close_application(self):
        print("Bye bye")
        sys.exit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Signal Viewer")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #The Graph Area
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 30, 761, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setBackground('#e1f5f3')

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)




def main(): 
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()

    application.setWindowTitle("Signal Viewer")
    application.setWindowIcon(QIcon("wave.png"))
    app.exec_()


if __name__ == "__main__":
    main()