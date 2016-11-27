#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt4.QtGui import QGraphicsPixmapItem
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore,  Qt
from PyQt4 import QtGui
import os
import math

class Bullet(QGraphicsPixmapItem):
    
    def __init__(self, power, color, bot):
        QGraphicsPixmapItem.__init__(self)
        #graphics
        self.maskColor = QtGui.QColor(255, 128, 0)
        self.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/blast.png")
        self.setPixmap(self.pixmap)
        self.setColour(color)
        self.isfired = False
        #physics
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        if power <=0.5:
            power = 0.5
        elif power >= 10:
            power = 10
        self.power = power
        bsize = power
        if power < 3:
            bsize = 4
        self.pixmap = self.pixmap.scaled(bsize, bsize)
        self.setPixmap(self.pixmap)
        self.robot = bot
        
    def init(self, pos, angle, scene):

        self.angle = angle
        self.setPos(pos)
        self.scene = scene
        self.isfired = True

        
    def setColour(self, color):
        mask = self.pixmap.createMaskFromColor(self.maskColor,  1)
        p = QtGui.QPainter(self.pixmap)
        p.setPen(color)
        p.drawPixmap(self.pixmap.rect(), mask, mask.rect())
        p.end()
        self.setPixmap(self.pixmap)
        self.maskColor = color
        
    def advance(self, i):
        if self.isfired:
            
            pos = self.pos()
            x = pos.x()
            y = pos.y()
            dx = - math.sin(math.radians(self.angle))*10.0
            dy = math.cos(math.radians(self.angle))*10.0
            self.setPos(x+dx, y+dy)
            if x < 0 or y < 0 or x > self.scene.width or y > self.scene.height:
                self.robot.onBulletMiss(id(self))
                self.scene.removeItem(self)
                self.robot.removeMyProtectedItem(self)

        
            
            
            
            
            
            
            
