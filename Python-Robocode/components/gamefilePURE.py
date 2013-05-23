import pygame, sys, copy, pickle
from Classes import *
sys.path.append(sys.path[0] + "/robots")

import %importrobotshere

robotmodules = %putrobotnameshere

RATIO = (len(robotmodules)-1)



#import libraries
import sys, pygame,random, string, math

#initiate the pygame library
pygame.init()
clock = pygame.time.Clock()

#top,left,bottom,right
battleboundary = top,left,bottom,right = 51,0,466,556

global cuurentRobot
currentRobot = None
#Robots = []

RobotsAlive = 0
Blasts = []


#Fonts
pygame.font.NameFont= pygame.font.SysFont("Tahoma", 11, bold=False, italic=False)
pygame.font.WinFont= pygame.font.SysFont("Tahoma", 24, bold=True, italic=False)
Arena = ""



def ScreenSetUp(ArenaName):
    Arena = "arenas/" + ArenaName+"/"
    #Set up the screen
    size = width, height = 700, 500 #Set the size as a tuple with width and height
    screen = pygame.display.set_mode(size, pygame.RESIZABLE) #Sets the screen display size
    pygame.display.set_caption('Robocode: A-Team') #Sets window Title
    pygame.display.flip()     #Refreshes Screen
    Menu(screen,width,height,Arena) #Sample function Call
    #You will notice the initial screen gets passed to every function
    #This is nessecary unless you define the screen outside a function to begin with.



### THESE ARE THE FUNCTIONS ACCESSABLE FROM OUTSIDE ####

def turn_right(deg):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)):
        currentRobot.command = "TURN RIGHT"
        currentRobot.turningDir = "RIGHT"
        turn(True,currentRobot,deg)
        THISchangecommand(currentRobot)
    currentRobot.currentCommand = currentRobot.currentCommand + 1
    
        
def turn_left(deg):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)):
        currentRobot.command = "TURN LEFT"
        currentRobot.turningDir = "LEFT"
        turn(True,currentRobot,-deg)
        THISchangecommand(currentRobot)
    currentRobot.currentCommand = currentRobot.currentCommand + 1
        
def move(distance):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)) and (currentRobot.ticksLeft < 1):
        currentRobot.command = "MOVE "
        THISmove(True,currentRobot,distance,[])
        THISchangecommand(currentRobot)
    currentRobot.currentCommand = currentRobot.currentCommand + 1

def pointgun(direction):
        currentRobot.command = currentRobot.command + " AIM "
        THISgunspin(True,currentRobot,direction)

def lockradar(where):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)):
        if (where == "FREE") or (where == "free"):
           currentRobot.RADARlock = "FREE"
        if (where == "GUN") or (where == "gun"):
            currentRobot.RADARlock = "GUN"
        if (where == "BASE") or (where == "base"):
            currentRobot.RADARlock = "BASE"
        currentRobot.command = currentRobot.command + " lockRADAR to " + where
        THISchangecommand(currentRobot)
    currentRobot.currentCommand = currentRobot.currentCommand + 1

def spinradar(LEFTorRIGHT):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)):
        currentRobot.command = currentRobot.command + " SPINRADAR " + LEFTorRIGHT
        currentRobot.RADARspin = LEFTorRIGHT
        THISchangecommand(currentRobot)
    currentRobot.currentCommand = currentRobot.currentCommand + 1


def stop(ticks):
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)) and (currentRobot.ticksLeft < 1):
        currentRobot.command = "STOP "
        currentRobot.moveLock = "STOP"
        currentRobot.ticksLeft = ticks
        THISchangecommand(currentRobot)

    currentRobot.currentCommand = currentRobot.currentCommand + 1

def done():
    if (currentRobot.currentCommand == (currentRobot.lastCommand + 1)):
        currentRobot.command = "DONE"
        currentRobot.lastCommand = -1
        currentRobot.VARhealth = int(currentRobot.health)

def fire(powB):
    if currentRobot.ticksSinceShot > 50:
        currentRobot.command = currentRobot.command + " FIRE "
        currentRobot.ticksSinceShot = 0
        THISfire(currentRobot, powB)
        
def robotHealth():
	return currentRobot.VARhealth
    
def robotX():
        return currentRobot.x
    
def robotY():
        return currentRobot.y
    
def nbr_bots_left():
    global RobotsAlive
    return RobotsAlive

