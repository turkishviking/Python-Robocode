# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature,  QTimer,  SIGNAL
from graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
import os,  pickle
from robot import Robot

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
        
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Start the last battle
        """
        with open(os.getcwd() + "/.datas/lastArena",  'rb') as file:
            unpickler = pickle.Unpickler(file)
            dico = unpickler.load()
        file.close()
        try:
            self.startBattle(dico["width"] , dico["height"], dico["botList"] )
        except Exception:
            print Exception
        
    def startBattle(self, width, height, botList):
        self.scene = Graph(self,  width,  height)
        self.graphicsView.setScene(self.scene)
        self.scene.AddRobots(botList)
        self.timer = QTimer()
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
        Slot documentation goes here.
        """
        self.battleMenu = Battle(self)
        self.battleMenu.show()
    
    @pyqtSignature("")
    def on_actionNew_2_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionOpen_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def resizeEvent(self, evt=None):
        try:
            self.graphicsView.fitInView(self.scene.sceneRect(), 4)
        except :
            pass

        
