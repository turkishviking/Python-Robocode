#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot

class Charlie(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColour(0, 200, 100)
        self.setGunColour(200, 200, 0)
        self.setRadarColour(255, 60, 0)
        self.setBulletsColor(255, 150, 150)
        
        #get the map size
        size = self.getMapSize()
        
    
    def run(self): #main loop to command the bot
        
        self.move(90) # for moving (negative values go back)
        
        self.turn(90) #for turning (negative values turn counter-clockwise)
        
        self.setGunDirection(90) # set the Gun direction (bottom = 0°)
        
        self.fire(9.2) # To Fire (power between 1 and 10)
        """
        self.move(100)
        
        self.turn(-50)
        
        self.setGunDirection(90)
        """
