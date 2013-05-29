#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot

class Charlier(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(255, 150, 150)
        
        #get the map size
        size = self.getMapSize()
        
    
    def run(self): #main loop to command the bot
        
        #self.move(90) # for moving (negative values go back)
        #self.stop()
        self.gunTurn(180)
        self.stop()
        self.turn(90) #for turning (negative values turn counter-clockwise)
        self.move(90)
        self.stop()
        #self.setGunDirection(40) # set the Gun direction (bottom = 0°)

        
