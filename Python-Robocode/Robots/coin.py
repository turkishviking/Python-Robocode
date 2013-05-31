#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math

class Camper(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(250, 10, 20)
        self.setGunColor(0, 0, 0)
        self.setRadarColor(200, 100, 0)
        self.setBulletsColor(100, 150, 250)
        
        self.radarvisible(True) # if True the radar field is visible
        
        #get the map size
        size = self.getMapSize()
        
        self.lockRadar("gun")
        self.inTheCorner = False
        

    
    def run(self): #main loop to command the bot
        
        pos = self.getPosition()
        if pos.x() > 50 or pos.y() > 50:
            angle = self.getHeading()
            a = 90 + math.degrees(math.acos(pos.x()/math.sqrt(pos.x()**2+pos.y()**2)))
            if angle < a:
                self.turn(a-angle)
            elif angle > a:
                self.turn(angle-a)
            self.stop()
            self.move(10)
            self.stop()
        else:
            angle = self.getGunHeading()
            if angle < 315:
                self.gunTurn(315 - angle)
            elif angle > 315:
                self.gunTurn(angle-315)
            self.inTheCorner = True

    def onHitWall(self):
        pass

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId):
        pass
        
    def onHitByRobot(self):
        pass

    def onHitByBullet(self, bulletBotId, bulletPower): 
        pass
        
    def onBulletHit(self, botId, bulletId):
        pass
        
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botPos):
        self.gunTurn(5)
        self.stop()
        if self.inTheCorner:
            pos = self.getPosition()
            angle = self.getGunHeading()
            a = 270+math.degrees(math.acos(pos.x()/math.sqrt(pos.x()**2+pos.y()**2)))
            if angle < a:
                self.gunTurn(angle-a)
            elif angle > a:
                
                self.gunTurn(a - angle)
            self.fire(5)
           