###end of functions accessable from robot####
        
def THISchangecommand(robot):
    robot.lastCommand = robot.currentCommand
    #this function switches the robot's store of the position of the last successful command to the current command
    

    

def ThreeSixtyFix(value):
	#this function should ensure that angles are always between 0 and 360
    if (value > 360):
        value = value - 360
    if (value < 0):
        value = value + 360
    return value
        

def THISfire(robot, powB):
    #fire takes in the robot and
    #this is similar to the code for determining where the robot is pointing, which works.
    #it does tell where the arm of the robot is pointing and store the right movex movey values
    bmovex = math.sin(math.radians(((-robot.currDirec)+robot.GUNcurrDirec)))
    bmovey = math.cos(math.radians(((-robot.currDirec)+robot.GUNcurrDirec)))
    #this makes the blast come from roughly the middle of the robot
    bx = robot.x-15+(robot.GUNrect.width/2)
    by = robot.y-15+(robot.GUNrect.height/2)
    bx = bx + bmovex*25
    by = by + bmovey*25
    #loads the blast image
    #and adds the blast to the blast list also multiplies the move values by 3 so the blasts go faster 	than the robot
    blast = BlastC()
    blast.x = bx
    blast.y = by
    blast.movex = bmovex*3/RATIO
    blast.movey = bmovey*3/RATIO
    blast.w = blast.image.get_width()/RATIO
    blast.h = blast.image.get_height()/RATIO
    blast.image = pygame.transform.scale(blast.image, (blast.w, blast.h))
    blast.robot = robot
    #blast.power = robot.shotPower
    if powB > 10:
        blast.power = 10
    elif powB <= 0:
        blast.power = 0.1
    else:
        blast.power = powB
    robot.health = robot.health - blast.power
        
    blast.name = robot.name
    blast.hit = False
    Blasts.append(blast)


    

def turn(change,robot,deg):
    if (change == True):
        robot.newDirec = robot.currDirec + deg

    robot.newDirec = ThreeSixtyFix(robot.newDirec)
    robot.currDirec = ThreeSixtyFix(robot.currDirec)
        

    if (robot.turningDir == "RIGHT"):
        if (robot.newDirec != robot.currDirec):
            robot.currDirec = robot.currDirec + 1
    if (robot.turningDir == "LEFT"):
        if (robot.newDirec != robot.currDirec):
            robot.currDirec = robot.currDirec - 1
        
        
    robot.movex = math.sin(-math.radians(robot.currDirec))/RATIO #for speed 
    robot.movey = math.cos(-math.radians(robot.currDirec))/RATIO

def THISmove(change,robot,distance, Robots):
    if (change == True):
        robot.ticksLeft = distance
        robot.moveLock = "GO"
    if (((robot.x+robot.movex) > left) and (robot.x+robot.movex+46 < right) and ((robot.y+robot.movey) >top and (robot.y+robot.movey+46 < bottom))):
        #if the robot's next move doesn't take it out of the battlefield then it can move
        robot.ticksLeft = robot.ticksLeft
    else:
        #if it would have taken it out of the battlefield then stop this movement
        robot.ticksLeft = 0

    myRect = robot.BASErect.move(robot.x+robot.movex,robot.y+robot.movey)
    for otherRobot in Robots:
        otherRobotRect = otherRobot.BASErect.move(otherRobot.x,otherRobot.y)
        if (myRect.colliderect(otherRobotRect) and otherRobot.name != robot.name):
            robot.ticksLeft = 0
            
    if iverammed(robot,Robots):
        robot.ticksLeft = 0

    if (robot.ticksLeft > 0):       
        robot.x = robot.x+robot.movex #add movex to the current x value
        robot.y = robot.y+robot.movey #add movey to the current y value


def THISgunspin(change,robot,direction):
    if (change == True):
        robot.GUNnewDirec = direction
    if (robot.GUNnewDirec > robot.GUNcurrDirec):
        robot.GUNcurrDirec = robot.GUNcurrDirec + 1
    if(robot.GUNnewDirec < robot.GUNcurrDirec):
        robot.GUNcurrDirec = robot.GUNcurrDirec - 1

