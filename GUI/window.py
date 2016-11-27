# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QGraphicsScene
from PyQt4 import QtGui 
from PyQt4.QtCore import pyqtSignature,  QTimer,  SIGNAL
from graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
import os,  pickle
from robot import Robot
from RobotInfo import RobotInfo
from statistic import statistic

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.countBattle = 0
        self.timer = QTimer()
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.hide()
        
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Start the last battle
        """
        
        with open(os.getcwd() + "/.datas/lastArena",  'rb') as file:
            unpickler = pickle.Unpickler(file)
            dico = unpickler.load()
        file.close()

        self.setUpBattle(dico["width"] , dico["height"], dico["botList"] )
        
    def setUpBattle(self, width, height, botList):
        self.tableWidget.clearContents()
        self.tableWidget.hide()
        self.graphicsView.show()
        self.width = width
        self.height = height
        self.botList = botList
        self.statisticDico={}
        for bot in botList:
            self.statisticDico[self.repres(bot)] = statistic()
        self.startBattle()
        
    def startBattle(self):
        
        try:
            self.disconnect(self.timer, SIGNAL("timeout()"),  self.scene.advance)
            del self.timer
            del self.scene
            del self.sceneMenu
        except:
            pass
            
        self.timer = QTimer()
        self.countBattle += 1
        self.sceneMenu = QGraphicsScene()
        self.graphicsView_2.setScene(self.sceneMenu)
        self.scene = Graph(self,  self.width,  self.height)
        self.graphicsView.setScene(self.scene)
        self.scene.AddRobots(self.botList)
        self.connect(self.timer, SIGNAL("timeout()"),  self.scene.advance)
        self.timer.start((self.horizontalSlider.value()**2)/100.0)
        self.resizeEvent()
    
    @pyqtSignature("int")
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.timer.setInterval((value**2)/100.0)
    
    @pyqtSignature("")
    def on_actionNew_activated(self):
        """
        Battle Menu
        """
        self.battleMenu = Battle(self)
        self.battleMenu.show()
    
    @pyqtSignature("")
    def on_actionNew_2_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Not Implemented Yet")
    
    @pyqtSignature("")
    def on_actionOpen_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Not Implemented Yet")

    def resizeEvent(self, evt=None):
        try:
            self.graphicsView.fitInView(self.scene.sceneRect(), 4)
        except :
            pass

    def addRobotInfo(self, robot):
        self.sceneMenu.setSceneRect(0, 0, 170, 800)
        rb = RobotInfo()
        rb.pushButton.setText(str(robot))
        rb.progressBar.setValue(100)
        rb.robot = robot
        robot.info = rb
        robot.progressBar = rb.progressBar
        robot.icon = rb.toolButton
        robot.icon2 = rb.toolButton_2
        p = self.sceneMenu.addWidget(rb)
        l = (len(self.scene.aliveBots) )
        self.sceneMenu.setSceneRect(0, 0, 170, l*80)
        p.setPos(0, (l -1)*80)
        
    def chooseAction(self):
        if self.countBattle >= self.spinBox.value():
            "Menu Statistic"
            self.graphicsView.hide()
            self.tableWidget.show()
            self.tableWidget.setRowCount(len(self.statisticDico))
            i = 0
            for key, value in self.statisticDico.items():
                self.tableWidget.setItem(i, 0,  QtGui.QTableWidgetItem(key))
                self.tableWidget.setItem(i, 1,  QtGui.QTableWidgetItem(str(value.first)))
                self.tableWidget.setItem(i, 2,  QtGui.QTableWidgetItem(str(value.second)))
                self.tableWidget.setItem(i, 3,  QtGui.QTableWidgetItem(str(value.third)))
                self.tableWidget.setItem(i, 4,  QtGui.QTableWidgetItem(str(value.points)))
               
                i += 1
                
                
            self.countBattle = 0
            self.timer.stop()
        else:
            self.startBattle()
            
    def repres(self, bot):
        repres = repr(bot).split(".")
        return repres[1].replace("'>", "")
