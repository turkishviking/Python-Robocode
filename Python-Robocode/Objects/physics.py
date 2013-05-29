#! /usr/bin/python
#-*- coding: utf-8 -*-


class physics():
    
    def __init__(self):
        
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        
        self.animation = []
        self.animationList = []
        
        self.step = 10

            
    def reverse(self):
        self.animationList.reverse()     
        
    def newAnimation(self):
        
        self.makeAnimation()
        self.animation.reverse()
        self.animationList.append(self.animation)
        self.clearAnimation()
       
    def makeAnimation(self):
        for i in range(max(len(self.move), len(self.turn), len(self.gunTurn), len(self.radarTurn) )):
            try:
                m = self.move[i]
            except IndexError:
                m = 0
            try:
                t = self.turn[i]
            except IndexError:
                t = 0
            try:
                g = self.gunTurn[i]
            except IndexError:
                g = 0
            try:
                r = self.radarTurn[i]
            except IndexError:
                r = 0
            self.animation.append({"move": m, "turn": t, "gunTurn":g, "radarTurn":r})

            
    def clearAnimation(self):
        self.move = []
        self.turn = []
        self.animation = []
          
