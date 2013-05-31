# -*- coding: utf-8 -*-

"""
Module implementing RobotInfo.
"""

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature
from outPrint import outPrint
from Ui_RobotInfo import Ui_Form

class RobotInfo(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.out = outPrint()

    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        
        self.out.setWindowTitle(str(self.robot))
        self.out.show()
    
    @pyqtSignature("int")
    def on_progressBar_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        
        value -= 7
        if value <=0:
            value = 0
        if value >= 50:
            green = 255
            red = int(510 - (value*2)*2.55)
        else:
            red = 255
            green = int((value*2)*2.55)
        self.progressBar.setStyleSheet("""
        QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        height: 5px;
        }
        QProgressBar::chunk {
        background-color: rgb(""" + str(red) + "," + str(green) + """,0);
        }
        """)
        
