#! /usr/bin/python
#-*- coding: utf-8 -*-



from PyQt4 import QtCore,  Qt
from PyQt4 import QtGui
import os
from physics import physics
import math
from bullet import Bullet
from radarField import radarField
from animation import animation

class Robot(QtGui.QGraphicsItemGroup):
    
    def __init__(self,  mapSize, parent, repr):
        QtGui.QGraphicsItemGroup.__init__(self)
        #Attributes
        self.mapSize = mapSize
        self.parent = parent
        self.health = 100
        self.repr = repr
        self.outMsg = []
        self.isReading = False
        self.countFrame = 0
        self.gunLock = "free"
        self.radarLock = "Free"
        self.lockTarget = True
        
        #animation
        self.runAnimation = animation("run")
        self.targetAnimation = animation("target")
        self.physics = physics(self.runAnimation)
        
        
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
        
        #load radarField
        firstPoint = QtCore.QPointF(x - self.radarWidth/2, y)
        secondPoint = QtCore.QPointF(x + self.radarWidth/2, y)
        thirdPoint = QtCore.QPointF(x + 2*self.radarWidth, y + 400)
        fourthPoint = QtCore.QPointF(x - 2*self.radarWidth, y+ 400)
        qPointListe = []
        qPointListe.append(firstPoint)
        qPointListe.append(secondPoint)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.radarField = radarField(qPointListe, self)
        self.addToGroup(self.radarField)
        self.radarFieldWidth = self.radarField.boundingRect().width()
        self.radarFieldHeight = self.radarField.boundingRect().height()
        self.setPos(x - self.radarFieldWidth/2.0 ,  y - self.radarFieldHeight /2.0)
        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(0, 200, 100)
        self.setRadarColor(0, 200, 100)
        self.setBulletsColor(0, 200, 100)
        
        #set the Origin point for Transformation:
        #radarField
        self.radarField.setTransformOriginPoint(x, y)
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
        self.items = set([self, self.base, self.gun, self.radar, self.radarField])
        
        #init the subclassed Bot
        self.init()
        
        self.currentAnimation = []
        
    def advance(self, i):
        if self.health <= 0:
            self.death()
        self.countFrame +=1
        
        if self.currentAnimation == []:
            try:
                self.currentAnimation  = self.physics.animation.list.pop()
                self.rPrint("------------------------------------")
            except IndexError:
                if self.physics.animation.name == "target":
                    try:
                        self.physics.animation = self.runAnimation
                        self.currentAnimation  = self.physics.animation.list.pop()
                    except IndexError:
                        pass
                else:
                    self.stop()
                    self.run()
                    self.rPrint("--------------RUN-----------------")
                    self.physics.reverse()
                    self.currentAnimation  = self.physics.animation.list.pop()
                    
        if i == 1:
            try:
                command = self.currentAnimation.pop() #load animation
                self.rPrint(command)
                #translation
                dx, dy= self.getTranslation(command["move"])
                self.setPos(dx, dy)
                #rotation
                angle = self.getRotation(command["turn"])
                self.base.setRotation(angle)
                if self.gunLock.lower() == 'base':
                    self.gun.setRotation(angle)
                if self.radarLock.lower() == 'base':
                    self.radar.setRotation(angle)
                #gun Rotation
                angle = self.getGunRotation(command["gunTurn"])
                self.gun.setRotation(angle)
                if self.radarLock.lower() == 'gun':
                    self.radar.setRotation(angle)
                    self.radarField.setRotation(angle)
                #radar Rotation
                angle = self.getRadarRotation(command["radarTurn"])
                self.radar.setRotation(angle)
                self.radarField.setRotation(angle)
                #asynchronous fire
                if command["fire"] != 0:
                    self.makeBullet(command["fire"] )
            except:
                pass
            
        else:
            
            self.sensors()
                
                
            #collisions
            for item in set(self.base.collidingItems(1)) - self.items:
                if isinstance(item, QtGui.QGraphicsRectItem):
                    #wall Collision
                    self.wallRebound(item)
                elif isinstance(item, Robot):
                    if item.base.collidesWithItem(self.base):
                        #robot Collision
                        self.robotRebound(item)
                elif isinstance(item, Bullet):
                    #bullet colision
                    self.bulletRebound(item)
                elif isinstance(item, radarField):
                    if item.robot.physics.animation.name != "target":
                        #targetSpotted
                        self.targetSeen(item)
        
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

        
    def lockRadar(self, part):
        self.radarLock = part
        
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
        
    def radarvisible(self, bol):
        self.radarField.setVisible(bol)
        
    #------------------------------------------------Bullets---------------------------------------
        
    def fireNow(self, power):
        bullet = Bullet(power, self.bulletColor)
        self.makeBullet(bullet)
        return id(bullet)
        
    def fire(self, power):
        #asynchronous fire
        self.stop()
        bullet = Bullet(power, self.bulletColor)
        self.physics.fire.append(bullet)
        self.items.add(bullet)
        self.parent.addItem(bullet)
        return id(bullet)

    def makeBullet(self, bullet):
        pos = self.pos()
        angle = self.gun.rotation()
        #to find the initial position
        x = pos.x() + self.baseWidth/2.0
        y = pos.y() + self.baseHeight/2.0
        dx =  - math.sin(math.radians(angle))*self.gunWidth/2.0
        dy = math.cos(math.radians(angle))*self.gunHeight/2.0
        pos.setX(x+dx)
        pos.setY(y+dy)
        bot = self
        bullet.init(pos, bot, angle, self.parent)

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
        
    def getGunHeading(self):
        return self.gun.rotation()
        
    def getHeading(self):
        return self.gun.rotation()
        
    def getRadarHeading(self):
        return self.gun.rotation()
        
    def reset(self):
        self.physics.reset()
        self.currentAnimation = []
        
    def getEnemiesLeft(self):
        return len(self.parent.aliveBots)
        
    def rPrint(self, msg):
        self.info.out.add(str(msg))
        
    def pause(self, duration):
        self.stop()
        for i in range(int(duration)):
            self.physics.move.append(0)
        self.stop()
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
        self.stop()
        self.onHitWall()
        animation = self.physics.makeAnimation()
        if animation != []:
            self.currentAnimation = animation
        
       
        
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
        self.stop()
        self.onRobotHit(id(robot))
        animation = self.physics.makeAnimation()
        if animation != []:
            self.currentAnimation = animation
        robot.stop()
        robot.onHitByRobot()
        animation = robot.physics.makeAnimation()
        if animation != []:
            robot.currentAnimation = animation

        
        
    def bulletRebound(self, bullet):
        self.changeHealth(self,  - bullet.power)
        if bullet.robot in self.parent.aliveBots:
            self.changeHealth(bullet.robot,   bullet.power)
        self.stop()
        self.onHitByBullet(id(bullet.robot), bullet.power)
        animation = self.physics.makeAnimation()
        if animation != []:
            self.currentAnimation = animation
        bullet.robot.stop()
        bullet.robot.onBulletHit(id(self), id(bullet))
        animation = bullet.robot.physics.makeAnimation()
        if animation != []:
            bullet.robot.currentAnimation = animation
        self.parent.removeItem(bullet)
        
 
    def targetSeen(self, target):
        self.stop()
        target.robot.physics.animation = target.robot.targetAnimation
        target.robot.physics.reset()
        target.robot.onTargetSpotted(id(self), self.getPosition())
        target.robot.physics.newAnimation()
        target.robot.physics.reverse()
        target.robot.currentAnimation  = target.robot.physics.animation.list.pop()
        target.robot.rPrint("---------Target Animation----------")
        
    def changeHealth(self, bot, value):
        if bot.health + value>=100:
            bot.health = 100
        else:
            bot.health = bot.health + value
        try:
            bot.progressBar.setValue(bot.health)
        except:
            pass

    def death(self):
        try:
            self.progressBar.setValue(0)
        except :
            pass
        self.parent.deadBots.append(self)
        self.parent.aliveBots.remove(self)
        self.onRobotDeath()
        self.parent.removeItem(self)
        if  len(self.parent.aliveBots) <= 1:
            self.parent.battleFinished()
            
    def __repr__(self):
        return self.repr.replace("<class '", "").replace("'>", "")
