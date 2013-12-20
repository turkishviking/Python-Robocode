# -*- coding: utf-8 -*-

"""
Module implementing outPrint.
"""

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature,  SIGNAL

from Ui_outPrint import Ui_Form

class outPrint(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        
    def add(self, msg):
        self.textEdit.append(msg)
