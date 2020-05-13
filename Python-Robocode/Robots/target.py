#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math

class Target(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(255, 0, 0)
        self.setGunColor(255, 0, 0)
        self.setRadarColor(255, 0, 0)
        self.setBulletsColor(255, 0, 0)
        
        self.radarVisible(True) # if True the radar field is visible
        
        #get the map size
        size = self.getMapSize()
        
        self.lockRadar("gun")
        self.setRadarField("thin")
        self.inTheCorner = False
        

    
    def run(self): #main loop to command the bot
        # angle=self.getHeading() % 360
        # print ("going angle:",angle)
        # self.move(5)
        pass

    def onHitWall(self):
        pass

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        pass
        
    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        pass
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        pass
        
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        pass
