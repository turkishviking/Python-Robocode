#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt4.QtGui import QGraphicsScene,  QWidget,  QTransform
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore,  Qt
from PyQt4 import QtGui
import os
from physics import physics
import math
from bullet import Bullet

class Robot(QtGui.QGraphicsItemGroup):
    
    def __init__(self,  mapSize, parent):
        QtGui.QGraphicsItemGroup.__init__(self)
        #Attributes
        self.mapSize = mapSize
        self.physics = physics()
        self.parent = parent
        
        self.maskColor = QtGui.QColor(0, 255, 255)
        self.gunMaskColor = QtGui.QColor(0, 255, 255)
        self.radarMaskColor = QtGui.QColor(0, 255, 255)
        
        #load img
        self.base = QtGui.QGraphicsPixmapItem()
        self.base.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/baseGrey.png")
        self.base.setPixmap(self.base.pixmap)
        self.addToGroup(self.base)
        self.baseWidth = self.base.boundingRect().width()
        self.baseHeight = self.base.boundingRect().height()
        
        #load gun img
        self.gun = QtGui.QGraphicsPixmapItem()
        self.gun.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/gunGrey.png")
        self.gun.setPixmap(self.gun.pixmap)
        self.addToGroup(self.gun)
        self.gunWidth = self.gun.boundingRect().width()
        self.gunHeight = self.gun.boundingRect().height()
        #gun position
        x = self.base.boundingRect().center().x()
        y = self.base.boundingRect().center().y()
        self.gun.setPos(x - self.gunWidth/2.0 ,  y - self.gunHeight /2.0)
        
        #load radar img
        self.radar = QtGui.QGraphicsPixmapItem()
        self.radar.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/radar.png")
        self.radar.setPixmap(self.radar.pixmap)
        self.addToGroup(self.radar)
        self.radarWidth = self.radar.boundingRect().width()
        self.radarHeight = self.radar.boundingRect().height()
        #radar position
        self.radar.setPos(x - self.radarWidth/2.0 ,  y - self.radarHeight /2.0)
        
        #Set the bot color in RGB
        self.setColour(0, 200, 100)
        self.setGunColour(0, 200, 100)
        self.setRadarColour(0, 200, 100)
        self.setBulletsColor(0, 200, 100)
        
        #set the Origin point for Transformation:
        #base
        x = self.baseWidth/2
        y = self.baseHeight/2
        self.base.setTransformOriginPoint(x, y)
        #gun
        x = self.gunWidth/2
        y = self.gunHeight /2
        self.gun.setTransformOriginPoint(x, y)
        #radar
        x = self.radarWidth/2
        y = self.radarHeight /2
        self.radar.setTransformOriginPoint(x, y)
        self.items = set([self.base, self.gun, self.radar])
        self.init()
        self.base.setRotation(300)

        
    def advance(self, i):

        if not i:
            return
        
        if self.physics.canMove():
            self.run()
            self.physics.reverse()
        else:
            try:
                dx, dy= self.getTranslation(self.physics.move.pop())
                self.setPos(dx, dy)
            except:
                pass
            try:
                angle = self.getRotation(self.physics.turn.pop())
                self.base.setRotation(angle)
            except:
                pass
        
        for item in set(self.collidingItems(1)) - self.items:
            if isinstance(item, QtGui.QGraphicsRectItem):
                print "aille le mur"
            elif isinstance(item, Robot):
                print 'aille le robot'
            elif isinstance(item, Bullet):
                print 'aille le bullet'
        
        
     ### THESE ARE THE FUNCTIONS ACCESSABLE FROM OUTSIDE ###   
     
    def setGunDirection(self, direction):
        self.gun.setRotation(direction)
     
    def fire(self, power):
        
        pos = self.pos()
        angle = self.gun.rotation()
        
        #to find the initial position
        x = pos.x() + self.baseWidth/2
        y = pos.y() + self.baseHeight/2
        dx = - math.sin(math.radians(angle))*self.gunWidth/2
        dy = math.cos(math.radians(angle))*self.gunHeight/2
        pos.setX(x+dx)
        pos.setY(y+dy)
        
        color = self.bulletColor
        bot = self
        
        bullet = Bullet(pos, color, bot, angle, power, self.parent)
        self.items.add(bullet)
        self.parent.addItem(bullet)
         
     
    def move(self, distance):
        s = 1
        if distance < 0:
            s = -1
        steps = s*distance/self.physics.step
        for i in range(steps):
            self.physics.move.append(s*self.physics.step)
                
    def turn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = s*angle/self.physics.step
        for i in range(steps):
            self.physics.turn.append(s*self.physics.step)
            
    def setColour(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.base.pixmap.createMaskFromColor(self.maskColor,  1)
        p = QtGui.QPainter(self.base.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.base.pixmap.rect(), mask, mask.rect())
        p.end()
        self.base.setPixmap(self.base.pixmap)
        self.maskColor = QtGui.QColor(r, g, b)
        
    def setGunColour(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.gun.pixmap.createMaskFromColor(self.gunMaskColor,  1)
        p = QtGui.QPainter(self.gun.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.gun.pixmap.rect(), mask, mask.rect())
        p.end()
        self.gun.setPixmap(self.gun.pixmap)
        self.gunMaskColor = QtGui.QColor(r, g, b)
        
    def setRadarColour(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.radar.pixmap.createMaskFromColor(self.radarMaskColor,  1)
        p = QtGui.QPainter(self.radar.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.radar.pixmap.rect(), mask, mask.rect())
        p.end()
        self.radar.setPixmap(self.radar.pixmap)
        self.radarMaskColor = QtGui.QColor(r, g, b)
        
    def setBulletsColor(self, r, g, b):
        self.bulletColor = QtGui.QColor(r, g, b)
        
    def getMapSize(self):
        return self.mapSize
            
    ###end of functions accessable from robot###
            
    def getTranslation(self, step):
        angle = self.base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = - math.sin(math.radians(angle))*step
        dy = math.cos(math.radians(angle))*step
        return x+dx, y+dy
        
    def getRotation(self, alpha):
        return self.base.rotation() + alpha
            
    
