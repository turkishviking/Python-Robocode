import gamefile
def name():
        return "Genesis"
def colour():
	return (215,162,0)
def commands():
        gamefile.move(500)
	gamefile.fire(2)
	gamefile.turn_right(90)
	gamefile.fire(2)	
	gamefile.stop(10)
	gamefile.fire(2)	
	gamefile.move(500)
	gamefile.fire(2)
	gamefile.turn_right(90)
	gamefile.fire(2)
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun((direction)*1.3)
        gamefile.fire(2)
	
