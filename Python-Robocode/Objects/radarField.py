#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt4 import QtCore,  Qt
from PyQt4 import QtGui



class radarField(QtGui.QGraphicsPolygonItem):
    
    def __init__(self, qPointList, bot):
        QtGui.QGraphicsPolygonItem.__init__(self)
        self.robot = bot
        self.polygon = QtGui.QPolygonF(qPointList)
        self.setPolygon(self.polygon)
        color = QtGui.QColor(255, 100, 6, 10)
        brush = QtGui.QBrush(color)
        pen = QtGui.QPen(color)
        self.setBrush(brush)
        self.setPen(pen)
        
    def setVisible(self, bol):
        if bol:
            color = QtGui.QColor(255, 100, 6, 15)
        else:
            color = QtGui.QColor(255, 100, 6, 0)
        brush = QtGui.QBrush(color)
        pen = QtGui.QPen(color)
        self.setBrush(brush)
        self.setPen(pen)
        
        
        
