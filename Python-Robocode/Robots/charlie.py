#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot

class Charlie(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(0, 200, 100)
        
        #get the map size
        size = self.getMapSize()
        
    
    def run(self): #main loop to command the bot
        
        
        #self.move(90) # for moving (negative values go back)
        #self.stop()
        
        self.turn(360) #for turning (negative values turn counter-clockwise)
        self.stop()
        #self.setGunDirection(40) # set the Gun direction (bottom = 0°)
        
        self.fire(9.2) # To Fire (power between 1 and 10)
        
        self.move(100)
        self.turn(50)
        self.stop()
        
        self.move(180)
        self.turn(180)
        self.gunTurn(90)
        self.stop()
        
        self.radarTurn(180)
        self.stop()
        
    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        
        pos = self.getPosition() #return the center of the bot
        #print pos.x(),  pos.y() 
       
