import sys, pygame,random, string, math, os
sys.path.append(sys.path[0] + "/robots")

#initiate the pygame library
pygame.init()

#Fonts
pygame.font.NameFont= pygame.font.SysFont("Tahoma", 16, bold=True, italic=False)
pygame.font.RobotNameFont= pygame.font.SysFont("Tahoma", 48, bold=True, italic=False)
pygame.font.StatsFont= pygame.font.SysFont("Tahoma", 18, bold=True, italic=False)

def ScreenSetUp():
    #Set up the screen
    size = width, height = 700, 500 #Set the size as a tuple with width and height
    screen = pygame.display.set_mode(size) #Sets the screen display size
    pygame.display.set_caption('Python Bots') #Sets window Title
    pygame.display.flip()     #Refreshes Screen
    MainMenu(screen) #Sample function Call
    #You will notice the initial screen gets passed to every function
    #This is nessecary unless you define the screen outside a function to begin with.

def MainMenu(screen):
    menuimage = pygame.image.load('menuImages/TeamEditor.jpg') #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen

    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
                    
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>76 and mouseX<255 and mouseY>160 and mouseY<209):
                    NewTeam(screen)
                if (mouseX>77 and mouseX<254 and mouseY>221 and mouseY<258):
                    EditTeam(screen)
                if (mouseX>77 and mouseX<254 and mouseY>260 and mouseY<302):
                    CopyTeam(screen)
                if (mouseX>76 and mouseX<254 and mouseY>309 and mouseY<350):
                    Return(screen)
        screen.blit(menuimage,(0,0))
        pygame.display.flip()     #Refreshes Screen

def NewTeam(screen):
    botSelect(screen,"new")

def EditTeam(screen):
    teamSelect(screen,"edit")

def CopyTeam(screen):
    teamSelect(screen,"copy")

def parseForColour(filename):
    roboFile = file(filename)
    foundcolour = False
    for line in roboFile:
        if (foundcolour):
            newline = line.strip()
            newline = newline.lstrip("return")
            newline = newline.strip()
            newtuple = tuple(map(int,newline[1:-1].split(',')))
            return newtuple
        if line.startswith("def colour"):
            foundcolour = True
    return (0,0,0)

def parseForRobots(filename):
    roboFile = file("teams/"+ filename)
    foundcolour = False
    bots = []
    for line in roboFile:
        if (foundcolour):
            newline = line.strip()
            newline = newline.lstrip("return")
            bots = newline.strip()
            return bots
        if line.startswith("def robots"):
            foundcolour = True
    return []
    

