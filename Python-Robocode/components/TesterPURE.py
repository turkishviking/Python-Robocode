import sys, copy
sys.path.append(sys.path[0] + "/../robots")

robotName = "%ROBOTNAME"

#shutil.copyfile(src, dst)
import %ROBOTNAMETEST

#import libraries
import sys,random, string, math

robot = %ROBOTNAMETEST
commandlist = []
printed = -1

if (hasattr(robot,"startDirection")):
    if (robot.startDirection() < 0) and (robot.startDirection() > 360):
        global printed
        printed = printed + 1
        print("startDirection: Unsuccessful")
        
if (printed > -1):
    print("")
    
if (hasattr(robot,"colour")):
    colourValues = (robot.colour())
    if (len(colourValues) != 3):
        print "Colour Unsuccessful: Too many values."
        global printed
        printed = printed + 1
    for colour in colourValues:
        if ((colour < 0) or (colour > 255)):
            print("colour Unsuccessful: '" + str(colour) + "' is not a valid RGB colour value")
            global printed
            printed = printed + 1
if (printed > -1):
    print("")
if (hasattr(robot,"target_spotted")):
    global printed
    printed = printed + 1
    print("Testing target_spotted at 0, 360, and 67:")
    robot.target_spotted(0)
    robot.target_spotted(360)
    robot.target_spotted(67)
if (printed > -1):
    print("")
if (hasattr(robot,"commands")):
    global printed
    printed = printed + 1
    print("Start of command run:")
    robot.commands()


if (printed > -1):
    if (printed == 0):
        print("All operations successful but only because there wasn't any.")




def turn_right(deg):
    print("turn right by "+ str(deg))
    
        
def turn_left(deg):
    print("turn left by "+ str(deg))
        
def move(distance):
    print("move :"+ str(distance) + "")

def pointgun(direction):
    print("point gun at " + str(direction))

def lockradar(where):
    print("RADAR locked to" + where)

def spinradar(LEFTorRIGHT):
    print("RADAR spin set to" + LEFTorRIGHT)


def stop(ticks):
    print("stop for" + str(ticks))

def done():
    print("DONE!")

def fire():
    print("fire!")
        
def robotHealth():
    print("checkHealth")
    return random.randrange(1,82)


        