def THISradarspin(robot):
    if (robot.RADARlock == "FREE"):
        if (robot.RADARspin == "RIGHT"):
            robot.RADARnewDirec = robot.RADARcurrDirec + 2
        if (robot.RADARspin == "LEFT"):
            robot.RADARnewDirec = robot.RADARcurrDirec - 2
    if (robot.RADARlock == "GUN"):
        robot.RADARnewDirec = robot.GUNcurrDirec
    if (robot.RADARlock == "BASE"):
        robot.RADARnewDirec = robot.currDirec
        
    robot.RADARcurrDirec = robot.RADARnewDirec
    robot.RADARcurrDirec = ThreeSixtyFix(robot.RADARcurrDirec)

        
            
        
def blastCheck(robot,Blasts):
    for blast in Blasts:
        #checks against the list of active blasts to see if any occupy the same space as it does
        #the first part of this if statement is to make sure that robots own blasts don't hurt them.
        #second is to check if the blast is within the rect of the robot
        if (not(blast.name.endswith(robot.name))):
            if (((blast.x) > robot.x) and (blast.x+blast.w < robot.x+robot.w) and ((blast.y) >robot.y and (blast.y+blast.h < robot.y+robot.h))):
                #decrease health
                    robot.health = robot.health - blast.power
                    if blast.robot.health + blast.power < 82:
                       blast.robot.health = blast.robot.health + blast.power
                    else:
                       blast.robot.health = 82
                    #set frames since last damage to 0
                    robot.frameSinceDam = 0
                    #tell the blast it's hit something
                    blast.hit = True
                    try:
                        robot.roboModule.on_hit_by_bullet(blast.power, blast.name)
                    except AttributeError:
                        pass
        
        
        
        

def iverammed(thisrobot, Robots):
    #takes in thisrobot (the robot that's doing the ramming and runs it's "ram point" against the list of robots in the field
    rampointx = 0
    rampointy = 0
    radius = (thisrobot.BASErect.height)/2
        
    rampointx = (thisrobot.x+radius)+(thisrobot.movex*(radius+1))
    rampointy = (thisrobot.y+radius)+(thisrobot.movey*(radius+1))
    #screen.blit(pygame.image.load('blast.png'),(rampointx-5,rampointy-5)) debug code
    for robot in Robots:
        #moves the newly created robotrect to its current position and then uses a inbuilt pygame function to test if the rampoint is in it 
        robotRect = robot.BASErect.move(robot.x,robot.y)
        if (robotRect.collidepoint(rampointx,rampointy)):
            #if the robot isn't this robot and it is alive
            if (robot != thisrobot) and (robot.alive):
                #if it's not been damaged in the last 2ish frames (which would be this ramming)
                if robot.frameSinceDam > 2:
                    #then damage it
                    robot.health=robot.health-10
                #set it's frames since last damage to 0 (even if it hasn't been damaged, I don't like this.)
                robot.frameSinceDam=0
                #return true if the robot is ramming another robot
                return True
        return False;
    


def isfreetomove():
    if (currentRobot.ticksLeft < 0):
        return True
    else:
        return False
        
def setCurrentRobot(robot, Robots):
    i = 0
    while Robots[i].name != robot.name:
        i = i + 1
    global currentRobot
    currentRobot = Robots[i]
    
        
        
    
def sweep(thisrobot, Robots):
    #sets the sweep to happen in the area between -46 deg of the direction the radar is pointing
    sweepstart = thisrobot.RADARcurrDirec-16
    #and +46 of that direction
    sweepend = thisrobot.RADARcurrDirec+16
    #sets the number of "legs" / steps within those legs (like a spider)
    sweepstep = 10
    #set the length of the legs
    sweeplength = 280
    #code to workout where the radar should come from (which is currently set as the outside of the robot rather than where the radar is)
    radius = (thisrobot.BASErect.height)/2
    radarbasex = (thisrobot.x+radius)+(thisrobot.movex*(radius+1))
    radarbasey = (thisrobot.y+radius)+(thisrobot.movey*(radius+1))
    sweep = sweepstart
    while sweep < sweepend:
        #reset the stepping of the legsweep
        legsweep = 0
        #calculate the movex and movey of the new angle
        rmovex = math.sin(math.radians(((-thisrobot.currDirec)+sweep)))
        rmovey = math.cos(math.radians(((-thisrobot.currDirec)+sweep)))
        while legsweep < sweeplength:
            #hop the point along the line
            radarpointx = radarbasex + (rmovex*legsweep)
            radarpointy = radarbasey + (rmovey*legsweep)
            #this code shows the radar
            #screen.blit(pygame.image.load('blip.png'),(radarpointx-5,radarpointy-5))
            for robot in Robots:
                #uses the inbuilt pygame collide function to calculate the robot's Rect
                robotRect = robot.BASErect.move(robot.x,robot.y)
                #if the radar point is within the Rect of the robot and the robot isn't the robot that "fired" this radar
                if (robotRect.collidepoint(radarpointx,radarpointy)) and (robot != thisrobot):
                    #return the angle we were at when we found something, this bit will change to store details about the robot that's been scanned
                    return sweep, robot.name, robot.x, robot.y;
                
            legsweep = legsweep + sweepstep
        sweep = sweep + sweepstep
            
    return False,False,False,False;

  
    
