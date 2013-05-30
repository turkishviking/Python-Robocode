#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os

from Form import Form
from PyQt4 import QtGui


if __name__ == "__main__":

   app = QtGui.QApplication(sys.argv)
   app.setApplicationName("Python-Robocode")
   myapp = Form()
   myapp.show()
   sys.exit(app.exec_())
