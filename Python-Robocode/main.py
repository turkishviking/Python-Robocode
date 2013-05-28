#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd() + "/GUI")
sys.path.append(os.getcwd() + "/Objects")
sys.path.append(os.getcwd() + "/robotImages")
sys.path.append(os.getcwd() + "/Robots")
from window import MainWindow
from PyQt4 import QtGui


if __name__ == "__main__":

   app = QtGui.QApplication(sys.argv)
   app.setApplicationName("Python-Robocode")
   myapp = MainWindow()
   myapp.show()
   sys.exit(app.exec_())
