import gamefile
def name():
        return "stanTheSlayer"
def colour():
	return (80,80,80)
def commands():
        gamefile.move(200)
        gamefile.stop(100)
	gamefile.turn_left(90)
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun(direction*1.3)
        gamefile.fire(2)
        gamefile.fire(2)
        
