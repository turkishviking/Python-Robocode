#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math as m


class Tracker(Robot): #Create a Robot
    
    def init(self):# NECESARY FOR THE GAME   To initialyse your robot
        global size
        
        #Set the bot color in RGB
        self.setColor(200, 0, 0)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(0, 200, 100)
        
        #get the map size
        size = self.getMapSize() #get the map size
        self.radarVisible(True) # show the radarField
        self.setRadarField("normal")       
    
    def run(self): #NECESARY FOR THE GAME  main loop to command the bot
        self.radarTurn(90)
#        self.move(10)
#        self.stop()
        
    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        
        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate
        
        angle_gun = self.getGunHeading() #Returns the direction that the robot's gun is facing
        angle = self.getHeading() #Returns the direction that the robot is facing
        angle_radar = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        list = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        for robot in list:
            id = robot["id"]
            name = robot["name"]
            # each element of the list is a dictionnary with the bot's id and the bot's name
        
    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(100)
        self.move(-100)
        self.rPrint('ouch! a wall !')
        self.setRadarField("normal") #Change the radar field form
    
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.rPrint('collision with:' + str(robotName)) #Print information in the robotMenu (click on the righ panel to see it)
       
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.rPrint ("hit by " + str(bulletBotName) + "with power:" +str( bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))
        
    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        self.pause(10) #wait 10 frames
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")
    
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate
        x_op=botPos.x()
        y_op=botPos.y()
        angle_gun = self.getGunHeading() #Returns the direction that the robot's gun is facing
        angle = self.getHeading() #Returns the direction that the robot is facing
        angle_radar = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        distance=m.sqrt((x-x_op)**2+(y-y_op)**2)
        self.rPrint("distance="+str(distance))
        #Adaptative firepower
        if distance <=150:
            puissance=10
        elif distance >700:
            puissance=1
        else:
            puissance=int(-9/600.*(distance-100)+10)
        self.rPrint("puissance="+str(puissance))
        if x>x_op and y!=0:
            bearing=90+m.atan((y_op-y)/(x_op-x))*180/m.pi
        elif x<x_op and y!=0:
            bearing=-90+m.atan((y_op-y)/(x_op-x))*180/m.pi
        else:
            self.fire(puissance)
        if distance >= 150:
            n=1
            self.setRadarField("thin")
            self.radarTurn(-5)
#            self.radarTurn(bearing-angle)
        else:
            n=2
            self.setRadarField("normal")
        self.turn(bearing-angle+n*45)
        self.move(10)
        self.gunTurn(bearing-angle_gun)
        self.fire(puissance)