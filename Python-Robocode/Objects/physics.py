#! /usr/bin/python
#-*- coding: utf-8 -*-


class physics():
    
    def __init__(self):
        
        self.move = []
        self.turn = []
        
        self.gunTurn = []
        
        self.radarTurn = []
        
        self.step = 5

    def canMove(self):
        if self.move == [] and self.turn == []:
            return True
        else:
            return False
            
    def reverse(self):
        self.move.reverse()
        self.turn.reverse()
        self.gunTurn.reverse()
        self.radarTurn.reverse()       
                          
