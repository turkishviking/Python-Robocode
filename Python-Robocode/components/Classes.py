import pygame, math


class BlastC:
    
    x = None
    y = None
    movex = None
    movey = None
    hit = None
    robot = None
    image = pygame.image.load("robotImages/blast.png")
    name = "DEFAULTOWNDERNAME"
    power = 10     
    w = 10
    h = 10
        
class RobotC:
    x = 0
    y = 0
    health = 82
    maxhealth = 82
    currDirec = 0
    newDirec = 0

    VARhealth = 100
    
    BASEImage = None
    BASErect = None
    
    GUNimage = None
    GUNrect = None
    GUNcurrDirec = 0
    GUNnewDirec = 0
    GUNimage = None
    
    RADARrect = None
    RADARcurrDirec = 0
    RADARnewDirec = 0
    RADARlock = "FREE"
    RADARspin = "RIGHT"
    
    name = "DEFAULTNAME"
    movex = 0
    movey = 0
    smallImage = None
    alive = True
    ticksLeft = 0
    command = "DEFAULTCOMMAND"
    ticksSinceShot = 0
    moveLock = "GO"
    currentCommand = 0
    lastCommand = -1
    
    frameSinceDam = 0
    colourStore = (100,100,100)
    imageStore = []
    turningDir = "RIGHT"
    roboModule = None
    def toString(self):
        return "name: {0} position: {1},{2} health: {3}, command: {4}".format(self.name,math.floor(self.x),math.floor(self.y),self.health,self.command)
    
class DeadRobotC:
    x = 0
    y = 0
    image = None
    name = "DEFAULTDEADNAME"
    smallImage = None