def Menu(screen,width,height,Arena):
    global RobotsAlive
    RobotsAlive = 0
    def GameOver(Robots):
        def ReplayBattle(screen):
            print "replay"

        def RestartBattle(screen):
            print "restart"

        def MainMenu(screen):
            import setup
            setup.ScreenSetUp()
            Exit(screen)

        def ChangeType(screen):
            import setup
            setup.BattleTypeMenu(screen)
            Exit(screen)

        def ChangeArena(screen):
            import setup
            setup.ArenaMenu(screen,"Free4All")
            Exit(screen)

        def Statistics(screen):
            
            import setup
            setup.HallOfFame(screen)
            Exit(screen)

        
    	menuimage = pygame.image.load("menuImages/GameOver.jpg") #Load in an image
        overlay = pygame.image.load("menuImages/GameOverOptions.png") #Load in an image
    	screen.blit(menuimage,(0,0)) #Place your image
    	screen.blit(overlay,(0,0)) #Place your image
    	pygame.display.flip()     #Refreshes Screen

    	while 1 :
        	#Pygame.event.get() takes in input from the user
        	#It records keyboard input and mouse clicks on the window
        
        	for event in pygame.event.get():
            	#If the user hits the X button on the window
            		if event.type == pygame.QUIT:
                		Exit(screen)
            		if event.type == pygame.KEYDOWN:
                		if event.key == pygame.K_RETURN:
                    			MainMenu(screen)
            		mouseButtons = pygame.mouse.get_pressed()
            		if mouseButtons == (1,0,0):
                		mouseX,mouseY = pygame.mouse.get_pos()
                		if (mouseX>541 and mouseX<685 and mouseY>454 and mouseY<483):
                    			Exit(screen)
                    		if (mouseX>365 and mouseX<509 and mouseY>454 and mouseY<483):
                    			Statistics(screen)
                    		if (mouseX>189 and mouseX<333 and mouseY>454 and mouseY<483):
                    			MainMenu(screen)
                    		if (mouseX>13 and mouseX<157 and mouseY>454 and mouseY<483):
                    			RestartBattle(screen)
                    		if (mouseX>80 and mouseX<224 and mouseY>416 and mouseY<445):
                    			ReplayBattle(screen)
                    		if (mouseX>265 and mouseX<409 and mouseY>416 and mouseY<445):
                    			ChangeArena(screen)
                    		if (mouseX>447 and mouseX<591 and mouseY>416 and mouseY<445):
                    			ChangeType(screen)
        	screen.blit(menuimage,(0,0))
		counter = 0
        	for robot in Robots:
			robotName = pygame.font.WinFont.render("#"+str((counter+1))+" "+str(robot.name), True, (255,255,255))
			screen.blit(robotName,(100,(95+(25*counter))))
			counter = counter+1
		screen.blit(overlay,(0,0)) #Place your image
        	pygame.display.flip()     #Refreshes Screen
        	

    def createRobot(botX,botY,module,colourChooser,direction):
        robot = RobotC()
        imageStore = ["robotImages/baseGrey.png","robotImages/gunGrey.png","robotImages/radar.png","robotImages/smallgrey.png"]
        botName = (str(module).rsplit(" "))
        botName = botName[1][1:-1]
        robot.name = botName
        robot.x = botX
        robot.y = botY
        robot.health = 82 #Starts at 87 due to 87px size health bar
        robot.maxhealth = 82
        robot.newDirec = direction
        robot.movex = 0
        robot.movey = 1
        #colourChooser = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
        base = pygame.image.load(imageStore[0])
	changedColor = pygame.PixelArray(base)
	changedColor.replace((0,255,255),colourChooser,0.02,(0.299,0.587,0.114))
	
	robot.BASEimage = base = changedColor.make_surface()
	#scaling
        robot.w = robot.BASEimage.get_width()/RATIO
        robot.h = robot.BASEimage.get_height()/RATIO
        base = pygame.transform.scale(robot.BASEimage.copy(), (robot.w, robot.h))
        robot.BASEimage = base
        robot.BASErect = base.get_rect()
        
        robot.GUNimage = gun = pygame.image.load(imageStore[1])
        
        #scaling
        robot.gw = robot.GUNimage.get_width()/RATIO
        robot.gh = robot.GUNimage.get_height()/RATIO
        gun = pygame.transform.scale(robot.GUNimage.copy(), (robot.gw, robot.gh))
        robot.GUNimage = gun
        robot.GUNrect = gun.get_rect()
        
        robot.RADARimage = radar = pygame.image.load(imageStore[2])
        
        #scaling
        robot.rw = robot.RADARimage.get_width()/RATIO
        robot.rh = robot.RADARimage.get_height()/RATIO
        radar = pygame.transform.scale(robot.RADARimage.copy(), (robot.rw, robot.rh))
        robot.RADARimage = radar 
        robot.RADARrect = radar.get_rect()
        
	changedColor = pygame.PixelArray(gun)
	changedColor.replace((0,255,255),colourChooser,0.02,(0.299,0.587,0.114))
	robot.GUNimage = changedColor.make_surface()

	robot.colourStore = colourChooser
	
	
        robot.name = botName
        smallImage = pygame.image.load(imageStore[3])
	changedColor = pygame.PixelArray(smallImage)
	changedColor.replace((60,60,60),colourChooser,0.05,(0.299,0.587,0.114))
	
	robot.smallImage = smallImage = changedColor.make_surface()
        
        robot.imageStore = [colourChooser,base,gun,radar,smallImage]
        robot.roboModule = module
        
        return robot
    

        
        


        
    #Display the menu and control it
    Robots = []
    #Blasts = []
    DeadRobots = []
    f = open(Arena+'config.txt', 'r')
    rgb = f.readline()
    rgb = rgb.split(",")
    ArenaFontColor = (int(rgb[0][1:]),int(rgb[1]),int(rgb[2][:-2]))
    menuimage = pygame.image.load(Arena+'bg.jpg') #Load in an image
    healthBarBG = pygame.image.load(Arena+"healthBar.png")
    separator = pygame.image.load(Arena+"seperator.png")
    screen.blit(menuimage,(0,0)) #Place your image

    lowrange = 0
    step = (500/len(robotmodules))-40
    highrange = step
    
    
    
    for robot in robotmodules:
        
        RobotsAlive += 1
        colour = robot.colour()
        direction = 0
        if (hasattr(robot,"startDirection")):
            direction = robot.startDirection()
        Robots.append(createRobot(random.randrange(lowrange,highrange),random.randrange(60,400),robot,colour,direction))
        lowrange = highrange + 40
        highrange = lowrange + step
       

    #An infinite loop is the base of a python game
    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        clock.tick(600)
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
                
        screen.blit(menuimage,(0,0))

        
            
        #counter is the value of the robot (i.e robot 0 has a counter value of 0)
        counter = 0

        #pygame.time.wait(1)

        
        for deadRobot in DeadRobots:
            screen.blit(deadRobot.image,(deadRobot.x,deadRobot.y))
            #Sidebar Graphics
            #Image
            
            screen.blit(deadRobot.smallImage,(560,(466-37-(37*counter))))

            #Name
            robotName = pygame.font.NameFont.render(str(deadRobot.name), True, ArenaFontColor)
            screen.blit(robotName,(602,(466-37-(37*counter))))

            #Health Bar  - Colors are RGB values
            screen.blit(healthBarBG,(602,(466-20-(37*counter))))
                
            #Separator
            screen.blit(separator,(565,(466-37-(37*counter))))
            counter = counter+1
            
        counter = 0

        for blast in Blasts:
            #check if the blast is still within the arena
            if (((blast.x+blast.movex) > left) and (blast.x+blast.movex+7 < right) and ((blast.y+blast.movey) >top and (blast.y+blast.movey+7 < bottom))):
                blast.hit = blast.hit
            else:
                #if it's not then remove it
                blast.hit = True
            if (blast.hit == True):
                Blasts.remove(blast)
            else:
                blast.x = blast.x + blast.movex
                blast.y = blast.y + blast.movey
                screen.blit(blast.image,(blast.x-5/RATIO,blast.y-5/RATIO))
        
        
        for robot in Robots:
            if robot.alive: #If Robot is alive then deal with its movement
                robot.frameSinceDam = robot.frameSinceDam+1 #add one to time since impact
                global currentRobot
                
                setCurrentRobot(robot,Robots)
                #if counter == 1:
                #print(currentRobot.toString())
                if isfreetomove():
                    currentRobot.currentCommand = 0
                    currentRobot.roboModule.commands()
                else:
                    commandChanged = False
                    turn(commandChanged,currentRobot,0)
                    THISgunspin(commandChanged,currentRobot,0)
                    THISradarspin(currentRobot)
                    if (currentRobot.moveLock == "GO"):
                        THISmove(commandChanged,currentRobot,0,Robots)
                    robot.ticksLeft = currentRobot.ticksLeft - 1
                    
                blastCheck(currentRobot,Blasts)


                #add one to the frames since last damage
                robot.frameSinceDam = robot.frameSinceDam+1
                robot.ticksSinceShot = robot.ticksSinceShot+1
                #move the robot

                
                #fire the radar roughly once in every ten ticks
                if (random.randrange(0,10) == 1):
                    target = sweep(robot,Robots)
                    if (target[0] != False):
                        try:
                            robot.roboModule.target_spotted(target[0], target[1], target[2], target[3])
                        except AttributeError:
                            pass
                    
                

                
                ################################################################
                ################################################ FOR THE BASE
                if (robot.frameSinceDam > 7): #this changes the base image to one that looks like it's flashing for 8 frames after the robot is hit
                    image = robot.imageStore[1]
                else:
                    image = pygame.transform.scale(pygame.image.load("robotImages/baseFlash.png"), (robot.rw, robot.rh)) 
                
                robot.BASEimage = pygame.transform.rotate(image,(-robot.currDirec))
                rotated_rect = robot.BASEimage.get_rect()
                original_rect = robot.BASErect
                clipped_rect = pygame.Rect((rotated_rect.width - original_rect.width) / 2.0,(rotated_rect.height - original_rect.height) / 2.0,original_rect.width,original_rect.height,)
                try:
                    robot.BASEimage = robot.BASEimage.subsurface(clipped_rect)
                except:
                    #DO BUGGER ALL :D
                    nut = 3
                screen.blit(robot.BASEimage,(robot.x, robot.y))
                ###############################################################
                ################################################ FOR THE GUN
                if robot.GUNcurrDirec == 360:
                    robot.GUNcurrDirec = 0

                image = robot.imageStore[2]
                robot.GUNimage = pygame.transform.rotate(image,(-(robot.currDirec)+(robot.GUNcurrDirec)))
                #code found on the pygame comments
                rotated_rect = robot.GUNimage.get_rect()
                original_rect = robot.GUNrect
                try:
                    clipped_rect = pygame.Rect((rotated_rect.width - original_rect.width) / 2.0,(rotated_rect.height - original_rect.height) / 2.0,original_rect.width,original_rect.height,)
                    robot.GUNimage = robot.GUNimage.subsurface(clipped_rect)
                except ValueError:
                    #DO BUGGER ALL :D
                    nut = 3
                screen.blit(robot.GUNimage,(robot.x-15/RATIO, robot.y-15/RATIO))

                ################################################################
                ################################################ FOR THE RADAR  
                image = robot.imageStore[3]
                robot.RADARimage = pygame.transform.rotate(image,(-(robot.currDirec+robot.RADARcurrDirec)))
                rotated_rect = robot.RADARimage.get_rect()
                original_rect = robot.RADARrect
                try:
                    clipped_rect = pygame.Rect((rotated_rect.width - original_rect.width) / 2,(rotated_rect.height - original_rect.height) / 2,original_rect.width,original_rect.height,)
                    robot.RADARimage = robot.RADARimage.subsurface(clipped_rect)
                except ValueError:
                    #DO BUGGER ALL :D
                    
                    nut = 3
                screen.blit(robot.RADARimage,(robot.x,robot.y))


            else:
                if robot.frameSinceDam < 15:
                    image = "Explode/Explode1.png"
                elif robot.frameSinceDam < 30:
                    image = "Explode/Explode2.png"
                elif robot.frameSinceDam < 45:
                    image = "Explode/Explode3.png"
                elif robot.frameSinceDam < 60:
                    image = "Explode/Explode4.png"
                elif robot.frameSinceDam < 75:
                    image = "Explode/Explode5.png"
                elif robot.frameSinceDam < 90:
                    image = "Explode/Explode6.png"
                elif robot.frameSinceDam < 105:
                    image = "Explode/Explode8.png"
                elif robot.frameSinceDam < 106:
                    image = "Explode/ExplodeFinal.png"
                else:
                    image = "Explode/ExplodeFinal.png"
                    skull = pygame.image.load(Arena+"dead.png")
                    changedColor = pygame.PixelArray(skull)
                    changedColor.replace((188,186,186),robot.colourStore,0.2,(0.299,0.587,0.114))
                    skull = changedColor.make_surface()
                    deadRobot = DeadRobotC()
                    deadRobot.x = robot.x-5
                    deadRobot.y = robot.y-2
                    deadRobot.image = pygame.transform.rotate(pygame.image.load(image),(-robot.currDirec))
                    deadRobot.name = robot.name
                    deadRobot.smallImage = skull
                    DeadRobots.insert(0,deadRobot)
                    try:
                        robot.roboModule.on_death()
                    except AttributeError:
                        pass
                    Robots.remove(robot)
                    
                    RobotsAlive -= 1
                    
                    if len(Robots) == 1:
                        try:
                            Robots[0].roboModule.on_death()
                        except AttributeError:
                            pass
                        deadRobot = DeadRobotC()
                        deadRobot.x = Robots[0].x
                        deadRobot.y = Robots[0].y
                        deadRobot.image = pygame.transform.rotate(pygame.image.load(image),(-Robots[0].currDirec))
                        deadRobot.name = Robots[0].name
                        deadRobot.smallImage = skull
                        DeadRobots.insert(0,deadRobot)
                        GameOver(DeadRobots)
                

                robot.frameSinceDam = robot.frameSinceDam + 1
 

                robot.BASEimage = pygame.transform.rotate(pygame.image.load(image),(-robot.currDirec))
                rotated_rect = robot.BASEimage.get_rect()
                original_rect = robot.BASErect
                clipped_rect = pygame.Rect((rotated_rect.width - original_rect.width) / 2.0,(rotated_rect.height - original_rect.height) / 2.0,original_rect.width,original_rect.height,)
                try:
                    robot.BASEimage = robot.BASEimage.subsurface(clipped_rect)
                except:
                    #DO BUGGER ALL :D
                    nut = 3
                screen.blit(robot.BASEimage,(robot.x, robot.y))



            if robot.health<=0: #If robot has no health it's dead
                robot.alive = False

            #Sidebar Graphics
            #Image
            screen.blit(robot.smallImage,(560,(53+(37*counter))))

            #Name
            robotName = pygame.font.NameFont.render(str(robot.name), True, ArenaFontColor)
            screen.blit(robotName,(602,(54+(37*counter))))

            #Health Bar  - Colors are RGB values
            screen.blit(healthBarBG,(602,(69+(37*counter))))
            invHealth = robot.maxhealth-robot.health
            if robot.alive: #If Robot is alive then deal with it's health bar
                healthColour = (invHealth*11,255,0) # Green to Yellow
                #print healthColour
                if robot.health<60:
                    dwnHealth = (robot.health-35)
                    healthColour = (255, 165 + dwnHealth*3.6, 0) #Yellow to Orange
                if robot.health<35:
                    dwnHealth = (robot.health-18)
                    healthColour = (255,dwnHealth*9.7,0) #Orange to Red
                if robot.health<18:
                    invHealth = invHealth - (robot.maxhealth-23)
                    healthColour = (255, 0, 0) #Red
                pygame.draw.rect(screen, healthColour,(603,(70+(37*counter)),robot.health,6))
                
            #Separator
            screen.blit(separator,(565,(84+(37*counter))))
            counter = counter+1

            
        pygame.display.flip()


def Exit(screen):
    #Exit the system
    pygame.quit()
    sys.exit()