def botSelect(screen,action):
    menuimage = pygame.image.load('menuImages/BotSelected.jpg') #Load in an image
    robotSelectedImage = pygame.image.load('menuImages/botSelected.png') #Load in an image
    robotTargettedImage = pygame.image.load('menuImages/botTargetted.png') #Load in an image
    allimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    randomimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    hideimage = pygame.image.load('menuImages/startBattleHider.jpg') #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    screen.blit(hideimage,(541,452)) #Place your image
    pygame.display.flip()     #Refreshes Screen
    Robots = []
    SelectedRobots = []
    x = 15
    y= 273
    for filename in os.listdir("robots"): #Code for displaying robot .py files
        if filename[-3:] == ".py" and filename != ".svn":
            #Name
            robotName = pygame.font.RobotNameFont.render(str(filename[:-3]), True, (255,255, 255))
            colour = parseForColour("robots/"+filename)
            Robots.append([filename,robotName,x,y,False,colour,False])
            x = x+42
            if x>658:
                x = 18
                y = y+41
    Robots[0][6]=True
    current = 0
            
    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Robots[current][6] = False
                    current = current-1
                    if current<0:
                        current = len(Robots)-1
                    Robots[current][6] = True
                        
                if event.key == pygame.K_RIGHT:
                    Robots[current][6] = False
                    current = current+1
                    if current>len(Robots)-1:
                        current = 0
                    Robots[current][6] = True

                if event.key == pygame.K_UP:
                    Robots[current][6] = False
                    current = current-16
                    if current<0:
                        current = (int((len(Robots)-1)/16)*16)+(current-(int((current/16))*16))
                        if current> (len(Robots)-1):
                            current = len(Robots)-1
                    Robots[current][6] = True
                        
                if event.key == pygame.K_DOWN:
                    Robots[current][6] = False
                    current = current+16
                    if current>len(Robots)-1:
                        current = 0+(current-(int((current/16))*16))
                    Robots[current][6] = True

                if event.key == pygame.K_BACKSPACE:#Back
                    ScreenSetUp()
                    
                if event.key == pygame.K_RETURN:#Start Editor
                    StartEditor(screen,Robots[current])

                
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>11 and mouseX<155 and mouseY>452 and mouseY<482):#Back Button
                    ScreenSetUp()

                counter=0   
                for robot in Robots:
                    if (mouseX>robot[2] and mouseX<(robot[2]+39) and mouseY>robot[3] and mouseY<(robot[3]+39)):
                        if robot[6]:
                            StartEditor(screen,Robots[current])
                        else:
                            for trobot in Robots:
                                if trobot[6]:
                                    trobot[6]=False
                            robot[6]=True
                            current = counter
                    counter = counter+1

        screen.blit(menuimage,(0,0))
        screen.blit(hideimage,(541,452)) #Place your image
        for robot in Robots:
            if robot[6]:
                target = robot
        largeimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
        changedColor = pygame.PixelArray(largeimage)
        changedColor.replace((195,29,29),target[5],0.11,(0.299,0.587,0.114))
        robotImage = changedColor.make_surface()
        screen.blit(robotImage,(23,63)) #Place your image
        screen.blit(target[1],(223,63)) #Place your image
        counter = 0
        scounter = 0
        for robot in Robots:
            if robot[0]!="all" and robot[0]!="random":
                smallimage = pygame.image.load('menuImages/botImage.png') #Load in an image
                changedColor = pygame.PixelArray(smallimage)
                changedColor.replace((195,29,29),robot[5],0.1,(0.299,0.587,0.114))
                robotImage = changedColor.make_surface()
                screen.blit(robotImage,(robot[2],robot[3])) #Place your image
                if robot[4]:
                    screen.blit(robotSelectedImage,(robot[2]-1,robot[3]-1)) #Place your image
        screen.blit(robotTargettedImage,(target[2]-1,target[3]-1)) #Place your image
        pygame.display.flip()     #Refreshes Screen

def Return(screen):
    import setup
    setup.ScreenSetUp()
    Exit(screen)

def StartEditor(screen,robot):
    roboname = ""
    roboname = robot[0] #this code can be hashed back in to provide an argument
    #the following code will only work on unix systems,
    #we will need a switch case for windows
    os.system("python2.6 RobotEditor.py "+roboname+" &")
    print "Start the Editor"

def Exit(screen):
    #Exit the system
    pygame.quit()
    sys.exit()

