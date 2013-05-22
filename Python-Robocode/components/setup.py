#import libraries
import sys, pygame,random, string, math,os
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


def Exit(screen):
    #Exit the system
    pygame.quit()
    sys.exit()
    
def MainMenu(screen):
    menuimage = pygame.image.load('menuImages/Menu.jpg') #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen

    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Robots = []
                    counter = 0
                    for filename in os.listdir("robots"): #Code for displaying robot .py files
                        print "-----", filename, "----"
                        if filename[-3:] == ".py" and filename != ".svn":
                            #Name
                            
                            robotName = pygame.font.NameFont.render(str(filename[:-3]), True, (255,255, 255))
                            Robots.append([filename,robotName,155+(16*counter),False])
                            counter = counter+1
                    StartGame(screen,"Free4All",["Area 52","menuImages/Area52.jpg","BGImage.jpg","Open"],Robots)
                    
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>76 and mouseX<255 and mouseY>130 and mouseY<179):
                    BattleTypeMenu(screen)
                if (mouseX>77 and mouseX<254 and mouseY>181 and mouseY<228):
                    CreateABot(screen)
                if (mouseX>77 and mouseX<254 and mouseY>230 and mouseY<272):
                    Locked(screen)
                if (mouseX>76 and mouseX<254 and mouseY>279 and mouseY<320):
                    Locked(screen)
                if (mouseX>76 and mouseX<254 and mouseY>325 and mouseY<365):
                    Exit(screen)
        screen.blit(menuimage,(0,0))
        pygame.display.flip()     #Refreshes Screen

def Locked(screen):
    menuimage = pygame.image.load("menuImages/Menu.jpg") #Load in an image
    lockedImage = pygame.image.load("menuImages/Locked.png") #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    screen.blit(lockedImage,(120,100)) #Place your image
    pygame.display.flip()     #Refreshes Screen
    pygame.time.wait(250)
    MainMenu(screen)

def CreateABot(screen):
    import EditorMenu
    EditorMenu.ScreenSetUp()
    Exit(screen);

def TeamEditor(screen):
    import TeamEditorMenu
    TeamEditorMenu.ScreenSetUp()
    Exit(screen);

def BattleTypeMenu(screen):
    #[Name,MenuImage,Status]
    battleTypes = [["Free4All","menuImages/SingleBattle.jpg","Open"],
                   ["Team","menuImages/TeamBattle.jpg","Locked"],
                   ["Iron Man","menuImages/IronBattle.jpg","Locked"],
                   ["Corner Chaos","menuImages/CornerChaos.jpg","Locked"],
                   ["First Blood","menuImages/BloodBattle.jpg","Locked"],
                   ["Tournament","menuImages/Tournament.jpg","Locked"],
                   ["Dodgeball","menuImages/DodgeBattle.jpg","Locked"]]
    currentScreen = 0
    menuimage = pygame.image.load(battleTypes[currentScreen][1]) #Load in an image
    lockedImage = pygame.image.load("menuImages/Locked.png") #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen

    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentScreen = currentScreen-1
                    if currentScreen<0:
                        currentScreen = len(battleTypes)-1
                if event.key == pygame.K_RIGHT:
                    currentScreen = currentScreen+1
                    if currentScreen>len(battleTypes)-1:
                        currentScreen = 0
                if event.key == pygame.K_BACKSPACE:
                    MainMenu(screen)
                if event.key == pygame.K_RETURN:
                    if battleTypes[currentScreen][2] == "Open":
                        ArenaMenu(screen,battleTypes[currentScreen][0])
                        
            menuimage = pygame.image.load(battleTypes[currentScreen][1]) #Load in an image
    
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>11 and mouseX<155 and mouseY>452 and mouseY<482):
                    MainMenu(screen)
                if (mouseX>541 and mouseX<685 and mouseY>454 and mouseY<483):
                    if battleTypes[currentScreen][2] == "Open":
                        ArenaMenu(screen,battleTypes[currentScreen][0])
        screen.blit(menuimage,(0,0))
        if battleTypes[currentScreen][2] == "Locked":
            screen.blit(lockedImage,(120,100))  
        pygame.display.flip()     #Refreshes Screen

