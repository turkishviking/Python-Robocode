#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt4.QtGui import QGraphicsScene,  QWidget
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore,  Qt
from PyQt4 import QtGui
import os
from physics import physics
import math
from bullet import Bullet

class Robot(QtGui.QGraphicsItemGroup):
    
    def __init__(self,  mapSize, parent, repr):
        QtGui.QGraphicsItemGroup.__init__(self)
        QWidget.__init__(self)
        #Attributes
        self.mapSize = mapSize
        self.physics = physics()
        self.parent = parent
        self.health = 100
        self.repr = repr
        self.outMsg = []
        
        #graphics
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
        self.setColor(0, 200, 100)
        self.setGunColor(0, 200, 100)
        self.setRadarColor(0, 200, 100)
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
        
        #add self items in items to avoid collisions
        self.items = set([self, self.base, self.gun, self.radar])
        
        #init the subclassed Bot
        self.init()
        
        self.currentAnimation = []
        
    def advance(self, i):
        if self.health <= 0:
            self.death()
            
        if i == 1:
            
            if self.physics.animationList == []:
                self.run()
                self.physics.reverse()
                
            if self.currentAnimation == []:
                try:
                    self.currentAnimation  = self.physics.animationList.pop()
                except IndexError:
                    pass
            try:
                command = self.currentAnimation.pop() #load animation
                #translation
                dx, dy= self.getTranslation(command["move"])
                self.setPos(dx, dy)
                #rotation
                angle = self.getRotation(command["turn"])
                self.base.setRotation(angle)
                #gun Rotation
                angle = self.getGunRotation(command["gunTurn"])
                self.gun.setRotation(angle)
                #radar Rotation
                angle = self.getRadarRotation(command["radarTurn"])
                self.radar.setRotation(angle)
            except:
                pass
            
        else: #sensor
            
            self.sensors()
            
        #collisions
        for item in set(self.base.collidingItems(1)) - self.items:
            if isinstance(item, QtGui.QGraphicsRectItem):
                #wall Collision
                self.wallRebound(item)
            elif isinstance(item, Robot):
                #robot Collision
                self.robotRebound(item)
            elif isinstance(item, Bullet):
                self.bulletRebound(item)
        
     ### THESE ARE THE FUNCTIONS ACCESSABLE FROM OUTSIDE ###   
     
     #-----------------------------------------------------------Gun------------------------------------------------------
    def gunTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = s*angle/self.physics.step
        for i in range(steps):
            self.physics.gunTurn.append(s*self.physics.step)
         
    def setGunColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.gun.pixmap.createMaskFromColor(self.gunMaskColor,  1)
        p = QtGui.QPainter(self.gun.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.gun.pixmap.rect(), mask, mask.rect())
        p.end()
        self.gun.setPixmap(self.gun.pixmap)
        self.gunMaskColor = QtGui.QColor(r, g, b)
        
    #----------------------------------------------------------Base-----------------------------------------------------
        
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
            
    def setColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.base.pixmap.createMaskFromColor(self.maskColor,  1)
        p = QtGui.QPainter(self.base.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.base.pixmap.rect(), mask, mask.rect())
        p.end()
        self.base.setPixmap(self.base.pixmap)
        self.maskColor = QtGui.QColor(r, g, b)
        
    #---------------------------------------------RADAR------------------------------------------------
        
    def radarTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = s*angle/self.physics.step
        for i in range(steps):
            self.physics.radarTurn.append(s*self.physics.step)
        
    def setRadarColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.radar.pixmap.createMaskFromColor(self.radarMaskColor,  1)
        p = QtGui.QPainter(self.radar.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.radar.pixmap.rect(), mask, mask.rect())
        p.end()
        self.radar.setPixmap(self.radar.pixmap)
        self.radarMaskColor = QtGui.QColor(r, g, b)
        
    #------------------------------------------------Bullets---------------------------------------
        
    def fire(self, power):
        
        pos = self.pos()
        angle = self.gun.rotation()
        #to find the initial position
        x = pos.x() + self.baseWidth/2.0
        y = pos.y() + self.baseHeight/2.0
        dx =  - math.sin(math.radians(angle))*self.gunWidth/2.0
        dy = math.cos(math.radians(angle))*self.gunHeight/2.0
        pos.setX(x+dx)
        pos.setY(y+dy)
        
        color = self.bulletColor
        bot = self
        
        bullet = Bullet(pos, color, bot, angle, power, self.parent)
        self.items.add(bullet)
        self.parent.addItem(bullet)
        
        self.changeHealth(self, -bullet.power) 
        return id(bullet)
        
    def setBulletsColor(self, r, g, b):
        self.bulletColor = QtGui.QColor(r, g, b)
        
    #---------------------------------------General Methods---------------------------------------
    def stop(self):
        self.physics.newAnimation()
        
    def getMapSize(self):
        return self.mapSize
            
    def getPosition(self):
        p = self.pos()
        r = self.boundingRect()
        return QtCore.QPointF(p.x() + r.width()/2, p.y()+r.height()/2)
        
    def reset(self):
        self.physics.reset()
        
    def getNbrOfEnemiesLeft(self):
        return len(self.parent.aliveBots)
        
    def rPrint(self, msg):
        self.info.out.add(str(msg))
        
        
    ###end of functions accessable from robot###
            
    # Calculus
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
        
    def getGunRotation(self, alpha):
        return self.gun.rotation() + alpha
        
    def getRadarRotation(self,  alpha):
        return self.radar.rotation() + alpha
    
    def wallRebound(self, item):
        self.reset()
        if item.name == 'left':
            x = self.physics.step*1.1
            y = 0
        elif item.name == 'right':
            x = - self.physics.step*1.1
            y = 0
        elif item.name == 'top':
            x = 0
            y = self.physics.step*1.1
        elif item.name == 'bottom':
            x = 0
            y = - self.physics.step*1.1
        self.setPos(self.pos().x() + x, self.pos().y() + y)
        self.changeHealth(self,  -1)
       
        
    def robotRebound(self, robot):
        self.reset()
        robot.reset()
        angle = self.base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = - math.sin(math.radians(angle))*self.physics.step*1.1
        dy = math.cos(math.radians(angle))*self.physics.step*1.1
        self.setPos(x-dx, y-dy)
        pos = robot.pos()
        x = pos.x()
        y = pos.y()
        robot.setPos(x+dx, y+dy)
        self.changeHealth(robot,  -1)
        self.changeHealth(self,  -1)
        
    def bulletRebound(self, bullet):
        self.changeHealth(self,  - bullet.power)
        if bullet.robot in self.parent.aliveBots:
            self.changeHealth(bullet.robot,   bullet.power)
        self.onHitByBullet(id(bullet.robot), bullet.power)
        bullet.robot.onBulletHit(id(self), id(bullet))
        self.parent.removeItem(bullet)
        
    def changeHealth(self, bot, value):
        if bot.health + value>=100:
            bot.health = 100
        else:
            bot.health = bot.health + value
        
        bot.progressBar.setValue(bot.health)

    def death(self):
        self.progressBar.setValue(0)
        self.parent.deadBots.append(self)
        self.parent.aliveBots.remove(self)
        self.onRobotDeath()
        self.parent.removeItem(self)

        if  len(self.parent.aliveBots) <= 1:
            self.parent.battleFinished()
            
    def __repr__(self):
        return self.repr.replace("<class '", "").replace("'>", "")
