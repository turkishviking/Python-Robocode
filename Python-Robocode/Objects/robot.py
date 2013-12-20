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

import time

class Robot(QtGui.QGraphicsItemGroup):
    
    def __init__(self,  mapSize, parent, repr):
        QtGui.QGraphicsItemGroup.__init__(self)
        #Attributes
        self.__mapSize = mapSize
        self.__parent = parent
        self.__health = 100
        self.__repr = repr
        self.__gunLock = "free"
        self.__radarLock = "Free"
        

        
        #animation
        self.__runAnimation = animation("run")
        self.__targetAnimation = animation("target")
        self.__physics = physics(self.__runAnimation)
        
        
        #graphics
        self.maskColor = QtGui.QColor(0, 255, 255)
        self.gunMaskColor = QtGui.QColor(0, 255, 255)
        self.radarMaskColor = QtGui.QColor(0, 255, 255)
        
        #load img
        self.__base = QtGui.QGraphicsPixmapItem()
        self.__base.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/baseGrey.png")
        self.__base.setPixmap(self.__base.pixmap)
        self.addToGroup(self.__base)
        self.__baseWidth = self.__base.boundingRect().width()
        self.__baseHeight = self.__base.boundingRect().height()
        
        #load gun img
        self.__gun = QtGui.QGraphicsPixmapItem()
        self.__gun.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/gunGrey.png")
        self.__gun.setPixmap(self.__gun.pixmap)
        self.addToGroup(self.__gun)
        self.__gunWidth = self.__gun.boundingRect().width()
        self.__gunHeight = self.__gun.boundingRect().height()
        #gun position
        x = self.__base.boundingRect().center().x()
        y = self.__base.boundingRect().center().y()
        self.__gun.setPos(x - self.__gunWidth/2.0 ,  y - self.__gunHeight /2.0)
        
        #load radar img
        self.__radar = QtGui.QGraphicsPixmapItem()
        self.__radar.pixmap = QtGui.QPixmap(os.getcwd() + "/robotImages/radar.png")
        self.__radar.setPixmap(self.__radar.pixmap)
        self.addToGroup(self.__radar)
        self.__radarWidth = self.__radar.boundingRect().width()
        self.__radarHeight = self.__radar.boundingRect().height()
        #radar position
        self.__radar.setPos(x - self.__radarWidth/2.0 ,  y - self.__radarHeight /2.0)
        
        #load radarField
        firstPoint = QtCore.QPointF(x - self.__radarWidth/2, y)
        secondPoint = QtCore.QPointF(x + self.__radarWidth/2, y)
        thirdPoint = QtCore.QPointF(x + 4*self.__radarWidth, y + 700)
        fourthPoint = QtCore.QPointF(x - 4*self.__radarWidth, y+ 700)
        qPointListe = []
        qPointListe.append(firstPoint)
        qPointListe.append(secondPoint)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__radarField = radarField(qPointListe, self, "poly")
        
        #__largeRadarField
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        thirdPoint = QtCore.QPointF(x + 10*self.__radarWidth, y + 400)
        fourthPoint = QtCore.QPointF(x - 10*self.__radarWidth, y+ 400)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__largeRadarField = radarField(qPointListe, self, "poly")
        
        #thinRadarField
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        thirdPoint = QtCore.QPointF(x + 0.4*self.__radarWidth, y + 900)
        fourthPoint = QtCore.QPointF(x - 0.4*self.__radarWidth, y+ 900)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__thinRadarField = radarField(qPointListe, self, "poly")
        
        #roundRadarField
        self.__roundRadarField = radarField([0, 0, 300, 300], self, "round")
        self.addToGroup(self.__roundRadarField)
        self.__roundRadarField.setPos(x - self.__roundRadarField.boundingRect().width()/2.0 ,  y - self.__roundRadarField.boundingRect().height() /2.0)
        
        #add to group
        self.addToGroup(self.__radarField)
        self.addToGroup(self.__largeRadarField)
        self.addToGroup(self.__thinRadarField)
        
        self.__largeRadarField.hide()
        self.__thinRadarField.hide()
        self.__roundRadarField.hide()
        

        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(0, 200, 100)
        self.setRadarColor(0, 200, 100)
        self.setBulletsColor(0, 200, 100)
        
        #set the Origin point for Transformation:
        #radarField
        self.__radarField.setTransformOriginPoint(x, y)
        self.__largeRadarField.setTransformOriginPoint(x, y)
        self.__thinRadarField.setTransformOriginPoint(x, y)
        #base
        x = self.__baseWidth/2
        y = self.__baseHeight/2
        self.__base.setTransformOriginPoint(x, y)
        #gun
        x = self.__gunWidth/2
        y = self.__gunHeight /2
        self.__gun.setTransformOriginPoint(x, y)
        #radar
        x = self.__radarWidth/2
        y = self.__radarHeight /2
        self.__radar.setTransformOriginPoint(x, y)

        
        #add self items in items to avoid collisions
        self.__items = set([self, self.__base, self.__gun, self.__radar, self.__radarField, self.__largeRadarField, self.__thinRadarField, self.__roundRadarField])
        
        #init the subclassed Bot
        self.init()
        
        self.__currentAnimation = []
        
        #self.a = time.time()

        
    def advance(self, i):
        """
        if i ==1:
            print time.time() - self.a
            self.a = time.time()
        """
        if self.__health <= 0:
            self.__death()
        
        if self.__currentAnimation == []:
            try:
                self.__currentAnimation  = self.__physics.animation.list.pop()

            except IndexError:
                if self.__physics.animation.name == "target":
                    try:
                        self.__physics.animation = self.__runAnimation
                        self.__currentAnimation  = self.__physics.animation.list.pop()
                    except IndexError:
                        pass
                else:
                    self.stop()
                    self.run()
                    self.__physics.reverse()
                    try:
                        self.__currentAnimation  = self.__physics.animation.list.pop()
                    except:
                        pass
                    
        if i ==1:
            try:
                command = self.__currentAnimation.pop() #load animation

                #translation
                dx, dy= self.__getTranslation(command["move"])
                self.setPos(dx, dy)
                #rotation
                angle = self.__getRotation(command["turn"])
                self.__base.setRotation(angle)
                if self.__gunLock.lower() == 'base':
                    self.__gun.setRotation(angle)
                if self.__radarLock.lower() == 'base':
                    self.__setRadarRotation(angle)
                #gun Rotation
                angle = self.__getGunRotation(command["gunTurn"])
                self.__gun.setRotation(angle)
                if self.__radarLock.lower() == 'gun':
                    self.__setRadarRotation(angle)
                #radar Rotation
                angle = self.__getRadarRotation(command["radarTurn"])
                self.__setRadarRotation(angle)
                #asynchronous fire
                if command["fire"] != 0:
                    self.makeBullet(command["fire"] )
            except:
                pass
            
        else:
            
            self.sensors()
                
                
            #collisions
            for item in set(self.__base.collidingItems(1)) - self.__items:
                if isinstance(item, QtGui.QGraphicsRectItem):
                    #wall Collision
                    self.__wallRebound(item)
                elif isinstance(item, Robot):
                    if item.__base.collidesWithItem(self.__base):
                        #robot Collision
                        self.__robotRebound(item)
                elif isinstance(item, Bullet):
                    #bullet colision
                    self.__bulletRebound(item)
                elif isinstance(item, radarField):
                    if item.robot.__physics.animation.name != "target":
                        #targetSpotted
                        self.__targetSeen(item)
        
     ### THESE ARE THE FUNCTIONS ACCESSABLE FROM OUTSIDE ###   
     
     #-----------------------------------------------------------Gun------------------------------------------------------
    def gunTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s*angle/self.__physics.step)
        a = angle%self.__physics.step
        if a != 0:
            self.__physics.gunTurn.append(s*a)
        for i in range(steps):
            self.__physics.gunTurn.append(s*self.__physics.step)
            
    def lockGun(self, part):
        self.__gunLock = part
         
    def setGunColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.__gun.pixmap.createMaskFromColor(self.gunMaskColor,  1)
        p = QtGui.QPainter(self.__gun.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.__gun.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__gun.setPixmap(self.__gun.pixmap)
        self.gunMaskColor = QtGui.QColor(r, g, b)
        
    #----------------------------------------------------------Base-----------------------------------------------------
        
    def move(self, distance):
        s = 1
        if distance < 0:
            s = -1
        steps = s*distance/self.__physics.step
        d = distance%self.__physics.step
        if d != 0:
            self.__physics.move.append(s*d)
        for i in range(steps):
            self.__physics.move.append(s*self.__physics.step)
                
    def turn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s*angle/self.__physics.step)
        a = angle%self.__physics.step
        if a != 0:
            self.__physics.turn.append(s*a)
        for i in range(steps):
            self.__physics.turn.append(s*self.__physics.step)
            
    def setColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.__base.pixmap.createMaskFromColor(self.maskColor,  1)
        p = QtGui.QPainter(self.__base.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.__base.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__base.setPixmap(self.__base.pixmap)
        self.maskColor = QtGui.QColor(r, g, b)
        
    #---------------------------------------------RADAR------------------------------------------------
    
    def setRadarField(self, form):
        if form.lower() == "normal":
            self.__radarField.show()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()     
        if form.lower() == "large":
            self.__radarField.hide()
            self.__largeRadarField.show()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()       
        if form.lower() == "thin":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.show()
            self.__roundRadarField.hide()
        if form.lower() == "round":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.show()
        
        
    def lockRadar(self, part):
        self.__radarLock = part
        
    def radarTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s*angle/self.__physics.step)
        a = angle%self.__physics.step
        if a != 0:
            self.__physics.radarTurn.append(s*a)
        for i in range(steps):
            self.__physics.radarTurn.append(s*self.__physics.step)
        
    def setRadarColor(self, r, g, b):
        color = QtGui.QColor(r, g, b)
        mask = self.__radar.pixmap.createMaskFromColor(self.radarMaskColor,  1)
        p = QtGui.QPainter(self.__radar.pixmap)
        p.setPen(QtGui.QColor(r, g, b))
        p.drawPixmap(self.__radar.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__radar.setPixmap(self.__radar.pixmap)
        self.radarMaskColor = QtGui.QColor(r, g, b)
        
    def radarVisible(self, bol):
        self.__radarField.setVisible(bol)
        self.__roundRadarField.setVisible(bol)
        self.__thinRadarField.setVisible(bol)
        self.__largeRadarField.setVisible(bol)
        
    #------------------------------------------------Bullets---------------------------------------
        
    def fire(self, power):
        #asynchronous fire
        self.stop()
        bullet = Bullet(power, self.bulletColor, self)
        self.__physics.fire.append(bullet)
        self.__items.add(bullet)
        self.__parent.addItem(bullet)
        bullet.hide()
        return id(bullet)

    def makeBullet(self, bullet):
        bullet.show()
        pos = self.pos()
        angle = self.__gun.rotation()
        #to find the initial position
        x = pos.x() + self.__baseWidth/2.0
        y = pos.y() + self.__baseHeight/2.0
        dx =  - math.sin(math.radians(angle))*self.__gunWidth/2.0
        dy = math.cos(math.radians(angle))*self.__gunHeight/2.0
        pos.setX(x+dx)
        pos.setY(y+dy)
        bot = self
        bullet.init(pos, angle, self.__parent)

        self.__changeHealth(self, -bullet.power) 
        return id(bullet)
        
    def setBulletsColor(self, r, g, b):
        self.bulletColor = QtGui.QColor(r, g, b)
        
    #---------------------------------------General Methods---------------------------------------
    def stop(self):
        self.__physics.newAnimation()
        
    def getMapSize(self):
        return self.__mapSize
            
    def getPosition(self):
        p = self.pos()
        r = self.__base.boundingRect()
        return QtCore.QPointF(p.x() + r.width()/2, p.y()+r.height()/2)
        
    def getGunHeading(self):
        angle = self.__gun.rotation()
        if angle > 360:
            a = int(angle) / 360
            angle = angle - (360*a)
        return angle
        
    def getHeading(self):
        return self.__base.rotation()
        
    def getRadarHeading(self):
        return self.__gun.rotation()
        
    def reset(self):
        self.__physics.reset()
        self.__currentAnimation = []
        
    def getEnemiesLeft(self):
        l = []
        for bot in self.__parent.aliveBots:
            dic = {"id":id(bot), "name":bot.__repr__()}
            l.append(dic)
        return l
        
    def rPrint(self, msg):
        self.info.out.add(str(msg))
        
    def pause(self, duration):
        self.stop()
        for i in range(int(duration)):
            self.__physics.move.append(0)
        self.stop()
    ###end of functions accessable from outside###
            
    # Calculus & Private Methods
    def __getTranslation(self, step):
        angle = self.__base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = - math.sin(math.radians(angle))*step
        dy = math.cos(math.radians(angle))*step
        #print dx, dy
        return x+dx, y+dy
        
    def __setRadarRotation(self, angle):
        self.__radar.setRotation(angle)
        self.__radarField.setRotation(angle)
        self.__largeRadarField.setRotation(angle)
        self.__thinRadarField.setRotation(angle)
        
    def __getRotation(self, alpha):
        return self.__base.rotation() + alpha
        
    def __getGunRotation(self, alpha):
        return self.__gun.rotation() + alpha
        
    def __getRadarRotation(self,  alpha):
        return self.__radar.rotation() + alpha
    
    def __wallRebound(self, item):
        self.reset()
        if item.name == 'left':
            x = self.__physics.step*1.1
            y = 0
        elif item.name == 'right':
            x = - self.__physics.step*1.1
            y = 0
        elif item.name == 'top':
            x = 0
            y = self.__physics.step*1.1
        elif item.name == 'bottom':
            x = 0
            y = - self.__physics.step*1.1
        self.setPos(self.pos().x() + x, self.pos().y() + y)
        self.__changeHealth(self,  -1)
        self.stop()
        self.onHitWall()
        animation = self.__physics.makeAnimation()
        if animation != []:
            self.__currentAnimation = animation
        
       
        
    def __robotRebound(self, robot):
        self.reset()
        robot.reset()
        angle = self.__base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = - math.sin(math.radians(angle))*self.__physics.step*1.1
        dy = math.cos(math.radians(angle))*self.__physics.step*1.1
        self.setPos(x-dx, y-dy)
        pos = robot.pos()
        x = pos.x()
        y = pos.y()
        robot.setPos(x+dx, y+dy)
        self.__changeHealth(robot,  -1)
        self.__changeHealth(self,  -1)
        self.stop()
        self.onRobotHit(id(robot), robot.__repr__())
        animation = self.__physics.makeAnimation()
        if animation != []:
            self.__currentAnimation = animation
        robot.stop()
        robot.onHitByRobot(id(self), self.__repr__())
        animation = robot.__physics.makeAnimation()
        if animation != []:
            robot.__currentAnimation = animation

        
        
    def __bulletRebound(self, bullet):
        self.__changeHealth(self,  - 3*bullet.power)
        try:
            if bullet.robot in self.__parent.aliveBots:
                self.__changeHealth(bullet.robot,   2*bullet.power)
            self.stop()
            self.onHitByBullet(id(bullet.robot), bullet.robot.__repr__(), bullet.power)
            animation = self.__physics.makeAnimation()
            if animation != []:
                self.__currentAnimation = animation
            bullet.robot.stop()
            bullet.robot.onBulletHit(id(self), id(bullet))
            animation = bullet.robot.__physics.makeAnimation()
            if animation != []:
                bullet.robot.__currentAnimation = animation
            self.__parent.removeItem(bullet)
        except:
            pass
        
 
    def __targetSeen(self, target):
        self.stop()
        anim = target.robot.__currentAnimation
        target.robot.__physics.animation = target.robot.__targetAnimation
        target.robot.__physics.reset()
        target.robot.onTargetSpotted(id(self), self.__repr__(), self.getPosition())
        target.robot.__physics.newAnimation()
        target.robot.__physics.reverse()
        try:
            target.robot.__currentAnimation  = target.robot.__physics.animation.list.pop()
        except:
            target.robot.__physics.animation = target.robot.__runAnimation
            target.robot.__currentAnimation =  anim

        
    def __changeHealth(self, bot, value):
        if bot.__health + value>=100:
            bot.__health = 100
        else:
            bot.__health = bot.__health + value
        try:
            bot.progressBar.setValue(bot.__health)
        except:
            pass
            
    def removeMyProtectedItem(self, item):
        self.__items.remove(item)

    def __death(self):
        
        try:
            self.icon.setIcon(QtGui.QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.icon2.setIcon(QtGui.QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.progressBar.setValue(0)
        except :
            pass
        self.__parent.deadBots.append(self)
        self.__parent.aliveBots.remove(self)
        self.onRobotDeath()
        self.__parent.removeItem(self)
        if  len(self.__parent.aliveBots) <= 1:
            self.__parent.battleFinished()
            
    def __repr__(self):
        repr = self.__repr.split(".")
        return repr[1].replace("'>", "")