def ArenaMenu(screen,BattleType):
    #[Name,MenuImage,ActualBackground,Status]
    Arenas = [["Area 52","menuImages/Area52.jpg","BGImage.jpg","Open"],
              ["Wrestlemania","menuImages/Mania.jpg","BGImage.jpg","Open"],
              ["Wild West","menuImages/WildWest.jpg","BGImage.jpg","Locked"],
              ["Christmas Carnage","menuImages/Christmas.jpg","BGImage.jpg","Open"],
              ["Halloween Havoc","menuImages/Halloween.jpg","BGImage.jpg","Open"],
              ["Medieval Knightmare","menuImages/Medieval.jpg","BGImage.jpg","Locked"],
              ["Random","menuImages/Random.jpg","BGImage.jpg","Open"]]
    currentScreen = 0
    menuimage = pygame.image.load(Arenas[currentScreen][1]) #Load in an image
    lockedImage = pygame.image.load("menuImages/Locked.png") #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen

    while 1 :
        #Pygame.event.get() takes in input from the user
        #It records keyboard input and mouse clicks on the window
        
        for event in pygame.event.get():
            #If the user hits the X button on the window
            if event.type == pygame.QUIT:
                Exit(screen)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentScreen = currentScreen-1
                    if currentScreen<0:
                        currentScreen = len(Arenas)-1
                if event.key == pygame.K_RIGHT:
                    currentScreen = currentScreen+1
                    if currentScreen>len(Arenas)-1:
                        currentScreen = 0
                if event.key == pygame.K_BACKSPACE:
                    BattleTypeMenu(screen)
                if event.key == pygame.K_RETURN:
                    if Arenas[currentScreen][0]=="Random":
                        randomArena = random.randint(0,len(Arenas)-1)
                        while Arenas[randomArena][3] == "Locked" or Arenas[randomArena][0] == "Random":
                            randomArena = random.randint(0,len(Arenas)-1)
                        if BattleType=="Team" or BattleType=="Dodgeball":
                            teamSelect(screen,BattleType,Arenas[randomArena]) 
                        else:
                            botSelect(screen,BattleType,Arenas[randomArena]) 
                    if Arenas[currentScreen][3] == "Open":
                        if BattleType=="Team" or BattleType=="Dodgeball":
                            teamSelect(screen,BattleType,Arenas[currentScreen]) 
                        else:
                            botSelect(screen,BattleType,Arenas[currentScreen]) 

                        
            menuimage = pygame.image.load(Arenas[currentScreen][1]) #Load in an image
    
                
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>11 and mouseX<155 and mouseY>452 and mouseY<482):
                    BattleTypeMenu(screen)
                if (mouseX>541 and mouseX<685 and mouseY>454 and mouseY<499):
                    if Arenas[currentScreen][0]=="Random":
                        randomArena = random.randint(0,len(Arenas)-1)
                        while Arenas[randomArena][3] == "Locked" or Arenas[randomArena][0] == "Random":
                            randomArena = random.randint(0,len(Arenas)-1)
                        if BattleType=="Team" or BattleType=="Dodgeball":
                            teamSelect(screen,BattleType,Arenas[randomArena]) 
                        else:
                            botSelect(screen,BattleType,Arenas[randomArena]) 
                        
                    if Arenas[currentScreen][3] == "Open":
                        if BattleType=="Team" or BattleType=="Dodgeball":
                            teamSelect(screen,BattleType,Arenas[currentScreen]) 
                        else:
                            botSelect(screen,BattleType,Arenas[currentScreen]) 
        screen.blit(menuimage,(0,0))
        if Arenas[currentScreen][3] == "Locked":
            screen.blit(lockedImage,(120,100))
        pygame.display.flip()     #Refreshes Screen

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
    

