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
        self.width = width
        self.height = height
        self.botList = botList
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
        print "Not Implemented Yet"
    
    @pyqtSignature("")
    def on_actionOpen_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "Not Implemented Yet"

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
        p = self.sceneMenu.addWidget(rb)
        l = (len(self.scene.aliveBots) )
        self.sceneMenu.setSceneRect(0, 0, 170, l*80)
        p.setPos(0, (l -1)*80)
        
    def chooseAction(self):
        if self.countBattle >= self.spinBox.value():
            "Menu Statistic"
            self.countBattle = 0
            self.timer.stop()
        else:
            self.startBattle()
            
