# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os,  pickle

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer

from graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
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
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.hide()
        
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Start the last battle
        """
        
        if os.path.exists(os.getcwd() + "/.datas/lastArena"):
            with open(os.getcwd() + "/.datas/lastArena",  'rb') as file:
                unpickler = pickle.Unpickler(file)
                dico = unpickler.load()
            file.close()
        else:
            print("No last arena found.")

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
            self.timer.timeout.disconnect(self.scene.advance)
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
        self.timer.timeout.connect(self.scene.advance)
        self.timer.start((self.horizontalSlider.value()**2)/100.0)
        self.resizeEvent()
    
    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.timer.setInterval((value**2)/100.0)
    
    @pyqtSlot()
    def on_actionNew_triggered(self):
        """
        Battle Menu
        """
        self.battleMenu = Battle(self)
        self.battleMenu.show()
    
    @pyqtSlot()
    def on_actionNew_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Not Implemented Yet")
    
    @pyqtSlot()
    def on_actionOpen_triggered(self):
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
                self.tableWidget.setItem(i, 0,  QTableWidgetItem(key))
                self.tableWidget.setItem(i, 1,  QTableWidgetItem(str(value.first)))
                self.tableWidget.setItem(i, 2,  QTableWidgetItem(str(value.second)))
                self.tableWidget.setItem(i, 3,  QTableWidgetItem(str(value.third)))
                self.tableWidget.setItem(i, 4,  QTableWidgetItem(str(value.points)))
               
                i += 1
                
                
            self.countBattle = 0
            self.timer.stop()
        else:
            self.startBattle()
            
    def repres(self, bot):
        repres = repr(bot).split(".")
        return repres[1].replace("'>", "")
