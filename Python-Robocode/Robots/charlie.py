#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot

class Charlie(Robot): #Create a Robot
    
    def init(self):# NECESARY FOR THE GAME   To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(0, 200, 100)
        
        #get the map size
        size = self.getMapSize()
        
    
    def run(self): #NECESARY FOR THE GAME  main loop to command the bot
        
        
        self.move(90) # for moving (negative values go back)
        self.turn(360) #for turning (negative values turn counter-clockwise)
        self.stop()
        """
        the stop command is used to make moving sequences: here the robot will move 90steps and turn 360° at the same time
        """
        
        #self.setGunDirection(40) # set the Gun direction (bottom = 0°)
        
        self.fire(3) # To Fire (power between 1 and 10)
        
        self.move(100)
        self.turn(50)
        self.stop()
        bulletId = self.fire(2) #to let you you manage if the bullet hit or fail
        self.move(180)
        self.turn(180)
        self.gunTurn(90) #to turn the gun (negative values turn counter-clockwise)
        self.stop()
        self.fire(1) # To Fire (power between 1 and 10)
        self.radarTurn(180) #to turn the radar (negative values turn counter-clockwise)
        self.stop()
        
    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        
        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate
        
        angle = self.getGunHeading() #Returns the direction that the robot's gun is facing
        angle = self.getHeading() #Returns the direction that the robot is facing
        angle = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        
    def onHitByRobot(self):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(100)
        self.move(-100)
        self.rPrint('ouch! a wall !')
    
    def onRobotHit(self, robotId): # when My bot hit another
        self.rPrint('collision with:' + str(robotId))
       
    def onHitByBullet(self, bulletBotId, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.rPrint ("hit by " + str(bulletBotId) + "with power:" +str( bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))
        self.pause(30) #block the robot for 30 frames
        
    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")
    
    def onTargetSpotted(self, botId, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))
        self.fire(5)
    
