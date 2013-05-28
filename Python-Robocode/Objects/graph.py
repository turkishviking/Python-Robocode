#! /usr/bin/python
#-*- coding: utf-8 -*-

from PyQt4.QtGui import QGraphicsScene,  QWidget,  QCursor, QMouseEvent,  QBrush, QColor, QPixmap, QGraphicsRectItem
from PyQt4.QtCore import SIGNAL,  QPointF
from PyQt4 import QtCore,  Qt
from robot import Robot
import time,  os,  random

class Graph(QGraphicsScene):
    
    def __init__(self,  parent, width,  height):
        QGraphicsScene.__init__(self,  parent)
        self.setSceneRect(0, 0, width, height)
        self.Parent = parent
        
        #self.Parent.graphicsView.centerOn(250, 250)
        self.width = width
        self.height = height
        
        self.setTiles()

        
    def AddRobots(self, botList):
        
        """
        """
        
        for bot in botList:
            try:
                robot = bot((self.width, self.height), self)
                self.genPos(robot)
                self.addItem(robot)
                while set(robot.collidingItems()) - robot.items != set([]):
                    self.genPos(robot)
            except Exception,  e:
                print "Problem with bot file '%s': %s" % (botFile, str(e))


    def genPos(self, bot):
        
        x = random.random() * self.width
        y = random.random() * self.height
        if x < bot.baseWidth or x > self.width - bot.baseWidth:
            x = random.random() * self.width
        if y < bot.baseHeight or y > self.height - bot.baseHeight:
            y = random.random() * self.height
        bot.setPos(x, y)
       

                    
    def setTiles(self):
        #background
        brush = QBrush()
        pix = QPixmap(os.getcwd() + "/robotImages/tile.png")
        brush.setTexture(pix)
        brush.setStyle(24)
        self.setBackgroundBrush(brush)
        
        #wall
        #left
        left = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileVert.png")
        left.setRect(QtCore.QRectF(0, 0, pix.width(), self.height))
        brush.setTexture(pix)
        brush.setStyle(24)
        left.setBrush(brush)
        self.addItem(left)
        #right
        right = QGraphicsRectItem()
        right.setRect(self.width - pix.width(), 0, pix.width(), self.height)
        right.setBrush(brush)
        self.addItem(right)
        #top
        top = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        top.setRect(QtCore.QRectF(0, 0, self.width, pix.height()))
        brush.setTexture(pix)
        brush.setStyle(24)
        top.setBrush(brush)
        self.addItem(top)
        #bottom
        bottom = QGraphicsRectItem()
        bottom.setRect(0 ,self.height - pix.height() , self.width, pix.height())
        bottom.setBrush(brush)
        self.addItem(bottom)
        
        
