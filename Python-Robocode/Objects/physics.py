#! /usr/bin/python
#-*- coding: utf-8 -*-



class physics():
    
    def __init__(self, animation):
        
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []
        self.animation = animation

        self.step = 5

            
    def reverse(self):
        self.animation.list.reverse()     
        
    def newAnimation(self): 
        currentList = self.makeAnimation()
        if currentList != []:
            self.animation.list.append(currentList)
            self.clearAnimation()
        
       
    def makeAnimation(self ,  a = None):
        for i in range(max(len(self.move), len(self.turn), len(self.gunTurn), len(self.radarTurn), len(self.fire) )):
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
            try:
                f = self.fire[i]
            except IndexError:
                f = 0
            self.currentList.append({"move": m, "turn": t, "gunTurn":g, "radarTurn":r, "fire":f})
        self.currentList.reverse()
        return self.currentList

    def clearAnimation(self):
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []
          
    def reset(self):
        self.clearAnimation()
        self.animation.list = []
