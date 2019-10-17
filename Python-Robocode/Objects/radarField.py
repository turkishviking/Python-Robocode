#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPolygonF, QColor, QBrush, QPen


class radarField(QGraphicsItemGroup):
    
    def __init__(self, qPointList, bot, rType):
        QGraphicsItemGroup.__init__(self)
        self.rType = rType
        if rType == "poly":
            self.item = QGraphicsPolygonItem()
            self.robot = bot
            self.polygon = QPolygonF(qPointList)
            self.item.setPolygon(self.polygon)

        elif rType == "round":
            self.item = QGraphicsEllipseItem()
            self.robot = bot
            self.item.setRect(qPointList[0], qPointList[1],qPointList[2],qPointList[3])

        color = QColor(255, 100, 6, 10)
        brush = QBrush(color)
        pen = QPen(color)
        self.item.setBrush(brush)
        self.item.setPen(pen)
        self.addToGroup(self.item)
            
            
    def setVisible(self, bol):
        if bol:
            color = QColor(255, 100, 6, 15)
        else:
            color = QColor(255, 100, 6, 0)
        brush = QBrush(color)
        pen = QPen(color)
        self.item.setBrush(brush)
        self.item.setPen(pen)
    
        
        
