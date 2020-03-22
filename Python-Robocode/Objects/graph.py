#! /usr/bin/python
#-*- coding: utf-8 -*-

from PyQt4.QtGui import QGraphicsScene,  QMessageBox,  QBrush, QColor, QPixmap, QGraphicsRectItem
from PyQt4.QtCore import SIGNAL,  QPointF
from PyQt4 import QtCore,  Qt
from robot import Robot
import time,  os,  random
from outPrint import outPrint

class Graph(QGraphicsScene):
    
    def __init__(self,  parent, width,  height):
        QGraphicsScene.__init__(self,  parent)
        self.setSceneRect(0, 0, width, height)
        self.Parent = parent
        
        #self.Parent.graphicsView.centerOn(250, 250)
        self.width = width
        self.height = height
        self.grid = self.getGrid()
        self.setTiles()

        
    def AddRobots(self, botList):
        
        """
        """
        self.aliveBots = []
        self.deadBots = []
        try:
            posList = random.sample(self.grid, len(botList))
            for bot in botList:
                try:
                    robot = bot(self.sceneRect().size(), self, str(bot))
                    self.aliveBots.append(robot)
                    self.addItem(robot)
                    robot.setPos(posList.pop())
                    self.Parent.addRobotInfo(robot)
                except Exception as e:
                    print("Problem with bot file '%s': %s" % (bot, str(e)))
            self.Parent.battleMenu.close()
        except ValueError:
            QMessageBox.about(self.Parent, "Alert", "Too many Bots for the map's size!")
        except AttributeError:
            pass

    def  battleFinished(self):
        print("battle terminated")
        try:
            self.deadBots.append(self.aliveBots[0])
            self.removeItem(self.aliveBots[0])
        except IndexError:
            pass
        j = len(self.deadBots)
        
        
        for i in range(j):
            print("N°",  j - i , ":", (self.deadBots[i]))
            if j-i == 1: #first place
                self.Parent.statisticDico[repr(self.deadBots[i])].first += 1
            if j-i == 2: #2nd place
                self.Parent.statisticDico[repr(self.deadBots[i])].second += 1
            if j-i ==3:#3rd place
                self.Parent.statisticDico[repr(self.deadBots[i])].third += 1
                
            self.Parent.statisticDico[repr(self.deadBots[i])].points += i
                
        self.Parent.chooseAction()       

                    
    def setTiles(self):
        #background
        brush = QBrush()
        pix = QPixmap(os.getcwd() + "/robotImages/tile.png")
        brush.setTexture(pix)
        brush.setStyle(24)
        self.setBackgroundBrush(brush)
        
        #wall
        #left
        left = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileVert.png")
        left.setRect(QtCore.QRectF(0, 0, pix.width(), self.height))
        brush.setTexture(pix)
        brush.setStyle(24)
        left.setBrush(brush)
        left.name = 'left'
        self.addItem(left)
        #right
        right = QGraphicsRectItem()
        right.setRect(self.width - pix.width(), 0, pix.width(), self.height)
        right.setBrush(brush)
        right.name = 'right'
        self.addItem(right)
        #top
        top = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        top.setRect(QtCore.QRectF(0, 0, self.width, pix.height()))
        brush.setTexture(pix)
        brush.setStyle(24)
        top.setBrush(brush)
        top.name = 'top'
        self.addItem(top)
        #bottom
        bottom = QGraphicsRectItem()
        bottom.setRect(0 ,self.height - pix.height() , self.width, pix.height())
        bottom.setBrush(brush)
        bottom.name = 'bottom'
        self.addItem(bottom)
        
    def getGrid(self):
        w = int(self.width/80)
        h = int(self.height/80)
        l = []
        for i in range(w):
            for j in range(h):
                l.append(QtCore.QPointF((i+0.5)*80, (j+0.5)*80))
        return l
