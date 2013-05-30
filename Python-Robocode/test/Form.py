# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

from PyQt4.QtGui import QWidget, QGraphicsScene
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtGui
from Ui_Form import Ui_Form
from untitled import Form2

class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        pg = Form2()
        pg.resize(250, 250)
        self.p = self.scene.addWidget(pg)
        self.p.setPos(100, 100)
        
