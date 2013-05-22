import gamefile

global healthVal,lastTarget
healthVal = 82
lastTarget = 0
def startDirection():
        return 230
def colour():
	return (0,0,0)
def commands():
        gamefile.move(100)
        gamefile.lockradar("FREE")
        gamefile.spinradar("LEFT")
        if (healthVal > 40):
                gamefile.turn_left(45)
        gamefile.spinradar("RIGHT")
        if (healthVal > 40):
                gamefile.stop(60)
	gamefile.fire(2)
	gamefile.move(100)
	if (healthVal > 40):
                gamefile.turn_right(45)
        if (healthVal < 40):
                if (lastTarget > 0):
                        gamefile.turn_right(45)
                if (lastTarget < 0):
                        gamefile.turn_left(45)
                
	
	global healthVal
	healthVal = gamefile.robotHealth()
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun(direction*1.1)
        global lastTarget
        lastTarget = direction
        gamefile.fire(2)
        