def botSelect(screen,BattleType,Arena):
    menuimage = pygame.image.load('menuImages/BotSelected.jpg') #Load in an image
    robotSelectedImage = pygame.image.load('menuImages/botSelected.png') #Load in an image
    robotTargettedImage = pygame.image.load('menuImages/botTargetted.png') #Load in an image
    allimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    randomimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen
    Robots = []
    SelectedRobots = []
    x = 99
    y= 273
    robotName = pygame.font.RobotNameFont.render("Random Robots", True, (255,255, 255))
    Robots.append(["random",robotName,15,y,False,"",False])
    robotName = pygame.font.RobotNameFont.render("All Robots", True, (255,255, 255))
    Robots.append(["all",robotName,56,y,False,"",False])
    for filename in os.listdir("robots"): #Code for displaying robot .py files
        if filename[-3:] == ".py" and filename != ".svn":
            #Name
            robotName = pygame.font.RobotNameFont.render(str(filename[:-3]), True, (255,255, 255))
            colour = parseForColour("robots/"+filename)

            
            
            smallimage = pygame.image.load('menuImages/botImage.png') #Load in an image
            changedColour = pygame.PixelArray(smallimage)
            changedColour.replace((0,199,199),colour,0.11,(0.299,0.587,0.114))
            SRobotImage = changedColour.make_surface()
            
            largeimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
            changedColour = pygame.PixelArray(largeimage)
            changedColour.replace((0,199,199),colour,0.11,(0.299,0.587,0.114))
            LRobotImage = changedColour.make_surface()
            
            
            
            robot = [filename,robotName,x,y,False,colour,False,LRobotImage,SRobotImage]
            Robots.append(robot)
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
                    if Robots[current][0]=="all":
                        for robot in Robots:
                            if robot[0]!="random" and robot[0]!="all":
                                SelectedRobots.append(robot)
                        if len(SelectedRobots)>1:
                            if BattleType=="Free4All":
                                StartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Corner Chaos":
                                CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Iron Man":
                                IronManConfig(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="First Blood":
                                FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Tournament":
                                TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                        else:
                            SelectedRobots = []
                            
                    elif Robots[current][0]=="random":
                        NumberofBots = random.randint(2,len(Robots)-2)
                        for x in range(0,NumberofBots):
                            Added = False
                            while not Added:
                                naw = False
                                Bot = random.randint(0,len(Robots)-1)
                                for robot in SelectedRobots:
                                    if robot[0]==Robots[Bot][0]:
                                        naw = True
                                if not naw and Robots[Bot][0]!="random" and Robots[Bot][0]!="all":
                                    SelectedRobots.append(Robots[Bot])
                                    Added = True
                                    
                        if len(SelectedRobots)>1:
                            if BattleType=="Free4All":
                                StartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Corner Chaos":
                                CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Iron Man":
                                IronManConfig(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="First Blood":
                                FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Tournament":
                                TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                        else:
                            SelectedRobots = []
                        
                    else:
                        if Robots[current][4]:
                            Robots[current][4] = False
                        else:
                            Robots[current][4] = True

                if event.key == pygame.K_BACKSPACE:#Back
                    ArenaMenu(screen,BattleType)
                    
                if event.key == pygame.K_RETURN:#Start Battle
                    for robot in Robots:
                        if robot[4]:
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Free4All":
                            StartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Corner Chaos":
                            CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Iron Man":
                            IronManConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="First Blood":
                            FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Tournament":
                            TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []

                
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons == (1,0,0):
                mouseX,mouseY = pygame.mouse.get_pos()
                if (mouseX>11 and mouseX<155 and mouseY>452 and mouseY<482):#Back Button
                    ArenaMenu(screen,BattleType)
                    
                if (mouseX>541 and mouseX<685 and mouseY>454 and mouseY<483):#Start Battle
                    for robot in Robots:
                        if robot[4]:
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Free4All":
                                print SelectedRobots
                                StartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Corner Chaos":
                                CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Iron Man":
                                IronManConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="First Blood":
                                FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Tournament":
                                TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []
                        
                if (mouseX>58 and mouseX<98 and mouseY>273 and mouseY<314):#All Bots Button
                    for robot in Robots:
                        if robot[0]!="random" and robot[0]!="all":
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Free4All":
                                StartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Corner Chaos":
                                CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Iron Man":
                                IronManConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="First Blood":
                                FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Tournament":
                                TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []

                if (mouseX>17 and mouseX<57 and mouseY>273 and mouseY<314):#Random Bots Button
                    NumberofBots = random.randint(2,len(Robots)-2)
                    for x in range(0,NumberofBots):
                        Added = False
                        while not Added:
                            naw = False
                            Bot = random.randint(0,len(Robots)-1)
                            for robot in SelectedRobots:
                                if robot[0]==Robots[Bot][0]:
                                    naw = True
                            if not naw and Robots[Bot][0]!="random" and Robots[Bot][0]!="all":
                                SelectedRobots.append(Robots[Bot])
                                Added = True
                            
                    if len(SelectedRobots)>1:
                        if BattleType=="Free4All":
                                StartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Corner Chaos":
                                CornerChaosStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Iron Man":
                                IronManConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="First Blood":
                                FirstBloodConfig(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Tournament":
                                TournamentConfig(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []
                counter=0   
                for robot in Robots:
                    if (mouseX>robot[2] and mouseX<(robot[2]+39) and mouseY>robot[3] and mouseY<(robot[3]+39)):
                        if robot[6]:
                            if robot[0]!="all" and robot[0]!="random":
                                if robot[4]:
                                    robot[4] = False
                                else:
                                    robot[4] = True
                        else:
                            for trobot in Robots:
                                if trobot[6]:
                                    trobot[6]=False
                            robot[6]=True
                            current = counter
                    counter = counter+1

        screen.blit(menuimage,(0,0))
        for robot in Robots:
            if robot[6]:
                target = robot
        if target[0]=="all":
            screen.blit(allimage,(23,63)) #Place your image
        elif target[0]=="random":
            screen.blit(randomimage,(23,63)) #Place your image
        else:
            #This was what was causing the large image for the robot to be incorrect
            for robot in Robots:
                if robot[6]:
                    screen.blit(robot[7],(23,63)) #Place your image
        screen.blit(target[1],(223,63)) #Place your image
        counter = 0
        scounter = 0
        for robot in Robots:
            if robot[0]!="all" and robot[0]!="random":
                screen.blit(robot[8],(robot[2],robot[3])) #Place your image
                if robot[4]:
                    screen.blit(robotSelectedImage,(robot[2]-1,robot[3]-1)) #Place your image
        screen.blit(robotTargettedImage,(target[2]-1,target[3]-1)) #Place your image
        pygame.display.flip()     #Refreshes Screen

def teamSelect(screen,BattleType,Arena):
    menuimage = pygame.image.load('menuImages/BotSelected.jpg') #Load in an image
    robotSelectedImage = pygame.image.load('menuImages/botSelected.png') #Load in an image
    robotTargettedImage = pygame.image.load('menuImages/botTargetted.png') #Load in an image
    allimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    randomimage = pygame.image.load('menuImages/botImageLarge.png') #Load in an image
    screen.blit(menuimage,(0,0)) #Place your image
    pygame.display.flip()     #Refreshes Screen
    Robots = []
    SelectedRobots = []
    x = 141
    y= 273
    bots = []
    robotName = pygame.font.RobotNameFont.render("Random Teams", True, (255,255, 255))
    Robots.append(["random",robotName,15,y,False,"",False])
    robotName = pygame.font.RobotNameFont.render("All Teams", True, (255,255, 255))
    Robots.append(["all",robotName,56,y,False,"",False])
    robotName = pygame.font.RobotNameFont.render("New Team", True, (255,255, 255))
    Robots.append(["new",robotName,97,y,False,"",False])
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
                    if Robots[current][0]=="all":
                        for robot in Robots:
                            if robot[0]!="random" and robot[0]!="all" and robot[0]!="new":
                                SelectedRobots.append(robot)
                        if len(SelectedRobots)>1:
                            if BattleType=="Team":
                                TeamStartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Dodgeball":
                                DodgeballStartGame(screen,BattleType,Arena,SelectedRobots)
                        else:
                            SelectedRobots = []
                            
                    elif Robots[current][0]=="random":
                        NumberofBots = random.randint(2,len(Robots)-2)
                        for x in range(0,NumberofBots):
                            Added = False
                            while not Added:
                                naw = False
                                Bot = random.randint(0,len(Robots)-1)
                                for robot in SelectedRobots:
                                    if robot[0]==Robots[Bot][0]:
                                        naw = True
                                if not naw and Robots[Bot][0]!="random" and Robots[Bot][0]!="all" and Robots[Bot][0]!="new":
                                    SelectedRobots.append(Robots[Bot])
                                    Added = True
                                    
                        if len(SelectedRobots)>1:
                            if BattleType=="Team":
                                TeamStartGame(screen,BattleType,Arena,SelectedRobots)
                            elif BattleType=="Dodgeball":
                                DodgeballStartGame(screen,BattleType,Arena,SelectedRobots)
                        else:
                            SelectedRobots = []
                        
                    else:
                        if Robots[current][4]:
                            Robots[current][4] = False
                        else:
                            Robots[current][4] = True

                if event.key == pygame.K_BACKSPACE:#Back
                    ArenaMenu(screen,BattleType)
                    
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
                    ArenaMenu(screen,BattleType)
                    
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
                        
                if (mouseX>58 and mouseX<98 and mouseY>273 and mouseY<314):#All Bots Button
                    for robot in Robots:
                        if robot[0]!="random" and robot[0]!="all" and robot[0]!="new":
                            SelectedRobots.append(robot)
                    if len(SelectedRobots)>1:
                        if BattleType=="Team":
                                TeamStartGame(screen,BattleType,Arena,SelectedRobots)
                        elif BattleType=="Dodgeball":
                                DodgeballStartGame(screen,BattleType,Arena,SelectedRobots)
                    else:
                        SelectedRobots = []

                if (mouseX>17 and mouseX<57 and mouseY>273 and mouseY<314):#Random Bots Button
                    NumberofBots = random.randint(2,len(Robots)-2)
                    for x in range(0,NumberofBots):
                        Added = False
                        while not Added:
                            naw = False
                            Bot = random.randint(0,len(Robots)-1)
                            for robot in SelectedRobots:
                                if robot[0]==Robots[Bot][0]:
                                    naw = True
                            if not naw and Robots[Bot][0]!="random" and Robots[Bot][0]!="all" and Robots[Bot][0]!="new":
                                SelectedRobots.append(Robots[Bot])
                                Added = True
                            
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

def IronManConfig(screen,BattleType,Arena,SelectedRobots):
    #Time Configuration goes here
    IronManStartGame(screen,BattleType,Arena,SelectedRobots)

def FirstBloodConfig(screen,BattleType,Arena,SelectedRobots):
    #Rounds configuration goes here
    FirstBloodStartGame(screen,BattleType,Arena,SelectedRobots)

def TournamentConfig(screen,BattleType,Arena,SelectedRobots):
    #Brackets set up and display goes here
    TournamentStartGame(screen,BattleType,Arena,SelectedRobots)

def StartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "gamefile")

    
    
    import gamefile
    gamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def TeamStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    TeamRobots = []
    for robot in Robots:
        for bot in robot[7]:
            TeamRobots.append([bot[0],robot[0][0:-3]])
    Robots = TeamRobots
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + "["+robot[0][0:-3]+","+robot[1]+"]"
    RobotArrayString = RobotArrayString + "]"
    print RobotArrayString
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "teamgamefile")

    
    
    import teamgamefile
    teamgamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def DodgeballStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "dodgeballgamefile")

    
    
    import dodgeballgamefile
    dodgeballgamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def CornerChaosStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "cornerchaosgamefile")

    
    
    import cornerchaosgamefile
    cornerchaosgamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def IronManStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "ironmangamefile")

    
    
    import ironmangamefile
    ironmangamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def FirstBloodStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "firstbloodgamefile")

    
    
    import firstbloodgamefile
    firstbloodgamefile.ScreenSetUp(Arena[0])
    Exit(screen)

def TournamentStartGame(screen,BattleType,Arena,Robots):
    RobotArrayString = "["
    RobotFNString = ""
    for robot in Robots:
        if robot != Robots[0]:
            RobotArrayString = RobotArrayString + ", "
            RobotFNString = RobotFNString + ", "
            
        RobotFNString = RobotFNString + robot[0][0:-3]
        RobotArrayString = RobotArrayString + robot[0][0:-3]
    RobotArrayString = RobotArrayString + "]"
    addRobotsToGameFile(RobotArrayString,RobotFNString, Arena, "tournamentgamefile")

    
    
    import tournamentgamefile
    tournamentgamefile.ScreenSetUp(Arena[0])
    Exit(screen)
    


def addRobotsToGameFile(robotnames,robotfiles, Arena, gamefile):
    gamefilepure = file("components/"+gamefile+"PURE.py")
    newlines = []
    for line in gamefilepure:
        if "%importrobotshere" in line:
            line = line.replace("%importrobotshere", robotfiles)
        if "%putrobotnameshere" in line:
            line = line.replace("%putrobotnameshere",robotnames)
        newlines.append(line)
    
    gamefile = file("components/"+gamefile+".py", 'w')
    gamefile.writelines(newlines)
    
        