def teamSelect(screen,action):
    menuimage = pygame.image.load('menuImages/BotSelected.jpg') #Load in an image
    robotSelectedImage = pygame.image.load('menuImages/botSelected.png') #Load in an image
    robotTargettedImage = pygame.image.load('menuImages/botTargetted.png') #Load in an image
    allimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    randomimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    hideimage = pygame.image.load('menuImages/startBattleHider.jpg') #Load in an image
    screen.blit(menuimage,(0,0))
    screen.blit(hideimage,(541,452))#Place your image
    pygame.display.flip()     #Refreshes Screen
    Robots = []
    SelectedRobots = []
    x = 15
    y= 273
    bots = []
    for filename in os.listdir("teams"): #Code for displaying robot .py files
        if filename[-3:] == ".py" and filename != ".svn":
            #Name
            robotName = pygame.font.RobotNameFont.render(str(filename[:-3]), True, (255,255, 255))
            colour = parseForColour("teams/"+filename)
            bots = parseForRobots(filename)
            Robots.append([filename,robotName,x,y,False,colour,False,bots])
            x = x+42
            if x>658:
                x = 18
                y = y+41
    Robots[0][6]=True
    current = 0
            
    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Robots[current][6] = False
                    current = current-1
                    if current<0:
                        current = len(Robots)-1
                    Robots[current][6] = True
                        
                if event.key == pygame.K_RIGHT:
                    Robots[current][6] = False
                    current = current+1
                    if current>len(Robots)-1:
                        current = 0
                    Robots[current][6] = True

                if event.key == pygame.K_UP:
                    Robots[current][6] = False
                    current = current-16
                    if current<0:
                        current = (int((len(Robots)-1)/16)*16)+(current-(int((current/16))*16))
                        if current> (len(Robots)-1):
                            current = len(Robots)-1
                    Robots[current][6] = True
                        
                if event.key == pygame.K_DOWN:
                    Robots[current][6] = False
                    current = current+16
                    if current>len(Robots)-1:
                        current = 0+(current-(int((current/16))*16))
                    Robots[current][6] = True
                    
                if event.key == pygame.K_SPACE:#Select
                    if Robots[current][4]:
                        Robots[current][4] = False
                    else:
                        Robots[current][4] = True

                if event.key == pygame.K_BACKSPACE:#Back
                    ScreenSetUp()
                    
                if event.key == pygame.K_RETURN:#Start Battle
                    for robot in Robots:
                        if robot[4]:
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Team":
                                TeamStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Dodgeball":
                                DodgeballStartGame(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []

                
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>11 and mouseX<155 and mouseY>452 and mouseY<482):#Back Button
                    ScreenSetUp()
                    
                if (mouseX>541 and mouseX<685 and mouseY>454 and mouseY<483):#Start Battle
                    for robot in Robots:
                        if robot[4]:
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Team":
                                TeamStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Dodgeball":
                                DodgeballStartGame(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []
                        

                counter = 0
                for robot in Robots:
                    if (mouseX>robot[2] and mouseX<(robot[2]+39) and mouseY>robot[3] and mouseY<(robot[3]+39)):
                        if robot[6]:
                            if robot[0]!="all" and robot[0]!="random" and robot[0]!="new":
                                if robot[4]:
                                    robot[4] = False
                                else:
                                    robot[4] = True
                        else:
                            for trobot in Robots:
                                if trobot[6]:
                                    trobot[6]=False
                            current = counter
                            robot[6]=True
                    counter = counter+1

        screen.blit(menuimage,(0,0))
        screen.blit(hideimage,(541,452))
        for robot in Robots:
            if robot[6]:
                target = robot
        if target[0]=="all":
            screen.blit(allimage,(23,63)) #Place your image
        elif target[0]=="random":
            screen.blit(randomimage,(23,63)) #Place your image
        elif target[0]=="new":
            screen.blit(randomimage,(23,63)) #Place your image
        else:
            largeimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
            changedColor = pygame.PixelArray(largeimage)
            changedColor.replace((195,29,29),target[5],0.11,(0.299,0.587,0.114))
            robotImage = changedColor.make_surface()
            screen.blit(robotImage,(23,63)) #Place your image
        screen.blit(target[1],(223,63)) #Place your image
        counter = 0
        scounter = 0
        for robot in Robots:
            if robot[0]!="all" and robot[0]!="random" and robot[0]!="new":
                smallimage = pygame.image.load('menuImages/botImage.png') #Load in an image
                changedColor = pygame.PixelArray(smallimage)
                changedColor.replace((195,29,29),robot[5],0.1,(0.299,0.587,0.114))
                robotImage = changedColor.make_surface()
                screen.blit(robotImage,(robot[2],robot[3])) #Place your image
                if robot[4]:
                    screen.blit(robotSelectedImage,(robot[2]-1,robot[3]-1)) #Place your image
        screen.blit(robotTargettedImage,(target[2]-1,target[3]-1)) #Place your image
        pygame.display.flip()     #Refreshes Screen
